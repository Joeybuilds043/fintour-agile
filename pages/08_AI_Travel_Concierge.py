from __future__ import annotations

import streamlit as st
from src.ui import apply_visitor_theme
from src.catalog import DESTINATIONS
from src.services.gemini import GeminiAPIError, generate_text, get_api_key

st.set_page_config(page_title="AI Travel Concierge | VoyagePK", page_icon=None, layout="wide")
apply_visitor_theme()
st.title("AI travel concierge")
st.markdown("Plan with destination context, local culture and current web research when needed.")
st.write(
    "Ask for destination ideas and itinerary help. Answers are grounded in Horizon's current pilot catalogue, "
    "not a live booking or road-information service."
)

api_key = get_api_key()
if api_key:
    st.caption("Gemini connected through app configuration.")
else:
    with st.expander("Use your existing Gemini key for this session"):
        st.text_input("Existing Gemini API key", type="password", key="horizon_gemini_key")
        st.caption("For a persistent connection, store the same key in Streamlit Secrets as GEMINI_API_KEY or GOOGLE_API_KEY.")
    api_key = get_api_key()

destination = st.selectbox("Primary destination context", list(DESTINATIONS), key="selected_destination")
d = DESTINATIONS[destination]
ground_search = st.checkbox("Ground current details with Google Search", value=False, help="Google Search grounding may add Gemini API usage charges.")
question = st.text_area(
    "What kind of trip are you planning?",
    placeholder="Example: I have four days, prefer nature and local food, and want a moderate walking itinerary.",
    height=130,
)

if st.button("Ask Horizon", type="primary", disabled=not bool(api_key and question.strip())):
    context = (
        f"Destination: {destination}. Region: {d['region']}. Overview: {d['overview']}. "
        f"Experiences: {', '.join(d['experiences'])}. Highlights: {', '.join(d['highlights'])}. "
        f"Season: {d['season']}. Access: {d['access']}. Responsible travel: {d['responsible']}."
    )
    system = (
        "You are Horizon's visitor travel concierge for Pakistan. Use only the supplied destination context "
        "for factual destination claims. Do not invent prices, hotel availability, road status, opening hours, "
        "permits, safety conditions or exact journey times. If the user asks for missing live information, say "
        "it must be checked with an authoritative provider. Give a practical itinerary with flexible pacing and "
        "responsible local experiences. State assumptions and data gaps. When Google Search grounding is enabled, cite sources and distinguish official sources from travel blogs or user-generated content."
    )
    with st.spinner("VoyagePK is preparing your travel guidance..."):
        try:
            answer = generate_text(
                api_key=api_key,
                system_instruction=system,
                user_prompt=f"{context}\nVisitor request: {question}",
                temperature=0.3,
                max_output_tokens=1200,
                timeout=(10, 60),
                google_search=ground_search,
            )
            st.markdown(answer)
        except GeminiAPIError as exc:
            st.error(str(exc))

if not api_key:
    st.info("Gemini key not detected. In Streamlit Community Cloud → this app → Settings → Secrets, set GEMINI_API_KEY = \"your key\" (or GOOGLE_API_KEY). Save and reboot this app. If the key is already present, check that it is saved on this exact deployment under one of those names; do not create a second key.")
st.caption("AI-generated plans are suggestions. Verify access, weather, permits, prices, safety and bookings independently.")
