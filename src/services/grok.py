from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st

XAI_API_URL = "https://api.x.ai/v1/responses"
DEFAULT_MODEL = os.getenv("VOYAGEPK_GROK_MODEL", "grok-4.7")


class GrokAPIError(RuntimeError):
    """Safe, user-facing xAI API error."""


def get_api_key() -> str:
    """Read the Grok key from Streamlit Secrets or the server environment only."""
    value = os.getenv("XAI_API_KEY", "").strip()
    if value:
        return value
    try:
        return str(st.secrets.get("XAI_API_KEY", "")).strip()
    except Exception:
        return ""


def generate_text(
    *,
    api_key: str,
    system_instruction: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_output_tokens: int = 1400,
    timeout: tuple[int, int] = (10, 180),
    web_search: bool = False,
) -> str:
    """Generate a VoyagePK response with xAI's recommended Responses API."""
    if not api_key:
        raise GrokAPIError(
            "Grok is not configured. Add XAI_API_KEY in Streamlit Community Cloud → App settings → Secrets."
        )

    prompt = (
        f"{system_instruction.strip()}\n\n"
        "Current user request and destination context:\n"
        f"{user_prompt.strip()}"
    )
    payload: dict[str, Any] = {
        "model": DEFAULT_MODEL,
        "input": [{"role": "user", "content": prompt}],
        "max_output_tokens": max_output_tokens,
        "reasoning": {"effort": "low"},
        "store": False,
    }
    if web_search:
        payload["tools"] = [{"type": "web_search"}]
        payload["include"] = ["web_search_call.action.sources"]

    try:
        response = requests.post(
            XAI_API_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=timeout,
        )
    except requests.Timeout as exc:
        raise GrokAPIError("Grok took too long to respond. Please try again.") from exc
    except requests.RequestException as exc:
        raise GrokAPIError("Could not connect to the Grok service. Please try again.") from exc

    if response.status_code == 429:
        raise GrokAPIError("The xAI API rate or usage limit has been reached. Check your xAI Console usage and billing.")
    if response.status_code in (401, 403):
        raise GrokAPIError("xAI rejected the configured API key. Check XAI_API_KEY in Streamlit Secrets.")
    if response.status_code == 404:
        raise GrokAPIError(f"The configured Grok model '{DEFAULT_MODEL}' is unavailable to this API key.")
    if response.status_code >= 500:
        raise GrokAPIError(f"The xAI service is temporarily unavailable (HTTP {response.status_code}). Try again later.")

    try:
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise GrokAPIError("Grok returned an unreadable response. Please try again.") from exc

    answer_parts: list[str] = []
    citations: list[tuple[str, str]] = []
    for item in data.get("output", []):
        if item.get("type") == "message":
            for part in item.get("content", []):
                if part.get("type") == "output_text" and part.get("text"):
                    answer_parts.append(part["text"])
                for annotation in part.get("annotations", []):
                    if annotation.get("type") == "url_citation":
                        url = annotation.get("url")
                        title = annotation.get("title") or url
                        if url and all(url != existing[1] for existing in citations):
                            citations.append((title, url))
        if item.get("type") == "web_search_call":
            for source in item.get("action", {}).get("sources", []):
                url = source.get("url")
                title = source.get("title") or url
                if url and all(url != existing[1] for existing in citations):
                    citations.append((title, url))

    answer = "\n\n".join(part.strip() for part in answer_parts if part.strip())
    if not answer:
        detail = data.get("error", {}).get("message") if isinstance(data.get("error"), dict) else ""
        if detail:
            raise GrokAPIError(f"Grok could not complete the request: {detail[:300]}")
        raise GrokAPIError("Grok returned no text. Please try again.")

    if citations:
        answer += "\n\n**Sources**\n" + "\n".join(f"- [{title}]({url})" for title, url in citations[:8])
    return answer.strip()
