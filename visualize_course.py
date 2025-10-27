#!/usr/bin/env python3
"""
Visualize the prerequisite graph of a course YAML file.

Usage: python visualize_course.py <course_file.yaml>
"""

from dataclasses import dataclass
import sys
from typing import Optional
import yaml
from graphviz import Digraph  # type: ignore


@dataclass
class KnowledgeGraph:
    title: str
    nodes: dict[str, str]
    edges: list[tuple[str, str]]


def extract_graph_data_from_yaml(
    yaml_file_path: str,
) -> KnowledgeGraph:
    with open(yaml_file_path, "r") as f:
        course_data = yaml.safe_load(f)

    title = course_data.get("title", "Course Graph")
    nodes: dict[str, str] = {}
    edges: list[tuple[str, str]] = []
    for lesson in course_data.get("lessons", []):
        lesson_title = lesson["title"]
        for kp in lesson.get("knowledge_points", []):
            kp_name = kp["name"]
            label = f"{kp_name}\\n({lesson_title})"
            nodes[kp_name] = label
            for prereq in kp.get("prerequisites", []):
                edges.append((prereq, kp_name))

    return KnowledgeGraph(title, nodes, edges)


def create_knowledge_graph(graph: KnowledgeGraph, output_path: str) -> str:
    dot = Digraph(comment=graph.title)
    dot.attr(rankdir="TB")  # Top to bottom layout
    dot.attr("node", shape="box", style="rounded,filled", fillcolor="lightblue")
    for node_id, label in graph.nodes.items():
        dot.node(node_id, label=label)
    for from_node, to_node in graph.edges:
        dot.edge(from_node, to_node)
    rendered_path: str = dot.render(output_path, format="png", cleanup=True)
    return rendered_path


def visualize_course_graph(
    yaml_file_path: str, output_file: Optional[str] = None
) -> str:
    graph = extract_graph_data_from_yaml(yaml_file_path)
    if output_file is None:
        # Sanitize course title for filename
        output_file = graph.title.lower().replace(" ", "_").replace(":", "")
    output_path = create_knowledge_graph(graph, output_file)
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
