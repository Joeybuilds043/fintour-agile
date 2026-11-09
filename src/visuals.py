"""Data-grounded, responsive line charts for VoyagePK's destination catalogue.

These charts show catalogue coverage only. They are not visitor-demand time series,
popularity rankings, travel-time estimates, road conditions or forecasts.
"""
from __future__ import annotations

from collections import Counter

import plotly.graph_objects as go
import streamlit as st

from src.ui import style_plotly_figure


def catalogue_distribution_figures(destinations: dict):
    """Return regional and experience-theme line charts from actual catalogue records."""
    regions = Counter()
    themes = Counter()
    for item in destinations.values():
        regions[item.get("province") or item.get("region") or "Unclassified"] += 1
        themes.update(set(item.get("experiences") or []))

    region_items = sorted(regions.items(), key=lambda pair: pair[0])
    theme_items = sorted(themes.items(), key=lambda pair: pair[0])
    dark = st.session_state.get("voyage_theme", "Light") == "Dark"

    regional_line = "#249B87" if not dark else "#55D6B5"
    theme_line = "#C58A35" if not dark else "#F2B65D"
    regional_markers = (
        ["#249B87", "#63AFC0", "#8EBA79", "#C58A35", "#6E91C8", "#B17AA1", "#D47F65"]
        if not dark else
        ["#55D6B5", "#79CBE0", "#A8D98D", "#F2B65D", "#91B5F2", "#D5A0CA", "#F09A7D"]
    )
    theme_markers = (
        ["#C58A35", "#249B87", "#6E91C8", "#B17AA1", "#D47F65", "#8EBA79", "#63AFC0"]
        if not dark else
        ["#F2B65D", "#55D6B5", "#91B5F2", "#D5A0CA", "#F09A7D", "#A8D98D", "#79CBE0"]
    )
    paper = "#0B100D" if dark else "#FFFEF9"

    regional = go.Figure(
        go.Scatter(
            x=[name for name, _ in region_items],
            y=[count for _, count in region_items],
            mode="lines+markers+text",
            line=dict(color=regional_line, width=3, shape="linear"),
            marker=dict(
                size=11,
                color=[regional_markers[i % len(regional_markers)] for i in range(len(region_items))],
                line=dict(color=paper, width=2),
            ),
            text=[str(count) for _, count in region_items],
            textposition="top center",
            textfont=dict(size=11),
            fill="tozeroy",
            fillcolor="rgba(36,155,135,0.10)" if not dark else "rgba(85,214,181,0.12)",
            customdata=[name for name, _ in region_items],
            hovertemplate="<b>%{customdata}</b><br>%{y} destination clusters<extra></extra>",
        )
    )
    regional.update_layout(
        title="Destination clusters by region",
        xaxis_title=None,
        yaxis_title="Catalogue clusters",
        showlegend=False,
        transition={"duration": 650, "easing": "cubic-in-out"},
    )

    thematic = go.Figure(
        go.Scatter(
            x=[name for name, _ in theme_items],
            y=[count for _, count in theme_items],
            mode="lines+markers+text",
            line=dict(color=theme_line, width=3, shape="linear"),
            marker=dict(
                size=11,
                color=[theme_markers[i % len(theme_markers)] for i in range(len(theme_items))],
                line=dict(color=paper, width=2),
            ),
            text=[str(count) for _, count in theme_items],
            textposition="top center",
            textfont=dict(size=11),
            fill="tozeroy",
            fillcolor="rgba(197,138,53,0.10)" if not dark else "rgba(242,182,93,0.12)",
            customdata=[name for name, _ in theme_items],
            hovertemplate="<b>%{customdata}</b><br>%{y} tagged destination clusters<extra></extra>",
        )
    )
    thematic.update_layout(
        title="Destination clusters across experience themes",
        xaxis_title=None,
        yaxis_title="Tagged clusters",
        showlegend=False,
        transition={"duration": 650, "easing": "cubic-in-out"},
    )

    regional_height = max(340, min(470, 320 + 12 * len(region_items)))
    thematic_height = max(370, min(520, 330 + 11 * len(theme_items)))
    regional.update_layout(height=regional_height)
    thematic.update_layout(height=thematic_height)

    return (
        style_plotly_figure(regional, height=regional_height),
        style_plotly_figure(thematic, height=thematic_height),
    )


def render_catalogue_visuals(destinations: dict, *, key_prefix: str = "catalogue"):
    """Render full-width, responsive catalogue line charts beneath the page workflow."""
    regional, thematic = catalogue_distribution_figures(destinations)
    with st.container(border=True):
        st.markdown('<div class="voyage-chart-kicker">REGIONAL DISTRIBUTION</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="voyage-chart-note">A line view of how the current destination catalogue is distributed across regions. Each point is a category, not a time period.</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            regional,
            use_container_width=True,
            config={"displayModeBar": False, "responsive": True},
            key=f"{key_prefix}_regional",
        )
    with st.container(border=True):
        st.markdown('<div class="voyage-chart-kicker">EXPERIENCE THEMES</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="voyage-chart-note">Counts of destination clusters tagged with each experience theme. Chart height and spacing adapt to the number of categories.</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            thematic,
            use_container_width=True,
            config={"displayModeBar": False, "responsive": True},
            key=f"{key_prefix}_themes",
        )
