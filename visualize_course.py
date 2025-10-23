#!/usr/bin/env python3
"""
Visualize the prerequisite graph of a course YAML file.

Usage: python visualize_course.py <course_file.yaml>
"""

import sys
import yaml
from graphviz import Digraph


def visualize_course_graph(yaml_file_path, output_file=None):
    """
    Create a graph visualization of knowledge point prerequisites.

    Args:
        yaml_file_path: Path to the course YAML file
        output_file: Optional output filename (without extension).
                    Defaults to course title or 'course_graph'
    """
    # Load the YAML file
    with open(yaml_file_path, "r") as f:
        course_data = yaml.safe_load(f)

    # Create a directed graph
    dot = Digraph(comment=course_data.get("title", "Course Graph"))
    dot.attr(rankdir="TB")  # Top to bottom layout
    dot.attr("node", shape="box", style="rounded,filled", fillcolor="lightblue")

    # Track all knowledge points and their prerequisites
    kp_to_lesson = {}  # Map knowledge point name to lesson title

    # First pass: add all nodes
    for lesson in course_data.get("lessons", []):
        lesson_title = lesson["title"]
        for kp in lesson.get("knowledge_points", []):
            kp_name = kp["name"]
            kp_to_lesson[kp_name] = lesson_title

            # Create node label with lesson context
            label = f"{kp_name}\n({lesson_title})"
            dot.node(kp_name, label=label)

    # Second pass: add edges for prerequisites
    for lesson in course_data.get("lessons", []):
        for kp in lesson.get("knowledge_points", []):
            kp_name = kp["name"]
            for prereq in kp.get("prerequisites", []):
                # Draw edge from prerequisite to knowledge point
                dot.edge(prereq, kp_name)

    # Determine output filename
    if output_file is None:
        # Sanitize course title for filename
        title = course_data.get("title", "course_graph")
        output_file = title.lower().replace(" ", "_").replace(":", "")

    # Render the graph
    output_path = dot.render(output_file, format="png", cleanup=True)
    print(f"Graph saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python visualize_course.py <course_file.yaml> [output_name]")
        sys.exit(1)

    yaml_path = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        visualize_course_graph(yaml_path, output_name)
    except FileNotFoundError:
        print(f"Error: File '{yaml_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
