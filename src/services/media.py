"""Fetch candidate openly licensed destination images from Wikimedia Commons."""
from __future__ import annotations
import os
import re
import requests
import streamlit as st

def _plain(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value or "").strip()

@st.cache_data(ttl=86400, show_spinner=False)
def get_commons_image(query: str) -> dict | None:
    if os.getenv("HORIZON_DISABLE_REMOTE_MEDIA") == "1":
        return None
    params={"action":"query","generator":"search","gsrsearch":f'filetype:bitmap "{query}"',
            "gsrnamespace":6,"gsrlimit":5,"prop":"imageinfo","iiprop":"url|extmetadata",
            "iiurlwidth":1400,"format":"json"}
    try:
        response=requests.get("https://commons.wikimedia.org/w/api.php",params=params,
          headers={"User-Agent":"HorizonTourismPrototype/0.1 (educational project)"},timeout=(5,12))
        response.raise_for_status()
        pages=response.json().get("query",{}).get("pages",{})
        for page in pages.values():
            info=(page.get("imageinfo") or [{}])[0]
            meta=info.get("extmetadata",{})
            licence=_plain(meta.get("LicenseShortName",{}).get("value",""))
            if not licence: continue
            artist=_plain(meta.get("Artist",{}).get("value","")) or "Attribution not supplied"
            return {"title":page.get("title","Wikimedia Commons image"),
              "thumb_url":info.get("thumburl") or info.get("url"),
              "page_url":info.get("descriptionurl","https://commons.wikimedia.org/"),
              "license":licence,"artist":artist}
    except (requests.RequestException,ValueError,TypeError,KeyError):
        return None
    return None
