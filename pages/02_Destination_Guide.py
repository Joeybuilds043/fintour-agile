from __future__ import annotations
import os
import pandas as pd
import streamlit as st
from src.ui import apply_visitor_theme
from src.catalog import DESTINATIONS
from src.services.media import get_commons_image
from src.services.weather import get_weather

st.set_page_config(page_title="Destination Guide | Horizon",page_icon=None,layout="wide")
apply_visitor_theme()
st.title("Destination guides")
name=st.selectbox("Choose a destination",list(DESTINATIONS))
d=DESTINATIONS[name]
image=None if os.getenv("HORIZON_DISABLE_REMOTE_MEDIA")=="1" else get_commons_image(d["image_query"])
if image:
    st.image(image["thumb_url"],use_container_width=True)
    st.caption(f'{image["title"]} · {image["license"]} · {image["artist"]} · [Licence]({image["license_url"]}) · [Original file]({image["page_url"]})')
st.caption(f'{d["region"]} · Destination cluster')
st.header(name)
st.subheader(d["tagline"])
st.write(d["overview"])
left,right=st.columns([1.15,1])
with left:
    st.markdown("### Culture and local identity")
    st.write(d["culture"])
    st.markdown("### Experiences")
    for x in d["experiences"]: st.markdown(f"- {x}")
    st.markdown("### Places and highlights")
    for x in d["highlights"]: st.markdown(f"- {x}")
with right:
    st.markdown("### Season and travel considerations")
    st.write(d["season"])
    st.markdown("### Getting there")
    st.write(d["access"])
    st.markdown("### Responsible travel")
    st.write(d["responsible"])
    st.markdown("### Destination location")
    st.map(pd.DataFrame([{"lat":d["lat"],"lon":d["lon"]}]),zoom=7)
st.markdown("### Local weather outlook")
weather=get_weather(d["lat"],d["lon"])
if weather:
    current=weather.get("current",{})
    a,b,c=st.columns(3)
    a.metric("Temperature",f'{current.get("temperature_2m","—")} °C')
    b.metric("Feels like",f'{current.get("apparent_temperature","—")} °C')
    c.metric("Wind",f'{current.get("wind_speed_10m","—")} km/h')
    daily=weather.get("daily",{})
    if daily.get("time"):
        frame=pd.DataFrame({"Date":daily["time"],"Max °C":daily.get("temperature_2m_max",[]),"Min °C":daily.get("temperature_2m_min",[]),"Rain probability %":daily.get("precipitation_probability_max",[])})
        st.dataframe(frame,use_container_width=True,hide_index=True)
    st.caption(f'Forecast by Open-Meteo · Model time: {weather.get("current", {}).get("time", "not supplied")}. Forecasts are not road-safety or mountaineering advice.')
else: st.info("Weather service is temporarily unavailable. Check a local meteorological source before travel.")
st.warning("This is an editorial prototype. Verify opening hours, permits, access, safety, prices and local protocols before travelling.")
