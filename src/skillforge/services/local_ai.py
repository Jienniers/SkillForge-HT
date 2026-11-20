"""OpenAI-compatible local model integration (for example, LM Studio)."""

import logging

from openai import OpenAI

from skillforge.exceptions import GenerationError

LOGGER = logging.getLogger(__name__)


class LocalAITextGenerator:
    """Text generator for a local OpenAI-compatible chat-completions server."""

    def __init__(self, base_url: str, model: str) -> None:
        self._client = OpenAI(base_url=base_url, api_key="lm-studio")
        self._model = model

    def generate(self, prompt: str, system_instruction: str = "") -> str:
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as error:  # Provider errors differ across local servers.
            LOGGER.exception("Local AI generation request failed")
            raise GenerationError(
                "Local AI could not complete the request. Check that LM Studio is running "
                "and the selected model is loaded."
            ) from error

        content = response.choices[0].message.content
        if not content:
            raise GenerationError("Local AI returned an empty response.")
        return content
