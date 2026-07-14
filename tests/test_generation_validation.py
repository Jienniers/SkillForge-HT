import pytest

from skillforge.exceptions import GenerationError
from skillforge.services.json_parser import parse_json_object
from skillforge.services.validation import validate_practice_plan, validate_roadmap


def _days(value: object) -> dict[str, object]:
    return {f"day_{index}": value for index in range(1, 31)}


def test_parser_accepts_fenced_json() -> None:
    assert parse_json_object("```json\n{\"day_1\": []}\n```") == {"day_1": []}


def test_parser_rejects_text_without_json() -> None:
    with pytest.raises(GenerationError, match="JSON object"):
        parse_json_object("not JSON")


def test_roadmap_requires_all_thirty_days() -> None:
    roadmap = _days(["A topic"])
    assert validate_roadmap(roadmap) == roadmap
    roadmap.pop("day_30")
    with pytest.raises(GenerationError, match="day_1 through day_30"):
        validate_roadmap(roadmap)


def test_practice_plan_requires_three_questions_per_topic() -> None:
    plan = _days({"Topic": ["one", "two", "three"]})
    assert validate_practice_plan(plan) == plan
    plan["day_1"] = {"Topic": ["only one"]}
    with pytest.raises(GenerationError, match="3 questions"):
        validate_practice_plan(plan)
