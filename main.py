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
    QUESTION = "question"


@dataclass
class Choice:
    text: str
    correct: Optional[bool] = None


@dataclass
class Block:
    kind: BlockKind
    content: Optional[str] = None  # for content blocks
    prompt: Optional[str] = None  # for question blocks
    choices: Optional[List[Choice]] = None  # for question blocks


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
            elif block_data["kind"] == BlockKind.QUESTION:
                choices = [
                    Choice(text=choice["text"], correct=choice.get("correct", False))
                    for choice in block_data.get("choices", [])
                ]
                blocks.append(
                    Block(
                        kind=BlockKind.QUESTION,
                        prompt=block_data["prompt"],
                        choices=choices,
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


@app.route("/course/<course_route>/lesson/<lesson_route>")
def lesson_page(course_route: str, lesson_route: str) -> str:
    course = load_course_by_route(course_route)
    if not course:
        abort(404)

    # Find the lesson with matching route
    lesson = None
    lesson_index = None
    for i, lesson in enumerate(course.lessons):
        if lesson.route == lesson_route:
            lesson = lesson
            lesson_index = i
            break

    if not lesson:
        abort(404)

    return render_template(
        "lesson.html", course=course, lesson=lesson, lesson_index=lesson_index
    )


def render_macro(template_file: str, macro_name: str, **kwargs: Any) -> str:
    """Helper function to render a single Jinja2 macro with given arguments."""
    args = ", ".join(kwargs.keys())
    template_string = (
        f"{{% from '{template_file}' import {macro_name} %}}"
        + f"{{{{ {macro_name}({args}) }}}}"
    )
    return render_template_string(template_string, **kwargs)


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
    if not block_index_str:
        abort(404)
    block_index = int(block_index_str)
    if block_index >= len(lesson.blocks):
        raise ValueError("Block index of range")
    # Render the next button using macro
    if block_index < len(lesson.blocks) - 1:
        button_html = render_macro(
            "lesson_macros.html",
            "render_next_button",
            course=course,
            lesson=lesson,
            block_index=block_index,
        )
    else:
        button_html = ""

    # Render the current block using macros
    block = lesson.blocks[block_index]

    if block.kind == BlockKind.CONTENT:
        block_html = render_macro("lesson_macros.html", "render_content", block=block)
    elif block.kind == BlockKind.QUESTION:
        block_html = render_macro("lesson_macros.html", "render_question", block=block)
    else:
        block_html = ""

    return f"{block_html}{button_html}"


@app.route("/increment", methods=["POST"])
def increment() -> str:
    global counter
    counter += 1
    # return just the snippet HTMX will swap in
    return f"<div id='count'>Count: {counter}</div>"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
