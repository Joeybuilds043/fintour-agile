from __future__ import annotations

import streamlit as st
from src.catalog import DESTINATIONS
from src.itinerary import build_itinerary, build_itinerary_pdf
from src.services.weather import get_weather
from src.ui import apply_visitor_theme

st.set_page_config(page_title="Plan a Journey | VoyagePK", layout="wide")
apply_visitor_theme()
st.markdown('<div class="kicker">A JOURNEY, SHAPED AROUND YOU</div>', unsafe_allow_html=True)
st.title("Build your Pakistan itinerary")
st.markdown("Plan morning, afternoon and evening experiences, with regional food suggestions and a print-ready PDF.")
names = list(DESTINATIONS)
if st.session_state.get("selected_destination") not in DESTINATIONS:
    st.session_state["selected_destination"] = names[0]

with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    destination = c1.selectbox("Destination", names, key="selected_destination")
    days = c2.slider("Duration", 1, 14, 4)
    travellers = c3.number_input("Travellers", 1, 20, 2)
    interests = st.multiselect("Interests", DESTINATIONS[destination]["experiences"],
                               default=DESTINATIONS[destination]["experiences"][:2])
    pace = st.radio("Travel pace", ["Relaxed", "Balanced", "Full days"], horizontal=True)
    budget = st.number_input("Group planning budget (PKR)", 1000, 100000000, 100000, 5000)

weather_unit = st.segmented_control("Weather units", ["°C", "°F"], default="°C")
weather = get_weather(DESTINATIONS[destination]["lat"], DESTINATIONS[destination]["lon"],
                      "fahrenheit" if weather_unit == "°F" else "celsius")
if weather and weather.get("current"):
    current = weather["current"]
    st.caption(f"Current model forecast: {current.get('temperature_2m', '—')}{weather_unit} · "
               f"Feels like {current.get('apparent_temperature', '—')}{weather_unit} · "
               f"Wind {current.get('wind_speed_10m', '—')} km/h · "
               f"Forecast updated {weather.get('current', {}).get('time', 'time not supplied')}")
else:
    st.caption("Live forecast unavailable. Check a trusted local forecast close to departure.")

month = st.selectbox("Expected travel season", ["Spring (Mar–May)", "Summer (Jun–Aug)",
                       "Autumn (Sep–Nov)", "Winter (Dec–Feb)"])
packing = {
    "Spring (Mar–May)": ["Light layers", "Comfortable walking shoes", "Sun protection", "Light rain shell"],
    "Summer (Jun–Aug)": ["Breathable clothing", "Sun hat and SPF", "Reusable water bottle", "Light layer for evenings"],
    "Autumn (Sep–Nov)": ["Layered clothing", "Closed walking shoes", "Light insulated jacket", "Rain shell"],
    "Winter (Dec–Feb)": ["Insulated jacket", "Thermal base layers", "Warm socks and gloves", "Water-resistant footwear"],
}
if "Mountain" in DESTINATIONS[destination]["region"] or destination in ["Hunza Valley", "Skardu"]:
    packing[month] = packing[month] + ["Extra warm layer for altitude", "Check snow/road conditions and traction needs"]
with st.expander("Climate-adaptive packing notes", expanded=True):
    st.write(" · ".join(packing[month]))
    st.caption("Seasonal guidance is a checklist, not a live hazard assessment. Altitude and local microclimates can change conditions substantially.")

if st.button("Generate day-by-day itinerary", type="primary"):
    st.session_state["voyage_itinerary"] = build_itinerary(
        destination, DESTINATIONS[destination]["highlights"], days, pace
    )
    st.session_state["voyage_trip_meta"] = {
        "destination": destination, "travellers": int(travellers),
        "budget": float(budget), "interests": interests,
    }

if st.session_state.get("voyage_itinerary") and st.session_state.get("voyage_trip_meta", {}).get("destination") == destination:
    itinerary = st.session_state["voyage_itinerary"]
    meta = st.session_state["voyage_trip_meta"]
    st.markdown("### Your journey")
    m1, m2, m3 = st.columns(3)
    m1.metric("Duration", f"{len(itinerary)} days")
    m2.metric("Travellers", meta["travellers"])
    m3.metric("Budget per traveller", f"PKR {meta['budget'] / meta['travellers']:,.0f}")
    for day in itinerary:
        with st.container(border=True):
            st.subheader(f"Day {day['day']:02d} · {destination}")
            cols = st.columns(3)
            for col, (slot, detail) in zip(cols, day["slots"].items()):
                with col:
                    st.markdown(f"**{slot}**")
                    st.caption(detail["time"])
                    st.write(detail["activity"])
                    st.markdown("**Local food idea**")
                    st.write(detail["food"])
            st.caption(f"Snack idea: {day['snack']} · Sequence is indicative; not a route or reservation.")
    pdf = build_itinerary_pdf(destination, itinerary, meta["travellers"], meta["budget"], meta["interests"])
    st.download_button("Download print-ready PDF itinerary + QR codes", pdf,
                       file_name=f"voyagepk-{destination.lower().replace(' ', '-')}-itinerary.pdf",
                       mime="application/pdf", type="primary", use_container_width=True)

st.caption("Food suggestions are regional examples, not endorsements of specific vendors. Verify hygiene, opening times, prices, access and current travel conditions.")
