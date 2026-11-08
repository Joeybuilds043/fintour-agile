from __future__ import annotations

import pandas as pd
import pydeck as pdk
import streamlit as st

from src.catalog import DESTINATIONS, EXPERIENCE_CATEGORIES

st.set_page_config(page_title="Pakistan Travel Atlas | Horizon", page_icon=None, layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
.stApp{background:#f7f5ef;font-family:'DM Sans',sans-serif;color:#172f38}
.block-container{max-width:1500px;padding-top:1.3rem}
h1,h2,h3{color:#18343c!important;font-family:'Playfair Display',Georgia,serif!important}
.kicker{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#167f83;font-weight:700}
.map-intro{font-size:14px;line-height:1.75;color:#687a7e;max-width:820px}
.legend{display:flex;flex-wrap:wrap;gap:14px 22px;padding:12px 0;color:#53686e;font-size:12px}
.legend-item{display:flex;align-items:center;gap:7px}
.legend-dot{width:10px;height:10px;border-radius:50%;display:inline-block}
div[data-testid="stVerticalBlockBorderWrapper"]{background:#fffefa;border-color:#e7e2d8;border-radius:18px}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="kicker">THE HORIZON TRAVEL ATLAS</div>', unsafe_allow_html=True)
st.title("Pakistan, mapped by experience.")
st.markdown('<div class="map-intro">Move from the Karakoram to the Arabian Sea. Explore the country’s mountain regions, heritage cities, desert landscapes and coastal destinations on one geographic canvas. Select a region or travel interest to bring relevant places into focus.</div>', unsafe_allow_html=True)

palette = {
    "Mountain & nature": [32, 130, 145, 225],
    "Culture & heritage": [190, 126, 76, 235],
    "Coastal & marine": [45, 155, 180, 235],
    "City & food": [119, 111, 166, 235],
    "Adventure & outdoors": [91, 145, 105, 235],
}

def map_theme(item: dict) -> str:
    experiences = set(item["experiences"])
    if "Coastal & marine" in experiences:
        return "Coastal & marine"
    if "Religious & archaeology" in experiences or ("Culture & heritage" in experiences and "Food & gastronomy" in experiences):
        return "Culture & heritage"
    if "Food & gastronomy" in experiences and "Nature & wildlife" not in experiences:
        return "City & food"
    if "Adventure" in experiences and "Nature & wildlife" not in experiences:
        return "Adventure & outdoors"
    return "Mountain & nature"

records = []
for name, item in DESTINATIONS.items():
    theme = map_theme(item)
    records.append({
        "name": name,
        "region": item["region"],
        "lat": item["lat"],
        "lon": item["lon"],
        "theme": theme,
        "color": palette[theme],
        "experiences": ", ".join(item["experiences"]),
        "tagline": item["tagline"],
    })
frame = pd.DataFrame(records)

with st.container(border=True):
    f1, f2 = st.columns([1, 1.5], gap="medium")
    with f1:
        selected_regions = st.multiselect("Regions", sorted(frame["region"].unique()), placeholder="All regions")
    with f2:
        selected_experiences = st.multiselect("Travel experiences", [x["name"] for x in EXPERIENCE_CATEGORIES], placeholder="All experiences")

filtered = frame.copy()
if selected_regions:
    filtered = filtered[filtered["region"].isin(selected_regions)]
if selected_experiences:
    filtered = filtered[filtered["experiences"].apply(lambda value: any(x in value for x in selected_experiences))]

st.markdown('<div class="legend">' + "".join(
    f'<span class="legend-item"><span class="legend-dot" style="background:rgb({rgb[0]},{rgb[1]},{rgb[2]})"></span>{label}</span>'
    for label, rgb in palette.items()
) + '</div>', unsafe_allow_html=True)
st.caption(f"{len(filtered)} of {len(frame)} destination clusters shown · Markers represent approximate destination areas, not exact attraction entrances or turn-by-turn routes.")

if filtered.empty:
    st.info("No places match those filters. Remove a filter to broaden the map.")
else:
    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=filtered,
            get_position="[lon, lat]",
            get_radius=9500,
            get_fill_color="color",
            get_line_color=[255, 255, 255, 235],
            line_width_min_pixels=1.5,
            radius_min_pixels=5,
            radius_max_pixels=17,
            pickable=True,
            auto_highlight=True,
        )
    ]
    if len(filtered) <= 20:
        layers.append(
            pdk.Layer(
                "TextLayer",
                data=filtered,
                get_position="[lon, lat]",
                get_text="name",
                get_size=12,
                get_color=[25, 47, 54, 245],
                get_pixel_offset=[0, -18],
                get_alignment_baseline="'bottom'",
                billboard=True,
                size_min_pixels=10,
                size_max_pixels=15,
            )
        )
    deck = pdk.Deck(
        layers=layers,
        initial_view_state=pdk.ViewState(
            latitude=30.6,
            longitude=69.1,
            zoom=4.25,
            pitch=24,
            bearing=-4,
        ),
        map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
        tooltip={
            "html": "<div style='padding:8px'><b>{name}</b><br/>{region}<br/><span>{tagline}</span></div>",
            "style": {"backgroundColor": "#17343c", "color": "#fffefa", "fontSize": "12px"},
        },
    )
    st.pydeck_chart(deck, use_container_width=True, height=670)

st.markdown("### Explore the places on the map")
st.dataframe(
    filtered[["name", "region", "theme", "tagline"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "name": "Destination",
        "region": "Region",
        "theme": "Landscape & experience",
        "tagline": "Why go",
    },
)
st.caption("Map tiles by CARTO; geographic data and place labels are provided by OpenStreetMap contributors. Approximate coordinates are intended for discovery only. Do not use this map for navigation, emergency response or road-safety decisions.")
