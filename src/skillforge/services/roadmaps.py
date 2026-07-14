"""Loading and validation for the bundled roadmap templates."""

import json
from pathlib import Path
from typing import Any

from skillforge.exceptions import InvalidRoadmapError


def load_roadmap_steps(path: Path, language: str) -> list[str]:
    """Return the source learning steps for a supported language."""
    try:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        steps = data["roadmaps"][language]["steps"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise InvalidRoadmapError(
            f"Could not load roadmap steps for '{language}' from {path}."
        ) from error

    if not isinstance(steps, list) or not all(isinstance(step, str) for step in steps):
        raise InvalidRoadmapError(f"Roadmap steps for '{language}' must be a list of text.")
    return steps
