from __future__ import annotations

import os

import streamlit as st
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = os.getenv("VOYAGEPK_GROQ_MODEL", "openai/gpt-oss-20b")


class GroqAPIError(RuntimeError):
    """Safe, user-facing Groq API error."""


def get_api_key() -> str:
    """Read the Groq key from Streamlit Secrets or server environment only."""
    value = os.getenv("GROQ_API_KEY", "").strip()
    if value:
        return value
    try:
        return str(st.secrets.get("GROQ_API_KEY", "")).strip()
    except Exception:
        return ""


def generate_text(
    *,
    api_key: str,
    system_instruction: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_output_tokens: int = 1400,
    timeout: int = 180,
) -> str:
    """Generate a VoyagePK answer through Groq's OpenAI-compatible Responses API."""
    if not api_key:
        raise GroqAPIError(
            "Groq is not configured. The app owner must add GROQ_API_KEY in "
            "Streamlit Community Cloud → App settings → Secrets."
        )

    try:
        client = OpenAI(
            api_key=api_key,
            base_url=GROQ_BASE_URL,
            timeout=timeout,
            max_retries=1,
        )
        response = client.responses.create(
            model=DEFAULT_MODEL,
            instructions=system_instruction.strip(),
            input=user_prompt.strip(),
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )
    except APITimeoutError as exc:
        raise GroqAPIError("Groq took too long to respond. Please try again.") from exc
    except APIConnectionError as exc:
        raise GroqAPIError("Could not connect to Groq. Please try again.") from exc
    except AuthenticationError as exc:
        raise GroqAPIError(
            "Groq rejected the configured API key. Check GROQ_API_KEY in Streamlit Secrets."
        ) from exc
    except RateLimitError as exc:
        raise GroqAPIError(
            "The Groq rate or usage limit has been reached. Check your Groq Console limits."
        ) from exc
    except APIStatusError as exc:
        if exc.status_code == 404:
            raise GroqAPIError(
                f"The configured Groq model '{DEFAULT_MODEL}' is unavailable. "
                "Check the model ID and your Groq account access."
            ) from exc
        raise GroqAPIError(
            f"Groq returned an API error (HTTP {exc.status_code}). Please try again."
        ) from exc

    answer = (getattr(response, "output_text", None) or "").strip()
    if not answer:
        raise GroqAPIError("Groq returned no text. Please try again.")
    return answer
