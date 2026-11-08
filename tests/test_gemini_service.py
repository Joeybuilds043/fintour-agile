from __future__ import annotations

from types import SimpleNamespace

import pytest
import requests

from src.services import gemini


def test_generate_text_parses_gemini_response(monkeypatch):
    captured = {}

    def fake_post(url, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return SimpleNamespace(
            status_code=200,
            raise_for_status=lambda: None,
            json=lambda: {"candidates": [{"content": {"parts": [{"text": "A useful answer."}]}}]},
        )

    monkeypatch.setattr(gemini.requests, "post", fake_post)
    result = gemini.generate_text(
        api_key="test-key",
        system_instruction="Be accurate.",
        user_prompt="Help plan a trip.",
    )

    assert result == "A useful answer."
    assert captured["headers"]["x-goog-api-key"] == "test-key"
    assert captured["url"].endswith(":generateContent")


def test_generate_text_explains_rate_limit(monkeypatch):
    monkeypatch.setattr(
        gemini.requests,
        "post",
        lambda *args, **kwargs: SimpleNamespace(status_code=429),
    )

    with pytest.raises(gemini.GeminiAPIError, match="rate limit"):
        gemini.generate_text(
            api_key="test-key",
            system_instruction="Be accurate.",
            user_prompt="Help plan a trip.",
        )


def test_generate_text_rejects_missing_key():
    with pytest.raises(gemini.GeminiAPIError, match="API key is missing"):
        gemini.generate_text(
            api_key="",
            system_instruction="Be accurate.",
            user_prompt="Help plan a trip.",
        )



def test_generate_text_enables_google_search_and_renders_citations(monkeypatch):
    captured = {}

    def fake_post(url, **kwargs):
        captured.update(kwargs)
        return SimpleNamespace(
            status_code=200,
            raise_for_status=lambda: None,
            json=lambda: {
                "candidates": [{
                    "content": {"parts": [{"text": "A sourced answer."}]},
                    "groundingMetadata": {
                        "groundingChunks": [
                            {"web": {"uri": "https://example.org/source", "title": "Example source"}}
                        ]
                    },
                }]
            },
        )

    monkeypatch.setattr(gemini.requests, "post", fake_post)
    result = gemini.generate_text(
        api_key="test-key",
        system_instruction="Be accurate.",
        user_prompt="Research a destination.",
        google_search=True,
    )
    assert captured["json"]["tools"] == [{"google_search": {}}]
    assert "[Example source](https://example.org/source)" in result


def test_get_api_key_reads_google_api_key_environment(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "env-google-key")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert gemini.get_api_key() == "env-google-key"


def test_get_api_key_reads_google_genai_secret_alias(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.setenv("GOOGLE_GENAI_API_KEY", "existing-secret-alias")
    assert gemini.get_api_key() == "existing-secret-alias"
