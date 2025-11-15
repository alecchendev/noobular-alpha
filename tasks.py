"""Huey task queue setup and task definitions"""

from huey import SqliteHuey
import sqlite3
import time

# Initialize Huey with SQLite storage
huey = SqliteHuey(filename="huey.db")


@huey.task()
def create_course_task(course_topic: str, task_id: str) -> str:
    """Simple hello world task for course creation"""
    print("Hello world")
    print(f"Creating course for topic: {course_topic}")
    time.sleep(5)

    # Update job status to completed
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?",
        ("completed", task_id),
    )
    conn.commit()
    conn.close()

    return f"Course creation completed for: {course_topic}"
