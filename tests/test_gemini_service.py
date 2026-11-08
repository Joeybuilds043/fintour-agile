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
