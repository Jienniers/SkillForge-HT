"""Type aliases for the JSON-shaped curriculum data."""

from typing import TypeAlias


Roadmap: TypeAlias = dict[str, list[str]]
PracticeDay: TypeAlias = dict[str, list[str]]
PracticePlan: TypeAlias = dict[str, PracticeDay]
