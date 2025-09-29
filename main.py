from flask import Flask, render_template, abort, request, render_template_string
import yaml
from pathlib import Path
from typing import Any, List, Optional
from dataclasses import dataclass
from enum import Enum

app = Flask(__name__)

counter = 0


class BlockKind(str, Enum):
    CONTENT = "content"
    KNOWLEDGE_POINT = "knowledge_point"


@dataclass
class Choice:
    text: str
    correct: Optional[bool] = None


@dataclass
class Question:
    prompt: str
    choices: List[Choice]


@dataclass
class KnowledgePoint:
    id: str  # kebab-case identifier
    description: str
    questions: List[Question]


@dataclass
class Block:
    kind: BlockKind
    content: Optional[str] = None  # for content blocks
    knowledge_point: Optional[KnowledgePoint] = None  # for knowledge point blocks


@dataclass
class Lesson:
    title: str
    route: str
    blocks: List[Block]


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
        blocks = []
        for block_data in lesson_data.get("blocks", []):
            if block_data["kind"] == BlockKind.CONTENT:
                blocks.append(
                    Block(kind=BlockKind.CONTENT, content=block_data["content"])
                )
            elif block_data["kind"] == BlockKind.KNOWLEDGE_POINT:
                questions = []
                for question_data in block_data.get("questions", []):
                    choices = [
                        Choice(
                            text=choice["text"], correct=choice.get("correct", False)
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
                        Question(prompt=question_data["prompt"], choices=choices)
                    )

                knowledge_point = KnowledgePoint(
                    id=block_data["id"],
                    description=block_data["description"],
                    questions=questions,
                )
                blocks.append(
                    Block(
                        kind=BlockKind.KNOWLEDGE_POINT, knowledge_point=knowledge_point
                    )
                )

        lessons.append(
            Lesson(
                title=lesson_data["title"], route=lesson_data["route"], blocks=blocks
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

    return render_template(
        "lesson.html",
        course=course,
        lesson=lesson,
    )


@app.route("/course/<course_route>/lesson/<lesson_route>/next", methods=["POST"])
def lesson_next_block(course_route: str, lesson_route: str) -> str:
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

    block_index_str = request.form.get("block_index")
    question_index_str = request.form.get("question_index", "0")
    if not block_index_str:
        abort(404)
    block_index = int(block_index_str)
    question_index = int(question_index_str)

    return render_macro(
        "lesson_macros.html",
        "render_lesson_block",
        course=course,
        lesson=lesson,
        block_index=block_index,
        question_index=question_index,
    )


@app.route("/increment", methods=["POST"])
def increment() -> str:
    global counter
    counter += 1
    # return just the snippet HTMX will swap in
    return f"<div id='count'>Count: {counter}</div>"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
