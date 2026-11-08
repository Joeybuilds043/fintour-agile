from __future__ import annotations
import pandas as pd
import streamlit as st
from src.catalog import DESTINATIONS

st.set_page_config(page_title="Explore Map | Horizon",page_icon="🌐",layout="wide")
st.title("Explore Pakistan on the map")
st.write("A geographic view of the ten pilot destination clusters. Pins are approximate cluster anchors, not exact attraction entrances or verified routes.")
rows=[{"Destination":n,"Region":d["region"],"lat":d["lat"],"lon":d["lon"],"Experiences":", ".join(d["experiences"][:3])} for n,d in DESTINATIONS.items()]
frame=pd.DataFrame(rows)
region=st.selectbox("Filter region",["All regions"]+sorted(frame["Region"].unique().tolist()))
if region!="All regions": frame=frame[frame["Region"]==region]
st.map(frame[["lat","lon"]],zoom=4)
st.dataframe(frame.drop(columns=["lat","lon"]),use_container_width=True,hide_index=True)
st.caption("Cluster coordinates should be refined against authoritative geographic data before navigation use.")
