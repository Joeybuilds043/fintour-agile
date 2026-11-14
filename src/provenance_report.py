from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.catalog import DESTINATIONS
from src.destination_gallery import DESTINATION_IMAGE_BATCHES
from src.event_images import ATLAS_EVENT_IMAGES
from src.research_register import EVENT_RECORDS, IMAGE_CANDIDATES, RESEARCH_DESTINATIONS

_PLACEHOLDER = re.compile(
    r"not provided|not confirmed|not independently verified|unverified|user-supplied|"
    r"source and reuse licence not independently|original image licence",
    re.IGNORECASE,
)


def _usable(value: Any) -> bool:
    text = str(value or "").strip()
    return bool(text) and not _PLACEHOLDER.search(text)


def _https(value: Any) -> bool:
    return str(value or "").strip().lower().startswith("https://")


def _record_has_source(record: dict[str, Any]) -> bool:
    if _https(record.get("source_link")) or _https(record.get("source")) or _https(record.get("page")):
        return True
    sources = record.get("sources") or []
    if isinstance(sources, dict):
        sources = [sources]
    return any(_https(item.get("url")) for item in sources if isinstance(item, dict))


def _photo_has_full_details(image_url: Any, source_page: Any, creator: Any, licence: Any) -> bool:
    return _https(image_url) and _https(source_page) and _usable(creator) and _usable(licence)


def provenance_summary() -> dict[str, dict[str, int]]:
    """Count source-complete entries; these are references, not deduplicated image files."""
    manifest_path = Path(__file__).resolve().parents[1] / "assets" / "manifest.json"
    with manifest_path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)

    photos: list[tuple[Any, Any, Any, Any]] = []
    for records in DESTINATION_IMAGE_BATCHES.values():
        for record in records:
            photos.append((
                record.get("image_url"),
                record.get("source_link"),
                record.get("creator"),
                record.get("licence") or record.get("license"),
            ))
    for record in IMAGE_CANDIDATES:
        photos.append((
            record.get("image_url") or record.get("thumb_url") or record.get("page"),
            record.get("source_link") or record.get("page"),
            record.get("creator") or record.get("artist"),
            record.get("licence") or record.get("license"),
        ))
    for record in ATLAS_EVENT_IMAGES.values():
        photos.append((
            record.get("thumb_url"),
            record.get("page_url"),
            record.get("artist") or record.get("creator"),
            record.get("license") or record.get("licence"),
        ))
    for record in manifest.get("assets", {}).values():
        photos.append((
            record.get("url"),
            record.get("page_url") or record.get("source_link"),
            record.get("author") or record.get("creator"),
            record.get("license") or record.get("licence"),
        ))
    for record in manifest.get("experience_collections", []):
        photos.append((
            record.get("url"),
            record.get("page_url") or record.get("source_link"),
            record.get("author") or record.get("creator"),
            record.get("license") or record.get("licence"),
        ))

    full_photos = sum(_photo_has_full_details(*photo) for photo in photos)
    records = list(DESTINATIONS.values()) + RESEARCH_DESTINATIONS + EVENT_RECORDS
    sourced_records = sum(_record_has_source(record) for record in records)

    return {
        "photos": {
            "total": len(photos),
            "full_details": full_photos,
            "being_checked": len(photos) - full_photos,
        },
        "records": {
            "total": len(records),
            "full_details": sourced_records,
            "being_checked": len(records) - sourced_records,
        },
    }
