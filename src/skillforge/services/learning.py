"""Application use cases that connect API requests to Gemini and domain logic."""

from skillforge.config import Settings
from skillforge.constants import ADVANCED_HINT_COST_XP, DEFAULT_AI_PROVIDER, QUESTION_XP
from skillforge.models import PracticePlan, Roadmap
from skillforge.services.gamification import can_buy_advanced_hint, completion_reward, level_for_xp
from skillforge.services.gemini import GeminiGenerator
from skillforge.services.generation import (
    create_practice_plan,
    create_roadmap,
    evaluate_answer,
    generate_hint,
)
from skillforge.services.local_ai import LocalAITextGenerator
from skillforge.services.validation import validate_roadmap


def _generator(provider: str = DEFAULT_AI_PROVIDER):
    settings = Settings.from_environment()
    if provider == "gemini":
        return GeminiGenerator(settings)
    if provider == "local":
        return LocalAITextGenerator(settings.local_ai_base_url, settings.local_ai_model)
    raise ValueError(f"Unsupported AI provider: {provider}")


def generate_roadmap_for(language: str, provider: str = DEFAULT_AI_PROVIDER) -> Roadmap:
    return create_roadmap(_generator(provider), language)


def generate_practice_for(
    language: str, roadmap: Roadmap, provider: str = DEFAULT_AI_PROVIDER
) -> PracticePlan:
    validate_roadmap(roadmap)
    del language  # The generated curriculum already contains its language-specific context.
    return create_practice_plan(_generator(provider), roadmap)


def evaluate(
    question: str, code: str, language: str, provider: str = DEFAULT_AI_PROVIDER
) -> tuple[str, bool, int]:
    feedback = evaluate_answer(_generator(provider), question, code, language)
    correct = "✅ Correct" in feedback
    return feedback, correct, QUESTION_XP if correct else 0


def generate_hint_for(
    question: str,
    language: str,
    level: int,
    xp: int,
    already_charged: bool,
    provider: str = DEFAULT_AI_PROVIDER,
) -> tuple[str, int]:
    cost = ADVANCED_HINT_COST_XP if level == 2 and not already_charged else 0
    if cost and not can_buy_advanced_hint(xp):
        raise ValueError("You don't have enough XP to use this hint.")
    return generate_hint(_generator(provider), question, language, level), cost


def completion_reward_for(
    day_number: int,
    completed_day_count: int,
    first_bonus_given: bool,
    total_practice_days: int = 30,
    final_practice_day: bool = False,
):
    return completion_reward(
        day_number=day_number,
        completed_day_count=completed_day_count,
        first_bonus_given=first_bonus_given,
        total_practice_days=total_practice_days,
        final_practice_day=final_practice_day,
    )


def level_for_experience(xp: int) -> str:
    return level_for_xp(xp)
