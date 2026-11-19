"""Gemini client configuration checks."""

from google.genai import types

from skillforge.config import Settings
from skillforge.services import gemini


def test_gemini_client_uses_beta_api_for_system_instructions(monkeypatch):
    client_args = {}

    def fake_client(**kwargs):
        client_args.update(kwargs)
        return object()

    monkeypatch.setattr(gemini.genai, "Client", fake_client)

    gemini.GeminiGenerator(Settings(gemini_api_key="test-key"))

    assert isinstance(client_args["http_options"], types.HttpOptions)
    assert client_args["http_options"].api_version == "v1beta"
