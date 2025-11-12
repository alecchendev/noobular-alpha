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
import yaml
from typing import Optional, Any, Dict, List
from xai_sdk import Client  # type: ignore
from xai_sdk.chat import user, system  # type: ignore
from validate import validate_question

MODEL = "grok-4-fast"


COURSE_OUTLINE_PROMPT = """Create a comprehensive course outline about {topic}.

OUTPUT FORMAT: Return a YAML structure with the course outline. Include the course title, lessons, and knowledge points with their descriptions and prerequisites, but DO NOT fill in any contents or questions yet.

COURSE REQUIREMENTS:
- Include all prerequisites needed to understand this topic
- Build from fundamentals to advanced concepts with clear scaffolding
- Target approximately {lesson_count} lessons (adjust as needed for the topic)
- 2-4 knowledge points per lesson (atomic and focused)
- Plan for at least 10 questions per knowledge point (to be filled in later)

KNOWLEDGE POINT QUALITY:
- Each knowledge point should be specific and focused on one concept
- Lean towards active problem-solving and application, not just memorization
- Content should progressively build understanding through examples
- Use realistic prerequisite relationships between knowledge points

QUESTION QUALITY (for future reference when filling in questions):
- Questions must be directly relevant to the knowledge point content
- All answer choices should be plausible - avoid obviously wrong answers
- Each question should test understanding, not just recall
- Include scenario-based and application questions where possible
- Explanations should clarify WHY the correct answer is right and why others are wrong

FORMATTING:
- Use spaces (2 spaces per indent level), not tabs
- No blank lines in the YAML structure
- Use kebab-case for knowledge point names (e.g., 'equilibrium-conditions')
- Use single quotes for all text fields

OUTPUT STRUCTURE - Return ONLY valid YAML in this exact format:

title: 'Course Title'
lessons:
  - title: 'Lesson 1 Title'
    knowledge_points:
      - name: 'kebab-case-id'
        description: 'Brief description of what this knowledge point covers'
        prerequisites: []
      - name: 'another-kp-id'
        description: 'Brief description'
        prerequisites: ['kebab-case-id']
  - title: 'Lesson 2 Title'
    knowledge_points:
      - name: 'advanced-topic'
        description: 'Brief description'
        prerequisites: ['another-kp-id']

IMPORTANT:
- Return ONLY raw YAML - do NOT wrap in ```yaml code fences and no additional commentary
- Use SINGLE QUOTES for all text fields to avoid escape character issues
- Do NOT include contents or questions fields - they will be added later
- Focus on creating a well-structured progression of lessons and knowledge points
- Ensure prerequisite relationships accurately reflect dependencies between concepts"""

KNOWLEDGE_POINT_CONTENT_PROMPT = """You are creating educational content for a knowledge point in a course about {course_title}.

KNOWLEDGE POINT DETAILS:
- Name: {kp_name}
- Description: {kp_description}
- Lesson: {lesson_title}
- Prerequisites: {prerequisites}

TASK: Generate educational content that teaches this concept.

CONTENT REQUIREMENTS:
- Create 2-4 content blocks that teach this concept
- Each content block should be focused and digestible
- Use markdown formatting with headers (###), **bold**, *italic*, `code`
- Include specific examples and applications
- Use inline math with $...$ and display math with $$...$$ where appropriate
- For lists, ensure a blank line precedes them
- Build understanding progressively from basic to applied

OUTPUT FORMAT: Return ONLY valid YAML (no code fences, no commentary) as an array:

- |
    ### Section Title

    Content with **markdown**, math $x^2$, etc.

    - Bullet point 1
    - Bullet point 2

    Display math:
    $$E = mc^2$$
- |
    ### Another Section

    More content here.

CRITICAL YAML FORMATTING RULES:
- Use | (pipe) for multi-line content blocks with no quotes
- If you need a single quote inside text, escape it by doubling it: 'It''s' becomes "It's"
- Return ONLY the array of content blocks as valid YAML
- No code fences, no commentary
"""

KNOWLEDGE_POINT_QUESTIONS_PROMPT = """You are creating assessment questions for a knowledge point in a course about {course_title}.

KNOWLEDGE POINT DETAILS:
- Name: {kp_name}
- Description: {kp_description}
- Lesson: {lesson_title}

CONTENT TAUGHT:
{content_summary}

TASK: Generate questions that test understanding of the content above.

QUESTION REQUIREMENTS:
- Create exactly 10 multiple choice questions
- Questions must strictly align with the skills and concepts from the content
- All 4 answer choices must be plausible - no obviously wrong answers
- Exactly one choice must be marked as correct
- Include scenario-based and application questions where possible
- Explanations should clarify WHY the correct answer is right AND why others are wrong
- Use markdown and math in prompts, choices, and explanations as needed

OUTPUT FORMAT: Return ONLY valid YAML (no code fences, no commentary) as an array:

- prompt: 'Question text here with $math$ allowed'
  choices:
    - text: 'Choice A with LaTeX like $x^2$'
    - text: 'Choice B'
      correct: true
    - text: 'Choice C'
    - text: 'Choice D'
  explanation: 'Explanation with **markdown** and $\lambda$ symbols'

CRITICAL YAML FORMATTING RULES:
- Use SINGLE QUOTES for all text fields (prompt, text, explanation)
- Single quotes prevent escape character issues with LaTeX symbols like \phi, \lambda, etc.
- If you need a single quote inside text, escape it by doubling it: 'It''s' becomes "It's"
- Return ONLY the array of questions as valid YAML
- No code fences, no commentary
"""


def generate_course_outline(
    topic: str, lesson_count: int, max_tokens: Optional[int]
) -> str:
    """
    Generate a course outline for the given topic using Grok API.

    Args:
        topic: The topic to create a course about
        lesson_count: Target number of lessons (default: 5)
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
        chat = client.chat.create(model=MODEL, max_tokens=max_tokens)
    else:
        chat = client.chat.create(model=MODEL)

    # Add system message
    chat.append(
        system(
            "You are an expert educational content creator who specializes in creating comprehensive, well-structured courses with clear learning progressions."
        )
    )

    # Add user prompt with the topic and lesson count
    prompt = COURSE_OUTLINE_PROMPT.format(topic=topic, lesson_count=lesson_count)
    chat.append(user(prompt))

    print(f"Generating course outline for: {topic}")
    print(f"Target lesson count: {lesson_count}")
    if max_tokens:
        print(f"(Limited to {max_tokens} tokens for testing)")
    print("=" * 80)
    print("Waiting for Grok response...\n")

    # Get response
    response = chat.sample()

    return str(response.content)


def generate_content(
    course_title: str,
    lesson_title: str,
    kp_name: str,
    kp_description: str,
    prerequisites: List[str],
    max_tokens: Optional[int] = None,
) -> List[str]:
    """
    Generate content for a single knowledge point.

    Args:
        course_title: The title of the course
        lesson_title: The title of the lesson this KP belongs to
        kp_name: The name/ID of the knowledge point
        kp_description: The description of the knowledge point
        prerequisites: List of prerequisite knowledge point IDs
        max_tokens: Maximum number of tokens in the response (None for unlimited)

    Returns:
        List of content blocks
    """
    # Initialize the client
    client = Client(
        api_key=os.getenv("XAI_API_KEY"),
        timeout=3600,
    )

    # Create a chat session
    if max_tokens:
        chat = client.chat.create(model=MODEL, max_tokens=max_tokens)
    else:
        chat = client.chat.create(model=MODEL)

    # Add system message
    chat.append(
        system(
            "You are an expert educational content creator who creates clear, comprehensive learning materials with excellent examples."
        )
    )

    # Format prerequisites
    prereq_str = ", ".join(prerequisites) if prerequisites else "None"

    # Add user prompt
    prompt = KNOWLEDGE_POINT_CONTENT_PROMPT.format(
        course_title=course_title,
        lesson_title=lesson_title,
        kp_name=kp_name,
        kp_description=kp_description,
        prerequisites=prereq_str,
    )
    chat.append(user(prompt))

    # Get response
    response = chat.sample()
    response_text = str(response.content)

    # Print full response
    print(f"\n{'=' * 80}")
    print(f"CONTENT RESPONSE for {kp_name}:")
    print(f"{'=' * 80}")
    print(response_text)
    print(f"{'=' * 80}\n")

    # Sanitize response - fix common escaping issues
    # Replace \' with '' (proper single quote escaping in YAML)
    response_text = response_text.replace("\\'", "''")

    # Parse YAML response
    try:
        contents: List[str] = yaml.safe_load(response_text)
        return contents if isinstance(contents, list) else []
    except yaml.YAMLError as e:
        print(f"    Warning: Failed to parse content YAML for {kp_name}: {e}")
        return []


def generate_questions(
    course_title: str,
    lesson_title: str,
    kp_name: str,
    kp_description: str,
    contents: List[str],
    max_tokens: Optional[int] = None,
    max_retries: int = 2,
) -> List[Dict[str, Any]]:
    """
    Generate questions for a single knowledge point based on its content.

    Args:
        course_title: The title of the course
        lesson_title: The title of the lesson this KP belongs to
        kp_name: The name/ID of the knowledge point
        kp_description: The description of the knowledge point
        contents: The content blocks that were generated
        max_tokens: Maximum number of tokens in the response (None for unlimited)
        max_retries: Maximum number of retry attempts if validation fails

    Returns:
        List of question dictionaries
    """
    # Create content summary
    assert contents
    content_summary = "\n\n".join(contents)

    for attempt in range(max_retries + 1):
        # Initialize the client
        client = Client(
            api_key=os.getenv("XAI_API_KEY"),
            timeout=3600,
        )

        # Create a chat session
        if max_tokens:
            chat = client.chat.create(model=MODEL, max_tokens=max_tokens)
        else:
            chat = client.chat.create(model=MODEL)

        # Add system message
        chat.append(
            system(
                "You are an expert educational content creator who creates thoughtful, challenging questions that test deep understanding."
            )
        )

        # Add user prompt
        prompt = KNOWLEDGE_POINT_QUESTIONS_PROMPT.format(
            course_title=course_title,
            lesson_title=lesson_title,
            kp_name=kp_name,
            kp_description=kp_description,
            content_summary=content_summary,
        )
        chat.append(user(prompt))

        # Get response
        response = chat.sample()
        response_text = str(response.content)

        # Print full response
        print(f"\n{'=' * 80}")
        print(
            f"QUESTIONS RESPONSE for {kp_name} (attempt {attempt + 1}/{max_retries + 1}):"
        )
        print(f"{'=' * 80}")
        print(response_text)
        print(f"{'=' * 80}\n")

        # Sanitize response - fix common escaping issues
        # Replace \' with '' (proper single quote escaping in YAML)
        response_text = response_text.replace("\\'", "''")

        # Parse YAML response
        try:
            questions: List[Dict[str, Any]] = yaml.safe_load(response_text)
            if not isinstance(questions, list):
                print("    Warning: Response is not a list, retrying...")
                continue

            # Validate each question
            validation_errors = []
            for q_idx, question_data in enumerate(questions):
                try:
                    validate_question(
                        question_data,
                        lesson_idx=0,  # Dummy values for validation
                        lesson_title=lesson_title,
                        kp_idx=0,
                        kp_name=kp_name,
                        q_idx=q_idx,
                    )
                except ValueError as e:
                    validation_errors.append(f"Question {q_idx}: {str(e)}")

            if validation_errors:
                print("    Validation errors found:")
                for error in validation_errors:
                    print(f"      - {error}")
                if attempt < max_retries:
                    print(f"    Retrying... ({attempt + 1}/{max_retries})")
                    continue
                else:
                    print("    Max retries reached. Returning invalid questions.")
                    return questions

            # All questions valid!
            print("    ✓ All questions validated successfully")
            return questions

        except yaml.YAMLError as e:
            print(f"    Warning: Failed to parse questions YAML for {kp_name}: {e}")
            if attempt < max_retries:
                print(f"    Retrying... ({attempt + 1}/{max_retries})")
                continue
            else:
                return []

    return []


def fill_course_content(
    outline_yaml: str, max_tokens: Optional[int] = None
) -> Dict[str, Any]:
    """
    Takes a course outline YAML and fills in content and questions for each knowledge point.

    Args:
        outline_yaml: The course outline as a YAML string
        max_tokens: Maximum number of tokens per knowledge point generation

    Returns:
        Complete course dictionary with all content and questions filled in
    """
    # Parse the outline
    try:
        course: Dict[str, Any] = yaml.safe_load(outline_yaml)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML outline: {e}")

    course_title = course.get("title", "Unknown Course")
    lessons = course.get("lessons", [])

    print(f"\nFilling content for course: {course_title}")
    print(f"Total lessons: {len(lessons)}")
    print("=" * 80)

    # Loop through each lesson and knowledge point
    for lesson_idx, lesson in enumerate(lessons, 1):
        lesson_title = lesson.get("title", f"Lesson {lesson_idx}")
        knowledge_points = lesson.get("knowledge_points", [])

        print(f"\nLesson {lesson_idx}/{len(lessons)}: {lesson_title}")
        print(f"  Knowledge points: {len(knowledge_points)}")

        for kp_idx, kp in enumerate(knowledge_points, 1):
            kp_name = kp.get("name", f"kp-{kp_idx}")
            kp_description = kp.get("description", "")
            prerequisites = kp.get("prerequisites", [])

            print(f"  [{kp_idx}/{len(knowledge_points)}] {kp_name}...")

            # Generate content
            print("    - Generating content...", end=" ")
            contents = generate_content(
                course_title=course_title,
                lesson_title=lesson_title,
                kp_name=kp_name,
                kp_description=kp_description,
                prerequisites=prerequisites,
                max_tokens=max_tokens,
            )
            print(f"✓ ({len(contents)} blocks)")

            # Generate questions based on content
            print("    - Generating questions...", end=" ")
            questions = generate_questions(
                course_title=course_title,
                lesson_title=lesson_title,
                kp_name=kp_name,
                kp_description=kp_description,
                contents=contents,
                max_tokens=max_tokens,
            )
            print(f"✓ ({len(questions)} questions)")

            # Add to knowledge point
            kp["contents"] = contents
            kp["questions"] = questions

    print("\n" + "=" * 80)
    print("Course content generation complete!")

    return course


def main() -> None:
    # Main parser
    parser = argparse.ArgumentParser(
        description="Course generator using Grok API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Add subparsers for outline and fill commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Outline subcommand
    outline_parser = subparsers.add_parser(
        "outline",
        help="Generate a course outline structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    outline_parser.add_argument(
        "topic",
        nargs="+",
        help="The course topic to generate an outline for",
    )
    outline_parser.add_argument(
        "--lessons",
        "-l",
        type=int,
        default=8,
        help="Target number of lessons (default: 8)",
    )
    outline_parser.add_argument(
        "--output",
        "-o",
        help="Output file path for the outline YAML",
    )
    outline_parser.add_argument(
        "--debug",
        action="store_true",
        help="Limit output to 500 tokens for testing",
    )

    # Fill subcommand
    fill_parser = subparsers.add_parser(
        "fill",
        help="Fill in content and questions for an existing outline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    fill_parser.add_argument(
        "outline_file",
        help="Path to the outline YAML file",
    )
    fill_parser.add_argument(
        "--output",
        "-o",
        help="Output file path for the complete course YAML",
    )
    fill_parser.add_argument(
        "--debug",
        action="store_true",
        help="Limit output to 500 tokens for testing",
    )

    args = parser.parse_args()

    # Check if command was provided
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Check for API key
    if not os.getenv("XAI_API_KEY"):
        print("Error: XAI_API_KEY environment variable not set")
        print("Please run: export XAI_API_KEY=your_api_key_here")
        sys.exit(1)

    # Set max_tokens based on debug flag
    max_tokens = 500 if args.debug else None

    try:
        if args.command == "outline":
            # Generate outline
            topic = " ".join(args.topic)

            outline = generate_course_outline(
                topic, lesson_count=args.lessons, max_tokens=max_tokens
            )

            # Save or print
            if args.output:
                with open(args.output, "w") as f:
                    f.write(outline)
                print(f"\n✓ Course outline saved to: {args.output}")
                print("\nNext step - fill in content:")
                print(f"  python create.py fill {args.output} -o complete_course.yaml")
            else:
                print("COURSE OUTLINE:")
                print("=" * 80)
                print(outline)
                print("=" * 80)

            if args.debug:
                print(
                    f"\nNote: Running in debug mode - output was limited to {max_tokens} tokens"
                )
                print("To run full generation, remove --debug flag")

        elif args.command == "fill":
            # Fill in content
            outline_path = args.outline_file

            if not os.path.exists(outline_path):
                print(f"Error: Outline file not found: {outline_path}")
                sys.exit(1)

            with open(outline_path, "r") as f:
                outline_yaml = f.read()

            # Fill in the content
            complete_course = fill_course_content(outline_yaml, max_tokens=max_tokens)

            # Convert to YAML
            output_yaml = yaml.dump(
                complete_course,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )

            # Save or print
            if args.output:
                with open(args.output, "w") as f:
                    f.write(output_yaml)
                print(f"\n✓ Complete course saved to: {args.output}")
            else:
                print("\n" + "=" * 80)
                print("COMPLETE COURSE:")
                print("=" * 80)
                print(output_yaml)

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
