from __future__ import annotations
import pandas as pd
import streamlit as st
from src.ui import apply_intelligence_theme
st.set_page_config(page_title="Data Observatory | Horizon",page_icon=None,layout="wide")
apply_intelligence_theme()
st.title("Tourism data observatory")
st.write("A transparent register of sources and limitations.")
sources=[
{"Source":"Open-Meteo","Use":"Current and forecast weather","Access":"Public API; free no-key tier for eligible non-commercial use","Caveat":"Attribution required; review commercial terms","URL":"https://open-meteo.com/en/docs"},
{"Source":"Wikimedia Commons","Use":"Destination photographs","Access":"Commons API","Caveat":"Check each file's individual licence, creator and attribution","URL":"https://commons.wikimedia.org/wiki/Commons:API"},
{"Source":"Government of Gilgit-Baltistan","Use":"Published tourist inflow dashboard","Access":"Public dashboard","Caveat":"Check publication date, coverage and observation period","URL":"https://e-tourism.visitgilgitbaltistan.gov.pk/plan-trip/tourist-inflows"},
{"Source":"Pakistan Tourism Development Corporation","Use":"Tourism publications and context","Access":"Public website","Caveat":"Publication dates and geographic coverage vary","URL":"https://tourism.gov.pk/publications.html"},
{"Source":"OpenStreetMap","Use":"Potential geographic reference data","Access":"Open geographic database","Caveat":"ODbL attribution and separate tile/geocoding policies apply","URL":"https://www.openstreetmap.org/copyright"}]
st.dataframe(pd.DataFrame(sources),use_container_width=True,hide_index=True)
st.subheader("Evidence labels")
for label,desc in [("Official","Published by an identifiable government or recognised institution."),("Verified partner","Submitted by a named organisation and checked."),("Survey-based","Collected through a documented survey."),("Estimated","Calculated from disclosed assumptions."),("Illustrative","Demonstration values, not market evidence."),("Missing","Not currently available or sufficiently reliable.")]:
    st.markdown(f"**{label}** — {desc}")
st.caption("A statistic should not be labelled verified without source, observation period, unit, geographic scope and last verification date.")
