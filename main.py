from flask import (
    Flask,
    render_template,
    abort,
    request,
    g,
    redirect,
    send_file,
    make_response,
)
from datetime import datetime, timedelta
from markupsafe import escape, Markup
import yaml
import sqlite3
import hashlib
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, NoReturn, Union
import random
from dataclasses import dataclass
from visualize_course import create_knowledge_graph, KnowledgeGraph
from validate import validate_course
import argparse
from werkzeug.exceptions import RequestEntityTooLarge
import markdown
from tasks import create_course_task, JobStatus, check_course_exists, save_course

# Init app
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # allow up to ~1MB uploads
app.config["MAX_FORM_MEMORY_SIZE"] = 1 * 1024 * 1024


# Jinja filter for rendering markdown
@app.template_filter("markdown")
def markdown_filter(text: str) -> Markup:
    """Convert markdown text to HTML (KaTeX renders client-side)"""
    return Markup(markdown.markdown(text))


@dataclass
class AppConfig:
    database: str = "database.db"
    courses_directory: Path = Path("courses")
    # number of answers correct in a row to let you skip the rest of the questions
    correct_count_threshold: int = 2
    # number of answers correct in a row to let you skip the rest of the questions in a review
    review_correct_count_threshold: int = 3
    # number of wrong answers for a knowledge point at which you will fail and have to restart a lesson
    incorrect_count_fail_threshold: int = 3
    # number of knowledge points completed before a quiz is ready
    quiz_knowledge_point_count_threshold: int = 8
    # number of questions in a quiz
    quiz_question_count: int = 4
    # number of minutes allowed for a quiz
    quiz_time_limit_minutes: int = 10
    # number of knowledge points completed before a review will surface
    # (if the knowledge point is completed and has no postreqs)
    review_knowledge_point_count_threshold: int = 4
    global_id: int = 1
    global_username: str = "global"

    @staticmethod
    def prod() -> "AppConfig":
        return AppConfig()

    @staticmethod
    def debug() -> "AppConfig":
        return AppConfig(
            quiz_knowledge_point_count_threshold=2,
            quiz_question_count=2,
        )

    def __post_init__(self) -> None:
        assert self.quiz_knowledge_point_count_threshold >= self.quiz_question_count


# Config is initialized later in main() based on --debug flag
config: AppConfig


def init_database() -> None:
    """Initialize SQLite database on app startup"""
    conn = create_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # Create courses table
    cursor.execute("""CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        file_hash BLOB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(file_hash)
    )""")

    # Create user_courses table (links users to courses)
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_courses (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (course_id) REFERENCES courses (id),
        UNIQUE(user_id, course_id)
    )""")

    # Create lessons table
    cursor.execute("""CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY,
        course_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses (id)
    )""")

    # Create knowledge_points table
    cursor.execute("""CREATE TABLE IF NOT EXISTS knowledge_points (
        id INTEGER PRIMARY KEY,
        lesson_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (lesson_id) REFERENCES lessons (id)
    )""")

    # Create contents table
    cursor.execute("""CREATE TABLE IF NOT EXISTS contents (
        id INTEGER PRIMARY KEY,
        knowledge_point_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points (id)
    )""")

    # Create questions table
    cursor.execute("""CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        knowledge_point_id INTEGER NOT NULL,
        prompt TEXT NOT NULL,
        explanation TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points (id)
    )""")

    # Create choices table
    cursor.execute("""CREATE TABLE IF NOT EXISTS choices (
        id INTEGER PRIMARY KEY,
        question_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        is_correct BOOLEAN NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )""")

    # Create answers table (user responses)
    cursor.execute("""CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        choice_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (question_id) REFERENCES questions (id),
        FOREIGN KEY (choice_id) REFERENCES choices (id),
        UNIQUE(user_id, question_id)
    )""")

    # Create prerequisites table
    cursor.execute("""CREATE TABLE IF NOT EXISTS prerequisites (
        id INTEGER PRIMARY KEY,
        knowledge_point_id INTEGER NOT NULL,
        prerequisite_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points (id),
        FOREIGN KEY (prerequisite_id) REFERENCES knowledge_points (id)
    )""")

    # Create quizzes table
    cursor.execute("""CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY,
        course_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        started_at TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )""")

    # Create quiz_questions table (links quizzes to questions)
    cursor.execute("""CREATE TABLE IF NOT EXISTS quiz_questions (
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (quiz_id) REFERENCES quizzes (id),
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )""")

    # Create reviews table
    cursor.execute("""CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY,
        knowledge_point_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        UNIQUE(knowledge_point_id, user_id)
    )""")

    # Create review_questions table (links reviews to questions)
    cursor.execute("""CREATE TABLE IF NOT EXISTS review_questions (
        id INTEGER PRIMARY KEY,
        review_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (review_id) REFERENCES reviews (id),
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )""")

    # Create diagnostics table
    cursor.execute("""CREATE TABLE IF NOT EXISTS diagnostics (
        id INTEGER PRIMARY KEY,
        course_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        UNIQUE(course_id, user_id)
    )""")

    # Create diagnostic_questions table (links diagnostics to questions)
    cursor.execute("""CREATE TABLE IF NOT EXISTS diagnostic_questions (
        id INTEGER PRIMARY KEY,
        diagnostic_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (diagnostic_id) REFERENCES diagnostics (id),
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )""")

    # Create lesson_questions table (tracks which questions are used in lessons)
    cursor.execute("""CREATE TABLE IF NOT EXISTS lesson_questions (
        id INTEGER PRIMARY KEY,
        question_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (question_id) REFERENCES questions (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )""")

    # Create jobs table (tracks background jobs)
    cursor.execute("""CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY,
        task_id TEXT NOT NULL UNIQUE,
        user_id INTEGER NOT NULL,
        topic TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )""")

    # Create default global user if it doesn't exist
    cursor.execute(
        "INSERT OR IGNORE INTO users (username) VALUES (?)", (config.global_username,)
    )
    conn.commit()

    print("✅ Database tables created successfully!")
    conn.close()


def create_db_connection() -> sqlite3.Connection:
    """Create a new database connection with foreign keys enabled"""
    conn = sqlite3.connect(config.database)
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
    return conn


@app.after_request
def commit_db_transaction(response: Any) -> Any:
    """Commit database transaction if request was successful"""
    db = g.get("db", None)
    if db is None:
        return response
    # Only commit if response was successful (2xx or 3xx status code)
    if 200 <= response.status_code < 400:
        db.commit()
    else:
        db.rollback()
    return response


@app.teardown_appcontext
def close_db_connection(error: Any) -> None:
    """Automatically close db connection at end of request"""
    db = g.pop("db", None)
    if db is not None:
        # Rollback if there was an uncaught exception
        if error:
            db.rollback()
        db.close()


@dataclass
class User:
    id: int
    username: str


@dataclass
class Job:
    id: int
    task_id: str
    user_id: int
    topic: str
    status: JobStatus
    created_at: str
    updated_at: str


@app.before_request
def initialize_request() -> None:
    """Initialize database connection and load user before each request"""
    # Initialize database connection and cursor
    g.db = create_db_connection()
    g.db.row_factory = sqlite3.Row
    g.cursor = g.db.cursor()

    # Load logged-in user
    username = request.cookies.get("username")
    g.user = User(config.global_id, config.global_username)
    if username is None:
        return
    g.cursor.execute("SELECT id, username FROM users WHERE username = ?", (username,))
    user_row = g.cursor.fetchone()
    if user_row:
        id, username = user_row
        g.user = User(id, username)


@app.before_request
def log_request() -> None:
    """Log incoming request details"""
    parts = []
    if request.args:
        parts.append(f"params={dict(request.args)}")
    if request.form:
        parts.append(f"form={dict(request.form)}")
    if request.is_json and request.get_json():
        parts.append(f"json={request.get_json()}")

    if parts:
        print(f"Request data: {', '.join(parts)}")


@dataclass
class Answer:
    id: int
    question_id: int
    choice_id: int


@dataclass
class Choice:
    id: int
    text: str
    correct: Optional[bool] = None


@dataclass
class Question:
    id: int
    prompt: str
    choices: List[Choice]
    answer: Optional[Answer]
    knowledge_point_id: int
    explanation: str

    def correct_choice(self) -> Choice:
        # Assumes there is a correct choice (should be validated upon course load)
        return next(choice for choice in self.choices if choice.correct)


@dataclass
class Content:
    id: int
    text: str


def last_consecutive_correct_answers(questions: List[Question]) -> int:
    last_correct_count = 0
    for question in questions[::-1]:
        if question.answer is None:
            continue
        if question.answer.choice_id == question.correct_choice().id:
            last_correct_count += 1
        else:
            break
    return last_correct_count


@dataclass
class KnowledgePoint:
    id: int
    name: str
    description: str
    prerequisites: List[int]
    contents: List[Content]
    questions: List[Question]  # Unused unanswered questions
    lesson_questions: List[Question]  # Includes questions used in a lesson
    quizzed_questions: List[Question]  # Includes questions used in a quiz
    reviewed_questions: List[Question]  # Includes questions used in a review
    diagnostic_questions: List[Question]  # Includes questions used in a diagnostic

    def last_consecutive_correct_answers(self) -> int:
        return last_consecutive_correct_answers(self.lesson_questions)

    def last_consecutive_correct_review_answers(self) -> int:
        return last_consecutive_correct_answers(self.reviewed_questions)


@dataclass
class Lesson:
    id: int
    title: str
    knowledge_points: List[KnowledgePoint]


@dataclass
class Course:
    id: int
    title: str
    lessons: List[Lesson]


@dataclass
class Quiz:
    id: int
    course_id: int
    questions: List[Question]
    started_at: Optional[str]


@dataclass
class Review:
    id: int
    knowledge_point: KnowledgePoint


@dataclass
class Diagnostic:
    id: int
    course_id: int


@dataclass
class CourseItem:
    type: str  # 'lesson', 'quiz', 'review', or 'diagnostic'
    item: Union[Lesson, Quiz, Review, Diagnostic]
    completion_date: Optional[str] = None


# Helper functions for common abort patterns
def abort_course_not_found(course_id: int) -> NoReturn:
    """Abort with a 404 error for course not found"""
    abort(404, description=f"Course with ID {course_id} not found")


def abort_lesson_not_found(lesson_id: int, course_id: int) -> NoReturn:
    """Abort with a 404 error for lesson not found"""
    abort(
        404, description=f"Lesson with ID {lesson_id} not found in course {course_id}"
    )


def abort_knowledge_point_not_found(knowledge_point_id: int) -> NoReturn:
    """Abort with a 404 error for knowledge_point not found"""
    abort(404, description=f"Knowledge point with ID {knowledge_point_id} not found")


def abort_quiz_not_found(quiz_id: int, course_id: int) -> NoReturn:
    """Abort with a 404 error for quiz not found"""
    abort(404, description=f"Quiz with ID {quiz_id} not found in course {course_id}")


def abort_review_not_found(review_id: int, course_id: int) -> NoReturn:
    """Abort with a 404 error for review not found"""
    abort(
        404, description=f"Review with ID {review_id} not found in course {course_id}"
    )


def abort_diagnostic_not_found(diagnostic_id: int, course_id: int) -> NoReturn:
    """Abort with a 404 error for diagnostic not found"""
    abort(
        404,
        description=f"Diagnostic with ID {diagnostic_id} not found in course {course_id}",
    )


def abort_missing_parameters(*param_names: str) -> NoReturn:
    """Abort with a 400 error for missing parameters"""
    abort(400, description=f"Missing required parameters: {', '.join(param_names)}")


def load_courses_to_db() -> None:
    """Load courses from YAML files into database"""
    if not config.courses_directory.is_dir():
        print("No courses directory found, skipping course loading")
        return

    conn = create_db_connection()
    cursor = conn.cursor()

    # Parse new courses (file hash isn't in DB)
    courses: list[tuple[bytes, dict[str, Any]]] = []  # hash, course_data
    for yaml_file in config.courses_directory.glob("*.yaml"):
        with open(yaml_file, "r") as f:
            course_data = yaml.safe_load(f) or {}

        # Calculate file hash (MD5, 16 bytes)
        with open(yaml_file, "rb") as f:
            file_hash = hashlib.md5(f.read()).digest()

        # Check if this file hash already exists
        if check_course_exists(cursor, file_hash):
            print(f"Course {yaml_file.name} already loaded (unchanged), skipping")
            continue

        try:
            validate_course(course_data)
        except ValueError as e:
            print(f"Error validating {yaml_file.name}: {e}")
            continue
        courses.append((file_hash, course_data))

    # Insert into DB
    for file_hash, course_data in courses:
        save_course(cursor, course_data, file_hash)

    conn.commit()

    print("✅ Courses loaded into database successfully!")

    conn.close()


def load_course_title_from_db(cursor: sqlite3.Cursor, course_id: int) -> Optional[str]:
    """Returns id, title if it exists"""
    cursor.execute("SELECT title FROM courses WHERE id = ?", (course_id,))
    course_row = cursor.fetchone()
    if not course_row:
        return None
    return str(course_row[0])


def load_choices_from_db(cursor: sqlite3.Cursor, question_id: int) -> List[Choice]:
    cursor.execute(
        "SELECT id, text, is_correct FROM choices WHERE question_id = ?",
        (question_id,),
    )
    choice_rows = cursor.fetchall()
    choices = [
        Choice(id=id, text=text, correct=bool(is_correct))
        for id, text, is_correct in choice_rows
    ]
    # Shuffle choices so they appear in random order
    random.shuffle(choices)
    return choices


def load_answer_from_db(
    cursor: sqlite3.Cursor, question_id: int, user_id: int
) -> Optional[Answer]:
    cursor.execute(
        """SELECT id, question_id, choice_id FROM answers
           WHERE question_id = ? AND user_id = ?""",
        (question_id, user_id),
    )
    answer_row = cursor.fetchone()
    if not answer_row:
        return None
    id, question_id, choice_id = answer_row
    return Answer(id=id, question_id=question_id, choice_id=choice_id)


def load_knowledge_point_from_db(
    cursor: sqlite3.Cursor, knowledge_point_id: int, user_id: int
) -> Optional[KnowledgePoint]:
    cursor.execute(
        "SELECT name, description FROM knowledge_points WHERE id = ?",
        (knowledge_point_id,),
    )
    kp_row = cursor.fetchone()
    name, description = kp_row

    # Get prerequisites for this knowledge point
    cursor.execute(
        "SELECT prerequisite_id FROM prerequisites WHERE knowledge_point_id = ?",
        (knowledge_point_id,),
    )
    prerequisite_rows = cursor.fetchall()
    prerequisites = [prereq_id for (prereq_id,) in prerequisite_rows]

    # Get contents for this knowledge point
    cursor.execute(
        "SELECT id, text FROM contents WHERE knowledge_point_id = ?",
        (knowledge_point_id,),
    )
    content_rows = cursor.fetchall()
    contents = [Content(id=id, text=text) for id, text in content_rows]

    # Get questions for this knowledge point
    cursor.execute(
        "SELECT id, prompt, explanation FROM questions WHERE knowledge_point_id = ?",
        (knowledge_point_id,),
    )
    question_rows = cursor.fetchall()

    cursor.execute(
        """SELECT q.id
           FROM quiz_questions qq
           JOIN quizzes qu ON qq.quiz_id = qu.id
           JOIN questions q ON qq.question_id = q.id
           WHERE q.knowledge_point_id = ?
           AND qu.user_id = ?""",
        (knowledge_point_id, user_id),
    )
    quizzed_question_ids = set(row[0] for row in cursor.fetchall())

    cursor.execute(
        """SELECT q.id
           FROM review_questions rq
           JOIN reviews r ON rq.review_id = r.id
           JOIN questions q ON rq.question_id = q.id
           WHERE q.knowledge_point_id = ?
           AND r.user_id = ?""",
        (knowledge_point_id, user_id),
    )
    # We need to keep these in order so that when we answer later with
    # the index, we can find the right question. Later we should
    # probably just submit based on the question id.
    reviewed_question_id_to_idx = {row[0]: i for i, row in enumerate(cursor.fetchall())}

    cursor.execute(
        """SELECT q.id
           FROM diagnostic_questions dq
           JOIN diagnostics d ON dq.diagnostic_id = d.id
           JOIN questions q ON dq.question_id = q.id
           WHERE q.knowledge_point_id = ?
           AND d.user_id = ?""",
        (knowledge_point_id, user_id),
    )
    # We need to keep these in order so that when we answer later with
    # the index, we can find the right question. Later we should
    # probably just submit based on the question id.
    diagnostic_question_id_to_idx = {
        row[0]: i for i, row in enumerate(cursor.fetchall())
    }

    cursor.execute(
        """SELECT q.id
           FROM lesson_questions lq
           JOIN questions q ON lq.question_id = q.id
           WHERE q.knowledge_point_id = ?
           AND lq.user_id = ?""",
        (knowledge_point_id, user_id),
    )
    lesson_question_id_to_idx = {row[0]: i for i, row in enumerate(cursor.fetchall())}

    questions = []
    lesson_questions: list[Question] = [Question(-1, "", [], None, -1, "")] * len(
        lesson_question_id_to_idx
    )
    quizzed_questions = []
    reviewed_questions: list[Question] = [Question(-1, "", [], None, -1, "")] * len(
        reviewed_question_id_to_idx
    )
    diagnostic_questions: list[Question] = [Question(-1, "", [], None, -1, "")] * len(
        diagnostic_question_id_to_idx
    )
    for question_id, prompt, explanation in question_rows:
        choices = load_choices_from_db(cursor, question_id)
        answer = load_answer_from_db(cursor, question_id, user_id)

        question = Question(
            id=question_id,
            prompt=prompt,
            choices=choices,
            answer=answer,
            knowledge_point_id=knowledge_point_id,
            explanation=explanation,
        )
        if question.id in quizzed_question_ids:
            quizzed_questions.append(question)
        elif question.id in reviewed_question_id_to_idx.keys():
            reviewed_questions[reviewed_question_id_to_idx[question.id]] = question
        elif question.id in diagnostic_question_id_to_idx.keys():
            diagnostic_questions[diagnostic_question_id_to_idx[question.id]] = question
        elif question.id in lesson_question_id_to_idx.keys():
            lesson_questions[lesson_question_id_to_idx[question.id]] = question
        else:
            questions.append(question)
    assert all(q.id != -1 for q in reviewed_questions)
    assert all(q.id != -1 for q in diagnostic_questions)
    assert all(q.id != -1 for q in lesson_questions)

    return KnowledgePoint(
        id=knowledge_point_id,
        name=name,
        description=description,
        prerequisites=prerequisites,
        contents=contents,
        questions=questions,
        lesson_questions=lesson_questions,
        quizzed_questions=quizzed_questions,
        reviewed_questions=reviewed_questions,
        diagnostic_questions=diagnostic_questions,
    )


def load_lesson_from_db(
    cursor: sqlite3.Cursor, lesson_id: int, user_id: int
) -> Optional[Lesson]:
    cursor.execute("SELECT title FROM lessons WHERE id = ?", (lesson_id,))
    lesson_row = cursor.fetchone()
    if not lesson_row:
        return None
    lesson_title = lesson_row[0]

    cursor.execute(
        "SELECT id FROM knowledge_points WHERE lesson_id = ?",
        (lesson_id,),
    )
    kp_ids = [row[0] for row in cursor.fetchall()]

    knowledge_points = []
    for knowledge_point_id in kp_ids:
        knowledge_point = load_knowledge_point_from_db(
            cursor, knowledge_point_id, user_id
        )
        if knowledge_point:
            knowledge_points.append(knowledge_point)

    return Lesson(id=lesson_id, title=lesson_title, knowledge_points=knowledge_points)


def load_full_course_from_db(
    cursor: sqlite3.Cursor, course_id: int, user_id: int
) -> Optional[Course]:
    """Load a course from the database by ID"""
    course_title = load_course_title_from_db(cursor, course_id)
    if not course_title:
        return None

    # Get lessons
    cursor.execute("SELECT id FROM lessons WHERE course_id = ?", (course_id,))
    lesson_ids = [row[0] for row in cursor.fetchall()]

    lessons = []
    for lesson_id in lesson_ids:
        lesson = load_lesson_from_db(cursor, lesson_id, user_id)
        if lesson:
            lessons.append(lesson)

    return Course(id=course_id, title=course_title, lessons=lessons)


@app.route("/")
def index() -> str:
    g.cursor.execute("SELECT id, title FROM courses")
    courses = [(id, title) for id, title in g.cursor.fetchall()]

    user = None if g.user.username == config.global_username else g.user
    return render_template("index.html", courses=courses, user=user)


@app.route("/login", methods=["GET", "POST"])
def login() -> Any:
    if request.method == "GET":
        return render_template("login.html")

    # POST request - handle form submission
    username = request.form.get("username")
    if not username or not username.strip():
        return "<p>Error: Username is required</p>"

    username = username.strip()

    # Try to create the user (will fail silently if username already exists due to UNIQUE constraint)
    try:
        g.cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    except sqlite3.IntegrityError:
        # Username already exists, which is fine - just log them in
        pass

    # Create response with redirect and set cookie
    response = make_response(redirect("/"))
    response.set_cookie(
        "username",
        username,
        httponly=True,
        samesite="Lax",
        secure=not app.debug,
        path="/",
    )
    return response


@app.route("/logout")
def logout() -> Any:
    response = make_response(redirect("/"))
    response.delete_cookie("username", path="/")
    return response


@app.route("/create")
def create_course_page() -> str:
    sample_yaml_path = Path("sample.yaml")
    sample_content = ""
    if sample_yaml_path.exists():
        with open(sample_yaml_path, "r") as f:
            sample_content = f.read()

    # Read the prompt template
    prompt_path = Path("prompt/create.txt")
    prompt_text = ""
    if prompt_path.exists():
        with open(prompt_path, "r") as f:
            prompt_text = f.read()

    # Load latest 5 jobs for current user
    g.cursor.execute(
        """SELECT id, task_id, user_id, topic, status, created_at, updated_at
           FROM jobs
           ORDER BY created_at DESC
           LIMIT 5""",
    )
    jobs = [
        Job(
            id=row[0],
            task_id=row[1],
            user_id=row[2],
            topic=row[3],
            status=JobStatus(row[4]),
            created_at=row[5],
            updated_at=row[6],
        )
        for row in g.cursor.fetchall()
    ]

    return render_template(
        "create.html", sample_content=sample_content, prompt_text=prompt_text, jobs=jobs
    )


@app.route("/create", methods=["POST"])
def create_course() -> str:
    """Start a Huey task to generate a course from a topic"""
    course_topic = request.form.get("course_topic", "")

    if not course_topic or not course_topic.strip():
        return "<p>Error: No course topic provided</p>"

    # Check if user already has 5 pending jobs
    g.cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE status = ?",
        (JobStatus.PENDING,),
    )
    pending_count = g.cursor.fetchone()[0]

    if pending_count >= 5:
        return "<p>Error: You already have 5 pending jobs. Please wait for some to complete.</p>"

    # Queue the task - need to create result first to get task_id
    # Use schedule to delay getting result.id
    import uuid

    task_id = str(uuid.uuid4())

    # Save job to database first
    g.cursor.execute(
        "INSERT INTO jobs (task_id, user_id, topic, status) VALUES (?, ?, ?, ?)",
        (task_id, g.user.id, course_topic.strip(), JobStatus.PENDING),
    )

    # Queue the task with the pre-generated task_id
    create_course_task(course_topic.strip(), task_id)

    return f"<p>Course generation started for topic: {escape(course_topic)}</p>"


@app.route("/create-manual", methods=["POST"])
def create_course_manual() -> str:
    # Read input
    yaml_content = ""

    uploaded_file = request.files.get("yaml_file")
    if uploaded_file and uploaded_file.filename:
        try:
            yaml_content = uploaded_file.read().decode("utf-8")
        except UnicodeDecodeError:
            return "<p>Error: Uploaded file must be UTF-8 encoded text.</p>"

    if not yaml_content:
        yaml_content = request.form.get("yaml_content", "")

    if not yaml_content or not yaml_content.strip():
        return "<p>Error: No YAML content provided</p>"

    # validate yaml, hash, check if it exists
    try:
        course_data = yaml.safe_load(yaml_content)
        if not course_data:
            return "<p>Error: Empty or invalid YAML</p>"

        validate_course(course_data)

        file_hash = hashlib.md5(yaml_content.encode()).digest()

        if check_course_exists(g.cursor, file_hash):
            return "<p>Error: This course already exists</p>"

        # save in db if it doesn't exist
        course_id = save_course(g.cursor, course_data, file_hash)

        # return message based on success or error
        return f'<p>Success! Course "{escape(course_data["title"])}" created. <a href="/course/{course_id}">View course</a></p>'

    except yaml.YAMLError as e:
        return f"<p>Error: YAML parsing failed: {escape(str(e))}</p>"
    except ValueError as e:
        return f"<p>Error: {escape(str(e))}</p>"
    except Exception as e:
        return f"<p>Error: {escape(str(e))}</p>"


@app.errorhandler(RequestEntityTooLarge)
def handle_large_upload(_: RequestEntityTooLarge) -> tuple[str, int]:
    return (
        "<p>Error: Upload too large. Maximum supported size is 1 MB.</p>",
        413,
    )


def knowledge_point_ids_completed_after_time(
    cursor: sqlite3.Cursor, completed_kp_ids: List[int], time: str, user_id: int
) -> List[int]:
    placeholders = ",".join("?" * len(completed_kp_ids))
    cursor.execute(
        f"""SELECT DISTINCT kp.id
            FROM knowledge_points kp
            JOIN questions q ON q.knowledge_point_id = kp.id
            JOIN lesson_questions lq ON lq.question_id = q.id
            JOIN answers a ON a.question_id = q.id
            WHERE kp.id IN ({placeholders})
            AND lq.user_id = ?
            AND a.user_id = ?
            AND a.created_at > ?""",
        (*completed_kp_ids, user_id, user_id, time),
    )
    return [row[0] for row in cursor.fetchall()]


@app.route("/course/<int:course_id>")
def course_page(course_id: int) -> str:
    # TODO: simplify this page logic
    course = load_full_course_from_db(g.cursor, course_id, g.user.id)
    if not course:
        abort_course_not_found(course_id)

    # Build a map of knowledge point ID to completion status
    completed_kp_ids = set()
    completed_kp_via_diagnostic_ids = set()
    for lesson in course.lessons:
        for kp in lesson.knowledge_points:
            # Either all questions have been answered, or last X questions were
            # answered correctly in a row
            answered_questions = [
                question for question in kp.lesson_questions if question.answer
            ]
            all_questions_answered = len(answered_questions) == len(kp.lesson_questions)
            no_new_questions = len(kp.questions) == 0
            passed_consec_questions = (
                kp.last_consecutive_correct_answers() >= config.correct_count_threshold
            )
            if (all_questions_answered and no_new_questions) or passed_consec_questions:
                completed_kp_ids.add(kp.id)
            passed_diagnostic = len(kp.diagnostic_questions) > 0 and all(
                q.answer is not None and q.answer.choice_id == q.correct_choice().id
                for q in kp.diagnostic_questions
            )
            if passed_diagnostic:
                completed_kp_via_diagnostic_ids.add(kp.id)

    next_lessons: list[Lesson] = []
    completed_lessons: list[Lesson] = []
    remaining_lessons: list[Lesson] = []
    for lesson in course.lessons:
        # Check if lesson is completed
        lesson_completed = all(
            kp.id in completed_kp_ids.union(completed_kp_via_diagnostic_ids)
            for kp in lesson.knowledge_points
        )

        if lesson_completed:
            completed_lessons.append(lesson)
            continue

        prerequisites_met = True
        lesson_kp_ids = set()
        for kp in lesson.knowledge_points:
            lesson_kp_ids.add(kp.id)
            if any(
                prereq_id
                not in (
                    completed_kp_ids.union(completed_kp_via_diagnostic_ids).union(
                        lesson_kp_ids
                    )
                )
                for prereq_id in kp.prerequisites
            ):
                prerequisites_met = False
                break

        if prerequisites_met:
            next_lessons.append(lesson)
            continue

        remaining_lessons.append(lesson)

    # Create a diagnostic if one doesn't exist for this course
    g.cursor.execute(
        "SELECT id FROM diagnostics WHERE course_id = ? AND user_id = ?",
        (course_id, g.user.id),
    )
    diagnostic_row = g.cursor.fetchone()
    if not diagnostic_row:
        g.cursor.execute(
            "INSERT INTO diagnostics (course_id, user_id) VALUES (?, ?)",
            (course_id, g.user.id),
        )
        diagnostic_id = g.cursor.lastrowid
    else:
        diagnostic_id = diagnostic_row[0]
    assert diagnostic_id is not None

    # Get the creation time of the last quiz (or use epoch if no quizzes exist)
    g.cursor.execute(
        "SELECT created_at FROM quizzes WHERE course_id = ? AND user_id = ? ORDER BY created_at DESC LIMIT 1",
        (course_id, g.user.id),
    )
    last_quiz_row = g.cursor.fetchone()
    last_quiz_time = last_quiz_row[0] if last_quiz_row else "1970-01-01 00:00:00"

    # Get KP IDs completed after the last quiz using a single query
    # Exclude questions that are quiz questions
    # Exclude questions that are review questions
    recent_completed_kp_ids = knowledge_point_ids_completed_after_time(
        g.cursor, list(completed_kp_ids), last_quiz_time, g.user.id
    )

    # Create a new quiz if threshold is met
    if len(recent_completed_kp_ids) >= config.quiz_knowledge_point_count_threshold:
        # Get recently completed KPs from the course data

        recent_kps: list[KnowledgePoint] = []
        for lesson in course.lessons:
            for kp in lesson.knowledge_points:
                if kp.id in recent_completed_kp_ids:
                    recent_kps.append(kp)

        # Randomly select up to quiz_question_count KPs
        selected_kps = random.sample(recent_kps, config.quiz_question_count)

        # Collect one unanswered question from each selected KP
        quiz_questions = []
        for kp in selected_kps:
            if len(kp.questions) == 0:
                continue
            question = random.choice(kp.questions)
            quiz_questions.append(question.id)

        # Create quiz, then insert all quiz questions in one query
        assert len(quiz_questions) > 0

        g.cursor.execute(
            "INSERT INTO quizzes (course_id, user_id) VALUES (?, ?)",
            (course_id, g.user.id),
        )
        quiz_id = g.cursor.lastrowid

        g.cursor.executemany(
            "INSERT INTO quiz_questions (quiz_id, question_id) VALUES (?, ?)",
            zip([quiz_id] * len(quiz_questions), quiz_questions),
        )

    # Load all quizzes for this course
    g.cursor.execute(
        "SELECT id FROM quizzes WHERE course_id = ? AND user_id = ?",
        (course_id, g.user.id),
    )
    quiz_rows = g.cursor.fetchall()

    # Separate quizzes into available and completed
    available_quizzes = []
    completed_quizzes = []

    for (quiz_id,) in quiz_rows:
        quiz = load_quiz_from_db(g.cursor, quiz_id, course_id)
        if not quiz:
            continue

        # Check if quiz is completed (time is up OR has any answers)
        has_answers = any(q.answer is not None for q in quiz.questions)
        time_is_up = False

        if quiz.started_at:
            start_time = datetime.fromisoformat(quiz.started_at)
            end_time = start_time + timedelta(minutes=config.quiz_time_limit_minutes)
            now = datetime.now()
            time_is_up = now > end_time

        if has_answers or time_is_up:
            completed_quizzes.append(quiz)
        else:
            available_quizzes.append(quiz)

    # Create a new review if needed
    # Get completed kps with no postreqs
    # If they haven't had any review yet (TODO fix later, should be able to have multiple)
    # if it's been X knowledge points completed since then
    id_to_knowledge_points: Dict[int, KnowledgePoint] = {}
    for lesson in course.lessons:
        for knowledge_point in lesson.knowledge_points:
            id_to_knowledge_points[knowledge_point.id] = knowledge_point
    postreqs: Dict[int, List[int]] = {id: [] for id in id_to_knowledge_points.keys()}
    for id, knowledge_point in id_to_knowledge_points.items():
        for prereq in knowledge_point.prerequisites:
            postreqs[prereq].append(id)
    completed_kp_no_post_reqs = [
        kp
        for id, kp in id_to_knowledge_points.items()
        if id in completed_kp_ids and len(postreqs[id]) == 0
    ]
    g.cursor.execute(
        """SELECT
            kp.id as knowledge_point_id,
            MAX(a.created_at) as last_answered_at
        FROM knowledge_points kp
        JOIN lessons l ON kp.lesson_id = l.id
        JOIN questions q ON q.knowledge_point_id = kp.id
        JOIN lesson_questions lq ON lq.question_id = q.id AND lq.user_id = ?
        LEFT JOIN answers a ON a.question_id = q.id AND a.user_id = ?
        WHERE l.course_id = ?
        GROUP BY kp.id
        HAVING MAX(a.created_at) IS NOT NULL
        ORDER BY last_answered_at DESC""",
        (g.user.id, g.user.id, course_id),
    )
    answered_kp_id_to_completed_time: Dict[int, str] = {
        row[0]: row[1] for row in g.cursor.fetchall()
    }

    g.cursor.execute(
        """SELECT r.id, r.knowledge_point_id
           FROM reviews r
           JOIN knowledge_points kp ON r.knowledge_point_id = kp.id
           JOIN lessons l ON kp.lesson_id = l.id
           WHERE l.course_id = ?
           AND r.user_id = ?""",
        (course_id, g.user.id),
    )
    kp_ids_with_reviews = set(kp_id for _, kp_id in g.cursor.fetchall())

    for knowledge_point in completed_kp_no_post_reqs:
        if knowledge_point.id in kp_ids_with_reviews:
            continue
        assert knowledge_point.id in answered_kp_id_to_completed_time.keys()
        completed_time = answered_kp_id_to_completed_time[knowledge_point.id]
        completed_kp_ids_after_kp = knowledge_point_ids_completed_after_time(
            g.cursor, list(completed_kp_ids), completed_time, g.user.id
        )
        if (
            len(completed_kp_ids_after_kp)
            >= config.review_knowledge_point_count_threshold
        ):
            g.cursor.execute(
                "INSERT INTO reviews (knowledge_point_id, user_id) VALUES (?, ?)",
                (knowledge_point.id, g.user.id),
            )

    # Load all reviews for this course using a single query with JOINs
    g.cursor.execute(
        """SELECT r.id, r.knowledge_point_id
           FROM reviews r
           JOIN knowledge_points kp ON r.knowledge_point_id = kp.id
           JOIN lessons l ON kp.lesson_id = l.id
           WHERE l.course_id = ?
           AND r.user_id = ?""",
        (course_id, g.user.id),
    )
    review_rows = g.cursor.fetchall()

    available_reviews = []
    completed_reviews = []

    for review_id, kp_id in review_rows:
        # Find the knowledge point
        knowledge_point = id_to_knowledge_points[kp_id]
        review = Review(id=review_id, knowledge_point=knowledge_point)

        # Either all questions have been answered, or last X questions were
        # answered correctly in a row
        answered_questions = [
            question
            for question in knowledge_point.reviewed_questions
            if question.answer
        ]
        if (
            (
                len(knowledge_point.reviewed_questions) > 0
                and len(answered_questions) == len(knowledge_point.reviewed_questions)
            )
            or knowledge_point.last_consecutive_correct_review_answers()
            >= config.review_correct_count_threshold
        ):
            completed_reviews.append(review)
        else:
            available_reviews.append(review)

    # Get completion dates for all completed items
    completed_items: List[CourseItem] = []

    # Add completed lessons with their completion dates
    for lesson in completed_lessons:
        # Get the latest answer date for any question in this lesson
        lesson_question_ids = []
        for kp in lesson.knowledge_points:
            lesson_question_ids += [q.id for q in kp.lesson_questions]
            lesson_question_ids += [q.id for q in kp.diagnostic_questions]
        placeholders = ",".join("?" * len(lesson_question_ids))
        g.cursor.execute(
            f"""SELECT MAX(a.created_at)
                FROM answers a
                WHERE a.question_id IN ({placeholders})
                AND a.user_id = ?""",
            (*lesson_question_ids, g.user.id),
        )
        completion_date = g.cursor.fetchone()[0]
        if completion_date:
            completed_items.append(
                CourseItem(
                    type="lesson",
                    item=lesson,
                    completion_date=completion_date,
                )
            )

    # Add completed quizzes with their completion dates
    for quiz in completed_quizzes:
        quiz_question_ids = [q.id for q in quiz.questions]
        if quiz_question_ids:
            placeholders = ",".join("?" * len(quiz_question_ids))
            g.cursor.execute(
                f"""SELECT MAX(a.created_at)
                    FROM answers a
                    WHERE a.question_id IN ({placeholders})
                    AND a.user_id = ?""",
                (*quiz_question_ids, g.user.id),
            )
            completion_date = g.cursor.fetchone()[0]
            if completion_date:
                completed_items.append(
                    CourseItem(
                        type="quiz",
                        item=quiz,
                        completion_date=completion_date,
                    )
                )

    # Add completed reviews with their completion dates
    for review in completed_reviews:
        review_question_ids = [q.id for q in review.knowledge_point.reviewed_questions]
        if review_question_ids:
            placeholders = ",".join("?" * len(review_question_ids))
            g.cursor.execute(
                f"""SELECT MAX(a.created_at)
                    FROM answers a
                    WHERE a.question_id IN ({placeholders})
                    AND a.user_id = ?""",
                (*review_question_ids, g.user.id),
            )
            completion_date = g.cursor.fetchone()[0]
            if completion_date:
                completed_items.append(
                    CourseItem(
                        type="review",
                        item=review,
                        completion_date=completion_date,
                    )
                )

    # Check if diagnostic is completed
    g.cursor.execute(
        """SELECT question_id FROM diagnostic_questions
           WHERE diagnostic_id = ?
           ORDER BY id""",
        (diagnostic_id,),
    )
    diagnostic_question_ids = [row[0] for row in g.cursor.fetchall()]

    placeholders = ",".join("?" * len(diagnostic_question_ids))
    g.cursor.execute(
        f"""SELECT COUNT(*) FROM answers a
            WHERE a.question_id IN ({placeholders})
            AND a.user_id = ?""",
        (*diagnostic_question_ids, g.user.id),
    )
    answered_count = g.cursor.fetchone()[0]
    diagnostic_complete = (
        answered_count == len(diagnostic_question_ids)
        and len(diagnostic_question_ids) > 0
    )
    if diagnostic_complete:
        # Get completion date
        g.cursor.execute(
            f"""SELECT MAX(a.created_at)
                FROM answers a
                WHERE a.question_id IN ({placeholders})
                AND a.user_id = ?""",
            (*diagnostic_question_ids, g.user.id),
        )
        completion_date = g.cursor.fetchone()[0]
        completed_items.append(
            CourseItem(
                type="diagnostic",
                item=Diagnostic(id=diagnostic_id, course_id=course_id),
                completion_date=completion_date,
            )
        )

    # Sort by completion date (latest completed first)
    completed_items.sort(key=lambda x: x.completion_date or "", reverse=True)

    # Determine what to show in "Next" section (prioritized order)
    next_items: List[CourseItem] = []

    if not diagnostic_complete:
        next_items.append(
            CourseItem(
                type="diagnostic",
                item=Diagnostic(id=diagnostic_id, course_id=course_id),
            )
        )
        remaining_lessons = next_lessons + remaining_lessons
    elif available_quizzes:
        for quiz in available_quizzes:
            next_items.append(CourseItem(type="quiz", item=quiz))
        remaining_lessons = next_lessons + remaining_lessons
    elif available_reviews:
        for review in available_reviews:
            next_items.append(CourseItem(type="review", item=review))
        remaining_lessons = next_lessons + remaining_lessons
    elif next_lessons:
        for lesson in next_lessons:
            next_items.append(CourseItem(type="lesson", item=lesson))

    return render_template(
        "course.html",
        course_id=course.id,
        course_title=course.title,
        next_items=next_items,
        remaining_lessons=remaining_lessons,
        completed_items=completed_items,
    )


def extract_graph_data_from_course(
    course: Course,
) -> KnowledgeGraph:
    """Extract graph data from a Course object for visualization."""
    nodes: Dict[str, str] = {}
    edges: list[tuple[str, str]] = []
    for lesson in course.lessons:
        for kp in lesson.knowledge_points:
            node_id = str(kp.id)
            label = f"{kp.name}\\n({lesson.title})"
            nodes[node_id] = label
            for prereq_id in kp.prerequisites:
                edges.append((str(prereq_id), node_id))

    return KnowledgeGraph(course.title, nodes, edges)


@app.route("/course/<int:course_id>/graph")
def course_graph(course_id: int) -> Any:
    """Generate and return the knowledge graph visualization for a course"""
    # TODO: only load what's needed, not entire course
    course = load_full_course_from_db(g.cursor, course_id, g.user.id)
    if not course:
        abort_course_not_found(course_id)

    graph = extract_graph_data_from_course(course)
    dot = create_knowledge_graph(graph)
    png_bytes = dot.pipe(format="png")

    return send_file(BytesIO(png_bytes), mimetype="image/png")


@app.route("/course/<int:course_id>/lesson/<int:lesson_id>")
def lesson_page(course_id: int, lesson_id: int) -> str:
    course_title = load_course_title_from_db(g.cursor, course_id)
    if not course_title:
        abort_course_not_found(course_id)
    lesson = load_lesson_from_db(g.cursor, lesson_id, g.user.id)
    if not lesson:
        abort_lesson_not_found(lesson_id, course_id)
    assert len(lesson.knowledge_points) > 0

    # Create lesson questions for all knowledge points in this lesson if they don't exist
    for i, kp in enumerate(lesson.knowledge_points):
        # Check if we already have lesson questions for this knowledge point
        if len(kp.lesson_questions) == 0 and len(kp.questions) > 0:
            # Create lesson questions for all available questions
            next_question = random.choice(kp.questions)
            g.cursor.execute(
                "INSERT INTO lesson_questions (question_id, user_id) VALUES (?, ?)",
                (next_question.id, g.user.id),
            )
            lesson.knowledge_points[i].lesson_questions.append(next_question)

    return render_template(
        "lesson.html",
        course_id=course_id,
        course_title=course_title,
        lesson_id=lesson_id,
        lesson_title=lesson.title,
        knowledge_point=lesson.knowledge_points[0],
        knowledge_point_index=0,
        i=0,
    )


@app.route("/course/<int:course_id>/lesson/<int:lesson_id>/submit", methods=["POST"])
def lesson_submit_answer(course_id: int, lesson_id: int) -> str:
    course_title = load_course_title_from_db(g.cursor, course_id)
    if not course_title:
        abort_course_not_found(course_id)
    lesson = load_lesson_from_db(g.cursor, lesson_id, g.user.id)
    if not lesson:
        abort_lesson_not_found(lesson_id, course_id)

    kp_index_str = request.form.get("knowledge_point_index")
    question_index_str = request.form.get("question_index")
    i_str = request.form.get("i")
    answer_str = request.form.get("answer")
    if (
        not kp_index_str
        or question_index_str is None
        or i_str is None
        or answer_str is None
    ):
        abort_missing_parameters(
            "knowledge_point_index", "question_index", "i", "answer"
        )

    kp_index = int(kp_index_str)
    question_index = int(question_index_str)
    i = int(i_str)
    choice_id = int(answer_str)

    # Validate the answer
    question = lesson.knowledge_points[kp_index].lesson_questions[question_index]
    # Find the choice by ID instead of using index
    user_choice = next((c for c in question.choices if c.id == choice_id), None)
    if not user_choice:
        print(
            f"Could not find choice {choice_id} in {[c.id for c in question.choices]}"
        )
        abort(400, description=f"Invalid choice ID: {choice_id}")

    # Save the user's answer to the database
    g.cursor.execute(
        "INSERT INTO answers (user_id, question_id, choice_id) VALUES (?, ?, ?)",
        (g.user.id, question.id, user_choice.id),
    )
    answer_id = g.cursor.lastrowid
    assert answer_id is not None
    # Important that we populate this the rest of this handler can assume correct state
    lesson.knowledge_points[kp_index].lesson_questions[question_index].answer = Answer(
        id=answer_id, question_id=question.id, choice_id=user_choice.id
    )

    is_correct = user_choice.correct
    correct_answer_index = next(
        i for i, choice in enumerate(question.choices) if choice.correct
    )
    correct_answer_text = question.choices[correct_answer_index].text

    feedback = render_template(
        "answer_feedback.html",
        is_correct=is_correct,
        correct_answer_text=correct_answer_text,
        explanation=question.explanation,
    )

    # Check if user has failed the knowledge point (3+ wrong answers)
    knowledge_point = lesson.knowledge_points[kp_index]
    incorrect_count = len(
        [
            question
            for question in knowledge_point.lesson_questions
            if question.answer is not None
            and question.answer.choice_id != question.correct_choice().id
        ]
    )
    failed_knowledge_point = incorrect_count >= config.incorrect_count_fail_threshold

    failure_message = ""
    next_button_html = ""
    if failed_knowledge_point:
        # Delete all answers for questions in this lesson
        for kp in lesson.knowledge_points:
            for q in kp.lesson_questions:
                if q.answer:
                    g.cursor.execute(
                        "DELETE FROM answers WHERE id = ? and user_id = ?",
                        (q.answer.id, g.user.id),
                    )
                g.cursor.execute(
                    "DELETE FROM lesson_questions WHERE question_id = ? and user_id = ?",
                    (q.id, g.user.id),
                )

        failure_message = f"""
        <div>
            <p>❌ You need to restart this lesson.</p>
            <a href="/course/{course_id}/lesson/{lesson_id}" class="button">Restart Lesson</a>
        </div>
        """
    else:
        if (
            knowledge_point.last_consecutive_correct_answers()
            < config.correct_count_threshold
            and len(knowledge_point.questions) > 0
        ):
            next_question = random.choice(knowledge_point.questions)
            g.cursor.execute(
                "INSERT INTO lesson_questions (question_id, user_id) VALUES (?, ?)",
                (next_question.id, g.user.id),
            )
            lesson.knowledge_points[kp_index].lesson_questions.append(next_question)
        if kp_index < len(lesson.knowledge_points):
            next_button_html = render_template(
                "next_button.html",
                course_id=course_id,
                lesson_id=lesson.id,
                knowledge_point_index=kp_index,
                knowledge_point=lesson.knowledge_points[kp_index],
                i=i,
            )

    return f"{feedback}{failure_message}{next_button_html}"


@app.route("/course/<int:course_id>/lesson/<int:lesson_id>/next", methods=["POST"])
def lesson_next_lesson_chunk(course_id: int, lesson_id: int) -> str:
    course_title = load_course_title_from_db(g.cursor, course_id)
    if not course_title:
        abort_course_not_found(course_id)
    lesson = load_lesson_from_db(g.cursor, lesson_id, g.user.id)
    if not lesson:
        abort_lesson_not_found(lesson_id, course_id)

    kp_index_str = request.form.get("knowledge_point_index")
    i_str = request.form.get("i")
    if not kp_index_str or not i_str:
        abort_missing_parameters("knowledge_point_index", "i")
    kp_index = int(kp_index_str)
    if kp_index >= len(lesson.knowledge_points):
        return ""

    i = int(i_str)
    knowledge_point = lesson.knowledge_points[kp_index]
    completed_kp = (
        knowledge_point.last_consecutive_correct_answers()
        >= config.correct_count_threshold
    )
    question_index = i - len(knowledge_point.contents)
    new_question = question_index >= len(
        [question for question in knowledge_point.lesson_questions if question.answer]
    )
    if completed_kp and new_question:
        kp_index += 1
        i = 0

    return render_template(
        "knowledge_point.html",
        course_id=course_id,
        lesson_id=lesson.id,
        knowledge_point_index=kp_index,
        knowledge_point=lesson.knowledge_points[kp_index],
        i=i,
    )


def load_quiz_from_db(
    cursor: sqlite3.Cursor, quiz_id: int, course_id: int
) -> Optional[Quiz]:
    """Load a quiz with its questions, choices, and answers from the database"""
    # Verify quiz exists and belongs to course, and get started_at
    cursor.execute(
        "SELECT started_at FROM quizzes WHERE id = ? AND course_id = ? AND user_id = ?",
        (quiz_id, course_id, g.user.id),
    )
    quiz_row = cursor.fetchone()
    if not quiz_row:
        return None

    started_at = quiz_row[0]

    # Load quiz questions
    cursor.execute(
        """SELECT q.id, q.prompt, q.knowledge_point_id, q.explanation
           FROM quiz_questions qq
           JOIN questions q ON qq.question_id = q.id
           WHERE qq.quiz_id = ?""",
        (quiz_id,),
    )
    question_rows = cursor.fetchall()

    questions = []
    for q_id, q_prompt, q_kp_id, q_explanation in question_rows:
        # Load choices for this question
        cursor.execute(
            "SELECT id, text, is_correct FROM choices WHERE question_id = ?", (q_id,)
        )
        choices = [
            Choice(id=c_id, text=c_text, correct=c_correct)
            for c_id, c_text, c_correct in cursor.fetchall()
        ]

        # Load answer if exists
        cursor.execute(
            "SELECT id, choice_id FROM answers WHERE question_id = ? AND user_id = ?",
            (q_id, g.user.id),
        )
        answer_row = cursor.fetchone()
        answer = (
            Answer(id=answer_row[0], question_id=q_id, choice_id=answer_row[1])
            if answer_row
            else None
        )

        questions.append(
            Question(
                id=q_id,
                prompt=q_prompt,
                choices=choices,
                answer=answer,
                knowledge_point_id=q_kp_id,
                explanation=q_explanation,
            )
        )

    return Quiz(
        id=quiz_id, course_id=course_id, questions=questions, started_at=started_at
    )


@app.route("/course/<int:course_id>/quiz/<int:quiz_id>")
def quiz_page(course_id: int, quiz_id: int) -> str:
    course_title = load_course_title_from_db(g.cursor, course_id)
    if not course_title:
        abort_course_not_found(course_id)

    # Load quiz using helper function
    quiz = load_quiz_from_db(g.cursor, quiz_id, course_id)
    if not quiz:
        abort_quiz_not_found(quiz_id, course_id)

    # Set started_at if this is the first time loading the quiz
    if quiz.started_at is None:
        g.cursor.execute(
            "UPDATE quizzes SET started_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?",
            (quiz_id, g.user.id),
        )

    # Check if quiz has been submitted (all questions have answers)
    is_submitted = all(q.answer is not None for q in quiz.questions)

    # Calculate score if submitted
    score = None
    if is_submitted:
        correct_count = sum(
            1
            for q in quiz.questions
            if q.answer and q.answer.choice_id == q.correct_choice().id
        )
        total_questions = len(quiz.questions)
        score_percentage = (
            (correct_count / total_questions * 100) if total_questions > 0 else 0
        )
        score = f"{correct_count}/{total_questions} ({score_percentage:.0f}%)"

    return render_template(
        "quiz.html",
        course_id=course_id,
        course_title=course_title,
        quiz=quiz,
        quiz_time_limit_minutes=config.quiz_time_limit_minutes,
        is_submitted=is_submitted,
        score=score,
    )


@app.route("/course/<int:course_id>/quiz/<int:quiz_id>/submit", methods=["POST"])
def quiz_submit(course_id: int, quiz_id: int) -> Any:
    quiz = load_quiz_from_db(g.cursor, quiz_id, course_id)
    if not quiz or quiz.started_at is None:
        abort_quiz_not_found(quiz_id, course_id)

    # Validate submission time (within 10 seconds of expected end time)
    from datetime import datetime, timedelta

    start_time = datetime.fromisoformat(quiz.started_at)
    expected_end_time = start_time + timedelta(minutes=config.quiz_time_limit_minutes)
    now = datetime.now()

    # Check if submission is within 10 seconds after expected end time
    if now > expected_end_time + timedelta(seconds=10):
        abort(400, description="Quiz time limit exceeded")

    # Collect knowledge point IDs for incorrect answers
    incorrect_kp_ids = set()

    # Process and store answers
    for question in quiz.questions:
        answer_key = f"question_{question.id}"
        if answer_key in request.form:
            choice_id = int(request.form[answer_key])

            # Find the choice by ID
            user_choice = next((c for c in question.choices if c.id == choice_id), None)
            if user_choice:
                # Store the answer
                g.cursor.execute(
                    "INSERT OR REPLACE INTO answers (user_id, question_id, choice_id) VALUES (?, ?, ?)",
                    (g.user.id, question.id, choice_id),
                )

                # Check if answer is incorrect
                is_correct = user_choice.correct
                if not is_correct:
                    incorrect_kp_ids.add(question.knowledge_point_id)

    # Create reviews for incorrect knowledge points
    for kp_id in incorrect_kp_ids:
        g.cursor.execute(
            "INSERT INTO reviews (knowledge_point_id, user_id) VALUES (?, ?)",
            (kp_id, g.user.id),
        )

    # Redirect to quiz page to show results
    return redirect(f"/course/{course_id}/quiz/{quiz_id}")


def create_review_question(
    cursor: sqlite3.Cursor, review_id: int, knowledge_point: KnowledgePoint
) -> Optional[Question]:
    if len(knowledge_point.questions) == 0:
        return None  # No more questions available

    # Pick a random question
    unanswered = [q for q in knowledge_point.questions if q.answer is None]
    selected_question = random.choice(unanswered)

    # Create review_question entry
    cursor.execute(
        "INSERT INTO review_questions (review_id, question_id) VALUES (?, ?)",
        (review_id, selected_question.id),
    )

    return selected_question


@app.route("/course/<int:course_id>/review/<int:review_id>")
def review_page(course_id: int, review_id: int) -> str:
    course_title = load_course_title_from_db(g.cursor, course_id)
    if not course_title:
        abort_course_not_found(course_id)

    g.cursor.execute(
        "SELECT knowledge_point_id FROM reviews WHERE id = ? AND user_id = ?",
        (review_id, g.user.id),
    )
    review_row = g.cursor.fetchone()
    if not review_row:
        abort_review_not_found(review_id, course_id)

    kp_id = review_row[0]
    knowledge_point = load_knowledge_point_from_db(g.cursor, kp_id, g.user.id)

    if not knowledge_point:
        abort_knowledge_point_not_found(kp_id)

    # Get or create first review question (i=0)
    question = None
    if len(knowledge_point.reviewed_questions) > 0:
        question = knowledge_point.reviewed_questions[0]
    else:
        question = create_review_question(g.cursor, review_id, knowledge_point)

    return render_template(
        "question_page.html",
        page_title=f"Review: {knowledge_point.name}",
        course_id=course_id,
        course_title=course_title,
        entity_type="review",
        entity_id=review_id,
        question=question,
        i=0,
    )


@app.route("/course/<int:course_id>/review/<int:review_id>/submit", methods=["POST"])
def review_submit_answer(course_id: int, review_id: int) -> str:
    course_title = load_course_title_from_db(g.cursor, course_id)
    if not course_title:
        abort_course_not_found(course_id)

    g.cursor.execute(
        "SELECT knowledge_point_id FROM reviews WHERE id = ? AND user_id = ?",
        (review_id, g.user.id),
    )
    review_row = g.cursor.fetchone()
    if not review_row:
        abort_review_not_found(review_id, course_id)

    kp_id = review_row[0]
    knowledge_point = load_knowledge_point_from_db(g.cursor, kp_id, g.user.id)

    if not knowledge_point:
        abort_knowledge_point_not_found(kp_id)

    i_str = request.form.get("i")
    answer_str = request.form.get("answer")
    if i_str is None or answer_str is None:
        abort_missing_parameters("i", "answer")

    i = int(i_str)
    choice_id = int(answer_str)

    # Get the question at this index
    if i >= len(knowledge_point.reviewed_questions):
        print(f"Tried to submit answer for reviewed question index out of bounds: {i}")
        abort(400, description=f"Invalid question index: {i}")
    print(i)
    print(knowledge_point.reviewed_questions)
    question = knowledge_point.reviewed_questions[i]

    # Find the choice by ID
    user_choice = next((c for c in question.choices if c.id == choice_id), None)
    if not user_choice:
        print(
            f"Could not find choice {choice_id} in {[c.id for c in question.choices]}"
        )
        abort(400, description=f"Invalid choice ID: {choice_id}")

    # Save the user's answer to the database
    print(question.id)
    g.cursor.execute(
        "INSERT INTO answers (user_id, question_id, choice_id) VALUES (?, ?, ?)",
        (g.user.id, question.id, user_choice.id),
    )
    answer_id = g.cursor.lastrowid
    assert answer_id is not None
    # Important that we populate this the rest of this handler can assume correct state
    knowledge_point.reviewed_questions[i].answer = Answer(
        id=answer_id, question_id=question.id, choice_id=user_choice.id
    )

    is_correct = user_choice.correct
    correct_answer_index = next(
        idx for idx, choice in enumerate(question.choices) if choice.correct
    )
    correct_answer_text = question.choices[correct_answer_index].text

    feedback = render_template(
        "answer_feedback.html",
        is_correct=is_correct,
        correct_answer_text=correct_answer_text,
        explanation=question.explanation,
    )

    # Create new question if needed (haven't answered enough correct in a row, and unanswered questions left)
    if (
        knowledge_point.last_consecutive_correct_review_answers()
        < config.review_correct_count_threshold
        and len(knowledge_point.questions) > 0
    ):
        new_question = create_review_question(g.cursor, review_id, knowledge_point)
        assert new_question is not None

    next_button_html = render_template(
        "question_next_button.html",
        course_id=course_id,
        entity_type="review",
        entity_id=review_id,
        i=i,
    )

    return f"{feedback}{next_button_html}"


@app.route("/course/<int:course_id>/review/<int:review_id>/next", methods=["POST"])
def review_next_question(course_id: int, review_id: int) -> str:
    course_title = load_course_title_from_db(g.cursor, course_id)
    if not course_title:
        abort_course_not_found(course_id)

    g.cursor.execute(
        "SELECT knowledge_point_id FROM reviews WHERE id = ? AND user_id = ?",
        (review_id, g.user.id),
    )
    review_row = g.cursor.fetchone()
    if not review_row:
        abort_review_not_found(review_id, course_id)

    kp_id = review_row[0]
    knowledge_point = load_knowledge_point_from_db(g.cursor, kp_id, g.user.id)

    if not knowledge_point:
        abort_knowledge_point_not_found(kp_id)

    i_str = request.form.get("i")
    if not i_str:
        abort_missing_parameters("i")
    i = int(i_str)

    if i >= len(knowledge_point.reviewed_questions):
        # No more questions left, we're done
        return ""

    question = knowledge_point.reviewed_questions[i]

    return render_template(
        "question_form.html",
        course_id=course_id,
        entity_type="review",
        entity_id=review_id,
        question=question,
        i=i,
    )


def create_diagnostic_question(
    cursor: sqlite3.Cursor, diagnostic_id: int, course_id: int, user_id: int
) -> Optional[Question]:
    # All knowledge points for this course
    cursor.execute(
        """SELECT kp.id
           FROM courses c
           JOIN lessons l ON l.course_id = c.id
           JOIN knowledge_points kp ON kp.lesson_id = l.id
           WHERE c.id = ?""",
        (course_id,),
    )
    kp_ids = [id for (id,) in cursor.fetchall()]

    cursor.execute(
        """SELECT q.id, q.knowledge_point_id, q.prompt, q.explanation
           FROM questions q
           JOIN diagnostic_questions dq ON dq.question_id = q.id
           WHERE dq.diagnostic_id = ?
           ORDER BY q.id""",
        (diagnostic_id,),
    )
    question_rows = g.cursor.fetchall()
    diagnostic_questions: list[Question] = []
    for question_id, knowledge_point_id, prompt, explanation in question_rows:
        choices = load_choices_from_db(g.cursor, question_id)
        answer = load_answer_from_db(g.cursor, question_id, g.user.id)
        diagnostic_questions.append(
            Question(
                id=question_id,
                prompt=prompt,
                choices=choices,
                answer=answer,
                knowledge_point_id=knowledge_point_id,
                explanation=explanation,
            )
        )

    # Get all diagnostic completed knowledge points
    diagnostic_completed_knowledge_point_ids = set()
    for question in diagnostic_questions:
        # Assuming only 1 diagnostic question per knowledge point
        if (
            question.answer is not None
            and question.answer.choice_id == question.correct_choice().id
        ):
            diagnostic_completed_knowledge_point_ids.add(question.knowledge_point_id)

    used_knowledge_point_ids = set(
        question.knowledge_point_id for question in diagnostic_questions
    )
    unused_knowledge_point_ids = set(kp_ids).difference(used_knowledge_point_ids)

    placeholders = ",".join("?" * len(unused_knowledge_point_ids))
    cursor.execute(
        f"""SELECT knowledge_point_id, prerequisite_id
           FROM prerequisites
           WHERE knowledge_point_id IN ({placeholders})""",
        (*unused_knowledge_point_ids,),
    )
    prereqs: dict[int, list[int]] = {id: [] for id in unused_knowledge_point_ids}
    for knowledge_point_id, prereq_id in cursor.fetchall():
        prereqs[knowledge_point_id].append(prereq_id)

    next_knowledge_point_id = None
    for knowledge_point_id in unused_knowledge_point_ids:
        if all(
            prereq in diagnostic_completed_knowledge_point_ids
            for prereq in prereqs[knowledge_point_id]
        ):
            next_knowledge_point_id = knowledge_point_id

    if next_knowledge_point_id is None:
        return None

    next_knowledge_point = load_knowledge_point_from_db(
        cursor, next_knowledge_point_id, user_id
    )
    assert next_knowledge_point is not None
    assert len(next_knowledge_point.questions) > 0
    selected_question = random.choice(next_knowledge_point.questions)

    # Create review_question entry
    cursor.execute(
        "INSERT INTO diagnostic_questions (diagnostic_id, question_id) VALUES (?, ?)",
        (diagnostic_id, selected_question.id),
    )

    return selected_question


def load_question_from_db(
    cursor: sqlite3.Cursor, question_id: int, user_id: int
) -> Optional[Question]:
    cursor.execute(
        """SELECT id, knowledge_point_id, prompt, explanation
           FROM questions q
           WHERE id = ?""",
        (question_id,),
    )
    question_row = g.cursor.fetchone()
    if question_row is None:
        return None

    question_id, knowledge_point_id, prompt, explanation = question_row
    choices = load_choices_from_db(cursor, question_id)
    answer = load_answer_from_db(cursor, question_id, user_id)
    return Question(
        id=question_id,
        prompt=prompt,
        choices=choices,
        answer=answer,
        knowledge_point_id=knowledge_point_id,
        explanation=explanation,
    )


@app.route("/course/<int:course_id>/diagnostic/<int:diagnostic_id>")
def diagnostic_page(course_id: int, diagnostic_id: int) -> str:
    course_title = load_course_title_from_db(g.cursor, course_id)
    if not course_title:
        abort_course_not_found(course_id)

    # Verify diagnostic exists and belongs to course
    g.cursor.execute(
        "SELECT id FROM diagnostics WHERE id = ? AND course_id = ? AND user_id = ?",
        (diagnostic_id, course_id, g.user.id),
    )
    if not g.cursor.fetchone():
        abort_diagnostic_not_found(diagnostic_id, course_id)

    # Get or create first diagnostic question (i=0)
    g.cursor.execute(
        """SELECT q.id
           FROM questions q
           JOIN diagnostic_questions dq ON dq.question_id = q.id
           WHERE dq.diagnostic_id = ?
           ORDER BY q.id
           LIMIT 1""",
        (diagnostic_id,),
    )
    question_row = g.cursor.fetchone()
    if question_row is not None:
        question_id = question_row[0]
        first_question = load_question_from_db(g.cursor, question_id, g.user.id)
    else:
        first_question = create_diagnostic_question(
            g.cursor, diagnostic_id, course_id, g.user.id
        )
    assert first_question is not None

    return render_template(
        "question_page.html",
        page_title="Diagnostic",
        course_id=course_id,
        course_title=course_title,
        entity_type="diagnostic",
        entity_id=diagnostic_id,
        question=first_question,
        i=0,
    )


@app.route(
    "/course/<int:course_id>/diagnostic/<int:diagnostic_id>/submit", methods=["POST"]
)
def diagnostic_submit_answer(course_id: int, diagnostic_id: int) -> str:
    course_title = load_course_title_from_db(g.cursor, course_id)
    if not course_title:
        abort_course_not_found(course_id)

    # Verify diagnostic exists
    g.cursor.execute(
        "SELECT id FROM diagnostics WHERE id = ? AND course_id = ? AND user_id = ?",
        (diagnostic_id, course_id, g.user.id),
    )
    if not g.cursor.fetchone():
        abort_diagnostic_not_found(diagnostic_id, course_id)

    i_str = request.form.get("i")
    answer_str = request.form.get("answer")
    if i_str is None or answer_str is None:
        abort_missing_parameters("i", "answer")

    i = int(i_str)
    choice_id = int(answer_str)

    # Get diagnostic questions
    g.cursor.execute(
        """SELECT question_id FROM diagnostic_questions
           WHERE diagnostic_id = ?
           ORDER BY id""",
        (diagnostic_id,),
    )
    diagnostic_question_ids = [row[0] for row in g.cursor.fetchall()]

    if i >= len(diagnostic_question_ids):
        abort(400, description=f"Invalid question index: {i}")

    question_id = diagnostic_question_ids[i]

    # Find the question in the course
    question = load_question_from_db(g.cursor, question_id, g.user.id)
    if not question:
        abort(404, description=f"Question with ID {question_id} not found")

    # Find the choice by ID
    user_choice = next((c for c in question.choices if c.id == choice_id), None)
    if not user_choice:
        print(
            f"Could not find choice {choice_id} in {[c.id for c in question.choices]}"
        )
        abort(400, description=f"Invalid choice ID: {choice_id}")

    # Save the user's answer to the database
    g.cursor.execute(
        "INSERT INTO answers (user_id, question_id, choice_id) VALUES (?, ?, ?)",
        (g.user.id, question.id, user_choice.id),
    )

    is_correct = user_choice.correct
    correct_answer_index = next(
        idx for idx, choice in enumerate(question.choices) if choice.correct
    )
    correct_answer_text = question.choices[correct_answer_index].text

    feedback = render_template(
        "answer_feedback.html",
        is_correct=is_correct,
        correct_answer_text=correct_answer_text,
        explanation=None,
    )

    # Create new question if more questions are needed
    # For now, just create one new question
    create_diagnostic_question(g.cursor, diagnostic_id, course_id, g.user.id)

    next_button_html = render_template(
        "question_next_button.html",
        course_id=course_id,
        entity_type="diagnostic",
        entity_id=diagnostic_id,
        i=i,
    )

    return f"{feedback}{next_button_html}"


@app.route(
    "/course/<int:course_id>/diagnostic/<int:diagnostic_id>/next", methods=["POST"]
)
def diagnostic_next_question(course_id: int, diagnostic_id: int) -> str:
    course_title = load_course_title_from_db(g.cursor, course_id)
    if not course_title:
        abort_course_not_found(course_id)

    # Verify diagnostic exists
    g.cursor.execute(
        "SELECT id FROM diagnostics WHERE id = ? AND course_id = ? AND user_id = ?",
        (diagnostic_id, course_id, g.user.id),
    )
    if not g.cursor.fetchone():
        abort_diagnostic_not_found(diagnostic_id, course_id)

    i_str = request.form.get("i")
    if not i_str:
        abort_missing_parameters("i")
    i = int(i_str)

    # Get diagnostic questions
    g.cursor.execute(
        """SELECT question_id FROM diagnostic_questions
           WHERE diagnostic_id = ?
           ORDER BY id""",
        (diagnostic_id,),
    )
    diagnostic_question_ids = [row[0] for row in g.cursor.fetchall()]

    if i >= len(diagnostic_question_ids):
        # No more questions left, we're done
        return ""

    question_id = diagnostic_question_ids[i]

    # Find the question in the course
    question = load_question_from_db(g.cursor, question_id, g.user.id)
    if question is None:
        abort(
            404,
            description=f"Question id {question_id} not found for diagnostic {diagnostic_id}",
        )

    return render_template(
        "question_form.html",
        course_id=course_id,
        entity_type="diagnostic",
        entity_id=diagnostic_id,
        question=question,
        i=i,
    )


# Error handlers
@app.errorhandler(400)
def handle_400(e: Any) -> tuple[str, int]:
    """Handle bad request errors"""
    return render_template(
        "error.html", error_code=400, error_message=e.description
    ), 400


@app.errorhandler(403)
def handle_403(e: Any) -> tuple[str, int]:
    """Handle forbidden errors"""
    return render_template(
        "error.html", error_code=403, error_message=e.description
    ), 403


@app.errorhandler(404)
def handle_404(e: Any) -> tuple[str, int]:
    """Handle not found errors"""
    return render_template(
        "error.html", error_code=404, error_message=e.description
    ), 404


@app.errorhandler(500)
def handle_500(e: Any) -> tuple[str, int]:
    """Handle internal server errors"""
    return render_template(
        "error.html", error_code=500, error_message=e.description
    ), 500


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Noobular Flask application")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument(
        "--port", type=int, default=5000, help="Port to run on (default: 5000)"
    )
    args = parser.parse_args()
    global config  # Initialize the module level config instead of declaring new var
    config = AppConfig.debug() if args.debug else AppConfig.prod()
    init_database()
    load_courses_to_db()
    app.run(debug=args.debug, port=args.port)


if __name__ == "__main__":
    main()
