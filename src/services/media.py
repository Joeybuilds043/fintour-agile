"""Retrieve and gently enhance openly licensed travel photography."""
from __future__ import annotations

import os
import re
from html import unescape
from io import BytesIO

import requests
import streamlit as st
from PIL import Image, ImageEnhance, ImageOps


STOP_WORDS = {"pakistan", "the", "and", "with", "from", "view", "photo", "image", "file"}


def _plain(value: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", value or "")).strip()


def _tokens(value: str) -> set[str]:
    return {
        token for token in re.findall(r"[a-z0-9]+", (value or "").lower())
        if len(token) > 2 and token not in STOP_WORDS
    }


@st.cache_data(ttl=86400, show_spinner=False)
def get_commons_image(query: str) -> dict | None:
    """Return a relevant, high-resolution landscape photo with file attribution."""
    if os.getenv("HORIZON_DISABLE_REMOTE_MEDIA") == "1":
        return None

    terms = _tokens(query)
    params = {
        "action": "query", "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}", "gsrnamespace": 6,
        "gsrlimit": 40, "prop": "imageinfo",
        "iiprop": "url|extmetadata", "iiurlwidth": 1600, "format": "json",
    }
    headers = {"User-Agent": "HorizonTourismPrototype/0.3 (educational project; image attribution enabled)"}
    try:
        response = requests.get(
            "https://commons.wikimedia.org/w/api.php", params=params,
            headers=headers, timeout=(5, 15),
        )
        response.raise_for_status()
        pages = response.json().get("query", {}).get("pages", {})
    except (requests.RequestException, ValueError, TypeError):
        return None

    candidates = []
    for page in pages.values():
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        title = page.get("title", "Wikimedia Commons image")
        description_url = info.get("descriptionurl")
        thumb_url = info.get("thumburl") or info.get("url")
        licence = _plain(meta.get("LicenseShortName", {}).get("value", ""))
        licence_url = meta.get("LicenseUrl", {}).get("value", "")
        artist = _plain(meta.get("Artist", {}).get("value", "")) or "Attribution not supplied"
        width, height = int(info.get("width", 0) or 0), int(info.get("height", 0) or 0)
        mime = info.get("mime", "")
        if not (description_url and thumb_url and licence and width >= 1000 and height >= 600):
            continue
        if mime not in {"image/jpeg", "image/png", "image/webp"}:
            continue
        ratio = width / max(height, 1)
        if not 1.08 <= ratio <= 2.6:
            continue
        title_tokens = _tokens(title)
        overlap = len(terms & title_tokens)
        if overlap == 0:
            continue
        score = overlap * 10
        score += 2 if 1.25 <= ratio <= 1.9 else 0
        score += 1 if width >= 1800 else 0
        if any(word in title.lower() for word in ("map", "logo", "flag", "diagram", "coat of arms", "location map")):
            score -= 30
        candidates.append((score, {
            "title": title, "thumb_url": thumb_url, "page_url": description_url,
            "license": licence, "license_url": licence_url, "artist": artist,
            "width": width, "height": height,
        }))

    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


@st.cache_data(ttl=86400, show_spinner=False)
def get_display_image(image_url: str) -> bytes | None:
    """Apply restrained colour, contrast and sharpness correction for display."""
    if not image_url or os.getenv("HORIZON_DISABLE_REMOTE_MEDIA") == "1":
        return None
    try:
        response = requests.get(
            image_url,
            headers={"User-Agent": "HorizonTourismPrototype/0.3"},
            timeout=(5, 15),
        )
        response.raise_for_status()
        image = ImageOps.exif_transpose(Image.open(BytesIO(response.content))).convert("RGB")
        image.thumbnail((1800, 1200), Image.Resampling.LANCZOS)
        image = ImageEnhance.Color(image).enhance(1.08)
        image = ImageEnhance.Contrast(image).enhance(1.055)
        image = ImageEnhance.Brightness(image).enhance(1.015)
        image = ImageEnhance.Sharpness(image).enhance(1.08)
        output = BytesIO()
        image.save(output, format="JPEG", quality=91, optimize=True, progressive=True)
        return output.getvalue()
    except (requests.RequestException, OSError, ValueError):
        return None
