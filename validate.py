"""
Course validation module.

Can be used as a module or run as a CLI script to validate course YAML files.
"""

import argparse
from dataclasses import dataclass
import sys
import yaml
from pathlib import Path
from typing import Any


@dataclass
class ValidationConfig:
    # Max number of knowledge points in a course
    max_course_knowledge_point_count: int
    # minimum number of questions per knowledge point
    min_question_count: int


def validate_course(course_data: dict[str, Any]) -> None:
    """Validate course data and return a Course object. Raises ValueError on validation failure."""
    # Config is just constant
    config = ValidationConfig(
        max_course_knowledge_point_count=1000, min_question_count=2
    )

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

            # Validate minimum question count
            if len(kp_data["questions"]) < config.min_question_count:
                raise ValueError(
                    f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}') must have at least {config.min_question_count} questions, found {len(kp_data['questions'])}"
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

                if "explanation" not in question_data:
                    raise ValueError(
                        f"Lesson {lesson_idx} ('{lesson_data['title']}'), knowledge_point {kp_idx} (name: '{kp_data['name']}'), question {q_idx} (prompt: '{question_data.get('prompt', 'unknown')}') missing required field: 'explanation'"
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

    knowledge_point_count = sum(
        len(lesson_data.get("knowledge_points", []))
        for lesson_data in course_data.get("lessons", [])
    )
    if knowledge_point_count > config.max_course_knowledge_point_count:
        raise ValueError(
            f"Too many knowledge points. Max knowledge point count: {config.max_course_knowledge_point_count}, observed: {knowledge_point_count}"
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


def main() -> int:
    """CLI entry point for validating course files."""
    parser = argparse.ArgumentParser(
        description="Validate course YAML files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "file", type=str, help="Path to the course YAML file to validate"
    )

    args = parser.parse_args()
    file_path = Path(args.file)

    # Check if file exists
    if not file_path.exists():
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        return 1

    # Check if file has .yaml extension
    if file_path.suffix not in [".yaml", ".yml"]:
        print(f"Error: File '{args.file}' is not a YAML file", file=sys.stderr)
        return 1

    try:
        # Read and parse YAML
        with open(file_path, "r") as f:
            course_data = yaml.safe_load(f)

        if not course_data:
            print("Error: File is empty or contains no valid YAML", file=sys.stderr)
            return 1

        # Validate the course
        validate_course(course_data)

        # Success!
        print(f"✓ Course '{course_data['title']}' is valid")
        return 0

    except yaml.YAMLError as e:
        print(f"Error: YAML parsing error: {str(e)}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: Unexpected error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
