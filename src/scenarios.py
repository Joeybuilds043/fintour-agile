"""Transparent visitor and revenue scenario calculations."""
import pandas as pd

def project_destination(visitors:int,spend_pkr:float,baseline_growth_pct:float,
    strategy_uplift_pct:float,execution_pct:int,local_retention_pct:int,years:int)->pd.DataFrame:
    if visitors<0 or spend_pkr<0: raise ValueError("Visitors and spending cannot be negative.")
    if not 0<=execution_pct<=100 or not 0<=local_retention_pct<=100: raise ValueError("Percentages must be between 0 and 100.")
    if years<1 or years>10: raise ValueError("Projection horizon must be between 1 and 10 years.")
    rows=[]
    for year in range(years+1):
        base=visitors*((1+baseline_growth_pct/100)**year)
        strategic=visitors*((1+(baseline_growth_pct+strategy_uplift_pct*execution_pct/100)/100)**year)
        base_spend=base*spend_pkr
        strategy_spend=strategic*spend_pkr
        rows.append({"Year":year,"Baseline visitors":round(base),"Strategy visitors":round(strategic),
          "Baseline visitor spend (PKR)":base_spend,"Strategy visitor spend (PKR)":strategy_spend,
          "Illustrative local value retained (PKR)":strategy_spend*local_retention_pct/100})
    return pd.DataFrame(rows)
