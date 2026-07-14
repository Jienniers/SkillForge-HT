"""Shared user-facing constants and application rules."""

from skillforge.config import SOUNDS_DIRECTORY

SUPPORTED_LANGUAGES = ("Python", "JavaScript", "Java", "C++", "Go")
DAYS_IN_PLAN = 30
QUESTIONS_PER_TOPIC = 3
QUESTION_XP = 10
FIRST_COMPLETION_BONUS_XP = 10
FINAL_COMPLETION_BONUS_XP = 50
ADVANCED_HINT_COST_XP = 5

ACHIEVEMENT_SOUND_PATH = SOUNDS_DIRECTORY / "AchievementSound.mp3"
DAY_COMPLETE_SOUND_PATH = SOUNDS_DIRECTORY / "DayCompleteSound.mp3"

LEVELS: tuple[tuple[int, str], ...] = (
    (100, "🌱 Beginner"),
    (300, "⚡ Apprentice"),
    (600, "🔥 Intermediate"),
    (1_000, "🚀 Advanced"),
)
