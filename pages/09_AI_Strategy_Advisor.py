from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from src.catalog import DESTINATIONS
from src.services.groq import GroqAPIError, generate_text, get_api_key
from src.ui import apply_visitor_theme, style_plotly_figure

st.set_page_config(page_title="AI Strategy Advisor | VoyagePK", page_icon=None, layout="wide")
apply_visitor_theme()
st.markdown('<div class="voyage-chart-kicker">TOURISM STRATEGY · DESTINATION INSIGHTS</div>', unsafe_allow_html=True)
st.title("AI tourism strategy advisor")

api_key = get_api_key()
if not api_key:
    st.info(
        "Groq is not configured yet. The app owner must add GROQ_API_KEY in "
        "Streamlit Community Cloud → App settings → Secrets. Visitors do not enter or manage API keys."
    )

name = st.selectbox("Destination", list(DESTINATIONS), key="selected_destination")
d = DESTINATIONS[name]
focus_options = [
    "Destination competitiveness and positioning",
    "Tourism business model and revenue streams",
    "Investment opportunity screening",
    "Sustainable visitor management",
    "Digital innovation roadmap",
    "Local value retention and community enterprise",
]
focus = st.selectbox("Analysis focus", focus_options, key="strategy_focus")
question = st.text_area(
    "Specific strategic question",
    placeholder="What decision are you trying to make? Include any known budget, capacity or operating constraints.",
    height=120,
    key="strategy_question",
)
submitted = st.button("Generate strategy brief", type="primary", use_container_width=True, key="generate_strategy")

if submitted:
    if not question.strip():
        st.warning("Enter your strategic question before submitting.")
    elif not api_key:
        st.error("VoyagePK AI is unavailable because the app owner has not configured GROQ_API_KEY.")
    else:
        context = (
            f"Destination: {name}; Province/territory: {d.get('administrative_region') or d.get('province', d['region'])}; "
            f"Region: {d['region']}; Overview: {d['overview']}; "
            f"Experiences: {', '.join(d['experiences'])}; Current editorial risk/season/access notes: "
            f"{d['season']} {d['access']} {d['responsible']}"
        )
        system = (
            "You are a rigorous tourism strategy, destination management and investment advisor. "
            "Use supplied context, but do not invent market size, visitor statistics, hotel occupancy, costs, "
            "approvals or citations. Separate verified information, user assumptions and research gaps. "
            "Evaluate demand, service quality, seasonality, local supplier participation, ecological constraints, "
            "governance and implementation. Return: Diagnosis; strategic options; business model; implementation "
            "roadmap; KPIs; risks; data required before investment. Do not fabricate citations or claim live "
            "verification; identify facts that require current official research."
        )
        with st.spinner("Preparing your destination strategy brief..."):
            try:
                answer = generate_text(
                    api_key=api_key, system_instruction=system,
                    user_prompt=f"{context}\nFocus: {focus}\nQuestion: {question}",
                    temperature=0.5, max_output_tokens=1800, timeout=180,
                )
                st.markdown(answer)
                st.download_button(
                    "Download strategy brief", answer,
                    file_name=f"{name.lower().replace(' ', '-')}-strategy.md",
                    mime="text/markdown",
                )
            except GroqAPIError as exc:
                st.error(str(exc))

st.caption(
    "This is strategic brainstorming, not professional investment, legal, engineering or safety advice. "
    "Groq API usage may incur charges."
)

if focus == "Investment opportunity screening":
    st.markdown("---")
    st.markdown("### Investment screening priorities")
    st.markdown(
        "Set the importance of each factor for this opportunity. The chart updates from your inputs; "
        "these are your screening weights, not measured market data or an investment rating."
    )
    criteria = [
        ("Demand evidence", "Evidence of addressable demand and visitor segments", 8),
        ("Revenue potential", "Ability to generate repeatable, diversified revenue", 7),
        ("Capital intensity", "Upfront investment and ongoing capital requirements", 6),
        ("Seasonality resilience", "Ability to operate beyond peak travel periods", 7),
        ("Community value", "Local jobs, supplier participation and value retention", 8),
        ("Environmental pressure", "Water, waste, biodiversity and carrying-capacity exposure", 9),
    ]
    weights = {}
    left, right = st.columns([1, 1.2], gap="large")
    with left:
        for label, help_text, default in criteria:
            weights[label] = st.slider(
                label, min_value=1, max_value=10, value=default, step=1,
                help=help_text, key=f"investment_weight_{label.lower().replace(' ', '_')}",
            )
    with right:
        chart_kind = st.radio(
            "Visualisation", ["Ranked bars", "Donut"], horizontal=True,
            key="investment_chart_kind",
        )
        labels = list(weights.keys())
        values = list(weights.values())
        palette = ["#2A9D8F", "#4C9FCE", "#82B66B", "#D4A64A", "#9276C5", "#D17C68"]
        if chart_kind == "Donut":
            fig = go.Figure(go.Pie(
                labels=labels, values=values, hole=0.62, sort=False,
                marker=dict(colors=palette, line=dict(color="#F4F1E7", width=2)),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Importance: %{value}/10<extra></extra>",
            ))
            fig.update_layout(showlegend=False, annotations=[dict(
                text="YOUR<br>WEIGHTS", x=0.5, y=0.5, showarrow=False,
                font=dict(size=17, family="Manrope, sans-serif"),
            )])
        else:
            order = sorted(labels, key=lambda label: weights[label])
            fig = go.Figure(go.Bar(
                x=[weights[label] for label in order], y=order, orientation="h",
                marker=dict(color=[palette[labels.index(label)] for label in order],
                            line=dict(width=0), cornerradius=7),
                text=[f"{weights[label]}/10" for label in order],
                textposition="outside", cliponaxis=False,
                hovertemplate="<b>%{y}</b><br>Importance: %{x}/10<extra></extra>",
            ))
            fig.update_xaxes(range=[0, 11], dtick=2, title="Importance (1–10)")
            fig.update_yaxes(title=None, autorange="reversed")
        fig.update_layout(
            uirevision="investment-priority-chart",
            transition={"duration": 300, "easing": "cubic-in-out"},
            margin=dict(l=8, r=36, t=28, b=38),
            height=440 if chart_kind == "Ranked bars" else 470,
        )
        fig = style_plotly_figure(fig, height=440 if chart_kind == "Ranked bars" else 470)
        fig.update_layout(uirevision="investment-priority-chart", margin=dict(l=8, r=36, t=28, b=38))
        st.plotly_chart(
            fig, use_container_width=True, key="investment_priority_chart",
            config={"displayModeBar": True, "displaylogo": False, "responsive": True, "scrollZoom": False},
        )
    st.caption("Use these weights to structure diligence. A real investment decision still needs verified demand, cost, financing, legal and environmental data.")
