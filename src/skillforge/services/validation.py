"""Validation for generated roadmap and practice-plan payloads."""

from typing import Any

from skillforge.constants import DAYS_IN_PLAN, QUESTIONS_PER_TOPIC
from skillforge.exceptions import GenerationError
from skillforge.models import PracticePlan, Roadmap


def expected_day_keys() -> set[str]:
    """Return the canonical set of day keys used throughout the app."""
    return {f"day_{day}" for day in range(1, DAYS_IN_PLAN + 1)}


def validate_roadmap(payload: dict[str, Any]) -> Roadmap:
    """Validate a generated 30-day roadmap before displaying it."""
    _validate_day_keys(payload)
    if not all(
        isinstance(topics, list) and all(isinstance(topic, str) for topic in topics)
        for topics in payload.values()
    ):
        raise GenerationError("Each roadmap day must contain a list of text topics.")
    return payload  # type: ignore[return-value]


def validate_practice_plan(payload: dict[str, Any]) -> PracticePlan:
    """Validate the strict day/topic/question structure required by the UI."""
    _validate_day_keys(payload)
    for day, topics in payload.items():
        if not isinstance(topics, dict):
            raise GenerationError(f"{day} must be an object of topics.")
        for topic, questions in topics.items():
            if not isinstance(topic, str) or not isinstance(questions, list):
                raise GenerationError(f"{day} contains an invalid topic.")
            if len(questions) != QUESTIONS_PER_TOPIC or not all(
                isinstance(question, str) for question in questions
            ):
                raise GenerationError(
                    f"Each topic in {day} must contain {QUESTIONS_PER_TOPIC} questions."
                )
    return payload  # type: ignore[return-value]


def _validate_day_keys(payload: dict[str, Any]) -> None:
    if set(payload) != expected_day_keys():
        raise GenerationError("The generated plan must contain exactly day_1 through day_30.")
