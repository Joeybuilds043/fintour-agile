from __future__ import annotations

import streamlit as st
from src.ui import apply_visitor_theme
from src.catalog import DESTINATIONS
from src.services.gemini import GeminiAPIError, generate_text, get_api_key, get_provider_name

st.set_page_config(page_title="AI Strategy Advisor | VoyagePK", page_icon=None, layout="wide")
apply_visitor_theme()
st.title("AI tourism strategy advisor")
st.write(
    "A destination-management and business-strategy assistant for tourism entrepreneurs, operators and public-sector planners."
)

api_key = get_api_key()
if api_key:
    st.caption(f"{get_provider_name(api_key)} connected through app configuration.")
else:
    with st.expander("Use your existing Gemini key for this session"):
        st.text_input("Existing Gemini API key", type="password", key="horizon_gemini_key")
        st.caption("For a persistent connection, store the same key in Streamlit Secrets as GEMINI_API_KEY or GOOGLE_API_KEY.")
    api_key = get_api_key()

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
provider_name = get_provider_name(api_key)
ground_search = st.checkbox(
    "Ground market and policy research with Google Search",
    value=False,
    disabled=(provider_name == "Groq"),
    help="Google Search grounding is supported here only through Gemini.",
)
if provider_name == "Groq":
    st.caption("Groq is active. Add GEMINI_API_KEY as well to enable Google Search grounding and automatic Gemini-first routing.")
question = st.text_area(
    "Specific strategic question",
    placeholder="What decision are you trying to make? Include any known budget, capacity or operating constraints.",
    height=120,
)

if st.button("Generate strategy brief", type="primary", disabled=not bool(api_key and question.strip())):
    context = (
        f"Destination: {name}; Region: {d['region']}; Overview: {d['overview']}; "
        f"Experiences: {', '.join(d['experiences'])}; Current editorial risk/season/access notes: "
        f"{d['season']} {d['access']} {d['responsible']}"
    )
    system = (
        "You are a rigorous tourism strategy, destination management and investment advisor. Use the supplied "
        "context, but do not invent market size, visitor statistics, hotel occupancy, costs, approvals or citations. "
        "Separate known context, user assumptions and research gaps. Evaluate demand, service quality, seasonality, "
        "local supplier participation, ecological constraints, governance and implementation. Return: Diagnosis; "
        "strategic options; business model; implementation roadmap; KPIs; risks; data required before investment."
    )
    with st.spinner("Preparing your destination strategy brief..."):
        try:
            answer = generate_text(
                api_key=api_key,
                system_instruction=system,
                user_prompt=f"{context}\nFocus: {focus}\nQuestion: {question}",
                temperature=0.2,
                max_output_tokens=1600,
                timeout=(10, 75),
                google_search=ground_search,
            )
            st.markdown(answer)
            st.download_button(
                "Download strategy brief",
                answer,
                file_name=f"{name.lower().replace(' ', '-')}-strategy.md",
                mime="text/markdown",
            )
        except GeminiAPIError as exc:
            st.error(str(exc))

if not api_key:
    st.info("No AI key detected. In Streamlit Community Cloud → this app → Settings → Secrets, set GEMINI_API_KEY = \"your key\" or GROQ_API_KEY = \"your key\". Save and reboot this app.")
st.caption("This is strategic brainstorming, not professional investment, legal, engineering or safety advice.")
