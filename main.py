from flask import Flask, render_template, abort, request, g, jsonify, redirect
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

    # Create quizzes table
    cursor.execute("""CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY,
        course_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        started_at TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses (id)
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

    def correct_choice(self) -> Choice:
        # Assumes there is a correct choice (should be validated upon course load)
        return next(choice for choice in self.choices if choice.correct)


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
    questions: List[Question]  # Does not include questions used in a quiz
    quizzed_questions: List[Question]  # Includes questions used in a quiz

    def last_consecutive_correct_answers(self) -> int:
        last_correct_count = 0
        for question in self.questions[::-1]:
            if question.answer is None:
                continue
            if question.answer.choice_id == question.correct_choice().id:
                last_correct_count += 1
            else:
                break
        return last_correct_count


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


def validate_course(course_data: dict[str, Any]) -> None:
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


def load_courses_to_database() -> None:
    """Load courses from YAML files into database"""
    if not COURSES_DIRECTORY.is_dir():
        print("No courses directory found, skipping course loading")
        return

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Parse new courses (file hash isn't in DB)
    courses: list[tuple[bytes, dict[str, Any]]] = []  # hash, course_data
    for yaml_file in COURSES_DIRECTORY.glob("*.yaml"):
        # Calculate file hash (MD5, 16 bytes)
        with open(yaml_file, "rb") as f:
            file_hash = hashlib.md5(f.read()).digest()

        # Check if this file hash already exists
        cursor.execute("SELECT id FROM courses WHERE file_hash = ?", (file_hash,))
        if cursor.fetchone():
            print(f"Course {yaml_file.name} already loaded (unchanged), skipping")
            continue

        with open(yaml_file, "r") as f:
            course_data = yaml.safe_load(f) or {}

        try:
            validate_course(course_data)
        except ValueError as e:
            print(f"Error validating {yaml_file.name}: {e}")
            continue
        courses.append((file_hash, course_data))

    # Insert into DB
    for file_hash, course_data in courses:
        # Insert course with hash
        cursor.execute(
            "INSERT INTO courses (title, file_hash) VALUES (?, ?)",
            (course_data["title"], file_hash),
        )
        course_id = cursor.lastrowid

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
                                     (knowledge_point_id, prompt)
                                     VALUES (?, ?)""",
                        (knowledge_point_db_id, question_data["prompt"]),
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

    conn.commit()

    print("✅ Courses loaded into database successfully!")

    conn.close()


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

            cursor.execute(
                """SELECT q.id FROM quiz_questions qq JOIN questions q on qq.question_id = q.id WHERE q.knowledge_point_id = ?""",
                (kp_db_id,),
            )
            quizzed_question_ids = set(row[0] for row in cursor.fetchall())

            questions = []
            quizzed_questions = []
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

                question = Question(
                    id=question_id, prompt=prompt, choices=choices, answer=answer
                )
                if question.id in quizzed_question_ids:
                    quizzed_questions.append(question)
                else:
                    questions.append(question)

            knowledge_points.append(
                KnowledgePoint(
                    id=kp_db_id,
                    name=kp_name,
                    description=kp_description,
                    prerequisites=prerequisites,
                    contents=contents,
                    questions=questions,
                    quizzed_questions=quizzed_questions,
                )
            )

        lessons.append(
            Lesson(id=lesson_id, title=lesson_title, knowledge_points=knowledge_points)
        )

    return Course(id=course_id, title=course_title, lessons=lessons)


@app.route("/")
def index() -> str:
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM courses")
    course_ids = cursor.fetchall()

    courses = []
    for (course_id,) in course_ids:
        course = load_course_from_db(course_id)
        if course:
            courses.append(course)

    return render_template("index.html", courses=courses)


# number of answers correct in a row to let you skip the rest of the questions
CORRECT_COUNT_THRESHOLD = 2
# percentage of wrong:right ratio to which you will fail and have to restart a lesson
INCORRECT_RATIO_FAIL_THRESHOLD = 0.6  # 3/5
# number of knowledge points completed before a quiz is ready
QUIZ_KNOWLEDGE_POINT_COUNT_THRESHOLD = 5  # 15
# number of questions in a quiz
QUIZ_QUESTION_COUNT = 5
assert QUIZ_KNOWLEDGE_POINT_COUNT_THRESHOLD >= QUIZ_QUESTION_COUNT
# number of minutes allowed for a quiz
QUIZ_TIME_LIMIT_MINUTES = 15
# TODO: have a cutoff of knowledge points before they must take a quiz


@app.route("/course/<int:course_id>")
def course_page(course_id: int) -> str:
    course = load_course_from_db(course_id)
    if not course:
        abort(404)

    # Build a map of knowledge point ID to completion status
    completed_kp_ids = set()
    for lesson in course.lessons:
        for kp in lesson.knowledge_points:
            # Either all questions have been answered, or last X questions were
            # answered correctly in a row
            answered_questions = [
                question for question in kp.questions if question.answer
            ]
            if (
                len(answered_questions) == len(kp.questions)
                or kp.last_consecutive_correct_answers() >= CORRECT_COUNT_THRESHOLD
            ):
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

    # Check if we need to create a new quiz
    db = get_db()
    cursor = db.cursor()

    # Get the creation time of the last quiz (or use epoch if no quizzes exist)
    cursor.execute(
        "SELECT created_at FROM quizzes WHERE course_id = ? ORDER BY created_at DESC LIMIT 1",
        (course_id,),
    )
    last_quiz_row = cursor.fetchone()
    last_quiz_time = last_quiz_row[0] if last_quiz_row else "1970-01-01 00:00:00"

    # Get KP IDs completed after the last quiz using a single query
    # Exclude questions that are quiz questions
    placeholders = ",".join("?" * len(completed_kp_ids))
    cursor.execute(
        f"""SELECT DISTINCT q.knowledge_point_id
            FROM questions q
            JOIN answers a ON a.question_id = q.id
            LEFT JOIN quiz_questions qq ON qq.question_id = q.id
            WHERE q.knowledge_point_id IN ({placeholders})
            AND a.created_at > ?
            AND qq.question_id IS NULL""",
        (*completed_kp_ids, last_quiz_time),
    )
    recent_completed_kp_ids = set(row[0] for row in cursor.fetchall())

    # Create a new quiz if threshold is met
    if len(recent_completed_kp_ids) >= QUIZ_KNOWLEDGE_POINT_COUNT_THRESHOLD:
        # Get recently completed KPs from the course data
        import random

        recent_kps: list[KnowledgePoint] = []
        for lesson in course.lessons:
            for kp in lesson.knowledge_points:
                if kp.id in recent_completed_kp_ids:
                    recent_kps.append(kp)

        # Randomly select up to QUIZ_QUESTION_COUNT KPs
        selected_kps = random.sample(recent_kps, QUIZ_QUESTION_COUNT)

        # Collect one unanswered question from each selected KP
        quiz_questions = []
        for kp in selected_kps:
            unanswered = [q for q in kp.questions if q.answer is None]
            # TODO: consider separate bank for quiz questions, or better enforce
            # assumption of large question bank upon course creation
            assert len(unanswered) > 0
            question = random.choice(unanswered)
            quiz_questions.append(question.id)

        # Create quiz, then insert all quiz questions in one query
        assert len(quiz_questions) > 0

        cursor.execute("INSERT INTO quizzes (course_id) VALUES (?)", (course_id,))
        quiz_id = cursor.lastrowid

        cursor.executemany(
            "INSERT INTO quiz_questions (quiz_id, question_id) VALUES (?, ?)",
            zip([quiz_id] * len(quiz_questions), quiz_questions),
        )
        db.commit()

    # Load all quizzes for this course
    cursor.execute("SELECT id FROM quizzes WHERE course_id = ?", (course_id,))
    quiz_rows = cursor.fetchall()

    # Separate quizzes into available and completed
    from datetime import datetime, timedelta

    available_quizzes = []
    completed_quizzes = []

    for (quiz_id,) in quiz_rows:
        quiz = load_quiz(quiz_id, course_id)
        if not quiz:
            continue

        # Check if quiz is completed (time is up OR has any answers)
        has_answers = any(q.answer is not None for q in quiz.questions)
        time_is_up = False

        if quiz.started_at:
            start_time = datetime.fromisoformat(quiz.started_at)
            end_time = start_time + timedelta(minutes=QUIZ_TIME_LIMIT_MINUTES)
            now = datetime.now()
            time_is_up = now > end_time

        if has_answers or time_is_up:
            completed_quizzes.append(quiz)
        else:
            available_quizzes.append(quiz)

    return render_template(
        "course.html",
        course=course,
        next_lessons=next_lessons,
        completed_lessons=completed_lessons,
        remaining_lessons=remaining_lessons,
        available_quizzes=available_quizzes,
        completed_quizzes=completed_quizzes,
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
    question = lesson.knowledge_points[kp_index].questions[question_index]
    user_choice = question.choices[answer_index]

    # Save the user's answer to the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO answers (question_id, choice_id) VALUES (?, ?)",
        (question.id, user_choice.id),
    )
    answer_id = cursor.lastrowid
    assert answer_id is not None
    # Important that we populate this the rest of this handler can assume correct state
    lesson.knowledge_points[kp_index].questions[question_index].answer = Answer(
        id=answer_id, question_id=question.id, choice_id=user_choice.id
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

    # Check if user has failed the knowledge point (3+ wrong answers)
    knowledge_point = lesson.knowledge_points[kp_index]
    incorrect_count = 0
    answered_count = 0
    for question in knowledge_point.questions:
        if question.answer is None:
            continue
        answered_count += 1
        incorrect_count += int(
            question.answer.choice_id != question.correct_choice().id
        )

    failed_knowledge_point = (
        answered_count >= 3
        and incorrect_count / answered_count >= INCORRECT_RATIO_FAIL_THRESHOLD
    )

    failure_message = ""
    next_button_html = ""
    if failed_knowledge_point:
        # Delete all answers for questions in this lesson
        for kp in lesson.knowledge_points:
            for q in kp.questions:
                if q.answer:
                    cursor.execute("DELETE FROM answers WHERE id = ?", (q.answer.id,))
        db.commit()

        failure_message = f"""
        <div>
            <p>❌ Your wrong:answered ratio for this knowledge point surpassed {INCORRECT_RATIO_FAIL_THRESHOLD * 100}%. You need to restart this lesson.</p>
            <a href="/course/{course_id}/lesson/{lesson_id}" class="button">Restart Lesson</a>
        </div>
        """
    else:
        next_button_html = render_template(
            "next_button.html",
            course=course,
            lesson=lesson,
            knowledge_point_index=kp_index,
            i=i,
        )

    return f"<p>{feedback}</p>{failure_message}{next_button_html}"


@app.route("/validate-course", methods=["POST"])
def validate() -> tuple[Any, int]:
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
        validate_course(course_data)
        return ValidationSuccess(
            success=True, message=f"Course '{course_data['title']}' is valid"
        ).jsonify()

    except yaml.YAMLError as e:
        return ValidationError(error=f"YAML parsing error: {str(e)}").jsonify()
    except ValueError as e:
        return ValidationError(error=str(e)).jsonify()
    except Exception as e:
        return ValidationError(
            error=f"Unexpected error: {str(e)}", status_code=500
        ).jsonify()


def load_quiz(quiz_id: int, course_id: int) -> Optional[Quiz]:
    """Load a quiz with its questions, choices, and answers from the database"""
    db = get_db()
    cursor = db.cursor()

    # Verify quiz exists and belongs to course, and get started_at
    cursor.execute(
        "SELECT started_at FROM quizzes WHERE id = ? AND course_id = ?",
        (quiz_id, course_id),
    )
    quiz_row = cursor.fetchone()
    if not quiz_row:
        return None

    started_at = quiz_row[0]

    # Load quiz questions
    cursor.execute(
        """SELECT q.id, q.prompt
           FROM quiz_questions qq
           JOIN questions q ON qq.question_id = q.id
           WHERE qq.quiz_id = ?""",
        (quiz_id,),
    )
    question_rows = cursor.fetchall()

    questions = []
    for q_id, q_prompt in question_rows:
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
            "SELECT id, choice_id FROM answers WHERE question_id = ?", (q_id,)
        )
        answer_row = cursor.fetchone()
        answer = (
            Answer(id=answer_row[0], question_id=q_id, choice_id=answer_row[1])
            if answer_row
            else None
        )

        questions.append(
            Question(id=q_id, prompt=q_prompt, choices=choices, answer=answer)
        )

    return Quiz(
        id=quiz_id, course_id=course_id, questions=questions, started_at=started_at
    )


@app.route("/course/<int:course_id>/quiz/<int:quiz_id>")
def quiz_page(course_id: int, quiz_id: int) -> str:
    course = load_course_from_db(course_id)
    if not course:
        abort(404)

    # Load quiz using helper function
    quiz = load_quiz(quiz_id, course_id)
    if not quiz:
        abort(404)

    db = get_db()
    cursor = db.cursor()

    # Set started_at if this is the first time loading the quiz
    if quiz.started_at is None:
        cursor.execute(
            "UPDATE quizzes SET started_at = CURRENT_TIMESTAMP WHERE id = ?", (quiz_id,)
        )
        db.commit()

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
        course=course,
        quiz=quiz,
        quiz_time_limit_minutes=QUIZ_TIME_LIMIT_MINUTES,
        is_submitted=is_submitted,
        score=score,
    )


@app.route("/course/<int:course_id>/quiz/<int:quiz_id>/submit", methods=["POST"])
def quiz_submit(course_id: int, quiz_id: int) -> Any:
    quiz = load_quiz(quiz_id, course_id)
    if not quiz or quiz.started_at is None:
        abort(404)

    # Validate submission time (within 10 seconds of expected end time)
    from datetime import datetime, timedelta

    start_time = datetime.fromisoformat(quiz.started_at)
    expected_end_time = start_time + timedelta(minutes=QUIZ_TIME_LIMIT_MINUTES)
    now = datetime.now()

    # Check if submission is within 10 seconds after expected end time
    if now > expected_end_time + timedelta(seconds=10):
        abort(400)  # Bad request - time limit exceeded

    db = get_db()
    cursor = db.cursor()

    # Process and store answers
    for question in quiz.questions:
        answer_key = f"question_{question.id}"
        if answer_key in request.form:
            choice_index = int(request.form[answer_key])

            if choice_index < len(question.choices):
                choice_id = question.choices[choice_index].id

                # Store the answer
                cursor.execute(
                    "INSERT OR REPLACE INTO answers (question_id, choice_id) VALUES (?, ?)",
                    (question.id, choice_id),
                )

    db.commit()

    # Redirect to quiz page to show results
    return redirect(f"/course/{course_id}/quiz/{quiz_id}")


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

    knowledge_point = lesson.knowledge_points[kp_index]
    completed_kp = (
        knowledge_point.last_consecutive_correct_answers() >= CORRECT_COUNT_THRESHOLD
    )
    question_index = i - len(knowledge_point.contents)
    new_question = question_index >= len(
        [question for question in knowledge_point.questions if question.answer]
    )
    if completed_kp and new_question:
        kp_index += 1
        i = 0

    return render_template(
        "knowledge_point.html",
        course=course,
        lesson=lesson,
        knowledge_point_index=kp_index,
        i=i,
    )


if __name__ == "__main__":
    init_database()
    load_courses_to_database()
    app.run(debug=True, port=5000)
