"""Google Gemini integration behind a small, testable interface."""

import logging
from typing import Protocol

from google import genai

from skillforge.config import Settings
from skillforge.exceptions import ConfigurationError, GenerationError


LOGGER = logging.getLogger(__name__)


class TextGenerator(Protocol):
    """Minimal interface required by the generation services."""

    def generate(self, prompt: str, system_instruction: str = "") -> str:
        """Generate text for a user prompt and optional system instruction."""


class GeminiGenerator:
    """Gemini-backed implementation of :class:`TextGenerator`."""

    def __init__(self, settings: Settings) -> None:
        if not settings.gemini_api_key:
            raise ConfigurationError(
                "GEMINI_API_KEY is not configured. Add it to your .env file."
            )
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._model = settings.gemini_model

    def generate(self, prompt: str, system_instruction: str = "") -> str:
        """Generate non-empty content or raise a useful application error."""
        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
                config={"system_instruction": system_instruction},
            )
        except Exception as error:  # Provider errors have no stable public hierarchy.
            LOGGER.exception("Gemini generation request failed")
            raise GenerationError("The AI service could not complete the request.") from error
        if not response.text:
            raise GenerationError("The AI service returned an empty response.")
        return response.text
