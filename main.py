from flask import Flask, render_template
import yaml
from pathlib import Path
from typing import List, Dict, Any

app = Flask(__name__)

counter = 0


def load_courses() -> List[Dict[str, Any]]:
    courses_dir = Path("courses")

    if not courses_dir.is_dir():
        raise FileNotFoundError(
            f"Courses directory '{courses_dir}' must exist and be a directory"
        )

    courses = []
    for yaml_file in courses_dir.glob("*.yaml"):
        with open(yaml_file, "r") as f:
            course_data = yaml.safe_load(f) or {}

        title = course_data.get("title")
        lessons = course_data.get("lessons", [])
        route = yaml_file.stem  # filename without extension

        if not title:
            raise ValueError(f"Course {yaml_file.name} missing required 'title' field")

        courses.append({"title": title, "route": route, "lessons": lessons})

    return courses


@app.route("/")
def index() -> str:
    courses = load_courses()
    return render_template("index.html", counter=counter, courses=courses)


@app.route("/course/<course_route>")
def course_page(course_route: str) -> str:
    courses = load_courses()

    # Find the course with matching route
    course = None
    for c in courses:
        if c["route"] == course_route:
            course = c
            break

    if not course:
        from flask import abort

        abort(404)

    return render_template("course.html", course=course)


@app.route("/increment", methods=["POST"])
def increment() -> str:
    global counter
    counter += 1
    # return just the snippet HTMX will swap in
    return f"<div id='count'>Count: {counter}</div>"


if __name__ == "__main__":
    app.run(debug=True)
