from __future__ import annotations
import pandas as pd
import streamlit as st
from src.ui import apply_visitor_theme
from src.catalog import DESTINATIONS

st.set_page_config(page_title="Trip Planner | Horizon",page_icon=None,layout="wide")
apply_visitor_theme()
st.title("Plan your journey")
st.write("Build a starting itinerary around your interests, time and own budget. This is a planning aid, not a booking confirmation.")
a,b,c=st.columns(3)
with a: destination=st.selectbox("Destination",list(DESTINATIONS))
with b: days=st.slider("Trip duration",1,10,4)
with c: travellers=st.number_input("Travellers",1,20,2)
d=DESTINATIONS[destination]
interests=st.multiselect("Your interests",d["experiences"],default=d["experiences"][:2])
budget=st.number_input("Your total trip budget (PKR)",min_value=1000,max_value=10000000,value=100000,step=5000)
st.caption("Budget is supplied by you. Horizon does not yet have verified live hotel, transport or restaurant prices.")
if st.button("Create my draft itinerary",type="primary"):
    highlights=d["highlights"]
    rows=[]
    for day in range(1,days+1):
        rows.append({"Day":day,"Morning":highlights[(day-1)%len(highlights)],"Afternoon":highlights[day%len(highlights)],"Evening":"Local food, rest and flexible time"})
    st.session_state["draft_itinerary"]=rows
    st.session_state["draft_trip_meta"]=(destination,travellers,budget)
if "draft_itinerary" in st.session_state:
    meta=st.session_state["draft_trip_meta"]
    st.subheader(f"Your {len(st.session_state['draft_itinerary'])}-day draft for {meta[0]}")
    st.dataframe(pd.DataFrame(st.session_state["draft_itinerary"]),use_container_width=True,hide_index=True)
    st.metric("Budget per traveller",f"PKR {meta[2]/meta[1]:,.0f}")
    st.caption("This itinerary uses curated highlights, not verified travel times or live availability. Confirm routes, opening hours and activity suitability.")
st.markdown("### Planning checks")
for item in ["Confirm route and weather close to departure","Verify accommodation and transport directly with providers","Check permits, local advisories and seasonal access","Plan emergency contacts and travel insurance","Respect local customs, protected areas and community guidance"]: st.markdown(f"- {item}")
