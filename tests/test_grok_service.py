from types import SimpleNamespace

import pytest

from src.services import grok


def test_grok_uses_responses_api_and_parses_text(monkeypatch):
    captured = {}

    def fake_post(url, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return SimpleNamespace(
            status_code=200,
            raise_for_status=lambda: None,
            json=lambda: {"output": [{
                "type": "message",
                "content": [{"type": "output_text", "text": "A useful answer."}],
            }]},
        )

    monkeypatch.setattr(grok.requests, "post", fake_post)
    answer = grok.generate_text(
        api_key="test-xai-key",
        system_instruction="Be accurate.",
        user_prompt="Suggest a Kumrat itinerary.",
    )
    assert answer == "A useful answer."
    assert captured["url"] == "https://api.x.ai/v1/responses"
    assert captured["headers"]["Authorization"] == "Bearer test-xai-key"
    assert captured["json"]["model"] == "grok-4.7"
    assert captured["json"]["store"] is False


def test_grok_adds_web_search_tool_when_requested(monkeypatch):
    captured = {}

    def fake_post(url, **kwargs):
        captured.update(kwargs)
        return SimpleNamespace(
            status_code=200,
            raise_for_status=lambda: None,
            json=lambda: {"output": [{
                "type": "message",
                "content": [{"type": "output_text", "text": "Current answer."}],
            }]},
        )

    monkeypatch.setattr(grok.requests, "post", fake_post)
    grok.generate_text(
        api_key="test-xai-key",
        system_instruction="Be accurate.",
        user_prompt="Check current road access.",
        web_search=True,
    )
    assert captured["json"]["tools"] == [{"type": "web_search"}]
    assert "web_search_call.action.sources" in captured["json"]["include"]


def test_grok_rate_limit_has_safe_message(monkeypatch):
    monkeypatch.setattr(grok.requests, "post", lambda *args, **kwargs: SimpleNamespace(status_code=429))
    with pytest.raises(grok.GrokAPIError, match="usage limit"):
        grok.generate_text(api_key="test-xai-key", system_instruction="Be accurate.", user_prompt="Hello.")


def test_grok_requires_key():
    with pytest.raises(grok.GrokAPIError, match="not configured"):
        grok.generate_text(api_key="", system_instruction="Be accurate.", user_prompt="Hello.")
