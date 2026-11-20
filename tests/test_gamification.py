from skillforge.constants import FINAL_COMPLETION_BONUS_XP, FIRST_COMPLETION_BONUS_XP
from skillforge.services.gamification import completion_reward


def test_final_bonus_uses_practical_day_count_instead_of_thirty():
    reward = completion_reward(
        day_number=29,
        completed_day_count=28,
        first_bonus_given=True,
        total_practice_days=28,
        final_practice_day=True,
    )

    assert reward.xp == FINAL_COMPLETION_BONUS_XP
    assert reward.achievement == "final_completion"


def test_final_bonus_waits_until_every_practical_day_is_complete():
    reward = completion_reward(
        day_number=29,
        completed_day_count=27,
        first_bonus_given=True,
        total_practice_days=28,
        final_practice_day=True,
    )

    assert reward.xp == 0
    assert reward.achievement is None


def test_first_completion_bonus_still_has_priority():
    reward = completion_reward(
        day_number=30,
        completed_day_count=1,
        first_bonus_given=False,
        total_practice_days=28,
        final_practice_day=True,
    )

    assert reward.xp == FIRST_COMPLETION_BONUS_XP
    assert reward.achievement == "first_completion"
