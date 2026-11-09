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
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


STOP_WORDS = {"pakistan", "the", "and", "with", "from", "view", "photo", "image", "file"}

# Verified Wikimedia Commons file pages and author/licence metadata.
# The first group is destination-specific; the second is clearly labelled illustrative.
CURATED_FILES = [
    (("k2", "concordia", "baltoro", "k2 base camp"),
     "K2 from Concordia.png", "Arsalan Majid", "CC BY-SA 4.0", False),
    (("kumrat", "jahaz banda", "katora lake", "upper dir"),
     "Kumrat valley upper dir, kyberpakhtunkhwa, pakistan.jpg", "Shah faisal zeb", "CC BY-SA 4.0", False),
    (("passu", "hunza", "attabad", "karimabad", "altit", "baltit"),
     "Passu Cones and the Hunza River.jpg", "Aly Ahmad1991", "CC BY-SA 4.0", False),
    (("skardu",),
     "An autumnal view of Skardu's skyline.jpg", "Vasiq Eqbal", "CC BY-SA 4.0", False),
    (("deosai", "bara pani"),
     "Deosai Plains - Bara Pani.jpg", "Syedmuradali22", "CC BY-SA 4.0", False),
    (("lahore", "badshahi", "wazir khan", "shalimar", "minar e pakistan"),
     "Badshahi Mosque front picture.jpg", "Romero Maia", "CC BY-SA 4.0", False),
    (("taxila", "sirkap", "jaulian", "gandhara"),
     "Dharmarajika stupa,Taxila.jpg", "Sasha Isachenko", "CC BY-SA 3.0", False),
    (("neelum", "ajk", "azad kashmir", "sharda", "arang kel"),
     "Beautiful Neelum Valley Kashmir Pakistan.jpg", "Azmat akbar", "CC BY-SA 4.0", False),
    (("swat", "kalam", "mahodand", "malam jabba", "ushu forest"),
     "Swat Valley , Pakistan.jpg", "Dr Ehsan Ullah", "CC BY-SA 4.0", True),
    (("islamabad", "faisal mosque", "margalla"),
     "Faisal Mosque, Islamabad III.jpg", "Fassifarooq", "CC BY-SA 4.0", False),
    (("rohtas", "jhelum"),
     "Sohail Gate - Rohtas Fort by Hassan.jpg", "Hassantahir6009", "CC BY-SA 4.0", False),
    (("katas raj", "chakwal"),
     "Katas Raj Temple Pakistan.jpg", "Asham Shahzad", "CC BY-SA 4.0", False),
    (("nankana", "janam asthan", "sikh pilgrimage", "gurdwara"),
     "Gurdwara Nankana Sahib Janam Asthan.jpg", "Harvinder Chandigarh", "CC BY 4.0", False),
    (("harappa", "indus valley archaeology"),
     "Archaeological site of Harappa.jpg", "M.sohailtariq", "CC BY-SA 3.0", False),
    (("salt range", "khewra"),
     "Katas Raj Temple 2.jpg", "Dowdoo14", "CC BY-SA 4.0", True),
    (("multan", "shah rukn", "bahauddin zakariya"),
     "Shrine of Shah Rukn-e-Alam Multan.jpg", "Mhtoori", "CC BY-SA 4.0", False),
    (("hingol", "kund malir"),
     "Kund Malir Beach, Hingol National Park, Balochistan.jpg", "Furqanlw", "CC BY-SA 4.0", False),
    (("gwadar", "makran", "balochistan coast", "pasni", "ormara"),
     "Kund Malir Beach, Hingol National Park, Balochistan.jpg", "Furqanlw", "CC BY-SA 4.0", True),
    (("faisalabad", "clock tower", "ghanta ghar"),
     "Clock Tower Faisalabad by Usman Nadeem.jpg", "Usman Nadeem", "See file page", False),
    (("fairy meadows", "nanga parbat"),
     "Fairy Meadows GB Pakistan.jpg", "Usmanbukhari3362", "CC BY-SA 4.0", False),
    (("naran", "kaghan", "saif ul muluk", "saiful muluk", "saif-ul-mulook"),
     "Lake Saif-Ul-Mulook.jpg", "Kamranki", "CC BY-SA 4.0", False),
    (("murree", "patriata", "nathia gali", "galiyat"),
     "Patriata Beautiful.jpg", "GrafixPlanner", "CC BY-SA 4.0", False),
    (("chitral", "garam chashma", "kalash"),
     "GaramChashma.jpg", "Fariskhan93", "CC BY-SA 4.0", True),
    (("makli", "thatta", "shah jahan mosque"),
     "Gate ways from Courtyard - Shah Jahan Mosque.jpg", "Saba Qayoom", "CC BY-SA 4.0", True),
    (("karachi", "mazar e quaid", "quaid e azam mausoleum"),
     "Mazar-e-Quaid Karachi.jpg", "Furqanlw", "CC BY-SA 4.0", False),
    (("mohenjo", "mohenjo-daro", "moenjodaro"),
     "Mohenjodaro - view of the stupa mound.JPG", "Saqib Qayyum", "CC BY-SA 3.0", False),
    (("peshawar", "bala hisar", "balahisar"),
     "Bala Hisar-Peshawar.JPG", "Ammad Malik-101", "CC BY-SA 3.0", False),
    (("rawalakot", "banjosa"),
     "Banjosa Lake 2.jpg", "Khawaja Zarrar Waheed", "CC BY-SA 4.0", False),
    # Regional visual references: never represented as photographs of the exact destination.
    (("mountain", "valley", "forest", "naran", "kaghan", "murree", "chitral", "kalash"),
     "Autumn color in Hunza Valley.jpg", "Ghazi Ghulamraza", "CC BY-SA 3.0", True),
]


# Destination-specific Pexels photography, with photographer and source-page credit.
PEXELS_FILES = [
    (("hunza", "passu", "attabad", "karimabad"), 35171324, "Asad Ali", "https://www.pexels.com/photo/scenic-autumn-view-of-hunza-valley-pakistan-35171324/"),
    (("skardu", "kachura", "shangrila", "shigar lake"), 19442074, "Wasif Mehmood", "https://www.pexels.com/photo/village-and-temple-near-lake-and-mountains-19442074/"),
    (("swat", "kalam", "malam jabba", "ushu"), 37385405, "Abdul Waheed", "https://www.pexels.com/photo/scenic-mountain-landscape-in-swat-valley-37385405/"),
    (("andrab lake", "andrab"), 38936576, "Amjad ali", "https://www.pexels.com/photo/scenic-andrab-lake-in-swat-valley-pakistan-38936576/"),
    (("badshahi", "lahore fort", "lahore"), 15839641, "Wasif Mehmood", "https://www.pexels.com/photo/side-wall-and-minaret-of-the-badshahi-mosque-in-lahore-punjab-pakistan-15839641/"),
]

USER_PROVIDED_RELIGIOUS_IMAGES = [
    (("nankana", "janam asthan", "sikh", "gurdwara", "kartarpur", "panja sahib"),
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6mSpVz_n-vku6oleiwZTj07bgxbfPopDvHUxpTllsJQ&s", "Sikh pilgrimage"),
    (("katas raj", "hindu", "temple", "chakwal"),
     "https://i.dawn.com/primary/2015/06/556c2870c7370.jpg", "Hinduism heritage · Katas Raj reference"),
    (("multan", "shah rukn", "sufi", "islamic", "muslim"),
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTjNKYbPE--eiBoUzeIcJaTlg8pvqgV8NGUOKxI0oc5tA&s=10", "Islamic and Sufi heritage"),
]


def _user_provided_religious_image(query: str) -> dict | None:
    q = (query or "").casefold()
    selected = next((entry for entry in USER_PROVIDED_RELIGIOUS_IMAGES if any(term in q for term in entry[0])), None)
    if not selected:
        return None
    _, url, label = selected
    return {
        "title": label, "thumb_url": url, "page_url": url,
        "license": "User-provided image · source and reuse rights not independently verified",
        "license_url": url, "artist": "User-provided", "width": 1600, "height": 900,
        "illustrative": False, "provider": "User-provided",
    }


def _curated_pexels_image(query: str) -> dict | None:
    q = (query or "").casefold()
    selected = next((entry for entry in PEXELS_FILES if any(term in q for term in entry[0])), None)
    if not selected:
        return None
    _, photo_id, artist, page_url = selected
    return {
        "title": f"Pexels destination photograph {photo_id}",
        "thumb_url": f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=1800",
        "page_url": page_url, "license": "Pexels License",
        "license_url": "https://www.pexels.com/license/", "artist": artist,
        "width": 1800, "height": 1100, "illustrative": False, "provider": "Pexels",
    }

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
        "thumb_url": f"https://commons.wikimedia.org/wiki/Special:FilePath/{encoded}?width=2000",
        "page_url": f"https://commons.wikimedia.org/wiki/File:{page_name}",
        "license": licence,
        "license_url": ("https://creativecommons.org/licenses/by-sa/4.0/" if "4.0" in licence else "https://creativecommons.org/licenses/by-sa/3.0/" if "3.0" in licence else f"https://commons.wikimedia.org/wiki/File:{page_name}"),
        "artist": artist,
        "width": 1600,
        "height": 900,
        "illustrative": illustrative,
    }


def get_commons_image(query: str) -> dict | None:
    """Return relevant photography without reusing another destination image in this session."""
    normalized_query = " ".join((query or "").casefold().split())
    assignments = st.session_state.setdefault("voyage_image_assignments", {})
    if normalized_query in assignments:
        return assignments[normalized_query]
    used_urls = {
        value.get("thumb_url") for value in assignments.values()
        if isinstance(value, dict) and value.get("thumb_url")
    }

    def claim(candidate):
        if not candidate or candidate.get("thumb_url") in used_urls:
            return None
        assignments[normalized_query] = candidate
        return candidate

    # Prefer curated, place-specific Commons files over legacy thumbnail URLs.
    selected = claim(_curated_pexels_image(query))
    if selected:
        return selected
    fallback = _curated_fallback(query)
    if fallback and fallback.get("thumb_url") in used_urls:
        fallback = None
    # Curated destination-specific assets are faster and more predictable than
    # a fresh search request; use live Commons search only for uncovered queries.
    if fallback:
        return claim(fallback)
    if os.getenv("HORIZON_DISABLE_REMOTE_MEDIA") == "1":
        return None

    terms = _tokens(query)
    params = {
        "action": "query", "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}", "gsrnamespace": 6,
        "gsrlimit": 40, "prop": "imageinfo",
        "iiprop": "url|extmetadata", "iiurlwidth": 2000, "format": "json",
    }
    headers = {
        "User-Agent": "VoyagePK/1.0 (educational destination guide; contact via GitHub repository)",
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
        if not (description_url and thumb_url and licence and width >= 1400 and height >= 800):
            continue
        if mime not in {"image/jpeg", "image/png", "image/webp"}:
            continue
        ratio = width / max(height, 1)
        if not 1.2 <= ratio <= 2.2:
            continue
        overlap = len(terms & _tokens(title))
        if overlap == 0 or thumb_url in used_urls:
            continue
        score = overlap * 10 + (2 if 1.4 <= ratio <= 1.9 else 0) + (1 if width >= 1800 else 0)
        if any(word in title.lower() for word in ("map", "logo", "flag", "diagram", "coat of arms")):
            score -= 30
        candidates.append((score, {
            "title": title, "thumb_url": thumb_url, "page_url": description_url,
            "license": licence, "license_url": licence_url, "artist": artist,
            "width": width, "height": height, "illustrative": False,
        }))

    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0], reverse=True)
    return claim(candidates[0][1])


@st.cache_data(ttl=86400, show_spinner=False)
def get_display_image(
    image_url: str,
    aspect_ratio: tuple[int, int] = (16, 9),
    focal_point: tuple[float, float] = (0.5, 0.5),
) -> bytes | None:
    """Crop consistently for editorial cards and apply restrained photo finishing.

    focal_point uses normalized (x, y) coordinates from 0 to 1 so a curator can
    position the crop around a subject instead of relying on arbitrary CSS.
    """
    if not image_url or os.getenv("HORIZON_DISABLE_REMOTE_MEDIA") == "1":
        return None
    try:
        response = requests.get(
            image_url, headers={"User-Agent": "HorizonTourism/1.0"},
            timeout=(4, 9),
        )
        response.raise_for_status()
        image = ImageOps.exif_transpose(Image.open(BytesIO(response.content))).convert("RGB")
        width, height = image.size
        ratio = max(0.2, aspect_ratio[0] / max(aspect_ratio[1], 1))
        if width / max(height, 1) > ratio:
            crop_width = int(height * ratio)
            left = int(width * min(max(focal_point[0], 0), 1) - crop_width / 2)
            left = min(max(left, 0), width - crop_width)
            image = image.crop((left, 0, left + crop_width, height))
        else:
            crop_height = int(width / ratio)
            top = int(height * min(max(focal_point[1], 0), 1) - crop_height / 2)
            top = min(max(top, 0), height - crop_height)
            image = image.crop((0, top, width, top + crop_height))
        image.thumbnail((1800, 1100), Image.Resampling.LANCZOS)
        image = ImageOps.autocontrast(image, cutoff=0.35)
        image = ImageEnhance.Color(image).enhance(1.045)
        image = ImageEnhance.Contrast(image).enhance(1.035)
        image = ImageEnhance.Brightness(image).enhance(1.005)
        image = image.filter(ImageFilter.UnsharpMask(radius=1.1, percent=105, threshold=3))
        output = BytesIO()
        image.save(output, format="JPEG", quality=92, optimize=True, progressive=True)
        return output.getvalue()
    except (requests.RequestException, OSError, ValueError):
        return None
