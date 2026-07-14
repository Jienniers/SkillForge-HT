"""Application configuration and paths."""

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIRECTORY = PROJECT_ROOT / "data"
SOUNDS_DIRECTORY = PROJECT_ROOT / "Sounds"


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings sourced from the environment."""

    gemini_api_key: str | None
    gemini_model: str = "gemini-2.5-flash"
    roadmap_path: Path = DATA_DIRECTORY / "roadmap.json"

    @classmethod
    def from_environment(cls) -> "Settings":
        """Build settings after dotenv has made local variables available."""
        return cls(gemini_api_key=os.getenv("GEMINI_API_KEY"))
