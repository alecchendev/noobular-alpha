import os
import sys
import argparse
import yaml
from typing import Optional, Any, Dict, List
from xai_sdk import Client  # type: ignore
from xai_sdk.chat import user, system, file  # type: ignore
from validate import validate_question
from enum import Enum


class Model(str, Enum):
    # Not the absolute cheapest ($1.50/mtok vs. $0.50/mtok), but seems to completely
    # fix syntax/structure errors.
    GROK_CODE_FAST = "grok-code-fast"
    GROK_4_FAST = "grok-4-fast"
    GROK_4 = "grok-4"


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

- prompt: |
    Question text here with $math$ allowed
  choices:
    - text: |
        Choice A with LaTeX like $x^2$
    - text: |
        Choice B
      correct: true
    - text: |
        Choice C
    - text: |
        Choice D
  explanation: |
    Explanation with **markdown** and $\lambda$ symbols

CRITICAL YAML FORMATTING RULES:
- Use | (pipe) for ALL text fields (prompt, text, explanation) - this avoids all quote escaping issues
- Do NOT use quotes around text - the pipe notation handles everything including apostrophes, quotes, and LaTeX
- Return ONLY the array of questions as valid YAML
- No code fences, no commentary
"""

TEXTBOOK_OUTLINE_PROMPT = """
The provided content and problems are transcribed sections from a textbook. Your goal is to transform the transcribed sections into a structured course outline that will most effectively teach a curious learner.

# Numbers
Create 1-4 lessons based on the provided content and problems.
Create 2-5 knowledge points per lesson.
Each knowledge point will later have at least 10 questions.

# Structure
Lessons should be scaffolded such that students are not exposed to too much information at once. Lessons should build up to students being able to solve the most challenging problems from the transcribed sections.
Each knowledge point should be atomic, and represent a discrete concept/skill that a student will master.
There should be a realistic structure formed through the prerequisites field on each knowledge point.

# Syntax and formatting
Use spaces not tabs. There should not be any blank lines in the YAML structure.
Use kebab-case for knowledge point names (e.g., 'force-equilibrium').
Use single quotes for all text fields to avoid escape character issues.

# Output format
Return ONLY valid YAML in this exact format (no code fences, no commentary):

title: 'Course Title Based on Section'
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
- Return ONLY raw YAML - do NOT wrap in ```yaml code fences
- Use SINGLE QUOTES for all text fields
- Do NOT include contents or questions fields - they will be added later
- Ensure prerequisite relationships accurately reflect dependencies between concepts

# Content from textbook:
{content}

# Problems from textbook:
{problems}"""

TEXTBOOK_CONTENT_PROMPT = """
You are creating educational content for a knowledge point based on transcribed textbook sections.

# Knowledge point details
- Course: {course_title}
- Lesson: {lesson_title}
- Knowledge point: {kp_name}
- Description: {kp_description}
- Prerequisites: {prerequisites}

# Task
Generate 2-4 content blocks that teach this specific concept/skill.
Content should include key concepts as well as an example practice problem being worked out in detail.
Each content block should be focused and digestible.
Use markdown formatting with headers (###), **bold**, *italic*, `code`.
Use inline math with $...$ and display math with $$...$$ where appropriate.
For lists, ensure a blank line precedes them.

# Output format
Return ONLY valid YAML (no code fences, no commentary) as an array:

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

# Content from textbook:
{content}

# Problems from textbook:
{problems}"""

TEXTBOOK_QUESTIONS_PROMPT = """
You are creating assessment questions for a knowledge point based on transcribed textbook sections.

# Knowledge point details
- Course: {course_title}
- Lesson: {lesson_title}
- Knowledge point: {kp_name}
- Description: {kp_description}

# Content taught in this knowledge point:
{content_summary}

# Task
Generate exactly 10 multiple choice questions that test this specific concept/skill.
Questions should strictly align with the skills used in the example problem from the content.
Questions will be served in a random order, so questions must not reference each other.
Answers should be difficult to guess. No choice should be obviously wrong. All 4 answer choices must be plausible.
Exactly one choice must be marked as correct.
Use markdown and math in prompts, choices, and explanations as needed.

# Output format
Return ONLY valid YAML (no code fences, no commentary) as an array:

- prompt: |
    Question text here with $math$ allowed
  choices:
    - text: |
        Choice A with LaTeX like $x^2$
    - text: |
        Choice B
      correct: true
    - text: |
        Choice C
    - text: |
        Choice D
  explanation: |
    Explanation with **markdown** and $\lambda$ symbols

CRITICAL YAML FORMATTING RULES:
- Use | (pipe) for ALL text fields (prompt, text, explanation) - this avoids all quote escaping issues
- Do NOT use quotes around text - the pipe notation handles everything including apostrophes, quotes, and LaTeX
- Return ONLY the array of questions as valid YAML
- No code fences, no commentary

# Content from textbook:
{content}

# Problems from textbook:
{problems}"""


def generate_course_outline(
    topic: str,
    lesson_count: int,
    max_tokens: Optional[int],
    model: str,
    content_file: Optional[str] = None,
    problems_file: Optional[str] = None,
) -> str:
    """
    Generate a course outline for the given topic using Grok API.

    Args:
        topic: The topic to create a course about (ignored if using textbook files)
        lesson_count: Target number of lessons (ignored if using textbook files)
        max_tokens: Maximum number of tokens in the response (None for unlimited)
        model: Model to use for generation
        content_file: Optional path to textbook content file
        problems_file: Optional path to textbook problems file

    Returns:
        The course outline as a string
    """
    # Read textbook files if provided
    content = None
    problems = None
    if content_file and problems_file:
        with open(content_file, "r") as f:
            content = f.read()
        with open(problems_file, "r") as f:
            problems = f.read()

    # Initialize the client
    client = Client(
        api_key=os.getenv("XAI_API_KEY"),
        timeout=3600,
    )

    # Create a chat session with optional max_tokens
    if max_tokens:
        chat = client.chat.create(model=model, max_tokens=max_tokens)
    else:
        chat = client.chat.create(model=model)

    chat.append(
        system(
            "You are an expert educational content creator who specializes in creating comprehensive, well-structured courses with clear learning progressions."
        )
    )

    # Add prompt based on mode (no separate system message needed)
    if content and problems:
        # Textbook mode
        prompt = TEXTBOOK_OUTLINE_PROMPT.format(content=content, problems=problems)
        print("Generating course outline from textbook files")
        print(f"Content file: {content_file}")
        print(f"Problems file: {problems_file}")
    else:
        # Topic mode
        prompt = COURSE_OUTLINE_PROMPT.format(topic=topic, lesson_count=lesson_count)
        print(f"Generating course outline for: {topic}")
        print(f"Target lesson count: {lesson_count}")

    chat.append(user(prompt))

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
    model: str,
    max_tokens: Optional[int] = None,
    content: Optional[str] = None,
    problems: Optional[str] = None,
) -> List[str]:
    """
    Generate content for a single knowledge point.

    Args:
        course_title: The title of the course
        lesson_title: The title of the lesson this KP belongs to
        kp_name: The name/ID of the knowledge point
        kp_description: The description of the knowledge point
        prerequisites: List of prerequisite knowledge point IDs
        model: Model to use for generation
        max_tokens: Maximum number of tokens in the response (None for unlimited)
        content: Optional textbook content text
        problems: Optional textbook problems text

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
        chat = client.chat.create(model=model, max_tokens=max_tokens)
    else:
        chat = client.chat.create(model=model)

    chat.append(
        system(
            "You are an expert educational content creator who creates clear, comprehensive learning materials with excellent examples."
        )
    )

    # Format prerequisites
    prereq_str = ", ".join(prerequisites) if prerequisites else "None"

    # Add prompt based on mode (no separate system message needed for textbook mode)
    if content and problems:
        # Textbook mode
        prompt = TEXTBOOK_CONTENT_PROMPT.format(
            course_title=course_title,
            lesson_title=lesson_title,
            kp_name=kp_name,
            kp_description=kp_description,
            prerequisites=prereq_str,
            content=content,
            problems=problems,
        )
    else:
        # Topic mode
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

    # Parse YAML response
    try:
        contents: List[str] = yaml.safe_load(response_text)
        return contents if isinstance(contents, list) else []
    except yaml.YAMLError as e:
        # Print full response
        print(f"\n{'=' * 80}")
        print(f"CONTENT RESPONSE for {kp_name}:")
        print(f"{'=' * 80}")
        print(response_text)
        print(f"{'=' * 80}\n")

        print(f"    Warning: Failed to parse content YAML for {kp_name}: {e}")
        return []


def generate_questions(
    course_title: str,
    lesson_title: str,
    kp_name: str,
    kp_description: str,
    contents: List[str],
    model: str,
    max_tokens: Optional[int] = None,
    max_retries: int = 2,
    content: Optional[str] = None,
    problems: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Generate questions for a single knowledge point based on its content.

    Args:
        course_title: The title of the course
        lesson_title: The title of the lesson this KP belongs to
        kp_name: The name/ID of the knowledge point
        kp_description: The description of the knowledge point
        contents: The content blocks that were generated
        model: Model to use for generation
        max_tokens: Maximum number of tokens in the response (None for unlimited)
        max_retries: Maximum number of retry attempts if validation fails
        content: Optional textbook content text
        problems: Optional textbook problems text

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
            chat = client.chat.create(model=model, max_tokens=max_tokens)
        else:
            chat = client.chat.create(model=model)

        chat.append(
            system(
                "You are an expert educational content creator who creates thoughtful, challenging questions that test deep understanding."
            )
        )

        # Add prompt based on mode (no separate system message needed for textbook mode)
        if content and problems:
            # Textbook mode
            prompt = TEXTBOOK_QUESTIONS_PROMPT.format(
                course_title=course_title,
                lesson_title=lesson_title,
                kp_name=kp_name,
                kp_description=kp_description,
                content_summary=content_summary,
                content=content,
                problems=problems,
            )
        else:
            # Topic mode
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

        # Parse YAML response
        questions: List[Dict[str, Any]] = []
        try:
            questions = yaml.safe_load(response_text)
            if not isinstance(questions, list):
                print("    Warning: Response is not a list, retrying...")
                continue
        except yaml.YAMLError as e:
            # Print full response
            print(f"\n{'=' * 80}")
            print(
                f"QUESTIONS RESPONSE for {kp_name} (attempt {attempt + 1}/{max_retries + 1}):"
            )
            print(f"{'=' * 80}")
            print(response_text)
            print(f"{'=' * 80}\n")

            print(f"    Warning: Failed to parse questions YAML for {kp_name}: {e}")
            if attempt < max_retries:
                print(f"    Retrying... ({attempt + 1}/{max_retries})")
                continue
            else:
                print("\n" + "=" * 80)
                print("ERROR: Max retries reached. Failed to parse YAML response.")
                print("=" * 80)
                raise ValueError(
                    f"Failed to parse YAML for {kp_name} after {max_retries + 1} attempts: {e}"
                )

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
            # Print full response
            print(f"\n{'=' * 80}")
            print(
                f"QUESTIONS RESPONSE for {kp_name} (attempt {attempt + 1}/{max_retries + 1}):"
            )
            print(f"{'=' * 80}")
            print(response_text)
            print(f"{'=' * 80}\n")

            print("    Validation errors found:")
            for error in validation_errors:
                print(f"      - {error}")
            if attempt < max_retries:
                print(f"    Retrying... ({attempt + 1}/{max_retries})")
                continue
            else:
                print("\n" + "=" * 80)
                print("ERROR: Max retries reached. Failed to generate valid questions.")
                print("=" * 80)
                raise ValueError(
                    f"Failed to generate valid questions for {kp_name} after {max_retries + 1} attempts"
                )

        # All questions valid!
        print("    ✓ All questions validated successfully")
        return questions

    raise ValueError(f"Failed to generate questions for {kp_name} - unexpected error")


def fill_course_content(
    outline_yaml: str,
    model: str,
    max_tokens: Optional[int] = None,
    content_file: Optional[str] = None,
    problems_file: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Takes a course outline YAML and fills in content and questions for each knowledge point.

    Args:
        outline_yaml: The course outline as a YAML string
        model: Model to use for generation
        max_tokens: Maximum number of tokens per knowledge point generation
        content_file: Optional path to textbook content file
        problems_file: Optional path to textbook problems file

    Returns:
        Complete course dictionary with all content and questions filled in
    """
    # Read textbook files if provided
    content = None
    problems = None
    if content_file and problems_file:
        with open(content_file, "r") as f:
            content = f.read()
        with open(problems_file, "r") as f:
            problems = f.read()

    # Parse the outline
    try:
        course: Dict[str, Any] = yaml.safe_load(outline_yaml)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML outline: {e}")

    course_title = course.get("title", "Unknown Course")
    lessons = course.get("lessons", [])

    print(f"\nFilling content for course: {course_title}")
    print(f"Total lessons: {len(lessons)}")
    if content_file and problems_file:
        print(f"Using textbook files: {content_file}, {problems_file}")
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
                model=model,
                max_tokens=max_tokens,
                content=content,
                problems=problems,
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
                model=model,
                max_tokens=max_tokens,
                content=content,
                problems=problems,
            )
            print(f"✓ ({len(questions)} questions)")

            # Add to knowledge point
            kp["contents"] = contents
            kp["questions"] = questions

    print("\n" + "=" * 80)
    print("Course content generation complete!")

    return course


def extract_textbook_content(
    textbook_file_id: str,
    section_name: str,
    model: str,
    max_tokens: Optional[int] = None,
) -> str:
    """
    Extract content from a textbook section using vision model.

    Args:
        textbook_file: Path to the textbook PDF file
        section_name: Name of the section to extract
        max_tokens: Maximum number of tokens in the response (None for unlimited)

    Returns:
        Extracted content as a string
    """
    # Initialize the client
    client = Client(
        api_key=os.getenv("XAI_API_KEY"),
        timeout=3600,
    )

    # Create a chat session with vision model
    if max_tokens:
        chat = client.chat.create(model=model, max_tokens=max_tokens)
    else:
        chat = client.chat.create(model=model)

    # Add system message
    chat.append(
        system(
            "You are an expert at extracting educational content from textbooks. Be comprehensive and accurate."
        )
    )

    # Create prompt for content extraction
    prompt = f"""Extract all the content from section {section_name}. Be comprehensive and make sure you get everything relevant. Review the material to make sure you have not made any mistakes. Output nicely formatted plaintext that can be written to a txt file."""

    # Add user message with file attachment
    chat.append(user(prompt, file(textbook_file_id)))

    print(f"Extracting content from section '{section_name}'...")

    # Get response
    response = chat.sample()
    return str(response.content)


def extract_textbook_problems(
    textbook_file_id: str,
    section_name: str,
    model: str,
    max_tokens: Optional[int] = None,
) -> str:
    """
    Extract practice problems from a textbook section using vision model.

    Args:
        textbook_file: Path to the textbook PDF file
        section_name: Name of the section to extract problems for
        max_tokens: Maximum number of tokens in the response (None for unlimited)

    Returns:
        Extracted problems as a string
    """
    # Initialize the client
    client = Client(
        api_key=os.getenv("XAI_API_KEY"),
        timeout=3600,
    )

    # Create a chat session with vision model
    if max_tokens:
        chat = client.chat.create(model=model, max_tokens=max_tokens)
    else:
        chat = client.chat.create(model=model)

    # Add system message
    chat.append(
        system(
            "You are an expert at extracting practice problems from textbooks. Be comprehensive and accurate."
        )
    )

    # Create prompt for problems extraction
    prompt = f"""Extract all the practice problems for section {section_name} from the section. This should include example problems from the section, as well as the probelms from the end of the chapter, from sections such as guided practice, exercises, challenge problems, and mcat-style problems. Be comprehensive and make sure you get everything relevant. DO NOT make up any new material, strictly transcribe. DO NOT include any text from images/figures. Output nicely formatted plaintext that can be written to a text file."""

    # Add user message with file attachment
    chat.append(user(prompt, file(textbook_file_id)))

    print(f"Extracting problems from section '{section_name}'...")

    # Get response
    response = chat.sample()
    return str(response.content)


def extract_section(
    textbook_file: str,
    section_name: str,
    content_output: str,
    problems_output: str,
    model: str,
    max_tokens: Optional[int] = None,
) -> None:
    """
    Extract content and problems from a textbook section.

    Args:
        textbook_file: Path to the textbook PDF file
        section_name: Name of the section to extract
        content_output: Path to write extracted content
        problems_output: Path to write extracted problems
        model: Model to use for generation
        max_tokens: Maximum number of tokens in the response (None for unlimited)
    """
    print(f"Extracting from: {textbook_file}")
    print(f"Section: {section_name}")
    print("=" * 80)

    # Upload the file if it hasn't been uploaded already
    client = Client(
        api_key=os.getenv("XAI_API_KEY"),
        timeout=3600,
    )
    files_response = client.files.list()
    textbook_chapter_file = None
    for uploaded_file in files_response.data:
        if uploaded_file.filename == os.path.basename(textbook_file):
            textbook_chapter_file = uploaded_file
            break
    if textbook_chapter_file is None:
        print(f"Uploading file: {textbook_file}...")
        textbook_chapter_file = client.files.upload(textbook_file)
    else:
        print("Skipping file upload, already exists.")
    textbook_file_id = textbook_chapter_file.id
    print(f"File ID: {textbook_file_id}")

    # Extract content
    content = extract_textbook_content(
        textbook_file_id, section_name, model, max_tokens
    )
    with open(content_output, "w") as f:
        f.write(content)
    print(f"✓ Content written to: {content_output}")

    # Extract problems
    problems = extract_textbook_problems(
        textbook_file_id, section_name, model, max_tokens
    )
    with open(problems_output, "w") as f:
        f.write(problems)
    print(f"✓ Problems written to: {problems_output}")

    print("=" * 80)
    print("Extraction complete!")


def main() -> None:
    # Main parser
    parser = argparse.ArgumentParser(
        description="Course generator using Grok API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Add global model argument
    parser.add_argument(
        "--model",
        "-m",
        default=Model.GROK_4_FAST,
        help=f"Grok model to use (default: {Model.GROK_4_FAST})",
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
        nargs="*",
        help="The course topic to generate an outline for (not used if --content and --problems provided)",
    )
    outline_parser.add_argument(
        "--lessons",
        "-l",
        type=int,
        default=8,
        help="Target number of lessons (default: 8, ignored if using textbook files)",
    )
    outline_parser.add_argument(
        "--content",
        "-c",
        help="Path to textbook content file (use with --problems)",
    )
    outline_parser.add_argument(
        "--problems",
        "-p",
        help="Path to textbook problems file (use with --content)",
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
        "--content",
        "-c",
        help="Path to textbook content file (use with --problems for textbook-based generation)",
    )
    fill_parser.add_argument(
        "--problems",
        "-p",
        help="Path to textbook problems file (use with --content for textbook-based generation)",
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

    # Extract subcommand
    extract_parser = subparsers.add_parser(
        "extract",
        help="Extract content and problems from a textbook section",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    extract_parser.add_argument(
        "textbook_file",
        help="Path to the textbook PDF file",
    )
    extract_parser.add_argument(
        "section_name",
        help="Name of the section to extract (e.g., 'Section 5.1')",
    )
    extract_parser.add_argument(
        "--content-output",
        "-c",
        required=True,
        help="Output file for extracted content",
    )
    extract_parser.add_argument(
        "--problems-output",
        "-p",
        required=True,
        help="Output file for extracted problems",
    )
    extract_parser.add_argument(
        "--debug",
        action="store_true",
        help="Limit output to 500 tokens for testing",
    )

    args = parser.parse_args()
    assert args.model in list(Model)

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
            # Validate textbook file arguments
            if args.content and not args.problems:
                print("Error: --content requires --problems")
                sys.exit(1)
            if args.problems and not args.content:
                print("Error: --problems requires --content")
                sys.exit(1)

            # Validate topic argument
            if not args.content and not args.topic:
                print("Error: Either provide a topic or use --content and --problems")
                sys.exit(1)

            # Generate outline
            topic = " ".join(args.topic) if args.topic else ""

            outline = generate_course_outline(
                topic,
                lesson_count=args.lessons,
                max_tokens=max_tokens,
                model=args.model,
                content_file=args.content,
                problems_file=args.problems,
            )

            # Save or print
            if args.output:
                with open(args.output, "w") as f:
                    f.write(outline)
                print(f"\n✓ Course outline saved to: {args.output}")
                print("\nNext step - fill in content:")
                if args.content and args.problems:
                    print(
                        f"  python create.py fill {args.output} -c {args.content} -p {args.problems} -o complete_course.yaml"
                    )
                else:
                    print(
                        f"  python create.py fill {args.output} -o complete_course.yaml"
                    )
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
            # Validate textbook file arguments
            if args.content and not args.problems:
                print("Error: --content requires --problems")
                sys.exit(1)
            if args.problems and not args.content:
                print("Error: --problems requires --content")
                sys.exit(1)

            # Fill in content
            outline_path = args.outline_file

            if not os.path.exists(outline_path):
                print(f"Error: Outline file not found: {outline_path}")
                sys.exit(1)

            with open(outline_path, "r") as f:
                outline_yaml = f.read()

            # Fill in the content
            complete_course = fill_course_content(
                outline_yaml,
                model=args.model,
                max_tokens=max_tokens,
                content_file=args.content,
                problems_file=args.problems,
            )

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

        elif args.command == "extract":
            # Extract from textbook
            textbook_file = args.textbook_file
            section_name = args.section_name

            if not os.path.exists(textbook_file):
                print(f"Error: Textbook file not found: {textbook_file}")
                sys.exit(1)

            # Extract section
            extract_section(
                textbook_file=textbook_file,
                section_name=section_name,
                content_output=args.content_output,
                problems_output=args.problems_output,
                model=args.model,
                max_tokens=max_tokens,
            )

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
