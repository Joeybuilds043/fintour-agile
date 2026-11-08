from __future__ import annotations

import streamlit as st
from src.ui import apply_visitor_theme
from src.catalog import DESTINATIONS
from src.services.gemini import GeminiAPIError, generate_text, get_api_key

st.set_page_config(page_title="AI Travel Concierge | Horizon", page_icon=None, layout="wide")
apply_visitor_theme()
st.title("AI travel concierge")
st.write(
    "Ask for destination ideas and itinerary help. Answers are grounded in Horizon's current pilot catalogue, "
    "not a live booking or road-information service."
)

api_key = get_api_key()
if not api_key:
    entered = st.text_input("Optional Gemini API key for this session", type="password")
    if entered:
        st.session_state["horizon_gemini_key"] = entered.strip()
        api_key = entered.strip()

destination = st.selectbox("Primary destination context", list(DESTINATIONS))
d = DESTINATIONS[destination]
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
        "responsible local experiences. State assumptions and data gaps."
    )
    with st.spinner("Horizon is preparing your travel guidance..."):
        try:
            answer = generate_text(
                api_key=api_key,
                system_instruction=system,
                user_prompt=f"{context}\nVisitor request: {question}",
                temperature=0.3,
                max_output_tokens=1200,
                timeout=(10, 60),
            )
            st.markdown(answer)
        except GeminiAPIError as exc:
            st.error(str(exc))

if not api_key:
    st.info("AI is optional. Add GEMINI_API_KEY in Streamlit Community Cloud Secrets to enable the concierge.")
st.caption("AI-generated plans are suggestions. Verify access, weather, permits, prices, safety and bookings independently.")
