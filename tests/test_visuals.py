from src.catalog import DESTINATIONS
from src.visuals import catalogue_distribution_figures


def test_catalogue_visuals_are_built_from_real_catalogue_records():
    regional, thematic = catalogue_distribution_figures(DESTINATIONS)
    assert regional.data
    assert thematic.data
    assert sum(regional.data[0].x) == len(DESTINATIONS)
    assert sum(thematic.data[0].x) >= len(DESTINATIONS)
