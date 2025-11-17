"""Huey task queue setup and task definitions"""

from huey import SqliteHuey
from xai_sdk import Client  # type: ignore

import os
import logging
import sqlite3
import yaml
import hashlib
from enum import StrEnum
from typing import Any

from noobular.create import (
    generate_topic_outline,
    fill_topic_course_content,
    Model,
)
from noobular.validate import validate_course

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("tasks.log"), logging.StreamHandler()],
)

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
def create_course_topic_task(course_topic: str, task_id: str) -> str:
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


@huey.task()
def create_course_textbook_task(section_number: str, task_id: str) -> str:
    """Generate a course from a textbook section"""
    from pathlib import Path
    from noobular.create import (
        extract_section,
        generate_textbook_outline,
        fill_textbook_course_content,
        Model,
    )

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    client = Client(
        api_key=os.getenv("XAI_API_KEY"),
        timeout=3600,
    )

    try:
        logger.info(
            f"Creating course from textbook section: {section_number} (task_id: {task_id})"
        )

        # Determine chapter number from section (e.g., "7.1" -> 7)
        chapter_num = int(section_number.split(".")[0])

        # Setup paths
        base_dir = Path(__file__).parent.parent
        pdf_path = base_dir / "physics_textbook" / "pdf" / f"{chapter_num}.pdf"
        extracted_dir = base_dir / "physics_textbook" / "extracted"
        outlines_dir = base_dir / "physics_textbook" / "outlines"
        courses_dir = base_dir / "physics_textbook" / "courses"

        # Create directories if they don't exist
        extracted_dir.mkdir(parents=True, exist_ok=True)
        outlines_dir.mkdir(parents=True, exist_ok=True)
        courses_dir.mkdir(parents=True, exist_ok=True)

        content_output = extracted_dir / f"section_{section_number}_content.txt"
        problems_output = extracted_dir / f"section_{section_number}_problems.txt"
        outline_output = outlines_dir / f"section_{section_number}_outline.yaml"
        course_output = courses_dir / f"section_{section_number}_course.yaml"

        # Check if PDF exists
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        # Step 1: Extract content and problems
        logger.info("=" * 80)
        logger.info(
            f"STEP 1: Extracting content and problems from Section {section_number}..."
        )
        logger.info("=" * 80)

        if content_output.exists() and problems_output.exists():
            logger.info("✓ Found existing extracted files, skipping extraction")
            logger.info(f"  Content: {content_output}")
            logger.info(f"  Problems: {problems_output}")
        else:
            extract_section(
                client=client,
                textbook_file=str(pdf_path),
                section_name=f"Section {section_number}",
                content_output=str(content_output),
                problems_output=str(problems_output),
                model=Model.GROK_4_FAST,
            )
            logger.info(f"✓ Extracted to {content_output} and {problems_output}")

        # Step 2: Generate outline
        logger.info("=" * 80)
        logger.info(
            f"STEP 2: Generating course outline for Section {section_number}..."
        )
        logger.info("=" * 80)

        if outline_output.exists():
            logger.info(f"✓ Found existing outline, loading from {outline_output}")
            with open(outline_output, "r") as f:
                outline_yaml = f.read()
        else:
            outline_yaml = generate_textbook_outline(
                client=client,
                content_file=str(content_output),
                problems_file=str(problems_output),
                model=Model.GROK_4_FAST,
            )

            # Save outline
            with open(outline_output, "w") as f:
                f.write(outline_yaml)

            logger.info(f"✓ Outline saved to {outline_output}")

        # Step 3: Fill in content and questions
        logger.info("=" * 80)
        logger.info(f"STEP 3: Filling course content for Section {section_number}...")
        logger.info("=" * 80)

        if course_output.exists():
            logger.info(f"✓ Found existing course, loading from {course_output}")
            with open(course_output, "r") as f:
                complete_course_yaml = f.read()
            complete_course = yaml.safe_load(complete_course_yaml)
        else:
            complete_course = fill_textbook_course_content(
                client=client,
                outline_yaml=outline_yaml,
                content_file=str(content_output),
                problems_file=str(problems_output),
                model=Model.GROK_4_FAST,
                question_count=8,
            )

            # Convert to YAML and save
            complete_course_yaml = yaml.dump(
                complete_course,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )

            with open(course_output, "w") as f:
                f.write(complete_course_yaml)

            logger.info(f"✓ Course saved to {course_output}")

        # Step 4: Validate and save to database
        logger.info("=" * 80)
        logger.info("STEP 4: Validating and saving to database...")
        logger.info("=" * 80)

        validate_course(complete_course)
        logger.info("✓ Course validation passed")

        file_hash = hashlib.md5(complete_course_yaml.encode()).digest()

        if check_course_exists(cursor, file_hash):
            logger.warning(
                f"Course already exists in database for section {section_number}"
            )
            result = f"Course already exists for section {section_number}"
        else:
            course_id = save_course(cursor, complete_course, file_hash)
            logger.info(f"✓ Course saved to database with ID: {course_id}")
            result = f"Course creation completed for section {section_number} (ID: {course_id})"

        # Mark as completed
        cursor.execute(
            "UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?",
            (JobStatus.COMPLETED, task_id),
        )
        conn.commit()

        logger.info("=" * 80)
        logger.info(
            f"✓ Textbook course creation completed for section {section_number}"
        )
        logger.info("=" * 80)

        return result

    except Exception as e:
        # Update job status to failed
        cursor.execute(
            "UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?",
            (JobStatus.FAILED, task_id),
        )
        conn.commit()
        logger.error(
            f"Task failed for section '{section_number}' (task_id: {task_id}): {e}",
            exc_info=True,
        )
        raise
    finally:
        conn.close()
