from flask import Flask, render_template, abort
import yaml
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

app = Flask(__name__)

counter = 0


@dataclass
class Lesson:
    title: str
    route: str
    blocks: List[str]


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

    lessons = [
        Lesson(
            title=lesson["title"],
            route=lesson["route"],
            blocks=lesson.get("blocks", []),
        )
        for lesson in course_data.get("lessons", [])
    ]
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


@app.route("/increment", methods=["POST"])
def increment() -> str:
    global counter
    counter += 1
    # return just the snippet HTMX will swap in
    return f"<div id='count'>Count: {counter}</div>"


if __name__ == "__main__":
    app.run(debug=True)
