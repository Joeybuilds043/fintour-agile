import pytest
from src.scenarios import project_destination

def test_scenario_base_year_equals_input():
    df=project_destination(100000,15000,2,4,50,40,5)
    assert int(df.iloc[0]["Baseline visitors"])==100000
    assert int(df.iloc[0]["Strategy visitors"])==100000

def test_strategy_scenario_exceeds_baseline_when_uplift_positive():
    df=project_destination(100000,15000,2,4,100,40,5)
    assert df.iloc[-1]["Strategy visitors"]>df.iloc[-1]["Baseline visitors"]

def test_invalid_horizon_rejected():
    with pytest.raises(ValueError):
        project_destination(100000,15000,2,4,50,40,11)
