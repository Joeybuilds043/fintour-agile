from __future__ import annotations

import pandas as pd
import streamlit as st

from src.catalog import DESTINATIONS
from src.services.media import get_commons_image, get_display_image
from src.services.weather import get_weather
from src.ui import apply_visitor_theme

st.set_page_config(page_title="Destination Field Guide | Horizon", page_icon=None, layout="wide")
apply_visitor_theme()

names = list(DESTINATIONS)
if st.session_state.get("selected_destination") not in DESTINATIONS:
    st.session_state["selected_destination"] = names[0]

st.markdown('<div class="kicker">HORIZON FIELD NOTES · PAKISTAN</div>', unsafe_allow_html=True)
st.title("Destination field guide")
name = st.selectbox("Choose a destination", names, key="selected_destination")
d = DESTINATIONS[name]

image = get_commons_image(d["image_query"])
left, right = st.columns([1.35, 1], gap="large", vertical_alignment="center")
with left:
    if image:
        display = get_display_image(image["thumb_url"], aspect_ratio=(16, 9), focal_point=(0.5, 0.5))
        st.image(display or image["thumb_url"], use_container_width=True)
        st.caption(
            f'{image["title"]} · {image["artist"]} · {image["license"]} · '
            f'[Licence]({image["license_url"]}) · [Original file]({image["page_url"]})' + (' · Illustrative regional reference' if image.get('illustrative') else '')
        )
    else:
        st.markdown(
            '<div style="min-height:300px;border-radius:18px;background:linear-gradient(135deg,#EEE9DF,#D9C8B7);display:flex;align-items:center;justify-content:center;padding:28px;color:#183B3B;font-family:Georgia,serif;font-size:28px">Discover the landscape. Respect the place.</div>',
            unsafe_allow_html=True,
        )
with right:
    st.markdown(f'<div class="kicker">{d["region"]} · DESTINATION COLLECTION</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="display-title" style="font-size:clamp(34px,4vw,54px)">{name}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="lede">{d["tagline"]}</div>', unsafe_allow_html=True)
    st.write(d["overview"])
    st.caption("Editorial destination cluster · Approximate location, not an attraction-level navigation point")

st.write("")
a, b = st.columns([1.1, 1], gap="large")
with a:
    with st.container(border=True):
        st.subheader("Culture and local identity")
        st.write(d["culture"])
        st.subheader("Experiences")
        for experience in d["experiences"]:
            st.markdown(f"- {experience}")
with b:
    with st.container(border=True):
        st.subheader("Places to explore")
        for highlight in d["highlights"]:
            st.markdown(f"- {highlight}")
        st.subheader("Season and access")
        st.write(d["season"])
        st.write(d["access"])

with st.container(border=True):
    st.subheader("Travel thoughtfully")
    st.write(d["responsible"])
    st.caption("Respect local customs, community consent, protected landscapes and current local guidance.")

st.subheader("Find the destination area")
st.map(pd.DataFrame([{"lat": d["lat"], "lon": d["lon"]}]), zoom=7)
st.caption("The marker is an approximate destination-cluster anchor. It is not a trailhead, attraction entrance or route instruction.")

st.subheader("Weather outlook")
with st.spinner("Checking the latest available forecast..."):
    weather = get_weather(d["lat"], d["lon"])
if weather:
    current = weather.get("current", {})
    x, y, z = st.columns(3)
    x.metric("Temperature", f'{current.get("temperature_2m", "—")} °C')
    y.metric("Feels like", f'{current.get("apparent_temperature", "—")} °C')
    z.metric("Wind", f'{current.get("wind_speed_10m", "—")} km/h')
    daily = weather.get("daily", {})
    if daily.get("time"):
        frame = pd.DataFrame({
            "Date": daily["time"],
            "High °C": daily.get("temperature_2m_max", []),
            "Low °C": daily.get("temperature_2m_min", []),
            "Rain chance %": daily.get("precipitation_probability_max", []),
        })
        st.dataframe(frame, use_container_width=True, hide_index=True)
    st.caption(
        f'Live forecast by Open-Meteo · Last model update: {current.get("time", "not supplied")}. '
        "Forecasts are not road-safety, avalanche or mountaineering advice."
    )
else:
    st.info("Weather is temporarily unavailable. Check a local meteorological source before travel.")

st.warning("Verify opening hours, permits, access, safety, prices and local protocols with responsible local sources before travelling.")
