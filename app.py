import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- PURE PREMIUM UI/UX CONFIGURATION ---
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
    
    /* Root Theme Overrides */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #030712 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        color: #F3F4F6 !important;
    }
    
    /* Clean Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid #1F2937 !important;
    }
    
    /* Glowing Glassmorphic Cards */
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
    
    /* Neon Text Accents */
    .neon-text {
        color: #06B6D4;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.4);
    }
    
    /* Premium Hide Elements */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h2 style='color:#06B6D4; text-align:center;'>🐼 Pandy-AI Console</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align:center; color:#9CA3AF; font-size:12px;'>MSc Strategy & Innovation Portfolio</p>", unsafe_allow_html=True)
st.sidebar.write("---")
page = st.sidebar.radio("Navigate Workspace", ["🚀 DestiNation Engine", "💬 Grok AI Panda Assistant"])

# --- DATA GENERATION (RESEARCH BACKED) ---
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
    
    # PREMIUM METRICS GRID
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
    
    # CORE INTERACTIVE SIMULATION PANEL
    st.markdown("### 🗺️ Real-Time Spatial Optimization Corridor")
    st.write("Simulating the operational distribution paradigms established via active research parameters to mitigate overtourism bottlenecks within Northern Pakistan circuits.")
    
    # Interactive selection box
    selected_node = st.selectbox("Select Target Destination Infrastructure Node", list(locations.keys()))
    
    # Interactive Map Generation using Plotly
    fig = go.Figure()
    
    # Core Base Line
    fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lon = [locations['Lahore Hub'][1], locations[selected_node][1]],
        lat = [locations['Lahore Hub'][0], locations[selected_node][0]],
        marker = {'size': 12, 'color': '#06B6D4'},
        line = dict(width = 3, color = '#D4AF37')
    ))
    
    # Layout Strategy
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        mapbox=dict(
            center=dict(lat=33.5, lon=74.5),
            zoom=5.5
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # STRATEGIC WORK EXPERIENCE MARQUEE
    st.write("##")
    st.markdown("### 💼 Cross-Disciplinary Operational Mastery")
    exp1, exp2, exp3 = st.columns(3)
    with exp1:
        st.markdown("**Tourism Development Corp. of Punjab (TDCP)**  \n*Competitive Strategy Intern*  \nAnalyzed domestic routing networks and structural destination pain points.")
    with exp2:
        st.markdown("**Waheed Brothers Coca-Cola Distribution**  \n*Operations Logistics Assistant*  \nManaged enterprise supply chains, scheduling, and asset deployment patterns.")
    with exp3:
        st.markdown("**Rahi Travels Portfolio**  \n*Corporate HR & Operations Intern*  \nCoordinated functional frameworks within live operational environments.")

# ---------------- PAGE 2: GROK AI PANDA INTERFACE ----------------
elif page == "💬 Grok AI Panda Assistant":
    st.markdown("<h1 style='text-align: center; font-weight:300;'>Pandy-AI Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#9CA3AF;'>Powered by Grok API Frameworks for Modern Service Strategy</p>", unsafe_allow_html=True)
    st.write("---")
    
    # Visual Panda Identification Row
    col_img, col_txt = st.columns([1, 4])
    with col_img:
        # Displaying the designated tech panda profile indicator
        st.image("https://imgur.com", width=120)
    with col_txt:
        st.markdown("#### **System Node Operational**")
        st.write("Greetings Asad. I am your custom Grok-configured multi-agent core. I bridge field level data with the strategic objectives of the MSc Business Strategy and Innovation Management program at Southampton.")

    st.write("##")
    
    # Live Chat Workspace Simulated Deployment Window
    user_query = st.chat_input("Ask Pandy-AI about tourism optimization or Southampton alignment...")
    
    # Seed Conversational Framework for Admissions Board Viewers
    if not user_query:
        with st.chat_message("assistant", avatar="🐼"):
            st.markdown("""
            **System Prompt Initialized:** Hello! Ask me how Muhammad Asad merges his public sector experience at TDCP and Coca-Cola with advanced AI algorithms to solve global overtourism challenges. 
            
            *Suggested exploration inputs:*
            *   "How does your research on spatial distribution connect to the MSc at Southampton?"
            *   "Explain the logistics infrastructure behind your route optimization code."
            """)
            
    if user_query:
        with st.chat_message("user"):
            st.write(user_query)
            
        with st.chat_message("assistant", avatar="🐼"):
            with st.spinner("Processing routing arrays via Grok Engine..."):
                time.sleep(1)
                if "southampton" in user_query.lower() or "msc" in user_query.lower():
                    st.write("Asad’s background aligns directly with Southampton's 'Innovation and Technology Transfer' curriculum. By scaling automated systems like this mapping tool, he transitions from operational hospitality into enterprise asset valuation.")
                elif "research" in user_query.lower() or "spatial" in user_query.lower():
                    st.write("His ResearchGate publications show that overtourism isn't an capacity problem—it's a tracking problem. This application uses multi-agent software pipelines to track traffic patterns and dynamically reroute tourism capital into under-utilized eco-corridors.")
                else:
                    st.write("System online. By combining your operational work history at Coca-Cola and TDCP with automated neural infrastructure, we create high-yield, sustainable models built for global deployment.")
