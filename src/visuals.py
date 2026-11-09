"""Responsive, data-grounded catalogue charts for VoyagePK."""
from __future__ import annotations
from collections import Counter
import plotly.graph_objects as go
import streamlit as st
from src.ui import style_plotly_figure


def catalogue_distribution_figures(destinations: dict, chart_style: str = "Line"):
    regions, themes = Counter(), Counter()
    for item in destinations.values():
        regions[item.get("administrative_region") or item.get("province") or item.get("region") or "Unclassified"] += 1
        themes.update(set(item.get("experiences") or []))
    # Rank categories by count: line joins compare ranks, not time-series observations.
    region_items = sorted(regions.items(), key=lambda p: (-p[1], p[0]))
    theme_items = sorted(themes.items(), key=lambda p: (-p[1], p[0]))
    dark = st.session_state.get("voyage_theme", "Light") == "Dark"
    palette = (["#55D6B5", "#79CBE0", "#A8D98D", "#F2B65D", "#91B5F2", "#D5A0CA", "#F09A7D"]
               if dark else ["#168C75", "#4B9DB5", "#86A85A", "#C58A35", "#6688BD", "#A8789A", "#C8785F"])
    line_colors = ["#55D6B5", "#F2B65D"] if dark else ["#168C75", "#C58A35"]

    def build(items, title, y_title, color):
        names, values = [p[0] for p in items], [p[1] for p in items]
        marker_colors = [palette[i % len(palette)] for i in range(len(items))]
        if chart_style == "Bars":
            trace = go.Bar(x=names, y=values, marker_color=marker_colors,
                           text=values, textposition="outside",
                           hovertemplate="<b>%{x}</b><br>%{y} clusters<extra></extra>")
        else:
            trace = go.Scatter(
                x=names, y=values, mode="lines+markers+text",
                line=dict(color=color, width=3.5, shape="spline", smoothing=0.8),
                marker=dict(size=10, color=marker_colors,
                            line=dict(color="#0B100D" if dark else "#FFFEF9", width=2)),
                text=values, textposition="top center",
                fill="tozeroy" if chart_style == "Area" else None,
                fillcolor=("rgba(85,214,181,.12)" if dark else "rgba(22,140,117,.10)") if chart_style == "Area" else None,
                hovertemplate="<b>%{x}</b><br>%{y} clusters<extra></extra>",
            )
        fig = go.Figure(trace)
        fig.update_layout(title=title, xaxis_title=None, yaxis_title=y_title,
                          showlegend=False, transition={"duration": 550, "easing": "cubic-in-out"},
                          bargap=0.34, margin=dict(l=14, r=18, t=64, b=72))
        fig.update_xaxes(tickangle=-28, automargin=True, showgrid=False)
        fig.update_yaxes(rangemode="tozero", automargin=True)
        return style_plotly_figure(fig, height=max(360, min(510, 340 + 13 * len(items))))
    return (
        build(region_items, "Destination clusters by region", "Catalogue clusters", line_colors[0]),
        build(theme_items, "Destination clusters by experience", "Tagged clusters", line_colors[1]),
    )


def render_catalogue_visuals(destinations: dict, *, key_prefix: str = "catalogue"):
    st.markdown("---")
    st.markdown("### Catalogue analytics")
    st.markdown(
        '<div class="voyage-chart-note">Explore catalogue coverage by region and experience. '
        'These are catalogue counts, not visitor-demand, popularity or travel-time data.</div>',
        unsafe_allow_html=True,
    )
    chart_style = st.selectbox(
        "Chart style", ["Line", "Area", "Bars"], index=0,
        key=f"{key_prefix}_chart_style",
        help="Categories are ranked by their catalogue counts.",
    )
    regional, thematic = catalogue_distribution_figures(destinations, chart_style)
    with st.container(border=True):
        st.markdown('<div class="voyage-chart-kicker">REGIONAL DISTRIBUTION</div>', unsafe_allow_html=True)
        st.plotly_chart(regional, use_container_width=True,
                        config={"displayModeBar": True, "displaylogo": False, "responsive": True},
                        key=f"{key_prefix}_regional")
    with st.container(border=True):
        st.markdown('<div class="voyage-chart-kicker">EXPERIENCE THEMES</div>', unsafe_allow_html=True)
        st.plotly_chart(thematic, use_container_width=True,
                        config={"displayModeBar": True, "displaylogo": False, "responsive": True},
                        key=f"{key_prefix}_themes")
