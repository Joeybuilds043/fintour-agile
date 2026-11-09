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
    assert {"Islamic & Sufi heritage", "Sikh pilgrimage", "Buddhist heritage", "Hinduism heritage"} <= categories
    assert "Nankana Sahib & Sikh Heritage" in DESTINATIONS
    assert "Swat Buddhist Heritage Circuit" in DESTINATIONS
    assert "Katas Raj Temples & Salt Range" in DESTINATIONS
    assert "Harappa & Indus Valley Archaeology" in DESTINATIONS
    assert "Hinduism heritage" not in DESTINATIONS["Harappa & Indus Valley Archaeology"]["experiences"]


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

def test_destination_catalog_covers_major_cities_and_k2_expedition():
    from src.catalog import DESTINATIONS
    expected = {
        "Islamabad & Margalla Hills", "Lahore", "Karachi & Makli–Thatta",
        "Peshawar", "Multan", "Faisalabad", "Hyderabad & Bhit Shah",
        "Sialkot", "Quetta & Hanna Lake", "Gilgit City & Karakoram Gateway",
        "K2 & Concordia Expedition", "Naran–Kaghan Valley", "Hunza Valley",
        "Skardu", "Swat Valley",
    }
    assert expected <= set(DESTINATIONS)
    assert "not a casual sightseeing stop" in DESTINATIONS["K2 & Concordia Expedition"]["overview"]


def test_curated_pexels_images_keep_photographer_credit():
    from src.services.media import _curated_pexels_image
    hunza = _curated_pexels_image("Hunza Valley Passu Cones Pakistan")
    swat = _curated_pexels_image("Swat Valley Kalam Pakistan")
    assert hunza and hunza["artist"] == "Asad Ali"
    assert "pexels.com/photo/" in hunza["page_url"]
    assert swat and "swat-valley" in swat["page_url"]


def test_homepage_featured_destinations_exist_in_catalog():
    from src.catalog import DESTINATIONS
    featured = ["Hunza Valley", "Skardu", "Naran–Kaghan Valley", "Lahore", "K2 & Concordia Expedition", "Swat Valley"]
    assert set(featured) <= set(DESTINATIONS)


def test_user_supplied_religious_images_are_mapped_to_their_requested_traditions():
    from src.services.media import _user_provided_religious_image
    sikh = _user_provided_religious_image("Nankana Sahib Janam Asthan Sikh pilgrimage")
    hindu = _user_provided_religious_image("Katas Raj Hindu heritage")
    islamic = _user_provided_religious_image("Shah Rukn Sufi heritage Multan")
    assert sikh and "S6mSpVz" in sikh["thumb_url"]
    assert hindu and "556c2870c7370.jpg" in hindu["thumb_url"]
    assert islamic and "TjNKYbPE" in islamic["thumb_url"]
    assert "not independently verified" in sikh["license"]
