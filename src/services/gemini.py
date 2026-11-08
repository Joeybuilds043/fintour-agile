from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st


DEFAULT_MODEL = os.getenv("HORIZON_GEMINI_MODEL", "gemini-3.6-flash")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class GeminiAPIError(RuntimeError):
    """A safe, user-facing Gemini API error."""


def get_api_key() -> str:
    """Read the key from Streamlit Secrets, with an optional session-only fallback."""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    return str(key or st.session_state.get("horizon_gemini_key", "")).strip()


def generate_text(
    *,
    api_key: str,
    system_instruction: str,
    user_prompt: str,
    temperature: float = 0.3,
    max_output_tokens: int = 1200,
    timeout: tuple[int, int] = (10, 75),
) -> str:
    """Generate a text response using Google's Gemini Developer API."""
    if not api_key:
        raise GeminiAPIError("Gemini API key is missing. Add GEMINI_API_KEY in Streamlit Secrets.")

    model = DEFAULT_MODEL
    url = GEMINI_API_URL.format(model=model)
    payload: dict[str, Any] = {
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
        },
    }

    try:
        response = requests.post(
            url,
            headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
            json=payload,
            timeout=timeout,
        )
    except requests.Timeout as exc:
        raise GeminiAPIError("Gemini request timed out. Please try again.") from exc
    except requests.RequestException as exc:
        raise GeminiAPIError("Could not connect to Gemini. Check the app's network connection and try again.") from exc

    if response.status_code == 429:
        raise GeminiAPIError(
            "Gemini free-tier rate limit reached. Wait before retrying; check your active limits in Google AI Studio."
        )
    if response.status_code in (400, 401, 403, 404):
        try:
            detail = response.json().get("error", {}).get("message", "")
        except (ValueError, AttributeError):
            detail = ""
        if response.status_code in (401, 403):
            message = "Gemini rejected the API key or the API is not enabled for its Google project."
        elif response.status_code == 404:
            message = f"Gemini model '{model}' is unavailable for this key or API version."
        else:
            message = "Gemini could not process this request."
        if detail:
            message += f" Details: {detail[:400]}"
        raise GeminiAPIError(message)
    try:
        response.raise_for_status()
    except requests.RequestException as exc:
        raise GeminiAPIError(f"Gemini service returned HTTP {response.status_code}. Please try again later.") from exc

    try:
        data = response.json()
        parts = data["candidates"][0]["content"]["parts"]
        text = "\n".join(part["text"] for part in parts if isinstance(part, dict) and part.get("text"))
    except (ValueError, KeyError, IndexError, TypeError, AttributeError) as exc:
        raise GeminiAPIError("Gemini returned an empty or unreadable response. Please try again.") from exc

    if not text.strip():
        raise GeminiAPIError("Gemini returned no text. The request may have been blocked by a safety filter.")
    return text.strip()
