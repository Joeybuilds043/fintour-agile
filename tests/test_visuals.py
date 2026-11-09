from collections import Counter

from src.catalog import DESTINATIONS
from src.visuals import catalogue_distribution_figures


def test_catalogue_visuals_are_ranked_line_charts_built_from_real_records():
    regional, thematic = catalogue_distribution_figures(DESTINATIONS)
    assert regional.data
    assert thematic.data
    assert regional.data[0].type == "scatter"
    assert thematic.data[0].type == "scatter"
    assert "lines" in regional.data[0].mode
    assert "markers" in regional.data[0].mode
    assert "lines" in thematic.data[0].mode
    assert "markers" in thematic.data[0].mode
    assert sum(regional.data[0].y) == len(DESTINATIONS)
    assert sum(thematic.data[0].y) >= len(DESTINATIONS)

    expected_regions = Counter(
        item.get("administrative_region") or item.get("province") or item.get("region") or "Unclassified"
        for item in DESTINATIONS.values()
    )
    assert set(regional.data[0].x) == set(expected_regions)
    assert list(regional.data[0].y) == sorted(expected_regions.values(), reverse=True)
    assert len(thematic.data[0].x) > 0


def test_catalogue_visuals_can_switch_to_bar_charts():
    regional, thematic = catalogue_distribution_figures(DESTINATIONS, "Bars")
    assert regional.data[0].type == "bar"
    assert thematic.data[0].type == "bar"
