import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import json

# --- PREMIUM UI/UX CONFIGURATION ---
st.set_page_config(
    page_title="DestiNation-AI // Muhammad Asad",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS INJECTION FOR ELITE EDITORIAL DESIGN ---
st.markdown("""
<style>
    @import url('https://googleapis.com');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #030712 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        color: #F3F4F6 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid #1F2937 !important;
    }
    
    .metric-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(8px);
        transition: transform 0.3s ease, border 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(6, 182, 212, 0.6);
    }
    
    .neon-text {
        color: #06B6D4;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.4);
    }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h2 style='color:#06B6D4; text-align:center;'>🐼 Pandy-AI Console</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align:center; color:#9CA3AF; font-size:12px;'>MSc Strategy & Innovation Portfolio</p>", unsafe_allow_html=True)
st.sidebar.write("---")
page = st.sidebar.radio("Navigate Workspace", ["🚀 DestiNation Engine", "💬 Live Grok Panda Assistant"])

locations = {
    'Lahore Hub': [31.5204, 74.3587],
    'Kaghan Ecosystem': [34.5412, 73.3512],
    'Skardu Node': [35.2974, 75.6322],
    'Murree Matrix': [33.9070, 73.3943]
}

# ---------------- PAGE 1: THE CORE STRUCTURAL ENGINE ----------------
if page == "🚀 DestiNation Engine":
    st.markdown("<h1 style='text-align: center; font-weight:300;'>DestiNation-AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#9CA3AF; font-size:18px;'>Pioneering Autonomous Spatial Tourism Redistribution</p>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>Matriculation</h3><h2 class="neon-text">1010/1100</h2><p style="color:#9CA3AF; font-size:12px;">Govt College (PEEF Scholar)</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>Intermediate</h3><h2 class="neon-text">921/1100</h2><p style="color:#9CA3AF; font-size:12px;">Pre-Engineering Base</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>BS Tourism</h3><h2 class="neon-text">3.75 / 4.0</h2><p style="color:#9CA3AF; font-size:12px;">Superior University Lahore</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>Strategic Elite</h3><h2 class="neon-text">HBS / ALP</h2><p style="color:#9CA3AF; font-size:12px;">Aspire Leaders Alumnus</p></div>', unsafe_allow_html=True)
        
    st.write("##")
    st.markdown("### 🗺️ Real-Time Spatial Optimization Corridor")
    selected_node = st.selectbox("Select Target Destination Infrastructure Node", list(locations.keys()))
    
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lon = [locations['Lahore Hub'], locations[selected_node]],
        lat = [locations['Lahore Hub'], locations[selected_node]],
        marker = {'size': 12, 'color': '#06B6D4'},
        line = dict(width = 3, color = '#D4AF37')
    ))
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        mapbox=dict(center=dict(lat=33.5, lon=74.5), zoom=5.5),
        margin={"r":0,"t":0,"l":0,"b":0},
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- PAGE 2: LIVE GROK INTERFACE ----------------
elif page == "💬 Live Grok Panda Assistant":
    st.markdown("<h1 style='text-align: center; font-weight:300;'>Pandy-AI Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#9CA3AF;'>Live Live Connected xAI Grok Engine for Global Strategy Analytics</p>", unsafe_allow_html=True)
    st.write("---")
    
    col_img, col_txt = st.columns([1, 5])
    with col_img:
        st.image("https://imgur.com", width=100)
    with col_txt:
        st.markdown("#### **Autonomous System Node Status: Active**")
        st.write("Greetings, Admissions Board. I am initialized as a live-compiled multi-agent wrapper connecting xAI's real-time Grok models to analyze tourism networks.")

    st.write("##")

    # Safe API Key Fetching from Streamlit Cloud Secrets Manager
    GROK_API_KEY = st.secrets.get("GROK_API_KEY", None)

    if not GROK_API_KEY:
        st.warning("⚠️ Grok API Key Missing: Please insert your secure key inside the Streamlit Cloud Dashboard Secrets panel to activate full live tracking responses.")
        # Local testing fall-back entry input
        GROK_API_KEY = st.text_input("Alternatively, paste your temporary xAI Key here for instant evaluation:", type="password")

    # Conversational History Instantiation
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am Asad's specialized agent. Ask me how his background in Pakistan's tourism sector, coupled with business strategy analytics, forms a unique profile for the University of Southampton."}
        ]

    for msg in st.session_state.messages:
        avatar_img = "🐼" if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=avatar_img):
            st.write(msg["content"])

    if user_query := st.chat_input("Ask a real-time question to Grok..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        with st.chat_message("assistant", avatar="🐼"):
            if GROK_API_KEY:
                with st.spinner("Streaming Live Data Arrays via xAI API Pipelines..."):
                    try:
                        # Constructing direct context constraints to align Grok with your application profile
                        system_prompt = (
                            "You are Pandy-AI, a specialized strategic assistant built for Muhammad Asad's portfolio. "
                            "Asad is an elite candidate applying for the MSc Business Strategy and Innovation Management at the University of Southampton "
                            "and competing for the Commonwealth Master's Scholarship. His metrics: 1010/1100 Matric, 921/1100 Inter, 3.75/4.0 CGPA from Superior University, "
                            "Harvard ALP Alumnus, and published author on ResearchGate regarding GenAI overtourism. His operations history includes TDCP and Coca-Cola. "
                            "Always link your answers back to how his rare tech-driven portfolio solves business bottlenecks or fits the Southampton innovation modules."
                        )
                        
                        headers = {
                            "Authorization": f"Bearer {GROK_API_KEY}",
                            "Content-Type": "application/json"
                        }
                        
                        payload = {
                            "model": "grok-2-beta",
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_query}
                            ],
                            "temperature": 0.3
                        }
                        
                        response = requests.post("https://x.ai", headers=headers, json=payload)
                        
                        if response.status_code == 200:
                            grok_res = response.json()["choices"][0]["message"]["content"]
                            st.write(grok_res)
                            st.session_state.messages.append({"role": "assistant", "content": grok_res})
                        else:
                            st.error(f"API connection error code: {response.status_code}. Response raw output: {response.text}")
                    except Exception as e:
                        st.error(f"System connection runtime issue: {str(e)}")
            else:
                # Simulated response if no API key is verified yet
                st.info("Simulated Echo Node: Please secure your Grok key via configuration settings to retrieve dynamic cross-platform outputs.")
