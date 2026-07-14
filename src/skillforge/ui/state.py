"""Centralized Streamlit session-state access."""

from collections.abc import MutableMapping
from typing import Any

from skillforge.constants import QUESTION_XP
from skillforge.models import PracticeDay


RESET_PREFIXES = ("done_", "result_", "xp_awarded_", "feedback_", "hint_", "completed_")
RESET_KEYS = (
    "practice_questions", "achievements", "bonus_given", "first_day_bonus_given",
    "plan", "selected_day", "language",
)


def reset_learning_session(state: MutableMapping[str, Any]) -> None:
    """Remove all progress belonging to the currently generated roadmap."""
    for key in list(state):
        if key.startswith(RESET_PREFIXES):
            del state[key]
    for key in RESET_KEYS:
        state.pop(key, None)
    state["xp"] = 0


def completed_day_count(state: MutableMapping[str, Any]) -> int:
    """Count completed days in the active learning session."""
    return sum(key.startswith("done_day_") and bool(value) for key, value in state.items())


def question_key(day: str, topic: str, index: int) -> str:
    """Return the stable ID used by Streamlit widgets and associated state."""
    return f"{day}_{topic}_{index}"


def result_key(day: str, topic: str, index: int) -> str:
    """Return the stable key for evaluator feedback."""
    return f"result_{question_key(day, topic, index)}"


def is_correct(result: str) -> bool:
    """Whether the model response has the app's required correct marker."""
    return "✅ Correct" in result


def update_day_progress(
    state: MutableMapping[str, Any], day: str, data: PracticeDay
) -> tuple[int, int]:
    """Award each correct answer once and return ``(correct, total)``."""
    correct = total = 0
    for topic, questions in data.items():
        for index, _question in enumerate(questions):
            total += 1
            key = result_key(day, topic, index)
            if not is_correct(str(state.get(key, ""))):
                continue
            correct += 1
            award_key = f"xp_awarded_{key}"
            if not state.get(award_key):
                state["xp"] = int(state.get("xp", 0)) + QUESTION_XP
                state[award_key] = True
                state[f"completed_{key}"] = True
    return correct, total
