"""Reliable parsing helpers for JSON returned by language models."""

import json
from typing import Any

from skillforge.exceptions import GenerationError


def parse_json_object(response_text: str) -> dict[str, Any]:
    """Extract and parse the first JSON object from a model response.

    Models are asked for raw JSON but may still wrap it in Markdown fences.  This
    intentionally accepts that harmless formatting while rejecting non-objects.
    """
    cleaned = response_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else ""
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start < 0 or end < start:
        raise GenerationError("The model response did not contain a JSON object.")

    try:
        payload = json.loads(cleaned[start : end + 1])
    except json.JSONDecodeError as error:
        raise GenerationError("The model returned malformed JSON.") from error

    if not isinstance(payload, dict):
        raise GenerationError("The model response must be a JSON object.")
    return payload
