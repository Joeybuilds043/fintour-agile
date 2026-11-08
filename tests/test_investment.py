import pytest
from src.investment import accommodation_metrics

def test_accommodation_metrics():
    result = accommodation_metrics(10,10000,50,10000000,20000000,40)
    assert result["available_room_nights"] == 3650
    assert result["sold_room_nights"] == 1825
    assert result["room_revenue_pkr"] == 18250000
    assert result["ebitda_proxy_pkr"] == 8250000
    assert result["local_procurement_proxy_pkr"] == 7300000

def test_invalid_occupancy_is_rejected():
    with pytest.raises(ValueError):
        accommodation_metrics(10,10000,110,10000000,20000000,40)
