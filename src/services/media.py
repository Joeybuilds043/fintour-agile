"""Reliable destination photography with attribution-preserving fallbacks.

Wikimedia Commons search is attempted first. If the API is unavailable, a small
curated set of verified Commons files keeps key destination pages visual.
Fallbacks are explicitly marked as illustrative when they are not the exact place.
"""
from __future__ import annotations

import os
import re
from html import unescape
from io import BytesIO
from urllib.parse import quote

import requests
import streamlit as st
from PIL import Image, ImageEnhance, ImageOps


STOP_WORDS = {"pakistan", "the", "and", "with", "from", "view", "photo", "image", "file"}

# Verified Wikimedia Commons file pages and author/licence metadata.
# The first group is destination-specific; the second is clearly labelled illustrative.
CURATED_FILES = [
    (("passu", "hunza", "attabad", "gilgit", "karimabad", "altit", "baltit"),
     "Passu Cones and the Hunza River.jpg", "Aly Ahmad1991", "CC BY-SA 4.0", False),
    (("skardu", "k2", "kachura", "satpara", "shigar", "khaplu"),
     "An autumnal view of Skardu's skyline.jpg", "Vasiq Eqbal", "CC BY-SA 4.0", False),
    (("deosai", "bara pani"),
     "Deosai Plains - Bara Pani.jpg", "Syedmuradali22", "CC BY-SA 4.0", False),
    (("lahore", "badshahi", "wazir khan", "shalimar", "minar e pakistan"),
     "Badshahi Mosque front picture.jpg", "Romero Maia", "CC BY-SA 4.0", False),
    (("taxila", "sirkap", "jaulian", "gandhara"),
     "Dharmarajika stupa,Taxila.jpg", "Sasha Isachenko", "CC BY-SA 3.0", False),
    (("neelum", "ajk", "azad kashmir", "sharda", "arang kel"),
     "Beautiful Neelum Valley Kashmir Pakistan.jpg", "Azmat akbar", "CC BY-SA 4.0", False),
    (("swat", "kalam", "mahodand", "malam jabba", "ush u forest"),
     "Scenery of Swat valley, Pakistan.jpg", "Uploader on Wikimedia Commons", "See file page", False),
    (("islamabad", "faisal mosque", "margalla"),
     "Faisal Mosque, Islamabad III.jpg", "Fassifarooq", "CC BY-SA 4.0", False),
    (("rohtas", "jhelum"),
     "Sohail Gate - Rohtas Fort by Hassan.jpg", "Hassantahir6009", "CC BY-SA 4.0", False),
    (("katas raj", "salt range", "chakwal"),
     "Katas Raj Temple 2.jpg", "Dowdoo14", "CC BY-SA 4.0", False),
    (("multan", "shah rukn", "bahauddin zakariya"),
     "Shrine of Shah Rukn-e-Alam Multan.jpg", "Mhtoori", "CC BY-SA 4.0", False),
    (("hingol", "kund malir", "gwadar", "makran", "balochistan coast"),
     "Kund Malir Beach, Hingol National Park, Balochistan.jpg", "Wikimedia Commons contributor", "See file page", False),
    (("faisalabad", "clock tower", "ghanta ghar"),
     "Clock Tower Faisalabad by Usman Nadeem.jpg", "Usman Nadeem", "See file page", False),
    (("fairy meadows", "nanga parbat"),
     "Fairy Meadows GB Pakistan.jpg", "Usmanbukhari3362", "CC BY-SA 4.0", False),
    (("naran", "kaghan", "saif ul muluk", "saiful muluk", "saif-ul-mulook"),
     "Lake Saif-Ul-Mulook.jpg", "Kamranki", "CC BY-SA 4.0", False),
    (("murree", "patriata", "nathia gali", "galiyat"),
     "Patriata Beautiful.jpg", "GrafixPlanner", "CC BY-SA 4.0", False),
    (("chitral", "garam chashma", "kalash"),
     "GaramChashma.jpg", "Fariskhan93", "CC BY-SA 4.0", False),
    (("karachi", "mazar e quaid", "quaid e azam mausoleum"),
     "Mazar-e-Quaid Karachi.jpg", "Furqanlw", "CC BY-SA 4.0", False),
    (("mohenjo", "mohenjo-daro", "moenjodaro"),
     "Mohenjodaro - view of the stupa mound.JPG", "Saqib Qayyum", "CC BY-SA 3.0", False),
    (("peshawar", "bala hisar", "balahisar"),
     "Bala Hisar-Peshawar.JPG", "Ammad Malik-101", "CC BY-SA 3.0", False),
    (("rawalakot", "banjosa"),
     "Banjosa Lake 2.jpg", "Khawaja Zarrar Waheed", "CC BY-SA 4.0", False),
    (("thatta", "makli", "shah jahan mosque"),
     "Gate ways from Courtyard - Shah Jahan Mosque.jpg", "Saba Qayoom", "CC BY-SA 4.0", False),
    # Regional visual references: never represented as photographs of the exact destination.
    (("mountain", "valley", "forest", "naran", "kaghan", "murree", "chitral", "kalash"),
     "Autumn color in Hunza Valley.jpg", "Ghazi Ghulamraza", "CC BY-SA 3.0", True),
]


def _plain(value: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", value or "")).strip()


def _tokens(value: str) -> set[str]:
    return {
        token for token in re.findall(r"[a-z0-9]+", (value or "").lower())
        if len(token) > 2 and token not in STOP_WORDS
    }


def _curated_fallback(query: str) -> dict | None:
    q = (query or "").casefold()
    selected = next((entry for entry in CURATED_FILES
                     if any(term in q for term in entry[0])), None)
    if not selected:
        return None
    _, filename, artist, licence, illustrative = selected
    encoded = quote(filename)
    page_name = quote(filename.replace(" ", "_"))
    return {
        "title": filename,
        "thumb_url": f"https://commons.wikimedia.org/wiki/Special:FilePath/{encoded}?width=1600",
        "page_url": f"https://commons.wikimedia.org/wiki/File:{page_name}",
        "license": licence,
        "license_url": ("https://creativecommons.org/licenses/by-sa/4.0/" if "4.0" in licence else "https://creativecommons.org/licenses/by-sa/3.0/" if "3.0" in licence else f"https://commons.wikimedia.org/wiki/File:{page_name}"),
        "artist": artist,
        "width": 1600,
        "height": 900,
        "illustrative": illustrative,
    }


@st.cache_data(ttl=86400, show_spinner=False)
def get_commons_image(query: str) -> dict | None:
    """Return relevant high-resolution Commons photography, with a curated fallback."""
    fallback = _curated_fallback(query)
    # Curated destination-specific assets are faster and more predictable than
    # a fresh search request; use live Commons search only for uncovered queries.
    if fallback:
        return fallback
    if os.getenv("HORIZON_DISABLE_REMOTE_MEDIA") == "1":
        return None

    terms = _tokens(query)
    params = {
        "action": "query", "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}", "gsrnamespace": 6,
        "gsrlimit": 40, "prop": "imageinfo",
        "iiprop": "url|extmetadata", "iiurlwidth": 1600, "format": "json",
    }
    headers = {
        "User-Agent": "HorizonTourism/1.0 (educational destination guide; contact via GitHub repository)",
        "Accept": "application/json",
    }
    try:
        response = requests.get(
            "https://commons.wikimedia.org/w/api.php", params=params,
            headers=headers, timeout=(4, 9),
        )
        response.raise_for_status()
        pages = response.json().get("query", {}).get("pages", {})
    except (requests.RequestException, ValueError, TypeError):
        return fallback

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
        overlap = len(terms & _tokens(title))
        if overlap == 0:
            continue
        score = overlap * 10 + (2 if 1.25 <= ratio <= 1.9 else 0) + (1 if width >= 1800 else 0)
        if any(word in title.lower() for word in ("map", "logo", "flag", "diagram", "coat of arms")):
            score -= 30
        candidates.append((score, {
            "title": title, "thumb_url": thumb_url, "page_url": description_url,
            "license": licence, "license_url": licence_url, "artist": artist,
            "width": width, "height": height, "illustrative": False,
        }))

    if not candidates:
        return fallback
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


@st.cache_data(ttl=86400, show_spinner=False)
def get_display_image(image_url: str) -> bytes | None:
    """Apply restrained colour, contrast and sharpness correction for display."""
    if not image_url or os.getenv("HORIZON_DISABLE_REMOTE_MEDIA") == "1":
        return None
    try:
        response = requests.get(
            image_url, headers={"User-Agent": "HorizonTourism/1.0"},
            timeout=(4, 9),
        )
        response.raise_for_status()
        image = ImageOps.exif_transpose(Image.open(BytesIO(response.content))).convert("RGB")
        image.thumbnail((1800, 1200), Image.Resampling.LANCZOS)
        image = ImageEnhance.Color(image).enhance(1.07)
        image = ImageEnhance.Contrast(image).enhance(1.045)
        image = ImageEnhance.Brightness(image).enhance(1.01)
        image = ImageEnhance.Sharpness(image).enhance(1.06)
        output = BytesIO()
        image.save(output, format="JPEG", quality=90, optimize=True, progressive=True)
        return output.getvalue()
    except (requests.RequestException, OSError, ValueError):
        return None
