from src.research_register import (
    DISCOVERY_LEADS,
    EVENT_RECORDS,
    IMAGE_CANDIDATES,
    RESEARCH_DESTINATIONS,
)


def test_research_register_preserves_all_intake_counts():
    assert len(RESEARCH_DESTINATIONS) == 34
    assert len(EVENT_RECORDS) == 27
    assert len(IMAGE_CANDIDATES) >= 27


def test_destination_and_event_ids_are_unique():
    destination_ids = [record["id"] for record in RESEARCH_DESTINATIONS]
    event_ids = [record["id"] for record in EVENT_RECORDS]
    assert len(destination_ids) == len(set(destination_ids))
    assert len(event_ids) == len(set(event_ids))


def test_every_research_record_has_core_display_fields():
    for record in RESEARCH_DESTINATIONS:
        assert record["name"]
        assert record["region"]
        assert record["summary"]
        assert record["source"].startswith("https://")
    for record in EVENT_RECORDS:
        assert record["name"]
        assert record["region"]
        assert record["location"]
        assert record["date"]
        assert record["date_status"]


def test_discovery_leads_are_retained_by_region():
    assert {"Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan",
            "Gilgit-Baltistan", "Azad Jammu & Kashmir",
            "Islamabad Capital Territory"} <= set(DISCOVERY_LEADS)
    assert sum(len(items) for items in DISCOVERY_LEADS.values()) >= 30
