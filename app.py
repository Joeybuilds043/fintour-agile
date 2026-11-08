import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

# --- SYSTEM METRICS & BRANDING ---
st.set_page_config(
    page_title="EcoRoute-AI // Infrastructure Allocation Platform",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN TECH-TOURISM INTERFACE INJECTION ---
st.markdown("""
<style>
    @import url('https://googleapis.com');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #020617 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #F8FAFC !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #334155 !important;
    }
    
    .panel-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(6, 182, 212, 0.15);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
    }
    
    .status-active {
        color: #10B981;
        font-weight: 600;
        text-shadow: 0 0 8px rgba(16, 185, 129, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR DEPLOYMENT STRATEGY ---
st.sidebar.markdown("<h2 style='color:#06B6D4; text-align:center;'>🐼 EcoRoute Console</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align:center; color:#94A3B8; font-size:12px;'>MSc Strategy & Innovation System Blueprint</p>", unsafe_allow_html=True)
st.sidebar.write("---")

app_mode = st.sidebar.radio("Platform Workspaces", ["🗺️ Strategic Infrastructure Allocator", "💬 Grok Panda Corporate Agent"])

# Geospatial Simulation Matrix
nodes = {
    'Supply Core (Lahore)': [31.5204, 74.3587],
    'Saturated Node (Murree Matrix)': [33.9070, 73.3943],
    'Overburdened Ecosystem (Kaghan)': [34.5412, 73.3512],
    'Under-utilized Market (Skardu Link)': [35.2974, 75.6322]
}

# ---------------- WORKSPACE 1: THE INFRASTRUCTURE ENGINE ----------------
if app_mode == "🗺️ Strategic Infrastructure Allocator":
    st.markdown("<h1 style='font-weight:600; letter-spacing:-1px;'>EcoRoute-AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; font-size:16px;'>Deploying Autonomous Allocation Models to Balance Destination Volatility and Supply Chain Bottlenecks</p>", unsafe_allow_html=True)
    st.write("---")
    
    # INDUSTRIAL PROBLEM ANALYSIS CONTAINER
    st.markdown("""
    <div class="panel-card">
        <h4>🚨 The Structural Market Failure:</h4>
        <p style="color:#CBD5E1; font-size:14px; margin-bottom:0px;">
            Unregulated traveler distribution strains regional electricity, food supply lines, and waste management infrastructure in target clusters while diverting potential revenue away from emerging micro-economies. 
            This enterprise application uses multi-agent resource tracking to orchestrate commercial assets dynamically across public-private tourism networks.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("##")
    
    # CONTROL INTERFACE FOR LOGISTICS CORRIDORS
    col_map, col_controls = st.columns()
    
    with col_controls:
        st.markdown("### ⚙️ Optimization Parameters")
        target_cluster = st.selectbox("Simulate Regional Logistics Hub Re-routing", list(nodes.keys()))
        demand_load = st.slider("Simulated Peak Foot-Traffic Saturation (%)", 40, 150, 95)
        capacity_buffer = st.slider("Local Supply Chain Inventory Margin (%)", 10, 100, 45)
        
        # Operational Analytics Processing
        efficiency_index = round((capacity_buffer / demand_load) * 100, 1)
        
        st.write("---")
        st.markdown(f"**Calculated Operational Efficiency Index:** `{efficiency_index}%`")
        if efficiency_index < 50:
            st.markdown("⚠️ **System Status:** <span class='status-active' style='color:#EF4444; text-shadow:0 0 8px rgba(239, 68, 68, 0.3);'>High Saturation Risk</span>", unsafe_allow_html=True)
        else:
            st.markdown("✅ **System Status:** <span class='status-active'>Optimal Allocation Corridor</span>", unsafe_allow_html=True)
            
    with col_map:
        # Plotly Spatial Matrix Rendering
        fig = go.Figure()
        fig.add_trace(go.Scattermap(
            mode = "markers+lines",
            lon = [nodes['Supply Core (Lahore)'], nodes[target_cluster]],
            lat = [nodes['Supply Core (Lahore)'], nodes[target_cluster]],
            marker = {'size': 14, 'color': '#06B6D4'},
            line = dict(width = 4, color = '#F59E0B')
        ))
        fig.update_layout(
            map_style="carto-darkmatter",
            map=dict(center=dict(lat=33.5, lon=74.5), zoom=5.2),
            margin={"r":0,"t":0,"l":0,"b":0},
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- WORKSPACE 2: THE BUSINESS SOLUTIONS CORE ----------------
elif app_mode == "💬 Grok Panda Corporate Agent":
    st.markdown("<h1 style='font-weight:600; letter-spacing:-1px;'>Pandy-AI Corporate Strategy Consultant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8;'>Real-Time Strategic Solutions for Public Governance Nodes and Tourism Logistics Enterprises</p>", unsafe_allow_html=True)
    st.write("---")
    
    col_img, col_txt = st.columns()
    with col_img:
        st.image("https://imgur.com", width=90)
    with col_txt:
        st.markdown("#### **Corporate Advisory Terminal Initialized**")
        st.write("Welcome to the multi-agent consulting portal. Backed by live xAI Grok computational parameters, I analyze industrial capacity data to resolve supply-chain bottlenecks, evaluate tourism infrastructure risk, and optimize capital distribution.")

    st.write("##")

    GROK_API_KEY = st.secrets.get("GROK_API_KEY", None)

    if not GROK_API_KEY:
        st.warning("🔒 Secure Integration Note: Connect an active xAI Developer Token inside the Secrets control block to unlock real-time streaming strategy analysis.")
        GROK_API_KEY = st.text_input("Or input temporary Grok API Key directly for session evaluation:", type="password")

    if "solution_messages" not in st.session_state:
        st.session_state.solution_messages = [
            {"role": "assistant", "content": "System operational. I am configured to address real-world industrial friction. Input your systemic issue, or select a predefined macroeconomic query profile below."}
        ]

    for msg in st.session_state.solution_messages:
        avatar_design = "🐼" if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=avatar_design):
            st.write(msg["content"])

    # Strategic Quick Buttons to populate live inquiries without typing
    quick_col1, quick_col2 = st.columns(2)
    with quick_col1:
        q1 = st.button("📊 Strategy for overtourism supply-chain strain in Northern regions?")
    with quick_col2:
        q2 = st.button("🚀 How can innovation management models fix localized resource inflation?")

    selected_query = None
    if q1: selected_query = "Provide a comprehensive business strategy to mitigate overtourism supply-chain strain in high-altitude regional corridors, referencing dynamic asset redistribution."
    if q2: selected_query = "How can emerging business innovation management frameworks protect rural host communities from hyper-inflation caused by seasonal tourism demand drops?"

    user_input = st.chat_input("Input specific structural bottleneck data for real-time analysis...")
    active_query = user_input if user_input else selected_query

    if active_query:
        if not user_input:  # Display selection if triggered via click arrays
            st.session_state.solution_messages.append({"role": "user", "content": active_query})
            with st.chat_message("user"):
                st.write(active_query)

        with st.chat_message("assistant", avatar="🐼"):
            if GROK_API_KEY:
                with st.spinner("Executing structural optimization via xAI Grok Core..."):
                    try:
                        system_context = (
                            "You are Pandy-AI, a world-class Corporate Strategy and Innovation Consultant specialized in resolving macroeconomic market failures "
                            "within emerging tourism and logistics sectors. Your task is to provide highly rigorous, enterprise-grade business strategy advice, "
                            "risk mitigations, and resource routing blueprints. Address the problems using the vocabulary of the MSc Business Strategy and Innovation Management "
                            "program at the University of Southampton (e.g., core competencies, asset reconfiguration, platform ecosystems, technology transfer, and agile operations). "
                            "Do not mention any individual personal portfolios, grades, or personal student bios. Focus entirely on delivering realistic, highly actionable industrial solutions."
                        )
                        
                        headers = {
                            "Authorization": f"Bearer {GROK_API_KEY}",
                            "Content-Type": "application/json"
                        }
                        
                        payload = {
                            "model": "grok-2-beta",
                            "messages": [
                                {"role": "system", "content": system_context},
                                {"role": "user", "content": active_query}
                            ],
                            "temperature": 0.2
                        }
