from __future__ import annotations
import streamlit as st
from src.ui import apply_intelligence_theme
from src.investment import accommodation_metrics
st.set_page_config(page_title="Investment Studio | Horizon",page_icon=None,layout="wide")
apply_intelligence_theme()
st.title("Tourism investment studio")
st.write("Test an accommodation concept using your own assumptions. This is an early feasibility calculator, not a valuation, lender model or investment recommendation.")
st.warning("Starting inputs are illustrative placeholders. Replace them with verified land, construction, payroll, utilities, tax, financing and market data.")
a,b,c=st.columns(3)
with a:
    rooms=st.number_input("Rooms",min_value=1,max_value=500,value=20)
    adr=st.number_input("Average daily room rate (PKR)",min_value=500,max_value=1000000,value=12000,step=500)
with b:
    occupancy=st.slider("Average annual occupancy (%)",0,100,40)
    costs=st.number_input("Annual operating costs (PKR)",min_value=0,max_value=1000000000,value=35000000,step=500000)
with c:
    capex=st.number_input("Initial investment (PKR)",min_value=0,max_value=5000000000,value=80000000,step=1000000)
    local_share=st.slider("Local procurement share (%)",0,100,45)
if st.button("Calculate scenario",type="primary"):
    try:
        r=accommodation_metrics(int(rooms),float(adr),float(occupancy),float(costs),float(capex),float(local_share))
        x,y,z=st.columns(3)
        x.metric("Annual room revenue",f'PKR {r["room_revenue_pkr"]:,.0f}')
        y.metric("Operating surplus proxy",f'PKR {r["ebitda_proxy_pkr"]:,.0f}')
        z.metric("Break-even occupancy","Not calculable" if r["break_even_occupancy_pct"] is None else f'{r["break_even_occupancy_pct"]:.1f}%')
        p,q=st.columns(2)
        p.metric("Simple payback","Not reached in this scenario" if r["simple_payback_years"] is None else f'{r["simple_payback_years"]:.1f} years')
        q.metric("Local procurement proxy",f'PKR {r["local_procurement_proxy_pkr"]:,.0f}')
        st.caption(f'Available room nights: {r["available_room_nights"]:,.0f} · Sold room nights: {r["sold_room_nights"]:,.0f}')
        st.info("Surplus proxy is room revenue less entered operating costs. It excludes financing, taxes, depreciation, replacement capex, non-room revenue and working capital. Payback is undiscounted.")
    except ValueError as exc: st.error(str(exc))
