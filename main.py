from flask import Flask, render_template, abort, request, render_template_string
import yaml
import sqlite3
import hashlib
from pathlib import Path
from typing import Any, List, Optional
from dataclasses import dataclass


def init_database() -> None:
    """Initialize SQLite database on app startup"""
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()

        # Create courses table
        cursor.execute("""CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            file_hash BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(file_hash)
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
            knowledge_point_id TEXT NOT NULL,
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
            question_id INTEGER NOT NULL,
            choice_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES questions (id),
            FOREIGN KEY (choice_id) REFERENCES choices (id),
            UNIQUE(question_id)
        )""")

        print("✅ Database tables created successfully!")


def load_courses_to_database() -> None:
    """Load courses from YAML files into database"""
    if not COURSES_DIRECTORY.is_dir():
        print("No courses directory found, skipping course loading")
        return

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()

        for yaml_file in COURSES_DIRECTORY.glob("*.yaml"):
            # Calculate file hash (MD5, 16 bytes)
            with open(yaml_file, "rb") as f:
                file_hash = hashlib.md5(f.read()).digest()

            # Check if this file hash already exists
            cursor.execute("SELECT id FROM courses WHERE file_hash = ?", (file_hash,))
            if cursor.fetchone():
                print(f"Course {yaml_file.name} already loaded (unchanged), skipping")
                continue

            course = load_course_by_route(yaml_file.stem)
            if not course:
                continue

            # Insert course with hash
            cursor.execute(
                "INSERT OR REPLACE INTO courses (title, file_hash) VALUES (?, ?)",
                (course.title, file_hash),
            )
            course_id = cursor.lastrowid

            # Insert lessons
            for lesson in course.lessons:
                cursor.execute(
                    "INSERT OR REPLACE INTO lessons (course_id, title) VALUES (?, ?)",
                    (course_id, lesson.title),
                )
                lesson_id = cursor.lastrowid

                # Insert knowledge points, contents, and questions
                for knowledge_point in lesson.knowledge_points:
                    cursor.execute(
                        """INSERT OR REPLACE INTO knowledge_points
                                     (lesson_id, knowledge_point_id, description)
                                     VALUES (?, ?, ?)""",
                        (lesson_id, knowledge_point.id, knowledge_point.description),
                    )
                    knowledge_point_db_id = cursor.lastrowid

                    # Insert contents
                    for content in knowledge_point.contents:
                        cursor.execute(
                            """INSERT OR REPLACE INTO contents
                                         (knowledge_point_id, text)
                                         VALUES (?, ?)""",
                            (knowledge_point_db_id, content.text),
                        )

                    # Insert questions and choices
                    for question in knowledge_point.questions:
                        cursor.execute(
                            """INSERT OR REPLACE INTO questions
                                         (knowledge_point_id, prompt)
                                         VALUES (?, ?)""",
                            (knowledge_point_db_id, question.prompt),
                        )
                        question_id = cursor.lastrowid

                        # Insert choices
                        for choice in question.choices:
                            cursor.execute(
                                """INSERT OR REPLACE INTO choices
                                             (question_id, text, is_correct)
                                             VALUES (?, ?, ?)""",
                                (question_id, choice.text, choice.correct or False),
                            )

        print("✅ Courses loaded into database successfully!")


# Init app
app = Flask(__name__)

counter = 0


@dataclass
class Choice:
    text: str
    correct: Optional[bool] = None


@dataclass
class Question:
    prompt: str
    choices: List[Choice]


@dataclass
class Content:
    text: str


@dataclass
class KnowledgePoint:
    id: str  # kebab-case identifier
    description: str
    contents: List[Content]
    questions: List[Question]


@dataclass
class Lesson:
    title: str
    route: str
    knowledge_points: List[KnowledgePoint]


@dataclass
class Course:
    title: str
    route: str
    lessons: List[Lesson]


COURSES_DIRECTORY = Path("courses")


def load_course_by_route(route: str) -> Optional[Course]:
    yaml_file = COURSES_DIRECTORY / f"{route}.yaml"
    if not yaml_file.exists():
        return None

    with open(yaml_file, "r") as f:
        course_data = yaml.safe_load(f) or {}

    title = course_data.get("title")
    if not title:
        raise ValueError(f"Course {yaml_file.name} missing required 'title' field")

    lessons = []
    for lesson_data in course_data.get("lessons", []):
        knowledge_points = []
        for kp_data in lesson_data.get("knowledge_points", []):
            # Parse contents
            contents = [
                Content(text=content_text)
                for content_text in kp_data.get("contents", [])
            ]

            # Parse questions
            questions = []
            for question_data in kp_data.get("questions", []):
                choices = [
                    Choice(text=choice["text"], correct=choice.get("correct", False))
                    for choice in question_data.get("choices", [])
                ]

                # Validate that there's exactly one correct choice
                correct_count = sum(1 for choice in choices if choice.correct)
                if correct_count != 1:
                    raise ValueError(
                        f"Question '{question_data['prompt']}' has {correct_count} correct answers, expected exactly 1"
                    )

                questions.append(
                    Question(prompt=question_data["prompt"], choices=choices)
                )

            knowledge_point = KnowledgePoint(
                id=kp_data["id"],
                description=kp_data["description"],
                contents=contents,
                questions=questions,
            )
            knowledge_points.append(knowledge_point)

        lessons.append(
            Lesson(
                title=lesson_data["title"],
                route=lesson_data["route"],
                knowledge_points=knowledge_points,
            )
        )
    return Course(title=title, route=route, lessons=lessons)


@app.route("/")
def index() -> str:
    if not COURSES_DIRECTORY.is_dir():
        raise FileNotFoundError(
            f"Courses directory '{COURSES_DIRECTORY}' must exist and be a directory"
        )

    courses = []
    for yaml_file in COURSES_DIRECTORY.glob("*.yaml"):
        course = load_course_by_route(yaml_file.stem)
        if course:
            courses.append(course)

    return render_template("index.html", counter=counter, courses=courses)


@app.route("/course/<course_route>")
def course_page(course_route: str) -> str:
    course = load_course_by_route(course_route)
    if not course:
        abort(404)
    return render_template("course.html", course=course)


def render_macro(template_file: str, macro_name: str, **kwargs: Any) -> str:
    """Helper function to render a single Jinja2 macro with given arguments."""
    args = ", ".join(kwargs.keys())
    template_string = (
        f"{{% from '{template_file}' import {macro_name} %}}"
        + f"{{{{ {macro_name}({args}) }}}}"
    )
    return render_template_string(template_string, **kwargs)


@app.route("/course/<course_route>/lesson/<lesson_route>")
def lesson_page(course_route: str, lesson_route: str) -> str:
    course = load_course_by_route(course_route)
    if not course:
        abort(404)

    # Find the lesson with matching route
    lesson = None
    for lesson in course.lessons:
        if lesson.route == lesson_route:
            lesson = lesson
            break

    if not lesson:
        abort(404)
    assert len(lesson.knowledge_points) > 0

    return render_template(
        "lesson.html",
        course=course,
        lesson=lesson,
    )


@app.route("/course/<course_route>/lesson/<lesson_route>/submit", methods=["POST"])
def lesson_submit_answer(course_route: str, lesson_route: str) -> str:
    course = load_course_by_route(course_route)
    if not course:
        abort(404)

    # Find the lesson
    lesson = None
    for lesson in course.lessons:
        if lesson.route == lesson_route:
            lesson = lesson
            break

    if not lesson:
        abort(404)

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
        abort(404)

    kp_index = int(kp_index_str)
    question_index = int(question_index_str)
    i = int(i_str)
    answer_index = int(answer_str)

    # Validate the answer
    knowledge_point = lesson.knowledge_points[kp_index]
    question = knowledge_point.questions[question_index]

    is_correct = question.choices[answer_index].correct
    correct_answer_index = next(
        i for i, choice in enumerate(question.choices) if choice.correct
    )
    correct_answer_text = question.choices[correct_answer_index].text
    if is_correct:
        feedback = f"✅ Correct! The correct answer is: {correct_answer_text}"
    else:
        feedback = f"❌ Incorrect. The correct answer is: {correct_answer_text}"

    print(
        kp_index,
        question_index,
        i,
        len(knowledge_point.contents) + len(knowledge_point.questions),
    )
    # Render next button with logic handled in macro
    next_button_html = render_macro(
        "lesson_macros.html",
        "render_next_button",
        course=course,
        lesson=lesson,
        knowledge_point=knowledge_point,
        kp_index=kp_index,
        i=i,
    )

    return f"<p>{feedback}</p>{next_button_html}"


@app.route("/course/<course_route>/lesson/<lesson_route>/next", methods=["POST"])
def lesson_next_lesson_chunk(course_route: str, lesson_route: str) -> str:
    course = load_course_by_route(course_route)
    if not course:
        abort(404)

    # Find the lesson
    lesson = None
    for lesson in course.lessons:
        if lesson.route == lesson_route:
            lesson = lesson
            break

    if not lesson:
        abort(404)

    kp_index_str = request.form.get("knowledge_point_index")
    i_str = request.form.get("i")
    if not kp_index_str or not i_str:
        abort(404)
    kp_index = int(kp_index_str)
    assert kp_index < len(lesson.knowledge_points)
    i = int(i_str)

    return render_macro(
        "lesson_macros.html",
        "render_knowledge_point",
        course=course,
        lesson=lesson,
        knowledge_point=lesson.knowledge_points[kp_index],
        knowledge_point_index=kp_index,
        i=i,
    )


@app.route("/increment", methods=["POST"])
def increment() -> str:
    global counter
    counter += 1
    # return just the snippet HTMX will swap in
    return f"<div id='count'>Count: {counter}</div>"


if __name__ == "__main__":
    init_database()
    load_courses_to_database()
    app.run(debug=True, port=5000)
