from __future__ import annotations

import streamlit as st

from src.catalog import DESTINATIONS
from src.services.grok import GroqAPIError, generate_text, get_api_key
from src.ui import apply_visitor_theme

st.set_page_config(page_title="AI Travel Concierge | VoyagePK", page_icon=None, layout="wide")
apply_visitor_theme()
st.title("AI travel concierge")
st.markdown("Plan with destination context, local culture using the selected destination context.")
st.write(
    "Ask for destination ideas and itinerary help. Answers use VoyagePK's destination catalogue "
    "This is not a live booking or road-information service."
)

api_key = get_api_key()
if api_key:
    st.caption("Groq is connected through secure app configuration.")
else:
    st.info(
        "Groq is not configured yet. The app owner must add GROQ_API_KEY in "
        "Streamlit Community Cloud → App settings → Secrets. Visitors do not enter or manage API keys."
    )

destination = st.selectbox("Primary destination context", list(DESTINATIONS), key="selected_destination")
d = DESTINATIONS[destination]
question = st.text_area(
    "What kind of trip are you planning?",
    placeholder="Example: I have four days, prefer nature and local food, and want a moderate walking itinerary.",
    height=130,
)

if st.button("Ask VoyagePK", type="primary", disabled=not bool(api_key and question.strip())):
    context = (
        f"Destination: {destination}. Province/territory: {d.get('province', d['region'])}. "
        f"Region: {d['region']}. Overview: {d['overview']}. "
        f"Experiences: {', '.join(d['experiences'])}. Highlights: {', '.join(d['highlights'])}. "
        f"Season: {d['season']}. Access: {d['access']}. Responsible travel: {d['responsible']}."
    )
    system = (
        "You are VoyagePK's Pakistan travel concierge. Be practical, precise and locally respectful. "
        "Use supplied destination context for catalogue facts. Do not invent prices, hotel availability, "
        "road status, opening hours, permits, safety conditions or exact journey times. If live research "
        "is enabled, use it for current facts and cite sources, prioritising official authorities and "
        "clearly distinguishing official information from travel blogs or user-generated content. "
        "State assumptions and data gaps. Provide a useful itinerary with realistic pacing and responsible "
        "local experiences. Never imply that a destination listing confirms it is safe or open today."
    )
    with st.spinner("VoyagePK is preparing your travel guidance..."):
        try:
            answer = generate_text(
                api_key=api_key,
                system_instruction=system,
                user_prompt=f"{context}\nVisitor request: {question}",
                temperature=0.7,
                max_output_tokens=1500,
                timeout=(10, 180),
            )
            st.markdown(answer)
        except GroqAPIError as exc:
            st.error(str(exc))

st.caption(
    "AI-generated plans are suggestions. Verify access, weather, permits, prices, safety and bookings "
    "independently. Groq API usage may incur charges."
)
