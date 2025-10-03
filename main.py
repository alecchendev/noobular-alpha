from flask import Flask, render_template, abort, request, g, jsonify
import yaml
import sqlite3
import hashlib
from pathlib import Path
from typing import Any, List, Optional
from dataclasses import dataclass


def init_database() -> None:
    """Initialize SQLite database on app startup"""
    conn = sqlite3.connect(DATABASE)
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
    conn.close()


# Init app
app = Flask(__name__)

DATABASE = "database.db"


def get_db() -> sqlite3.Connection:
    """Get database connection for current request"""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Enable dict-like access
    db: sqlite3.Connection = g.db
    return db


def close_db() -> None:
    """Close database connection"""
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.teardown_appcontext
def close_db_connection(error: Any) -> None:
    """Automatically close db connection at end of request"""
    close_db()


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


@dataclass
class Content:
    id: int
    text: str


@dataclass
class KnowledgePoint:
    id: int
    name: str
    description: str
    contents: List[Content]
    questions: List[Question]


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
class ValidationSuccess:
    success: bool
    message: str
    status_code: int = 200

    def jsonify(self) -> tuple[Any, int]:
        return jsonify(
            {"success": self.success, "message": self.message}
        ), self.status_code


@dataclass
class ValidationError:
    error: str
    status_code: int = 400

    def jsonify(self) -> tuple[Any, int]:
        return jsonify({"error": self.error}), self.status_code


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
                Content(id=-1, text=content_text)
                for content_text in kp_data.get("contents", [])
            ]

            # Parse questions
            questions = []
            for question_data in kp_data.get("questions", []):
                choices = [
                    Choice(
                        id=-1, text=choice["text"], correct=choice.get("correct", False)
                    )
                    for choice in question_data.get("choices", [])
                ]

                # Validate that there's exactly one correct choice
                correct_count = sum(1 for choice in choices if choice.correct)
                if correct_count != 1:
                    raise ValueError(
                        f"Question '{question_data['prompt']}' has {correct_count} correct answers, expected exactly 1"
                    )

                questions.append(
                    Question(
                        id=-1,
                        prompt=question_data["prompt"],
                        choices=choices,
                        answer=None,
                    )
                )

            knowledge_point = KnowledgePoint(
                id=-1,
                name=kp_data["name"],
                description=kp_data["description"],
                contents=contents,
                questions=questions,
            )
            knowledge_points.append(knowledge_point)

        lessons.append(
            Lesson(
                id=-1,
                title=lesson_data["title"],
                knowledge_points=knowledge_points,
            )
        )
    return Course(id=-1, title=title, lessons=lessons)


def load_courses_to_database() -> None:
    """Load courses from YAML files into database"""
    if not COURSES_DIRECTORY.is_dir():
        print("No courses directory found, skipping course loading")
        return

    with sqlite3.connect(DATABASE) as conn:
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
                                     (lesson_id, name, description)
                                     VALUES (?, ?, ?)""",
                        (lesson_id, knowledge_point.name, knowledge_point.description),
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


def load_course_from_db(course_id: int) -> Optional[Course]:
    """Load a course from the database by ID"""
    db = get_db()
    cursor = db.cursor()

    # Get course
    cursor.execute("SELECT title FROM courses WHERE id = ?", (course_id,))
    course_row = cursor.fetchone()
    if not course_row:
        return None

    course_title = course_row[0]

    # Get lessons
    cursor.execute("SELECT id, title FROM lessons WHERE course_id = ?", (course_id,))
    lesson_rows = cursor.fetchall()

    lessons = []
    for lesson_id, lesson_title in lesson_rows:
        # Get knowledge points for this lesson
        cursor.execute(
            "SELECT id, name, description FROM knowledge_points WHERE lesson_id = ?",
            (lesson_id,),
        )
        kp_rows = cursor.fetchall()

        knowledge_points = []
        for kp_db_id, kp_name, kp_description in kp_rows:
            # Get contents for this knowledge point
            cursor.execute(
                "SELECT id, text FROM contents WHERE knowledge_point_id = ?",
                (kp_db_id,),
            )
            content_rows = cursor.fetchall()
            contents = [Content(id=id, text=text) for id, text in content_rows]

            # Get questions for this knowledge point
            cursor.execute(
                "SELECT id, prompt FROM questions WHERE knowledge_point_id = ?",
                (kp_db_id,),
            )
            question_rows = cursor.fetchall()

            questions = []
            for question_id, prompt in question_rows:
                # Get choices for this question
                cursor.execute(
                    "SELECT id, text, is_correct FROM choices WHERE question_id = ?",
                    (question_id,),
                )
                choice_rows = cursor.fetchall()
                choices = [
                    Choice(id=id, text=text, correct=bool(is_correct))
                    for id, text, is_correct in choice_rows
                ]

                cursor.execute(
                    """SELECT id, question_id, choice_id FROM answers
                       WHERE question_id = ?""",
                    (question_id,),
                )
                answer_row = cursor.fetchone()
                answer = None
                if answer_row:
                    id, question_id, choice_id = answer_row
                    answer = Answer(id=id, question_id=question_id, choice_id=choice_id)

                questions.append(
                    Question(
                        id=question_id, prompt=prompt, choices=choices, answer=answer
                    )
                )

            knowledge_points.append(
                KnowledgePoint(
                    id=kp_db_id,
                    name=kp_name,
                    description=kp_description,
                    contents=contents,
                    questions=questions,
                )
            )

        lessons.append(
            Lesson(id=lesson_id, title=lesson_title, knowledge_points=knowledge_points)
        )

    return Course(id=course_id, title=course_title, lessons=lessons)


def get_all_courses() -> List[Course]:
    """Get all courses from the database"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM courses")
    course_ids = cursor.fetchall()

    courses = []
    for (course_id,) in course_ids:
        course = load_course_from_db(course_id)
        if course:
            courses.append(course)

    return courses


@app.route("/")
def index() -> str:
    courses = get_all_courses()
    return render_template("index.html", courses=courses)


@app.route("/course/<int:course_id>")
def course_page(course_id: int) -> str:
    course = load_course_from_db(course_id)
    if not course:
        abort(404)
    next_lessons = []
    completed_lessons = []
    for lesson in course.lessons:
        if all(
            all(question.answer is not None for question in kp.questions)
            for kp in lesson.knowledge_points
        ):
            completed_lessons.append(lesson)
        else:
            next_lessons.append(lesson)
    return render_template(
        "course.html",
        course=course,
        next_lessons=next_lessons,
        completed_lessons=completed_lessons,
    )


@app.route("/course/<int:course_id>/lesson/<int:lesson_id>")
def lesson_page(course_id: int, lesson_id: int) -> str:
    course = load_course_from_db(course_id)
    if not course:
        abort(404)

    # Find the lesson with matching ID
    lesson = None
    for lesson_obj in course.lessons:
        if lesson_obj.id == lesson_id:
            lesson = lesson_obj
            break

    if not lesson:
        abort(404)
    assert len(lesson.knowledge_points) > 0

    return render_template(
        "lesson.html",
        course=course,
        lesson=lesson,
    )


@app.route("/course/<int:course_id>/lesson/<int:lesson_id>/submit", methods=["POST"])
def lesson_submit_answer(course_id: int, lesson_id: int) -> str:
    course = load_course_from_db(course_id)
    if not course:
        abort(404)

    # Find the lesson
    lesson = None
    for lesson_obj in course.lessons:
        if lesson_obj.id == lesson_id:
            lesson = lesson_obj
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
    user_choice = question.choices[answer_index]

    # Save the user's answer to the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO answers (question_id, choice_id) VALUES (?, ?)",
        (question.id, user_choice.id),
    )
    db.commit()

    is_correct = user_choice.correct
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
    # Render next button with logic handled in template
    next_button_html = render_template(
        "next_button.html",
        course=course,
        lesson=lesson,
        knowledge_point=knowledge_point,
        knowledge_point_index=kp_index,
        i=i,
    )

    return f"<p>{feedback}</p>{next_button_html}"


@app.route("/validate-course", methods=["POST"])
def validate_course() -> tuple[Any, int]:
    """Validate that a course file parses correctly"""
    data = request.get_json()
    if not data or "filename" not in data:
        return ValidationError(error="Missing 'filename' in request body").jsonify()

    filename = data["filename"]
    file_path = COURSES_DIRECTORY / filename

    # Check if file exists
    if not file_path.exists():
        return ValidationError(
            error=f"File '{filename}' not found in courses directory", status_code=404
        ).jsonify()

    # Check if file has .yaml extension
    if file_path.suffix not in [".yaml", ".yml"]:
        return ValidationError(error=f"File '{filename}' is not a YAML file").jsonify()

    try:
        # Read and parse YAML
        with open(file_path, "r") as f:
            course_data = yaml.safe_load(f)

        if not course_data:
            return ValidationError(
                error="File is empty or contains no valid YAML"
            ).jsonify()

        # Validate required fields
        if "title" not in course_data:
            return ValidationError(error="Missing required field: 'title'").jsonify()

        if (
            not isinstance(course_data["title"], str)
            or not course_data["title"].strip()
        ):
            return ValidationError(
                error="Field 'title' must be a non-empty string"
            ).jsonify()

        # Validate lessons
        if "lessons" not in course_data:
            return ValidationError(error="Missing required field: 'lessons'").jsonify()

        if not isinstance(course_data["lessons"], list):
            return ValidationError(error="Field 'lessons' must be a list").jsonify()

        for lesson_idx, lesson_data in enumerate(course_data["lessons"]):
            if not isinstance(lesson_data, dict):
                return ValidationError(
                    error=f"Lesson {lesson_idx} must be an object"
                ).jsonify()

            if "title" not in lesson_data:
                return ValidationError(
                    error=f"Lesson {lesson_idx} missing required field: 'title'"
                ).jsonify()

            if "knowledge_points" not in lesson_data:
                return ValidationError(
                    error=f"Lesson {lesson_idx} ('{lesson_data.get('title', 'unnamed')}') missing required field: 'knowledge_points'"
                ).jsonify()

            if not isinstance(lesson_data["knowledge_points"], list):
                return ValidationError(
                    error=f"Lesson {lesson_idx} ('{lesson_data['title']}') field 'knowledge_points' must be a list"
                ).jsonify()

            # Validate knowledge points
            for kp_idx, kp_data in enumerate(lesson_data["knowledge_points"]):
                if not isinstance(kp_data, dict):
                    return ValidationError(
                        error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} must be an object"
                    ).jsonify()

                if "name" not in kp_data:
                    return ValidationError(
                        error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} missing required field: 'name'"
                    ).jsonify()

                if "description" not in kp_data:
                    return ValidationError(
                        error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data.get('name', 'unknown')}') missing required field: 'description'"
                    ).jsonify()

                if "contents" not in kp_data:
                    return ValidationError(
                        error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}') missing required field: 'contents'"
                    ).jsonify()

                if not isinstance(kp_data["contents"], list):
                    return ValidationError(
                        error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}') field 'contents' must be a list"
                    ).jsonify()

                if "questions" not in kp_data:
                    return ValidationError(
                        error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}') missing required field: 'questions'"
                    ).jsonify()

                if not isinstance(kp_data["questions"], list):
                    return ValidationError(
                        error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}') field 'questions' must be a list"
                    ).jsonify()

                # Validate questions
                for q_idx, question_data in enumerate(kp_data["questions"]):
                    if not isinstance(question_data, dict):
                        return ValidationError(
                            error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} must be an object"
                        ).jsonify()

                    if "prompt" not in question_data:
                        return ValidationError(
                            error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} missing required field: 'prompt'"
                        ).jsonify()

                    if "choices" not in question_data:
                        return ValidationError(
                            error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} (prompt: '{question_data.get('prompt', 'unknown')}') missing required field: 'choices'"
                        ).jsonify()

                    if not isinstance(question_data["choices"], list):
                        return ValidationError(
                            error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} (prompt: '{question_data['prompt']}') field 'choices' must be a list"
                        ).jsonify()

                    if len(question_data["choices"]) < 2:
                        return ValidationError(
                            error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} (prompt: '{question_data['prompt']}') must have at least 2 choices"
                        ).jsonify()

                    # Validate choices and count correct answers
                    correct_count = 0
                    for c_idx, choice_data in enumerate(question_data["choices"]):
                        if not isinstance(choice_data, dict):
                            return ValidationError(
                                error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} (prompt: '{question_data['prompt']}'), choice {c_idx} must be an object"
                            ).jsonify()

                        if "text" not in choice_data:
                            return ValidationError(
                                error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} (prompt: '{question_data['prompt']}'), choice {c_idx} missing required field: 'text'"
                            ).jsonify()

                        if choice_data.get("correct", False):
                            correct_count += 1

                    # Validate exactly one correct answer
                    if correct_count != 1:
                        return ValidationError(
                            error=f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question '{question_data['prompt']}' has {correct_count} correct answers, expected exactly 1"
                        ).jsonify()

        return ValidationSuccess(
            success=True, message=f"Course '{course_data['title']}' is valid"
        ).jsonify()

    except yaml.YAMLError as e:
        return ValidationError(error=f"YAML parsing error: {str(e)}").jsonify()
    except Exception as e:
        return ValidationError(
            error=f"Unexpected error: {str(e)}", status_code=500
        ).jsonify()


@app.route("/course/<int:course_id>/lesson/<int:lesson_id>/next", methods=["POST"])
def lesson_next_lesson_chunk(course_id: int, lesson_id: int) -> str:
    course = load_course_from_db(course_id)
    if not course:
        abort(404)

    # Find the lesson
    lesson = None
    for lesson_obj in course.lessons:
        if lesson_obj.id == lesson_id:
            lesson = lesson_obj
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

    return render_template(
        "knowledge_point.html",
        course=course,
        lesson=lesson,
        knowledge_point=lesson.knowledge_points[kp_index],
        knowledge_point_index=kp_index,
        i=i,
    )


if __name__ == "__main__":
    init_database()
    load_courses_to_database()
    app.run(debug=True, port=5000)
