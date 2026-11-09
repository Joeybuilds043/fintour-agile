from src.catalog import DESTINATIONS
from src.visuals import catalogue_distribution_figures


def test_catalogue_visuals_are_line_charts_built_from_real_records():
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
    assert len(regional.data[0].x) == len(set(item.get("province") or item.get("region") or "Unclassified" for item in DESTINATIONS.values()))
    assert len(thematic.data[0].x) > 0
