"""Data-grounded catalogue charts for VoyagePK.

These figures describe the catalogue itself, not live visitor demand, popularity,
travel times, road conditions or forecasts.
"""
from __future__ import annotations

from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

from src.ui import style_plotly_figure


def catalogue_distribution_figures(destinations: dict):
    """Return regional coverage and experience-tag charts from catalogue records."""
    regions = Counter()
    themes = Counter()
    for item in destinations.values():
        regions[item.get("province") or item.get("region") or "Unclassified"] += 1
        themes.update(set(item.get("experiences") or []))

    region_frame = pd.DataFrame(
        [{"Region": name, "Destination clusters": count} for name, count in regions.items()]
    ).sort_values("Destination clusters", ascending=True)
    theme_frame = pd.DataFrame(
        [{"Experience theme": name, "Tagged clusters": count} for name, count in themes.items()]
    ).sort_values("Tagged clusters", ascending=True)

    dark = st.session_state.get("voyage_theme", "Light") == "Dark"
    accent = "#45C477" if dark else "#328A67"
    secondary = "#8ED9A9" if dark else "#63AFC0"

    regional = px.bar(
        region_frame, x="Destination clusters", y="Region", orientation="h",
        title="Catalogue coverage by region",
        labels={"Destination clusters": "Clusters", "Region": ""},
    )
    regional.update_traces(
        marker_color=accent, marker_line_color="rgba(255,255,255,.28)", marker_line_width=1,
        hovertemplate="%{y}<br>%{x} catalogue clusters<extra></extra>",
    )
    regional.update_layout(bargap=0.34, transition={"duration": 700, "easing": "cubic-in-out"})

    thematic = px.bar(
        theme_frame, x="Tagged clusters", y="Experience theme", orientation="h",
        title="Experience themes across the atlas",
        labels={"Tagged clusters": "Tagged clusters", "Experience theme": ""},
    )
    thematic.update_traces(
        marker_color=secondary, marker_line_color="rgba(255,255,255,.28)", marker_line_width=1,
        hovertemplate="%{y}<br>%{x} tagged clusters<extra></extra>",
    )
    thematic.update_layout(bargap=0.34, transition={"duration": 700, "easing": "cubic-in-out"})

    return (
        style_plotly_figure(regional, height=max(300, 28 * len(region_frame) + 100)),
        style_plotly_figure(thematic, height=max(300, 27 * len(theme_frame) + 100)),
    )


def render_catalogue_visuals(destinations: dict, *, key_prefix: str = "catalogue"):
    """Render animated-on-entry views of actual catalogue coverage."""
    regional, thematic = catalogue_distribution_figures(destinations)
    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown('<div class="voyage-chart-kicker">REGIONAL DISTRIBUTION</div>', unsafe_allow_html=True)
            st.markdown('<div class="voyage-chart-note">Destination clusters currently listed for each region.</div>', unsafe_allow_html=True)
            st.plotly_chart(regional, use_container_width=True,
                            config={"displayModeBar": False, "responsive": True},
                            key=f"{key_prefix}_regional")
    with right:
        with st.container(border=True):
            st.markdown('<div class="voyage-chart-kicker">EXPERIENCE TAXONOMY</div>', unsafe_allow_html=True)
            st.markdown('<div class="voyage-chart-note">Catalogue clusters tagged with each experience theme.</div>', unsafe_allow_html=True)
            st.plotly_chart(thematic, use_container_width=True,
                            config={"displayModeBar": False, "responsive": True},
                            key=f"{key_prefix}_themes")
