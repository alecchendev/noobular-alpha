"""Huey task queue setup and task definitions"""

import os
import logging
from huey import SqliteHuey
import sqlite3
import yaml
import hashlib
from enum import StrEnum
from typing import Any
from xai_sdk import Client  # type: ignore
from create import (
    generate_topic_outline,
    fill_topic_course_content,
    Model,
)
from validate import validate_course


logger = logging.getLogger(__name__)


class JobStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


# Initialize Huey with SQLite storage
huey = SqliteHuey(filename="huey.db")


def check_course_exists(cursor: sqlite3.Cursor, file_hash: bytes) -> bool:
    cursor.execute("SELECT id FROM courses WHERE file_hash = ?", (file_hash,))
    if cursor.fetchone():
        return True
    return False


def save_course(
    cursor: sqlite3.Cursor, course_data: dict[str, Any], file_hash: bytes
) -> int:
    # Insert course with hash
    cursor.execute(
        "INSERT INTO courses (title, file_hash) VALUES (?, ?)",
        (course_data["title"], file_hash),
    )
    course_id = cursor.lastrowid
    assert course_id is not None

    # Map knowledge point names to database IDs for prerequisite resolution
    kp_name_to_db_id: dict[str, int] = {}

    # Insert lessons
    for lesson_data in course_data.get("lessons", []):
        cursor.execute(
            "INSERT INTO lessons (course_id, title) VALUES (?, ?)",
            (course_id, lesson_data["title"]),
        )
        lesson_id = cursor.lastrowid

        # Insert knowledge points, contents, and questions
        for kp_data in lesson_data.get("knowledge_points", []):
            cursor.execute(
                """INSERT INTO knowledge_points
                             (lesson_id, name, description)
                             VALUES (?, ?, ?)""",
                (lesson_id, kp_data["name"], kp_data["description"]),
            )
            knowledge_point_db_id = cursor.lastrowid
            assert knowledge_point_db_id is not None
            kp_name_to_db_id[kp_data["name"]] = knowledge_point_db_id

            # Insert contents
            for content in kp_data["contents"]:
                cursor.execute(
                    """INSERT INTO contents
                                 (knowledge_point_id, text)
                                 VALUES (?, ?)""",
                    (knowledge_point_db_id, content),
                )

            # Insert questions and choices
            for question_data in kp_data["questions"]:
                cursor.execute(
                    """INSERT INTO questions
                                 (knowledge_point_id, prompt, explanation)
                                 VALUES (?, ?, ?)""",
                    (
                        knowledge_point_db_id,
                        question_data["prompt"],
                        question_data["explanation"],
                    ),
                )
                question_id = cursor.lastrowid

                # Insert choices
                for choice_data in question_data["choices"]:
                    cursor.execute(
                        """INSERT INTO choices
                                     (question_id, text, is_correct)
                                     VALUES (?, ?, ?)""",
                        (
                            question_id,
                            choice_data["text"],
                            choice_data.get("correct", False),
                        ),
                    )

    # Insert prerequisites (after all knowledge points are created)
    for lesson_data in course_data.get("lessons", []):
        for kp_data in lesson_data.get("knowledge_points", []):
            kp_db_id = kp_name_to_db_id[kp_data["name"]]

            for prerequisite_name in kp_data.get("prerequisites", []):
                prerequisite_db_id = kp_name_to_db_id.get(prerequisite_name)
                if prerequisite_db_id:
                    cursor.execute(
                        """INSERT INTO prerequisites
                                     (knowledge_point_id, prerequisite_id)
                                     VALUES (?, ?)""",
                        (kp_db_id, prerequisite_db_id),
                    )

    return course_id


@huey.task()
def create_course_task(course_topic: str, task_id: str) -> str:
    """Generate a course outline and fill it with content"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    client = Client(
        api_key=os.getenv("XAI_API_KEY"),
        timeout=3600,
    )

    try:
        logger.info(f"Creating course for topic: {course_topic} (task_id: {task_id})")

        # Step 1: Generate outline
        logger.info("=" * 80)
        logger.info("STEP 1: Generating course outline...")
        logger.info("=" * 80)
        outline_yaml = generate_topic_outline(
            client=client,
            topic=course_topic,
            lesson_count=8,
            model=Model.GROK_4_FAST,
        )

        logger.info("OUTLINE GENERATED:")
        logger.info("=" * 80)
        logger.debug(outline_yaml)  # Use debug level for large output
        logger.info("=" * 80)

        # Step 2: Fill in content and questions
        logger.info("STEP 2: Filling course content...")
        logger.info("=" * 80)
        complete_course = fill_topic_course_content(
            client=client,
            outline_yaml=outline_yaml,
            model=Model.GROK_4_FAST,
            question_count=8,
        )

        # Convert to YAML
        complete_course_yaml = yaml.dump(
            complete_course,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )

        logger.info("COMPLETE COURSE GENERATED:")
        logger.info("=" * 80)
        logger.debug(complete_course_yaml)  # Use debug level for large output
        logger.info("=" * 80)

        # Step 3: Validate the course
        logger.info("STEP 3: Validating course...")
        logger.info("=" * 80)
        validate_course(complete_course)
        logger.info("✓ Course validation passed")

        # Step 4: Check if course already exists and save to database
        logger.info("STEP 4: Saving course to database...")
        logger.info("=" * 80)
        file_hash = hashlib.md5(complete_course_yaml.encode()).digest()

        result = ""
        if check_course_exists(cursor, file_hash):
            logger.warning(
                f"Course already exists in database (same hash) for topic: {course_topic}"
            )
            # Still mark as completed since the course was generated successfully
            cursor.execute(
                "UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?",
                (JobStatus.COMPLETED, task_id),
            )
            result = f"Course already exists for topic {course_topic}"
        else:
            course_id = save_course(cursor, complete_course, file_hash)
            logger.info(f"✓ Course saved to database with ID: {course_id}")

            # Update job status to completed
            cursor.execute(
                "UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?",
                (JobStatus.COMPLETED, task_id),
            )
            result = f"Course creation completed for: {course_topic} (ID: {course_id})"
            logger.info(
                f"✓ Course creation completed! Course ID: {course_id}, Title: {complete_course.get('title', 'Unknown')}"
            )

        conn.commit()
        return result
    except Exception as e:
        # Update job status to failed
        cursor.execute(
            "UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?",
            (JobStatus.FAILED, task_id),
        )
        conn.commit()
        logger.error(
            f"Task failed for topic '{course_topic}' (task_id: {task_id}): {e}",
            exc_info=True,
        )
        raise
    finally:
        conn.close()
