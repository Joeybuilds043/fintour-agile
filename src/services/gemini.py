from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st


DEFAULT_MODEL = os.getenv("HORIZON_GEMINI_MODEL", "gemini-3.8-flash")
GROQ_MODEL = os.getenv("HORIZON_GROQ_MODEL", "llama-3.3-70b-versatile")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


class GeminiAPIError(RuntimeError):
    """A safe, user-facing AI provider error."""


GEMINI_SECRET_NAMES = (
    "GEMINI_API_KEY", "GOOGLE_API_KEY", "GOOGLE_GENAI_API_KEY",
    "GOOGLE_AI_API_KEY", "gemini_api_key", "google_api_key",
    "google_genai_api_key", "api_key",
)
GROQ_SECRET_NAMES = ("GROQ_API_KEY", "GROQ_KEY", "groq_api_key", "groq_key")


def _read_secret(names: tuple[str, ...]) -> str:
    """Read a provider key from environment variables or Streamlit Secrets."""
    candidates = [os.getenv(name, "") for name in names]
    try:
        secrets = st.secrets
        candidates.extend(secrets.get(name, "") for name in names)
        for section_name in ("google", "gemini", "genai", "groq"):
            section = secrets.get(section_name, {})
            if hasattr(section, "get"):
                candidates.extend(section.get(name, "") for name in names)
        accepted = {name.casefold() for name in names}
        for key, value in secrets.items():
            if str(key).casefold() in accepted:
                candidates.append(value)
    except Exception:
        pass
    return next((str(value).strip() for value in candidates if str(value or "").strip()), "")


def get_gemini_api_key() -> str:
    """Return the configured Gemini key, including the session-only fallback."""
    return _read_secret(GEMINI_SECRET_NAMES) or str(
        st.session_state.get("horizon_gemini_key", "")
    ).strip()


def get_groq_api_key() -> str:
    """Return the configured Groq key."""
    return _read_secret(GROQ_SECRET_NAMES)


def get_api_key() -> str:
    """Return Gemini as primary, otherwise Groq, preserving existing page callers."""
    return get_gemini_api_key() or get_groq_api_key()


def get_provider_name(api_key: str | None = None) -> str:
    """Identify the selected provider without exposing its key."""
    key = api_key or get_api_key()
    if key and key == get_groq_api_key():
        return "Groq"
    if key:
        return "Gemini"
    return "Not connected"


def _generate_groq_text(
    *,
    api_key: str,
    system_instruction: str,
    user_prompt: str,
    temperature: float,
    max_output_tokens: int,
    timeout: tuple[int, int],
) -> str:
    """Generate text with Groq's OpenAI-compatible chat-completions API."""
    payload: dict[str, Any] = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_output_tokens,
    }
    try:
        response = requests.post(
            GROQ_API_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=timeout,
        )
    except requests.Timeout as exc:
        raise GeminiAPIError("Groq request timed out. Please try again.") from exc
    except requests.RequestException as exc:
        raise GeminiAPIError("Could not connect to Groq. Check the app's network connection.") from exc

    if response.status_code == 429:
        raise GeminiAPIError("Groq free-tier rate limit reached. Check your Groq console limits and retry later.")
    if response.status_code in (400, 401, 403, 404):
        try:
            detail = response.json().get("error", {}).get("message", "")
        except (ValueError, AttributeError):
            detail = ""
        message = "Groq rejected the API key, model, or request configuration."
        if detail:
            message += f" Details: {detail[:300]}"
        raise GeminiAPIError(message)
    try:
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"]
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError, AttributeError) as exc:
        raise GeminiAPIError("Groq returned an empty or unreadable response. Please try again.") from exc
    if not isinstance(text, str) or not text.strip():
        raise GeminiAPIError("Groq returned no text. Please try again.")
    return text.strip()


def generate_text(
    *,
    api_key: str,
    system_instruction: str,
    user_prompt: str,
    temperature: float = 0.3,
    max_output_tokens: int = 1200,
    timeout: tuple[int, int] = (10, 75),
    google_search: bool = False,
) -> str:
    """Generate with Gemini, using Groq automatically when Gemini is quota-limited."""
    if not api_key:
        raise GeminiAPIError(
            "No AI API key found. Add GEMINI_API_KEY or GROQ_API_KEY in Streamlit Secrets."
        )

    groq_key = get_groq_api_key()
    using_groq = bool(groq_key and api_key == groq_key)

    if using_groq:
        if google_search:
            raise GeminiAPIError(
                "Google Search grounding is only available through Gemini. Turn off that option or configure a Gemini key."
            )
        return _generate_groq_text(
            api_key=api_key,
            system_instruction=system_instruction,
            user_prompt=user_prompt,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            timeout=timeout,
        )

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
    if google_search:
        payload["tools"] = [{"google_search": {}}]

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
        if groq_key and not google_search:
            try:
                return _generate_groq_text(
                    api_key=groq_key,
                    system_instruction=system_instruction,
                    user_prompt=user_prompt,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                    timeout=timeout,
                )
            except GeminiAPIError as exc:
                raise GeminiAPIError(
                    f"Gemini quota reached and Groq fallback was unavailable. {exc}"
                ) from exc
        raise GeminiAPIError(
            "Gemini free-tier rate limit reached. Add GROQ_API_KEY in Streamlit Secrets to enable automatic fallback, or wait for Gemini limits to reset."
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
        candidate = data["candidates"][0]
        parts = candidate["content"]["parts"]
        text = "\n".join(
            part["text"] for part in parts
            if isinstance(part, dict) and part.get("text")
        )
        if google_search:
            sources = []
            for chunk in candidate.get("groundingMetadata", {}).get("groundingChunks", []):
                source = chunk.get("web", {})
                uri, title = source.get("uri"), source.get("title")
                if uri and title and uri not in [item[1] for item in sources]:
                    sources.append((title, uri))
            if sources:
                text += "\n\n**Sources**\n" + "\n".join(
                    f"- [{title}]({uri})" for title, uri in sources[:8]
                )
    except (ValueError, KeyError, IndexError, TypeError, AttributeError) as exc:
        raise GeminiAPIError("Gemini returned an empty or unreadable response. Please try again.") from exc

    if not text.strip():
        raise GeminiAPIError("Gemini returned no text. The request may have been blocked by a safety filter.")
    return text.strip()
