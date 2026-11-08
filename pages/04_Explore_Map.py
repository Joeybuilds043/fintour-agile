from __future__ import annotations

import pandas as pd
import pydeck as pdk
import streamlit as st

from src.catalog import DESTINATIONS, EXPERIENCE_CATEGORIES
from src.services.media import get_commons_image, get_display_image
from src.ui import apply_visitor_theme

st.set_page_config(page_title="VoyagePK | Illustrated Atlas", page_icon=None, layout="wide")
apply_visitor_theme()

st.markdown('<div class="kicker">THE HORIZON TRAVEL ATLAS</div>', unsafe_allow_html=True)
st.title("Pakistan, mapped by experience.")
st.markdown(
    '<div class="lede">Move from the Karakoram to the Arabian Sea. Explore mountain regions, heritage cities, '
    'desert landscapes and coastal destinations on one geographic canvas.</div>',
    unsafe_allow_html=True,
)

palette = {
    "Mountain & nature": [24, 59, 59, 230],
    "Culture & heritage": [196, 122, 80, 235],
    "Coastal & marine": [92, 147, 156, 235],
    "City & food": [112, 117, 122, 235],
    "Adventure & outdoors": [164, 137, 105, 235],
}

def map_theme(item: dict) -> str:
    experiences = set(item["experiences"])
    if "Coastal & marine" in experiences:
        return "Coastal & marine"
    if "Religious & archaeology" in experiences or (
        "Culture & heritage" in experiences and "Food & gastronomy" in experiences
    ):
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
        "name": name, "region": item["region"], "lat": item["lat"], "lon": item["lon"],
        "theme": theme, "color": palette[theme],
        "experiences": ", ".join(item["experiences"]), "tagline": item["tagline"],
    })
frame = pd.DataFrame(records)

with st.container(border=True):
    f1, f2 = st.columns([1, 1.5], gap="medium")
    with f1:
        selected_regions = st.multiselect(
            "Regions", sorted(frame["region"].unique()), placeholder="All regions"
        )
    with f2:
        selected_experiences = st.multiselect(
            "Travel experiences",
            [item["name"] for item in EXPERIENCE_CATEGORIES],
            placeholder="All experiences",
        )

filtered = frame.copy()
if selected_regions:
    filtered = filtered[filtered["region"].isin(selected_regions)]
if selected_experiences:
    filtered = filtered[
        filtered["experiences"].apply(
            lambda value: any(experience in value for experience in selected_experiences)
        )
    ]

st.markdown(
    '<div class="legend">' + "".join(
        f'<span class="legend-item"><span class="legend-dot" style="background:rgb({rgb[0]},{rgb[1]},{rgb[2]})"></span>{label}</span>'
        for label, rgb in palette.items()
    ) + '</div>',
    unsafe_allow_html=True,
)
st.caption(
    f"{len(filtered)} of {len(frame)} destination clusters shown · "
    "Markers indicate approximate destination areas."
)

if filtered.empty:
    st.info("No destinations match these filters. Remove a filter to broaden the map.")
else:
    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=filtered,
            get_position="[lon, lat]",
            get_radius=10500,
            get_fill_color="color",
            get_line_color=[255, 255, 255, 245],
            line_width_min_pixels=1.5,
            radius_min_pixels=6,
            radius_max_pixels=18,
            pickable=True,
            auto_highlight=True,
        )
    ]
    if len(filtered) <= 18:
        layers.append(
            pdk.Layer(
                "TextLayer",
                data=filtered,
                get_position="[lon, lat]",
                get_text="name",
                get_size=11,
                get_color=[25, 47, 54, 245],
                get_pixel_offset=[0, -19],
                get_alignment_baseline="'bottom'",
                billboard=True,
                size_min_pixels=9,
                size_max_pixels=13,
            )
        )
    deck = pdk.Deck(
        layers=layers,
        initial_view_state=pdk.ViewState(
            latitude=30.6, longitude=69.1, zoom=4.25, pitch=42, bearing=-8
        ),
        map_style=("https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json" if st.session_state.get("voyage_theme") == "Dark" else "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"),
        tooltip={
            "html": "<div style='padding:9px'><b>{name}</b><br/>{region}<br/><span>{tagline}</span></div>",
            "style": {"backgroundColor": "#183B3B", "color": "#FFFCF6", "fontSize": "12px"},
        },
    )
    st.pydeck_chart(deck, use_container_width=True, height=620)

st.markdown("### Landmark story cards")
landmark_a, landmark_b = st.columns(2, gap="large")
with landmark_a:
    st.image("https://commons.wikimedia.org/wiki/Special:FilePath/Passu%20Cones%20and%20the%20Hunza%20River.jpg?width=1000", use_container_width=True)
    st.markdown("**Passu Cones · Upper Hunza**")
    st.caption("A distinctive Karakoram skyline. Image source and exact focal crop require manual review.")
with landmark_b:
    st.image("https://commons.wikimedia.org/wiki/Special:FilePath/Lahore%20Fort%20pakistan.jpg?width=1000", use_container_width=True)
    st.markdown("**Lahore Fort · Walled City**")
    st.caption("Mughal-era heritage landmark. Photo: Riiyan.ch · CC BY-SA 4.0 · Source: https://commons.wikimedia.org/wiki/File:Lahore_Fort_pakistan.jpg")
st.markdown("### Explore a destination")
available_names = filtered["name"].tolist() if not filtered.empty else list(DESTINATIONS)
if available_names:
    selected = st.selectbox("Choose a place to see its field notes", available_names, key="atlas_selected_destination")
    item = DESTINATIONS[selected]
    detail_left, detail_right = st.columns([1, 1.2], gap="large", vertical_alignment="center")
    with detail_left:
        photo = get_commons_image(item["image_query"])
        if photo:
            rendered = get_display_image(photo["thumb_url"])
            st.image(rendered or photo["thumb_url"], use_container_width=True)
            st.caption(f'{photo["artist"]} · {photo["license"]} · [Image source]({photo["page_url"]})' + (' · Illustrative regional reference' if photo.get('illustrative') else ''))
        else:
            st.markdown(
                '<div style="height:210px;border-radius:16px;background:linear-gradient(135deg,#EEE9DF,#D9C8B7)"></div>',
                unsafe_allow_html=True,
            )
    with detail_right:
        st.markdown(f'**{item["region"]}**')
        st.subheader(selected)
        st.write(item["tagline"])
        st.caption(" · ".join(item["experiences"][:4]))
        if st.button("Open destination field guide", type="primary", key="open_atlas_guide"):
            st.session_state["selected_destination"] = selected
            st.switch_page("pages/02_Destination_Guide.py")

st.markdown("### Destination index")
st.dataframe(
    filtered[["name", "region", "theme", "tagline"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "name": "Destination", "region": "Region",
        "theme": "Landscape & experience", "tagline": "Why go",
    },
)
st.caption(
    "Map tiles by CARTO; geographic data and place labels by OpenStreetMap contributors. "
    "Approximate coordinates are for discovery, not navigation or safety decisions."
)
