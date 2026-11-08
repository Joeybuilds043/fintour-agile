from __future__ import annotations
import requests
import streamlit as st
from src.catalog import DESTINATIONS

st.set_page_config(page_title="AI Strategy Advisor | Horizon",page_icon="🧠",layout="wide")
st.title("AI tourism strategy advisor")
st.write("A destination-management and business-strategy assistant for tourism entrepreneurs, operators and public-sector planners.")
try: api_key=st.secrets.get("GROK_API_KEY","")
except Exception: api_key=""
api_key=api_key or st.session_state.get("horizon_ai_key","")
if not api_key:
    entered=st.text_input("Optional xAI API key for this session",type="password")
    if entered: st.session_state["horizon_ai_key"]=entered; api_key=entered
name=st.selectbox("Destination",list(DESTINATIONS))
d=DESTINATIONS[name]
focus=st.selectbox("Analysis focus",["Destination competitiveness and positioning","Tourism business model and revenue streams","Investment opportunity screening","Sustainable visitor management","Digital innovation roadmap","Local value retention and community enterprise"])
question=st.text_area("Specific strategic question",placeholder="What decision are you trying to make? Include any known budget, capacity or operating constraints.",height=120)
if st.button("Generate strategy brief",type="primary",disabled=not bool(api_key and question.strip())):
    context=f"Destination: {name}; Region: {d['region']}; Overview: {d['overview']}; Experiences: {', '.join(d['experiences'])}; Current editorial risk/season/access notes: {d['season']} {d['access']} {d['responsible']}"
    system=("You are a rigorous tourism strategy, destination management and investment advisor. "
      "Use the supplied context, but do not invent market size, visitor statistics, hotel occupancy, costs, approvals or citations. "
      "Separate known context, user assumptions and research gaps. Evaluate demand, service quality, seasonality, local supplier participation, ecological constraints, governance and implementation. "
      "Return: Diagnosis; strategic options; business model; implementation roadmap; KPIs; risks; data required before investment.")
    try:
        response=requests.post("https://api.x.ai/v1/chat/completions",
          headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"},
          json={"model":"latest","messages":[{"role":"system","content":system},{"role":"user","content":context+"\nFocus: "+focus+"\nQuestion: "+question}],"temperature":0.2,"max_tokens":1600},timeout=(10,75))
        response.raise_for_status()
        content=response.json().get("choices",[{}])[0].get("message",{}).get("content","")
        if content:
            st.markdown(content)
            st.download_button("Download strategy brief",content,file_name=f"{name.lower().replace(' ','-')}-strategy.md",mime="text/markdown")
        else: st.error("The AI provider returned an empty response.")
    except requests.RequestException as exc: st.error(f"AI service request failed: {exc}")
    except (ValueError,KeyError,IndexError) as exc: st.error(f"Could not read the AI response: {exc}")
if not api_key: st.info("AI is optional. Add GROK_API_KEY in Streamlit Community Cloud Secrets to enable this workspace.")
st.caption("This is strategic brainstorming, not professional investment, legal, engineering or safety advice.")
