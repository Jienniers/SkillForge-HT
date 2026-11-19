"""Regression tests for evaluation response serialization."""

from skillforge.api import routes
from skillforge.api.schemas import EvaluationRequest, EvaluationResponse


def test_evaluation_response_accepts_integer_xp_award(monkeypatch):
    monkeypatch.setattr(routes, "evaluate", lambda *_args: ("✅ Correct", True, 10))

    response = routes.evaluate_answer(
        EvaluationRequest(language="python", question="Print a value", code="print(1)")
    )

    assert isinstance(response, EvaluationResponse)
    assert response.model_dump() == {
        "feedback": "✅ Correct",
        "correct": True,
        "xp_awarded": 10,
    }
