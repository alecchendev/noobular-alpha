#!/usr/bin/env python3
"""
Course outline generator using Grok API.

Setup:
    pip install xai-sdk
    export XAI_API_KEY=your_api_key_here

Usage:
    python grok_api_test.py "Topic Name"
    python grok_api_test.py --debug "Topic Name"  # Limit output to 100 tokens for testing
"""

import os
import sys
import argparse
from typing import Optional
from xai_sdk import Client  # type: ignore
from xai_sdk.chat import user, system  # type: ignore


COURSE_OUTLINE_PROMPT = """Create a comprehensive course about {topic}.

IMPORTANT: First, generate an outline showing:
1. Course title
2. List of lessons with brief descriptions
3. For each lesson, list knowledge points with brief descriptions
4. Show prerequisite relationships between knowledge points

Do NOT start creating the full course YAML until I've approved this outline.

COURSE REQUIREMENTS:
- Include all prerequisites needed to understand this topic
- Build from fundamentals to advanced concepts with clear scaffolding
- 2-4 knowledge points per lesson (atomic and focused)
- At least 10 questions per knowledge point

KNOWLEDGE POINT QUALITY:
- Each knowledge point should be specific and focused on one concept
- Lean towards active problem-solving and application, not just memorization
- Content should progressively build understanding through examples
- Use realistic prerequisite relationships between knowledge points

QUESTION QUALITY:
- Questions must be directly relevant to the knowledge point content
- All answer choices should be plausible - avoid obviously wrong answers
- Each question should test understanding, not just recall
- Include scenario-based and application questions where possible
- Explanations should clarify WHY the correct answer is right and why others are wrong

FORMATTING:
- Use spaces, not tabs
- No blank lines outside of markdown content blocks
- Items in markdown unordered lists must follow a blank line
- Use $...$ for inline math, $$...$$ for display math
- Support for **bold**, *italic*, `code`, [links](url), and all standard markdown

YAML STRUCTURE REFERENCE:
```yaml
title: "Course Title"
lessons:
  - title: "Lesson Title"
    knowledge_points:
      - name: "kebab-case-id"
        description: "Brief description"
        prerequisites: [] # or ["other-kp-id"]
        contents:
          - |
              ### Section Title

              Content with **markdown**, math $x^2$, etc.

              - Bullet point 1
              - Bullet point 2

              Display math:
              $$E = mc^2$$
          - "Simple text content also works"
        questions:
          - prompt: "Question with math: $2+2=?$"
            choices:
              - text: "3"
              - text: "4"
                correct: true
            explanation: "Explanation with **markdown** and $math$"
```

Remember: ONLY generate the outline for now, NOT the full course."""


def generate_course_outline(topic: str, max_tokens: Optional[int] = None) -> str:
    """
    Generate a course outline for the given topic using Grok API.

    Args:
        topic: The topic to create a course about
        max_tokens: Maximum number of tokens in the response (None for unlimited)

    Returns:
        The course outline as a string
    """
    # Initialize the client
    client = Client(
        api_key=os.getenv("XAI_API_KEY"),
        timeout=3600,  # Override default timeout with longer timeout for reasoning models
    )

    # Create a chat session with optional max_tokens
    if max_tokens:
        chat = client.chat.create(model="grok-4", max_tokens=max_tokens)
    else:
        chat = client.chat.create(model="grok-4")

    # Add system message
    chat.append(
        system(
            "You are an expert educational content creator who specializes in creating comprehensive, well-structured courses with clear learning progressions."
        )
    )

    # Add user prompt with the topic
    prompt = COURSE_OUTLINE_PROMPT.format(topic=topic)
    chat.append(user(prompt))

    print(f"Generating course outline for: {topic}")
    if max_tokens:
        print(f"(Limited to {max_tokens} tokens for testing)")
    print("=" * 80)
    print("Waiting for Grok response...\n")

    # Get response
    response = chat.sample()

    return str(response.content)


def main() -> None:
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Generate a course outline using Grok API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "topic", nargs="*", help="The course topic to generate an outline for"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Limit output to 100 tokens for testing"
    )

    args = parser.parse_args()

    # Get topic from arguments or prompt user
    if args.topic:
        topic = " ".join(args.topic)
    else:
        topic = input("Enter the course topic: ").strip()
        if not topic:
            print("Error: No topic provided")
            sys.exit(1)

    # Check for API key
    if not os.getenv("XAI_API_KEY"):
        print("Error: XAI_API_KEY environment variable not set")
        print("Please run: export XAI_API_KEY=your_api_key_here")
        sys.exit(1)

    # Set max_tokens based on debug flag
    max_tokens = 500 if args.debug else None

    # Generate outline
    try:
        outline = generate_course_outline(topic, max_tokens=max_tokens)

        print("COURSE OUTLINE:")
        print("=" * 80)
        print(outline)
        print("=" * 80)

        if args.debug:
            print(
                f"\nNote: Running in debug mode - output was limited to {max_tokens} tokens"
            )
            print("To run full generation, remove --debug flag")

    except Exception as e:
        print(f"Error generating course outline: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
