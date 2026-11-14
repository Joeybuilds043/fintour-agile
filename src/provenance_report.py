from __future__ import annotations

import csv
from io import StringIO

from src.catalog import DESTINATIONS
from src.destination_gallery import DESTINATION_IMAGE_BATCHES
from src.research_register import EVENT_RECORDS, IMAGE_CANDIDATES, RESEARCH_DESTINATIONS


def review_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for name, record in DESTINATIONS.items():
        if not record.get("source_link"):
            rows.append({"type": "Destination", "record": name, "missing": "source_link"})
    for kind, records in (
        ("Research destination", RESEARCH_DESTINATIONS),
        ("Festival or event", EVENT_RECORDS),
        ("Photo candidate", IMAGE_CANDIDATES),
    ):
        for record in records:
            label = str(record.get("name") or record.get("subject") or record.get("id") or "Unnamed record")
            if not record.get("source_link"):
                rows.append({"type": kind, "record": label, "missing": "source_link"})
            if kind == "Photo candidate":
                missing = []
                if not record.get("creator"):
                    missing.append("creator")
                if not (record.get("licence") or record.get("license")):
                    missing.append("licence")
                if missing:
                    rows.append({"type": kind, "record": label, "missing": ", ".join(missing)})
    for batch, records in DESTINATION_IMAGE_BATCHES.items():
        for record in records:
            missing = []
            if not record.get("source_link"):
                missing.append("source_link")
            if not record.get("creator"):
                missing.append("creator")
            if not record.get("licence"):
                missing.append("licence")
            if missing:
                rows.append({
                    "type": "Destination photo",
                    "record": f"{batch}: {record.get('destination', 'Unnamed photo')}",
                    "missing": ", ".join(missing),
                })
    return rows


def review_csv() -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["type", "record", "missing"])
    writer.writeheader()
    writer.writerows(review_rows())
    return output.getvalue()
