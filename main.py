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

    # Create prerequisites table
    cursor.execute("""CREATE TABLE IF NOT EXISTS prerequisites (
        id INTEGER PRIMARY KEY,
        knowledge_point_id INTEGER NOT NULL,
        prerequisite_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points (id),
        FOREIGN KEY (prerequisite_id) REFERENCES knowledge_points (id)
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
    prerequisites: List[int]
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


def validate_and_parse_course(course_data: dict[str, Any]) -> Course:
    """Validate course data and return a Course object. Raises ValueError on validation failure."""
    # Validate required fields
    if "title" not in course_data:
        raise ValueError("Missing required field: 'title'")

    if not isinstance(course_data["title"], str) or not course_data["title"].strip():
        raise ValueError("Field 'title' must be a non-empty string")

    # Validate lessons
    if "lessons" not in course_data:
        raise ValueError("Missing required field: 'lessons'")

    if not isinstance(course_data["lessons"], list):
        raise ValueError("Field 'lessons' must be a list")

    # Collect all knowledge point names for prerequisite validation
    all_kp_names = set()
    for lesson_data in course_data.get("lessons", []):
        for kp_data in lesson_data.get("knowledge_points", []):
            if "name" in kp_data:
                all_kp_names.add(kp_data["name"])

    for lesson_idx, lesson_data in enumerate(course_data["lessons"]):
        if not isinstance(lesson_data, dict):
            raise ValueError(f"Lesson {lesson_idx} must be an object")

        if "title" not in lesson_data:
            raise ValueError(f"Lesson {lesson_idx} missing required field: 'title'")

        if "knowledge_points" not in lesson_data:
            raise ValueError(
                f"Lesson {lesson_idx} ('{lesson_data.get('title', 'unnamed')}') missing required field: 'knowledge_points'"
            )

        if not isinstance(lesson_data["knowledge_points"], list):
            raise ValueError(
                f"Lesson {lesson_idx} ('{lesson_data['title']}') field 'knowledge_points' must be a list"
            )

        # Validate knowledge points
        for kp_idx, kp_data in enumerate(lesson_data["knowledge_points"]):
            if not isinstance(kp_data, dict):
                raise ValueError(
                    f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} must be an object"
                )

            if "name" not in kp_data:
                raise ValueError(
                    f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} missing required field: 'name'"
                )

            if "description" not in kp_data:
                raise ValueError(
                    f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data.get('name', 'unknown')}') missing required field: 'description'"
                )

            if "contents" not in kp_data:
                raise ValueError(
                    f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}') missing required field: 'contents'"
                )

            if not isinstance(kp_data["contents"], list):
                raise ValueError(
                    f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}') field 'contents' must be a list"
                )

            if "questions" not in kp_data:
                raise ValueError(
                    f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}') missing required field: 'questions'"
                )

            if not isinstance(kp_data["questions"], list):
                raise ValueError(
                    f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}') field 'questions' must be a list"
                )

            # Validate prerequisites
            if "prerequisites" not in kp_data:
                raise ValueError(
                    f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}') missing required field: 'prerequisites'"
                )

            if not isinstance(kp_data["prerequisites"], list):
                raise ValueError(
                    f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}') field 'prerequisites' must be a list"
                )

            for prereq_idx, prerequisite_name in enumerate(kp_data["prerequisites"]):
                if not isinstance(prerequisite_name, str):
                    raise ValueError(
                        f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), prerequisite {prereq_idx} must be a string"
                    )

                if prerequisite_name not in all_kp_names:
                    raise ValueError(
                        f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), prerequisite '{prerequisite_name}' does not exist in this course"
                    )

            # Validate questions
            for q_idx, question_data in enumerate(kp_data["questions"]):
                if not isinstance(question_data, dict):
                    raise ValueError(
                        f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} must be an object"
                    )

                if "prompt" not in question_data:
                    raise ValueError(
                        f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} missing required field: 'prompt'"
                    )

                if "choices" not in question_data:
                    raise ValueError(
                        f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} (prompt: '{question_data.get('prompt', 'unknown')}') missing required field: 'choices'"
                    )

                if not isinstance(question_data["choices"], list):
                    raise ValueError(
                        f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} (prompt: '{question_data['prompt']}') field 'choices' must be a list"
                    )

                if len(question_data["choices"]) < 2:
                    raise ValueError(
                        f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} (prompt: '{question_data['prompt']}') must have at least 2 choices"
                    )

                # Validate choices and count correct answers
                correct_count = 0
                for c_idx, choice_data in enumerate(question_data["choices"]):
                    if not isinstance(choice_data, dict):
                        raise ValueError(
                            f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} (prompt: '{question_data['prompt']}'), choice {c_idx} must be an object"
                        )

                    if "text" not in choice_data:
                        raise ValueError(
                            f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} (prompt: '{question_data['prompt']}'), choice {c_idx} missing required field: 'text'"
                        )

                    if choice_data.get("correct", False):
                        correct_count += 1

                # Validate exactly one correct answer
                if correct_count != 1:
                    raise ValueError(
                        f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question '{question_data['prompt']}' has {correct_count} correct answers, expected exactly 1"
                    )

    # Validate prereq tree
    kp_to_prereqs: dict[str, set[str]] = {}
    prereq_to_kps: dict[str, set[str]] = {}
    for lesson_data in course_data.get("lessons", []):
        for kp_data in lesson_data.get("knowledge_points", []):
            if kp_data["name"] not in kp_to_prereqs.keys():
                kp_to_prereqs[kp_data["name"]] = set()
            kp_to_prereqs[kp_data["name"]].update(kp_data["prerequisites"])
            for prereq in kp_data["prerequisites"]:
                if prereq not in prereq_to_kps.keys():
                    prereq_to_kps[prereq] = set()
                prereq_to_kps[prereq].add(kp_data["name"])

    # Get roots
    roots = [kp for kp, prereqs in kp_to_prereqs.items() if len(prereqs) == 0]

    # Check cycles
    def has_cycle_dfs(node: str, visited: set[str], rec_stack: list[str]) -> bool:
        visited.add(node)
        rec_stack.append(node)

        for kp in prereq_to_kps.get(node, set()):
            if kp not in visited:
                if has_cycle_dfs(kp, visited, rec_stack):
                    return True
            elif kp in rec_stack:
                rec_stack.append(kp)
                return True

        rec_stack.remove(node)
        return False

    visited_for_cycles: set[str] = set()
    for kp_name in roots:
        if kp_name not in visited_for_cycles:
            rec_stack: list[str] = []
            if has_cycle_dfs(kp_name, visited_for_cycles, rec_stack):
                raise ValueError(
                    f"Prerequisite cycle detected in prerequisite graph: {' -> '.join(rec_stack)}"
                )

    # Check every node got visited once
    unreachable = set(kp_to_prereqs.keys()) - visited_for_cycles
    if len(unreachable) != 0:
        loop_rec_stack: list[str] = []
        has_cycle_dfs(list(unreachable)[0], set(), loop_rec_stack)
        raise ValueError(
            f"Cannot visit all knowledge points in prerequisite graph. Some knowledge points are not reachable from root nodes because they form a loop: {' -> '.join(loop_rec_stack)}"
        )

    # Build Course object
    lessons = []
    for lesson_data in course_data.get("lessons", []):
        knowledge_points = []
        for kp_data in lesson_data.get("knowledge_points", []):
            contents = [
                Content(id=-1, text=content_text)
                for content_text in kp_data.get("contents", [])
            ]

            questions = []
            for question_data in kp_data.get("questions", []):
                choices = [
                    Choice(
                        id=-1, text=choice["text"], correct=choice.get("correct", False)
                    )
                    for choice in question_data.get("choices", [])
                ]

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
                prerequisites=[],
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

    return Course(id=-1, title=course_data["title"], lessons=lessons)


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

            # Load YAML data
            with open(yaml_file, "r") as f:
                course_data = yaml.safe_load(f) or {}

            try:
                course = validate_and_parse_course(course_data)
            except ValueError as e:
                print(f"Error validating {yaml_file.name}: {e}")
                continue

            # Insert course with hash
            cursor.execute(
                "INSERT OR REPLACE INTO courses (title, file_hash) VALUES (?, ?)",
                (course.title, file_hash),
            )
            course_id = cursor.lastrowid

            # Map knowledge point names to database IDs for prerequisite resolution
            kp_name_to_db_id = {}

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
                    kp_name_to_db_id[knowledge_point.name] = knowledge_point_db_id

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

            # Insert prerequisites (after all knowledge points are created)
            for lesson_data in course_data.get("lessons", []):
                for kp_data in lesson_data.get("knowledge_points", []):
                    kp_name = kp_data["name"]
                    kp_db_id = kp_name_to_db_id.get(kp_name)
                    if not kp_db_id:
                        continue

                    for prerequisite_name in kp_data.get("prerequisites", []):
                        prerequisite_db_id = kp_name_to_db_id.get(prerequisite_name)
                        if prerequisite_db_id:
                            cursor.execute(
                                """INSERT OR REPLACE INTO prerequisites
                                             (knowledge_point_id, prerequisite_id)
                                             VALUES (?, ?)""",
                                (kp_db_id, prerequisite_db_id),
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
            # Get prerequisites for this knowledge point
            cursor.execute(
                "SELECT prerequisite_id FROM prerequisites WHERE knowledge_point_id = ?",
                (kp_db_id,),
            )
            prerequisite_rows = cursor.fetchall()
            prerequisites = [prereq_id for (prereq_id,) in prerequisite_rows]

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
                    prerequisites=prerequisites,
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

    # Build a map of knowledge point ID to completion status
    completed_kp_ids = set()
    for lesson in course.lessons:
        for kp in lesson.knowledge_points:
            if all(question.answer is not None for question in kp.questions):
                completed_kp_ids.add(kp.id)

    next_lessons = []
    completed_lessons = []
    remaining_lessons = []
    for lesson in course.lessons:
        # Check if lesson is completed
        lesson_completed = all(
            kp.id in completed_kp_ids for kp in lesson.knowledge_points
        )

        if lesson_completed:
            completed_lessons.append(lesson)
            continue

        prerequisites_met = True
        lesson_kp_ids = set()
        for kp in lesson.knowledge_points:
            lesson_kp_ids.add(kp.id)
            if any(
                prereq_id not in (completed_kp_ids.union(lesson_kp_ids))
                for prereq_id in kp.prerequisites
            ):
                prerequisites_met = False
                break

        if prerequisites_met:
            next_lessons.append(lesson)
            continue

        remaining_lessons.append(lesson)

    return render_template(
        "course.html",
        course=course,
        next_lessons=next_lessons,
        completed_lessons=completed_lessons,
        remaining_lessons=remaining_lessons,
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

        # Use the validation helper function
        course = validate_and_parse_course(course_data)
        return ValidationSuccess(
            success=True, message=f"Course '{course.title}' is valid"
        ).jsonify()

    except yaml.YAMLError as e:
        return ValidationError(error=f"YAML parsing error: {str(e)}").jsonify()
    except ValueError as e:
        return ValidationError(error=str(e)).jsonify()
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
