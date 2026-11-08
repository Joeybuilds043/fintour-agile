"""Transparent first-pass accommodation feasibility calculations."""
def accommodation_metrics(rooms:int,adr_pkr:float,occupancy_pct:float,
    annual_operating_cost_pkr:float,initial_investment_pkr:float,local_procurement_pct:float)->dict:
    if rooms<=0 or min(adr_pkr,annual_operating_cost_pkr,initial_investment_pkr)<0:
        raise ValueError("Rooms must be positive and financial inputs cannot be negative.")
    if not 0<=occupancy_pct<=100 or not 0<=local_procurement_pct<=100:
        raise ValueError("Percentages must be between 0 and 100.")
    available=rooms*365
    sold=available*occupancy_pct/100
    revenue=sold*adr_pkr
    surplus=revenue-annual_operating_cost_pkr
    breakeven=annual_operating_cost_pkr/(available*adr_pkr)*100 if adr_pkr else None
    payback=initial_investment_pkr/surplus if surplus>0 else None
    return {"available_room_nights":float(available),"sold_room_nights":float(sold),
      "room_revenue_pkr":float(revenue),"ebitda_proxy_pkr":float(surplus),
      "break_even_occupancy_pct":float(breakeven) if breakeven is not None else None,
      "simple_payback_years":float(payback) if payback is not None else None,
      "local_procurement_proxy_pkr":float(revenue*local_procurement_pct/100)}
