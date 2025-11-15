"""Huey task queue setup and task definitions"""

from huey import SqliteHuey
import sqlite3
import time
from enum import StrEnum


class JobStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


# Initialize Huey with SQLite storage
huey = SqliteHuey(filename="huey.db")


@huey.task()
def create_course_task(course_topic: str, task_id: str) -> str:
    """Simple hello world task for course creation"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        print("Hello world")
        print(f"Creating course for topic: {course_topic}")
        time.sleep(5)

        # Update job status to completed
        cursor.execute(
            "UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?",
            (JobStatus.COMPLETED, task_id),
        )
        conn.commit()
        return f"Course creation completed for: {course_topic}"
    except Exception as e:
        # Update job status to failed
        cursor.execute(
            "UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?",
            (JobStatus.FAILED, task_id),
        )
        conn.commit()
        print(f"Task failed: {e}")
        raise
    finally:
        conn.close()
