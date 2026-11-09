from __future__ import annotations

import streamlit as st

from src.catalog import DESTINATIONS
from src.services.grok import GroqAPIError, generate_text, get_api_key
from src.ui import apply_visitor_theme

st.set_page_config(page_title="AI Strategy Advisor | VoyagePK", page_icon=None, layout="wide")
apply_visitor_theme()
st.title("AI tourism strategy advisor")
st.write(
    "A destination-management and business-strategy assistant for tourism entrepreneurs, "
    "operators and public-sector planners. Answers use the selected destination context; "
    "the selected Llama model does not perform live web research."
)

api_key = get_api_key()
if api_key:
    st.caption("Groq is connected through secure app configuration.")
else:
    st.info(
        "Groq is not configured yet. The app owner must add GROQ_API_KEY in "
        "Streamlit Community Cloud → App settings → Secrets. Visitors do not enter or manage API keys."
    )

name = st.selectbox("Destination", list(DESTINATIONS), key="selected_destination")
d = DESTINATIONS[name]
focus = st.selectbox(
    "Analysis focus",
    [
        "Destination competitiveness and positioning",
        "Tourism business model and revenue streams",
        "Investment opportunity screening",
        "Sustainable visitor management",
        "Digital innovation roadmap",
        "Local value retention and community enterprise",
    ],
)
question = st.text_area(
    "Specific strategic question",
    placeholder="What decision are you trying to make? Include any known budget, capacity or operating constraints.",
    height=120,
)

if st.button("Generate strategy brief", type="primary", disabled=not bool(api_key and question.strip())):
    context = (
        f"Destination: {name}; Province/territory: {d.get('province', d['region'])}; "
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
        "roadmap; KPIs; risks; data required before investment. Do not fabricate citations or claim live verification; identify facts that require current official research."
    )
    with st.spinner("Preparing your destination strategy brief..."):
        try:
            answer = generate_text(
                api_key=api_key,
                system_instruction=system,
                user_prompt=f"{context}\nFocus: {focus}\nQuestion: {question}",
                temperature=0.5,
                max_output_tokens=1800,
                timeout=(10, 180),
            )
            st.markdown(answer)
            st.download_button(
                "Download strategy brief",
                answer,
                file_name=f"{name.lower().replace(' ', '-')}-strategy.md",
                mime="text/markdown",
            )
        except GroqAPIError as exc:
            st.error(str(exc))

st.caption(
    "This is strategic brainstorming, not professional investment, legal, engineering or safety advice. "
    "Groq API usage may incur charges."
)
