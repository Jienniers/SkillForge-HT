"""Pure progress and reward rules for the learning experience."""

from dataclasses import dataclass

from skillforge.constants import (
    ADVANCED_HINT_COST_XP,
    DAYS_IN_PLAN,
    FINAL_COMPLETION_BONUS_XP,
    FIRST_COMPLETION_BONUS_XP,
    LEVELS,
)


@dataclass(frozen=True, slots=True)
class CompletionReward:
    """The reward and presentation effect caused by completing a day."""

    xp: int = 0
    achievement: str | None = None


def level_for_xp(xp: int) -> str:
    """Return the display level for an XP total."""
    for threshold, level in LEVELS:
        if xp < threshold:
            return level
    return "👑 SkillForge Master"


def can_buy_advanced_hint(xp: int) -> bool:
    """Whether the user has enough XP for the second hint."""
    return xp >= ADVANCED_HINT_COST_XP


def completion_reward(
    *, day_number: int, completed_day_count: int, first_bonus_given: bool
) -> CompletionReward:
    """Determine achievement XP for a newly completed day.

    The final-day reward is granted only after all earlier days are complete.
    """
    if not first_bonus_given:
        return CompletionReward(FIRST_COMPLETION_BONUS_XP, "first_completion")
    if day_number == DAYS_IN_PLAN and completed_day_count >= DAYS_IN_PLAN:
        return CompletionReward(FINAL_COMPLETION_BONUS_XP, "final_completion")
    return CompletionReward()
