"""Shared user-facing constants and application rules."""

DAYS_IN_PLAN = 30
DEFAULT_AI_PROVIDER = "gemini"
QUESTIONS_PER_TOPIC = 3
QUESTION_XP = 10
FIRST_COMPLETION_BONUS_XP = 10
FINAL_COMPLETION_BONUS_XP = 50
ADVANCED_HINT_COST_XP = 5

LEVELS: tuple[tuple[int, str], ...] = (
    (100, "🌱 Beginner"),
    (300, "⚡ Apprentice"),
    (600, "🔥 Intermediate"),
    (1_000, "🚀 Advanced"),
)
