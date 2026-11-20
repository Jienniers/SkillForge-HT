"""Tests for the local OpenAI-compatible model provider."""

from types import SimpleNamespace

from skillforge.api import routes
from skillforge.api.schemas import RoadmapRequest
from skillforge.services import local_ai


def test_local_generator_uses_lm_studio_chat_completions(monkeypatch):
    captured = {}

    class FakeCompletions:
        def create(self, **kwargs):
            captured["request"] = kwargs
            return SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content="model output"))]
            )

    class FakeClient:
        def __init__(self, **kwargs):
            captured["client"] = kwargs
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setattr(local_ai, "OpenAI", FakeClient)

    generator = local_ai.LocalAITextGenerator(
        "http://localhost:1234/v1", "qwen2.5-coder-7b-instruct"
    )
    result = generator.generate("make a plan", "return JSON")

    assert result == "model output"
    assert captured["client"] == {
        "base_url": "http://localhost:1234/v1",
        "api_key": "lm-studio",
    }
    assert captured["request"] == {
        "model": "qwen2.5-coder-7b-instruct",
        "messages": [
            {"role": "system", "content": "return JSON"},
            {"role": "user", "content": "make a plan"},
        ],
    }


def test_local_provider_is_the_api_default():
    request = RoadmapRequest(language="python")

    assert request.provider == "local"


def test_provider_selection_is_passed_to_roadmap_service(monkeypatch):
    received = {}

    def fake_generate(language, provider):
        received.update(language=language, provider=provider)
        return {"day_1": ["topic"]}

    monkeypatch.setattr(routes, "generate_roadmap_for", fake_generate)

    result = routes.roadmap(RoadmapRequest(language="python", provider="gemini"))

    assert result == {"day_1": ["topic"]}
    assert received == {"language": "python", "provider": "gemini"}
