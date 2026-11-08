from __future__ import annotations

import pandas as pd
import streamlit as st

from src.catalog import DESTINATIONS
from src.ui import apply_visitor_theme

st.set_page_config(page_title="Plan a Journey | Horizon", page_icon=None, layout="wide")
apply_visitor_theme()

st.markdown('<div class="kicker">A JOURNEY, SHAPED AROUND YOU</div>', unsafe_allow_html=True)
st.title("Plan your journey")
st.markdown(
    '<div class="lede">Build a realistic starting brief around the destination, your pace and the experiences '
    'you care about. Horizon will organise a draft for discussion; it will not pretend to know live routes, '
    'prices or availability.</div>',
    unsafe_allow_html=True,
)

names = list(DESTINATIONS)
if st.session_state.get("selected_destination") not in DESTINATIONS:
    st.session_state["selected_destination"] = names[0]

with st.container(border=True):
    a, b, c = st.columns(3)
    with a:
        destination = st.selectbox("Where would you like to go?", names, key="selected_destination")
    with b:
        days = st.slider("How many days?", 1, 10, 4)
    with c:
        travellers = st.number_input("Travellers", min_value=1, max_value=20, value=2)

d = DESTINATIONS[destination]
interests = st.multiselect(
    "What matters on this trip?",
    d["experiences"],
    default=d["experiences"][:2],
)
pace = st.radio("Preferred pace", ["Relaxed", "Balanced", "Full days"], horizontal=True)
budget = st.number_input(
    "Total group budget (PKR)", min_value=1000, max_value=10000000, value=100000, step=5000
)
st.caption("Budget is your own planning input. No live accommodation, transport, restaurant or activity prices are available.")

if st.button("Create my draft plan", type="primary"):
    highlights = d["highlights"]
    daily_capacity = {"Relaxed": 1, "Balanced": 2, "Full days": 3}[pace]
    itinerary = []
    cursor = 0
    for day in range(1, days + 1):
        day_items = highlights[cursor:cursor + daily_capacity]
        cursor += len(day_items)
        if day == 1:
            title = "Arrival and orientation"
        elif day == days:
            title = "Final experiences and departure buffer"
        else:
            title = f"Explore {destination}"
        itinerary.append({
            "Day": day,
            "Focus": title,
            "Suggested places": " · ".join(day_items) if day_items else "Flexible time: ask a local guide about seasonal experiences",
            "Pace": pace,
        })
    st.session_state["draft_itinerary"] = itinerary
    st.session_state["draft_trip_meta"] = {
        "destination": destination,
        "travellers": int(travellers),
        "budget": float(budget),
        "interests": interests,
        "pace": pace,
    }

if "draft_itinerary" in st.session_state:
    meta = st.session_state["draft_trip_meta"]
    if meta["destination"] != destination:
        st.info("Your saved draft is for a different destination. Create a new plan to update it.")
    else:
        st.markdown("### Your journey at a glance")
        x, y, z = st.columns(3)
        x.metric("Duration", f'{len(st.session_state["draft_itinerary"])} days')
        y.metric("Travellers", meta["travellers"])
        z.metric("Budget per traveller", f'PKR {meta["budget"] / meta["travellers"]:,.0f}')
        st.write("**Your interests:** " + (", ".join(meta["interests"]) or "Open to suggestions"))
        for day in st.session_state["draft_itinerary"]:
            with st.container(border=True):
                day_left, day_right = st.columns([0.65, 1.35])
                day_left.markdown(f'**DAY {day["Day"]:02d}**')
                day_left.write(day["Focus"])
                day_right.write(day["Suggested places"])
                day_right.caption(f'Pace: {day["Pace"]} · Sequence is indicative, not a verified route')
        st.download_button(
            "Download draft itinerary",
            pd.DataFrame(st.session_state["draft_itinerary"]).to_csv(index=False),
            file_name=f'{destination.lower().replace(" ", "-")}-draft-itinerary.csv',
            mime="text/csv",
        )

st.markdown("### Before you set off")
checks = [
    "Confirm route conditions and weather close to departure",
    "Verify accommodation and transport directly with providers",
    "Check permits, local advisories and seasonal access",
    "Plan emergency contacts and suitable travel insurance",
    "Respect local customs, protected areas and community guidance",
]
for item in checks:
    st.markdown(f"- {item}")
