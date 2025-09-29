# Noobular

Noobular is software made to help me learn chemistry and physics actively and efficiently.

### Motivation 

Math Academy has proven that it's possible to build a software system that dramatically increases the rate of learning, using various techniques supported by decades of evidence.
In the past I've personally been a very satisfied customer of Math Academy, and I want to use Math Academy's learnings to learn subjects beyond math.

Unlike Math Academy, I don't have a team or the expertise to create educational content myself. I am the one trying to learn after all. However I have access to compressed versions of the internet that I can extract knowledge from via natural language. My hypothesis with this program is that for most things I want to learn, it should be possible to extract content from LLMs in the format needed to implement the accelerated learning techniques from Math Academy, to dramatically improve my rate of learning. Hopefully this can be done in a reproducible way across many subjects, and eventually become useful to others. But first, I'm starting with the man in the mirror ♪

### Primary functions

- Topic/question -> course content (primarily exercises)
- Effort -> learning (with minimal energy lost)

### Goals

- Be extremely simple. Get it all the work, then make it nice.

### Development

- HTMX + Python. Architecture similar to jupyter. Local app, web UI, with a backend that works directly with the filesystem.
    - Eventually can be repurposed as a web app so people don't have to run it themselves, but DON'T WORRY ABOUT THAT FOR NOW!
- Setup virtual environment:
    - `python3 -m venv venv`
    - `source venv/bin/activate.fish`
    - (deactivate virtual environment) `deactivate`
- Install dependencies: `python -m pip install -e .`
- Install dev dependencies: `python -m pip install -e ".[dev]"`
- Install pre-commit hooks: `pre-commit install`
- Run: `python main.py`
- Run tests: `python test.py`
- Lint: `ruff check`
- Format: `ruff format`
- Type check: `mypy`

### Database

The app uses SQLite3 for data storage, which is included in Python's standard library. A `database.db` file will be created automatically on first run.
