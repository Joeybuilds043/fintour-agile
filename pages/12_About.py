from __future__ import annotations

import streamlit as st

from src.ui import apply_visitor_theme

st.set_page_config(page_title="About VoyagePK", page_icon=None, layout="wide")
apply_visitor_theme()

st.title("About VoyagePK")
st.write("Built by Muhammad Asad, Lahore, Pakistan.")
st.write(
    "VoyagePK is a tourism discovery prototype for Pakistan. It brings destination "
    "information, regional attractions, festivals, travel planning and early tourism "
    "strategy tools into one Streamlit app."
)

st.subheader("What it can do")
st.write(
    "- Browse destination and experience information from the app catalogue.\n"
    "- Explore selected regional attractions and festival records.\n"
    "- Build a draft itinerary from catalogue information.\n"
    "- Use AI tools for travel ideas and tourism strategy when the service is available.\n"
    "- Explore example investment and growth scenarios."
)

st.subheader("What it cannot do")
st.write(
    "- It does not make bookings or confirm prices or availability.\n"
    "- It does not provide live road, weather or safety advice.\n"
    "- It does not replace local authorities, professional advice or on-site checks.\n"
    "- Its catalogue is not a complete or fully verified national tourism database.\n"
    "- AI responses can be wrong. Check important details independently."
)

st.subheader("Version")
st.write("Prototype version 1 (asset manifest version 1).")
