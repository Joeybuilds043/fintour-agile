from src.itinerary import build_itinerary, FOOD_GUIDE
from src.finance import simulate_project


def test_itinerary_has_three_dayparts_and_local_food():
    plan = build_itinerary("Lahore", ["Lahore Fort", "Walled City"], 2, "Balanced")
    assert len(plan) == 2
    assert set(plan[0]["slots"]) == {"Morning", "Afternoon", "Evening"}
    assert "Halwa puri" in plan[0]["slots"]["Morning"]["food"]
    assert plan[0]["snack"]


def test_itinerary_fallback_food_exists():
    plan = build_itinerary("Unlisted destination", ["Market"], 1, "Relaxed")
    assert plan[0]["slots"]["Morning"]["food"] == FOOD_GUIDE["default"]["breakfast"]


def test_monte_carlo_is_reproducible_and_returns_percentiles():
    a = simulate_project(20, 12000, 40, 35000000, 80000000, simulations=500)
    b = simulate_project(20, 12000, 40, 35000000, 80000000, simulations=500)
    assert a == b
    assert a["npv_p10"] <= a["npv_p50"] <= a["npv_p90"]
    assert 0 <= a["positive_npv_probability"] <= 100


def test_relaxed_pace_limits_scheduled_highlights_to_one_per_day():
    plan = build_itinerary("Hunza Valley", ["One", "Two", "Three"], 1, "Relaxed")
    scheduled = [
        detail["activity"] for detail in plan[0]["slots"].values()
        if detail["activity"] in {"One", "Two", "Three"}
    ]
    assert scheduled == ["One"]


def test_pdf_escapes_ampersands_in_destination_and_interests():
    from src.itinerary import build_itinerary_pdf

    plan = build_itinerary("Islamabad & Margalla Hills", ["Faisal Mosque"], 1, "Balanced")
    pdf = build_itinerary_pdf(
        "Islamabad & Margalla Hills", plan, 2, 120000, ["Nature & wildlife"]
    )
    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000



def test_religious_tourism_is_separated_by_tradition():
    from src.catalog import DESTINATIONS, EXPERIENCE_CATEGORIES

    categories = {item["name"] for item in EXPERIENCE_CATEGORIES}
    assert {"Islamic & Sufi heritage", "Sikh pilgrimage", "Buddhist heritage", "Hindu heritage"} <= categories
    assert "Nankana Sahib & Sikh Heritage" in DESTINATIONS
    assert "Swat Buddhist Heritage Circuit" in DESTINATIONS
    assert "Katas Raj Temples & Salt Range" in DESTINATIONS
    assert "Harappa & Indus Valley Archaeology" in DESTINATIONS
    assert "Hindu heritage" not in DESTINATIONS["Harappa & Indus Valley Archaeology"]["experiences"]


def test_upper_kalam_destinations_include_desan_and_gabral():
    from src.catalog import DESTINATIONS

    assert "Desan Meadows & Upper Kalam" in DESTINATIONS
    assert "Utror & Gabral Valleys" in DESTINATIONS
    assert "Matiltan & Mahodand Lake" in DESTINATIONS
    assert DESTINATIONS["Desan Meadows & Upper Kalam"].get("sources")



def test_upper_swat_lake_destinations_are_individually_mapped():
    from src.catalog import DESTINATIONS

    assert "Andrab Lake & Anakar Valley" in DESTINATIONS
    assert "Izmis Lake & Utror Meadows" in DESTINATIONS
    assert "Spinkhor Lake & Upper Utror" in DESTINATIONS
    assert DESTINATIONS["Andrab Lake & Anakar Valley"]["sources"]
    assert DESTINATIONS["Izmis Lake & Utror Meadows"]["sources"]
