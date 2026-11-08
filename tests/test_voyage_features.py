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
