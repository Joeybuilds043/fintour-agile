"""Weather forecast integration using Open-Meteo's public API."""
from __future__ import annotations
import os
import requests
import streamlit as st

@st.cache_data(ttl=1800, show_spinner=False)
def get_weather(latitude: float, longitude: float, temperature_unit: str = "celsius") -> dict | None:
    if os.getenv("HORIZON_DISABLE_EXTERNAL_DATA") == "1":
        return None
    unit = "fahrenheit" if temperature_unit.lower().startswith("f") else "celsius"
    params = {
        "latitude": latitude, "longitude": longitude,
        "current": "temperature_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "forecast_days": 7, "timezone": "auto", "temperature_unit": unit,
    }
    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=(5, 12))
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None
