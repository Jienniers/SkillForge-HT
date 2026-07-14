from skillforge.constants import FINAL_COMPLETION_BONUS_XP, FIRST_COMPLETION_BONUS_XP
from skillforge.services.gamification import can_buy_advanced_hint, completion_reward, level_for_xp


def test_level_boundaries() -> None:
    assert level_for_xp(0) == "🌱 Beginner"
    assert level_for_xp(100) == "⚡ Apprentice"
    assert level_for_xp(1_000) == "👑 SkillForge Master"


def test_first_completion_receives_one_time_bonus() -> None:
    reward = completion_reward(day_number=5, completed_day_count=1, first_bonus_given=False)

    assert reward.xp == FIRST_COMPLETION_BONUS_XP
    assert reward.achievement == "first_completion"


def test_final_completion_requires_all_days_and_prior_first_bonus() -> None:
    no_reward = completion_reward(day_number=30, completed_day_count=29, first_bonus_given=True)
    final_reward = completion_reward(day_number=30, completed_day_count=30, first_bonus_given=True)

    assert no_reward.xp == 0
    assert final_reward.xp == FINAL_COMPLETION_BONUS_XP
    assert final_reward.achievement == "final_completion"


def test_advanced_hint_requires_exact_cost() -> None:
    assert not can_buy_advanced_hint(4)
    assert can_buy_advanced_hint(5)
