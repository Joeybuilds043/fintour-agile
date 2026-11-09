from src.catalog import DESTINATIONS, EXPERIENCE_CATEGORIES


def test_destination_catalog_has_broad_pakistan_coverage():
    assert len(DESTINATIONS) >= 30
    assert "Multan" in DESTINATIONS
    assert "Faisalabad" in DESTINATIONS
    assert "Neelum Valley" in DESTINATIONS
    assert "Mohenjo-daro" in DESTINATIONS
    assert "Hingol & Gwadar Coast" in DESTINATIONS


def test_destination_coordinates_are_valid():
    for name, destination in DESTINATIONS.items():
        assert -90 <= destination["lat"] <= 90, name
        assert -180 <= destination["lon"] <= 180, name


def test_experience_taxonomy_is_unique_and_complete():
    names = [item["name"] for item in EXPERIENCE_CATEGORIES]
    assert len(names) == len(set(names))
    assert len(names) >= 10
    assert all(item.get("symbol") and not item.get("icon") for item in EXPERIENCE_CATEGORIES)


def test_each_destination_has_complete_editorial_fields():
    required = {
        "region", "lat", "lon", "tagline", "overview", "culture",
        "experiences", "highlights", "season", "access", "responsible",
        "image_query",
    }
    for name, destination in DESTINATIONS.items():
        assert required.issubset(destination), name
        assert destination["experiences"], name
        assert destination["highlights"], name
        assert destination["image_query"], name
        assert set(destination["experiences"]).issubset(
            {item["name"] for item in EXPERIENCE_CATEGORIES}
        ), name


def test_k2_concordia_featured_destination_exists():
    destination = DESTINATIONS.get("K2 & Concordia Expedition")
    assert destination is not None
    assert destination["region"] == "Gilgit-Baltistan"
    assert "Baltoro Glacier trekking corridor" in destination["highlights"]


def test_kumrat_valley_is_catalogued_under_khyber_pakhtunkhwa():
    destination = DESTINATIONS["Kumrat Valley"]
    assert destination["region"] == "Khyber Pakhtunkhwa"
    assert destination["province"] == "Khyber Pakhtunkhwa"
    assert "Katora Lake trek (high-altitude route requiring local guidance)" in destination["highlights"]


def test_province_taxonomy_covers_all_destinations():
    from src.catalog import PROVINCE_ORDER

    assert "Khyber Pakhtunkhwa" in PROVINCE_ORDER
    assert all(destination.get("province") in PROVINCE_ORDER for destination in DESTINATIONS.values())
