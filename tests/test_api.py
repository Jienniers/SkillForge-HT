"""API contract checks for the React learning workflows."""

import json

import pytest
from fastapi import HTTPException

from main import app
from skillforge.api import routes
from skillforge.api.schemas import (
    CompletionRequest,
    EvaluationRequest,
    HintRequest,
    LevelRequest,
    PracticeRequest,
    RoadmapPdfRequest,
    RoadmapRequest,
)
from skillforge.services.generation import create_roadmap

sample_plan = {f"day_{day}": [f"Python topic {day}"] for day in range(1, 31)}


def test_generate_roadmap(monkeypatch):
    monkeypatch.setattr(routes, "generate_roadmap_for", lambda language: sample_plan)

    response = routes.roadmap(RoadmapRequest(language="python"))

    assert len(response) == 30
    assert response["day_1"] == ["Python topic 1"]


def test_roadmap_use_case_uses_existing_gemini_workflow():
    class FakeGenerator:
        prompt = ""
        instruction = ""

        def generate(self, prompt, system_instruction=""):
            self.prompt = prompt
            self.instruction = system_instruction
            return json.dumps(sample_plan)

    generator = FakeGenerator()

    plan = create_roadmap(generator, "python")

    assert len(plan) == 30
    assert "python" in generator.prompt
    assert "python" in generator.instruction


def test_generate_practice(monkeypatch):
    practice = {
        f"day_{day}": {"Topic": ["Write a function" for _ in range(3)]}
        for day in range(1, 31)
    }
    monkeypatch.setattr(routes, "generate_practice_for", lambda _language, _plan: practice)

    response = routes.practice(PracticeRequest(language="python", roadmap=sample_plan))

    assert len(response) == 30
    assert len(response["day_1"]["Topic"]) == 3


def test_evaluate_answer(monkeypatch):
    monkeypatch.setattr(routes, "evaluate", lambda *_args: ("✅ Correct", True, 10))

    response = routes.evaluate_answer(
        EvaluationRequest(language="python", question="Q", code="print(1)")
    )

    assert response == {"feedback": "✅ Correct", "correct": True, "xp_awarded": 10}


def test_hint_and_advanced_hint_cost(monkeypatch):
    monkeypatch.setattr(routes, "generate_hint_for", lambda *_args: ("Try a loop.", 5))

    response = routes.hint(HintRequest(language="python", question="Q", level=2, xp=10))

    assert response == {"hint": "Try a loop.", "xp_cost": 5}


def test_advanced_hint_rejects_insufficient_xp():
    with pytest.raises(HTTPException) as error:
        routes.hint(HintRequest(language="python", question="Q", level=2, xp=0))
    assert error.value.status_code == 400


def test_completion_rewards_use_existing_gamification_rules():
    first = routes.completion(
        CompletionRequest(day_number=1, completed_day_count=1, first_bonus_given=False)
    )
    final = routes.completion(
        CompletionRequest(day_number=30, completed_day_count=30, first_bonus_given=True)
    )

    assert first == {"xp": 10, "achievement": "first_completion"}
    assert final == {"xp": 50, "achievement": "final_completion"}


def test_level_uses_existing_gamification_rules():
    assert routes.experience_level(LevelRequest(xp=350)) == {"level": "🔥 Intermediate"}


def test_download_roadmap_pdf():
    response = routes.roadmap_pdf(RoadmapPdfRequest(roadmap=sample_plan))

    assert response.media_type == "application/pdf"
    assert response.body.startswith(b"%PDF")


def test_api_routes_are_registered():
    paths = set(app.openapi()["paths"])
    expected = {
        "/api/roadmap", "/api/practice", "/api/evaluate", "/api/hint",
        "/api/roadmap/pdf", "/api/gamification/completion", "/api/gamification/level",
    }
    assert expected <= paths
