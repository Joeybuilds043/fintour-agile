from __future__ import annotations

from typing import Any

MAX_AI_INPUT_CHARS = 1200
SAFETY_NOTICE = "This is not a booking, road, weather or safety service."


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


def validate_user_input(value: str) -> str:
    text = (value or "").strip()
    if not text:
        raise ValueError("Enter a question before submitting.")
    if len(text) > MAX_AI_INPUT_CHARS:
        raise ValueError(f"Keep your question under {MAX_AI_INPUT_CHARS} characters.")
    return text
