from __future__ import annotations
import requests
import streamlit as st
from src.catalog import DESTINATIONS

st.set_page_config(page_title="AI Travel Concierge | Horizon",page_icon="💬",layout="wide")
st.title("AI travel concierge")
st.write("Ask for destination ideas and itinerary help. Answers are grounded in Horizon's current pilot catalogue, not a live booking or road-information service.")
try:
    api_key=st.secrets.get("GROK_API_KEY","")
except Exception:
    api_key=""
api_key=api_key or st.session_state.get("horizon_ai_key","")
if not api_key:
    entered=st.text_input("Optional xAI API key for this session",type="password")
    if entered: st.session_state["horizon_ai_key"]=entered; api_key=entered
destination=st.selectbox("Primary destination context",list(DESTINATIONS))
d=DESTINATIONS[destination]
question=st.text_area("What kind of trip are you planning?",placeholder="Example: I have four days, prefer nature and local food, and want a moderate walking itinerary.",height=130)
if st.button("Ask Horizon",type="primary",disabled=not bool(api_key and question.strip())):
    context=f"Destination: {destination}. Region: {d['region']}. Overview: {d['overview']}. Experiences: {', '.join(d['experiences'])}. Highlights: {', '.join(d['highlights'])}. Season: {d['season']}. Access: {d['access']}. Responsible travel: {d['responsible']}."
    system=("You are Horizon's visitor travel concierge for Pakistan. Use only the supplied destination context for factual destination claims. "
      "Do not invent prices, hotel availability, road status, opening hours, permits, safety conditions or exact journey times. "
      "If the user asks for missing live information, say it must be checked with an authoritative provider. "
      "Give a practical, friendly itinerary with flexible pacing and responsible local experiences. State assumptions and data gaps.")
    try:
        response=requests.post("https://api.x.ai/v1/chat/completions",
          headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"},
          json={"model":"latest","messages":[{"role":"system","content":system},{"role":"user","content":context+"\nVisitor request: "+question}],"temperature":0.3,"max_tokens":1200},timeout=(10,60))
        response.raise_for_status()
        content=response.json().get("choices",[{}])[0].get("message",{}).get("content","")
        if content: st.markdown(content)
        else: st.error("The AI provider returned an empty response.")
    except requests.RequestException as exc: st.error(f"AI service request failed: {exc}")
    except (ValueError,KeyError,IndexError) as exc: st.error(f"Could not read the AI response: {exc}")
if not api_key: st.info("AI is optional. Add GROK_API_KEY in Streamlit Community Cloud Secrets to enable the concierge.")
st.caption("AI-generated plans are suggestions. Verify access, weather, permits, prices, safety and bookings independently.")
