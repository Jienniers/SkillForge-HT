"""Application configuration and paths."""

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings sourced from the environment."""

    gemini_api_key: str | None
    gemini_model: str = "gemini-2.5-flash"
    local_ai_base_url: str = "http://localhost:1234/v1"
    local_ai_model: str = "qwen3.5-9b"

    @classmethod
    def from_environment(cls) -> "Settings":
        """Build settings after dotenv has made local variables available."""
        return cls(
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            local_ai_base_url=os.getenv("LOCAL_AI_BASE_URL", "http://localhost:1234/v1"),
            local_ai_model=os.getenv("LOCAL_AI_MODEL", "qwen2.5-coder-7b-instruct"),
        )
