"""High-level generation workflows for curricula, questions, feedback, and hints."""

import json
import logging

from prompts import (
    CHECK_ANSWER_PROMPT,
    HINT_LEVEL_1,
    HINT_LEVEL_2,
    HINT_SYSTEM_PROMPT,
    PLAN,
    PRACTICE_SYSTEM_PROMPT,
)
from skillforge.exceptions import GenerationError
from skillforge.models import PracticePlan, Roadmap
from skillforge.services.gemini import TextGenerator
from skillforge.services.json_parser import parse_json_object
from skillforge.services.validation import validate_practice_plan, validate_roadmap

LOGGER = logging.getLogger(__name__)


def create_roadmap(generator: TextGenerator, source_steps: list[str]) -> Roadmap:
    """Expand source roadmap steps into a validated 30-day curriculum."""
    response = generator.generate(json.dumps(source_steps), PLAN)
    return validate_roadmap(parse_json_object(response))


def create_practice_plan(
    generator: TextGenerator, plan: Roadmap, max_attempts: int = 5
) -> PracticePlan:
    """Generate a valid practice plan, retrying malformed model responses."""
    for attempt in range(1, max_attempts + 1):
        try:
            response = generator.generate(json.dumps(plan), PRACTICE_SYSTEM_PROMPT)
            return validate_practice_plan(parse_json_object(response))
        except GenerationError as error:
            LOGGER.warning("Practice-plan generation attempt %d/%d failed: %s", attempt,
                           max_attempts, error)
    raise GenerationError(
        "Failed to generate a valid 30-day practice plan after multiple attempts."
    )


def evaluate_answer(
    generator: TextGenerator, question: str, user_code: str, language: str
) -> str:
    """Return the evaluator's feedback for a learner's answer."""
    return generator.generate(CHECK_ANSWER_PROMPT(question, user_code, language))


def generate_hint(
    generator: TextGenerator, question: str, language: str, level: int
) -> str:
    """Return a non-solution hint at the requested level."""
    if level == 1:
        prompt = HINT_LEVEL_1(question, language)
    elif level == 2:
        prompt = HINT_LEVEL_2(question, language)
    else:
        raise ValueError("Hint level must be 1 or 2.")
    return generator.generate(prompt, HINT_SYSTEM_PROMPT)
