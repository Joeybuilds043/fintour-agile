from src.catalog import DESTINATIONS, EXPERIENCE_CATEGORIES

def test_destination_catalog_has_ten_pilot_clusters():
    assert len(DESTINATIONS) == 10

def test_destination_coordinates_are_valid():
    for destination in DESTINATIONS.values():
        assert -90 <= destination["lat"] <= 90
        assert -180 <= destination["lon"] <= 180

def test_experience_taxonomy_is_unique():
    names = [item["name"] for item in EXPERIENCE_CATEGORIES]
    assert len(names) == len(set(names))
    assert len(names) >= 10

def test_each_destination_has_experiences_and_image_query():
    for destination in DESTINATIONS.values():
        assert destination["experiences"]
        assert destination["image_query"]
