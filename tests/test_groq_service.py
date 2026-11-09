from types import SimpleNamespace

import pytest
from src.services import groq


def test_groq_uses_openai_responses_client_and_extracts_text(monkeypatch):
    captured = {}

    class FakeResponses:
        def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(output_text="A useful answer.")

    class FakeClient:
        def __init__(self, **kwargs):
            captured["client"] = kwargs
            self.responses = FakeResponses()

    monkeypatch.setattr(groq, "OpenAI", FakeClient)
    answer = groq.generate_text(
        api_key="test-groq-key",
        system_instruction="Be accurate.",
        user_prompt="Suggest a Kumrat itinerary.",
        temperature=0.4,
        max_output_tokens=900,
    )
    assert answer == "A useful answer."
    assert captured["client"]["api_key"] == "test-groq-key"
    assert captured["client"]["base_url"] == "https://api.groq.com/openai/v1"
    assert captured["model"] == groq.DEFAULT_MODEL
    assert captured["instructions"] == "Be accurate."
    assert captured["input"] == "Suggest a Kumrat itinerary."
    assert captured["temperature"] == 0.4
    assert captured["max_output_tokens"] == 900


def test_groq_requires_server_side_key():
    with pytest.raises(groq.GroqAPIError, match="GROQ_API_KEY"):
        groq.generate_text(api_key="", system_instruction="Be accurate.", user_prompt="Hello.")


def test_groq_handles_empty_response(monkeypatch):
    class FakeResponses:
        def create(self, **kwargs):
            return SimpleNamespace(output_text="")

    class FakeClient:
        def __init__(self, **kwargs):
            self.responses = FakeResponses()

    monkeypatch.setattr(groq, "OpenAI", FakeClient)
    with pytest.raises(groq.GroqAPIError, match="no text"):
        groq.generate_text(api_key="test-groq-key", system_instruction="Be accurate.", user_prompt="Hello.")
