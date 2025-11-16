#!/usr/bin/env python3
"""
Visualize the prerequisite graph of a course YAML file.

Usage: python visualize_course.py <course_file.yaml>
"""

from graphviz import Digraph  # type: ignore

import sys
import yaml
from dataclasses import dataclass
from typing import Any


@dataclass
class KnowledgeGraph:
    title: str
    nodes: dict[str, str]
    edges: list[tuple[str, str]]


def extract_graph_data_from_yaml_map(course_data: dict[str, Any]) -> KnowledgeGraph:
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


def create_knowledge_graph(graph: KnowledgeGraph) -> Digraph:
    """Create and return a Digraph object for the knowledge graph"""
    dot = Digraph(comment=graph.title)
    dot.attr(rankdir="TB")  # Top to bottom layout
    dot.attr("node", shape="box", style="rounded,filled", fillcolor="lightblue")
    for node_id, label in graph.nodes.items():
        dot.node(node_id, label=label)
    for from_node, to_node in graph.edges:
        dot.edge(from_node, to_node)
    return dot


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python visualize_course.py <course_file.yaml> [output_name]")
        sys.exit(1)

    yaml_path = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else None

    with open(yaml_path, "r") as f:
        course_data = yaml.safe_load(f)

    graph = extract_graph_data_from_yaml_map(course_data)

    if output_name is None:
        # Sanitize course title for filename
        output_name = graph.title.lower().replace(" ", "_").replace(":", "")
    dot = create_knowledge_graph(graph)
    output_path: str = dot.render(output_name, format="png", cleanup=True)
    print(f"Graph saved to: {output_path}")


if __name__ == "__main__":
    main()
