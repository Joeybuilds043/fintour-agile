from __future__ import annotations

import json
import re
from typing import Any

MAX_AI_INPUT_CHARS = 1200
SAFETY_NOTICE = "This is not a booking, road, weather or safety service."

# Conservative refusal patterns for common prompt-injection and secret-exfiltration
# attempts. This is a guardrail, not a guarantee against every possible attack.
_PROMPT_INJECTION_PATTERNS = (
    r"\bignore\s+(?:all\s+)?(?:the\s+)?(?:previous|prior|above|earlier)\s+(?:system\s+)?(?:instructions?|rules?|prompts?)\b",
    r"\b(?:disregard|forget|override|bypass)\s+(?:all\s+)?(?:the\s+)?(?:previous|prior|above|system|developer|safety)?\s*(?:instructions?|rules?|prompts?)\b",
    r"\b(?:reveal|show|print|display|repeat|output|dump|expose|leak)\b.{0,80}\b(?:system|developer|hidden|initial)\s+(?:prompt|instructions?|message|rules?)\b",
    r"\b(?:show|print|reveal|dump|expose|leak)\b.{0,50}\b(?:api[_ -]?key|secret|token|password|credential|environment variable|\.env)\b",
    r"\b(?:api[_ -]?key|secret|token|password|credential|environment variable|\.env)\b.{0,50}\b(?:show|print|reveal|dump|expose|leak|output)\b",
    r"\bact\s+as\s+(?:the\s+)?(?:system|developer|admin|root)\b",
    r"\bnew\s+(?:system|developer)\s+instructions?\b",
    r"\b(?:developer|system)\s+mode\b",
    r"\b(?:jailbreak|dan\s+mode|do\s+anything\s+now)\b",
    r"\b(?:you are now|from now on)\b.{0,60}\b(?:ignore|override|disregard|obey|follow)\b",
    r"\bdo not follow\s+(?:your\s+)?(?:system|developer|safety)\b",
    r"\b(?:read|open|cat|print|curl|fetch)\b.{0,60}(?:\.env|environment variables|secrets file)\b",
    r"\b(?:export|dump|exfiltrate)\b.{0,60}\b(?:all\s+)?(?:secrets|credentials|environment variables|keys)\b",
)
_PROMPT_INJECTION_RE = tuple(re.compile(pattern, re.IGNORECASE | re.DOTALL) for pattern in _PROMPT_INJECTION_PATTERNS)


def contains_prompt_injection(value: str) -> bool:
    """Return True for common attempts to override model instructions or expose secrets."""
    candidate = value or ""
    return any(pattern.search(candidate) for pattern in _PROMPT_INJECTION_RE)


def validate_user_input(value: str) -> str:
    text = (value or "").strip()
    if not text:
        raise ValueError("Enter a question before submitting.")
    if len(text) > MAX_AI_INPUT_CHARS:
        raise ValueError(f"Keep your question under {MAX_AI_INPUT_CHARS} characters.")
    if contains_prompt_injection(text):
        raise ValueError(
            "This request contains instructions that attempt to override the assistant or expose protected information. "
            "Remove those instructions and ask a travel or tourism strategy question."
        )
    return text


def serialize_untrusted_user_text(value: str) -> str:
    """Encode user text as a JSON data value, never as prompt instructions."""
    clean = validate_user_input(value)
    return json.dumps({"untrusted_user_text": clean}, ensure_ascii=False)


def catalogue_answer(name: str, destination: dict[str, Any], question: str, mode: str) -> str:
    """Build a useful answer from existing catalogue fields only."""
    region = (
        destination.get("administrative_region")
        or destination.get("province")
        or destination.get("region")
        or "Pakistan"
    )
    overview = str(destination.get("overview") or "No destination overview is available.")
    experiences = destination.get("experiences") or []
    highlights = destination.get("highlights") or []
    season = str(destination.get("season") or "Seasonal conditions need to be checked locally.")
    lines = [
        f"## {name}",
        f"Region: {region}",
        "",
        overview,
        "",
        "### Catalogue experiences",
        *([f"- {item}" for item in experiences[:8]] or ["- No experience list is available in the catalogue."]),
        "",
        "### Highlights",
        *([f"- {item}" for item in highlights[:6]] or ["- No highlights are listed."]),
        "",
        f"### Planning note\n{season}",
    ]
    if mode == "strategy":
        lines.extend([
            "",
            "### Practical next steps",
            "- Confirm visitor demand with current official or local data.",
            "- Check local capacity, seasonality and environmental limits.",
            "- Speak with local businesses and community groups before planning investment.",
            "- Build a cost model only after collecting verified operating figures.",
        ])
    else:
        lines.extend([
            "",
            "### Suggested planning steps",
            "- Choose activities from the catalogue that match your interests.",
            "- Confirm transport, opening times, permits and accommodation directly.",
            "- Check current weather, road access and local safety advice before travel.",
        ])
    lines.extend(["", SAFETY_NOTICE])
    return "\n".join(lines)
