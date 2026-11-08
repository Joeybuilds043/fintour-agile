
import streamlit as st
import plotly.graph_objects as go
import requests

# =========================================================
# 1. APPLICATION CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EcoRoute AI | Infrastructure Intelligence",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_NAME = "EcoRoute AI"
XAI_ENDPOINT = "https://api.x.ai/v1/chat/completions"
XAI_MODEL = "latest"

NODES = {
    "Supply Core — Lahore": {
        "lat": 31.5204,
        "lon": 74.3587,
        "type": "Supply Core"
    },
    "Saturated Node — Murree": {
        "lat": 33.9070,
        "lon": 73.3943,
        "type": "High Demand"
    },
    "Overburdened Ecosystem — Kaghan": {
        "lat": 34.5412,
        "lon": 73.3512,
        "type": "High Demand"
    },
    "Under-utilized Market — Skardu": {
        "lat": 35.2974,
        "lon": 75.6322,
        "type": "Growth Opportunity"
    }
}

SYSTEM_CONTEXT = """
You are Pandy AI, an enterprise-grade Corporate Strategy,
Infrastructure and Innovation Consultant.

Your expertise includes:
- Tourism infrastructure and destination management
- Supply chain optimization
- Regional resource allocation
- Public-private partnerships
- Innovation management
- Sustainable economic development
- Operational risk management
- Capital allocation

Provide commercially realistic, evidence-conscious and actionable
recommendations.

Structure substantial answers using:
1. Executive Assessment
2. Root Cause Analysis
3. Strategic Recommendations
4. Implementation Roadmap
5. Risks and Mitigations
6. Performance Indicators

Distinguish supplied facts from assumptions.
Never fabricate statistics, research findings or live market data.
Use professional business language.
"""

# =========================================================
# 2. CUSTOM ENTERPRISE DESIGN SYSTEM
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080D18;
    --surface: #101A2B;
    --surface-2: #142137;
    --border: #24344B;
    --text: #E8EEF8;
    --muted: #91A2BA;
    --blue: #38BDF8;
    --cyan: #67E8F9;
    --amber: #FBBF24;
    --red: #FB7185;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stSidebar"] {
    background: #0B1423 !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1550px;
}

h1, h2, h3, h4 {
    color: var(--text) !important;
    letter-spacing: -0.6px;
}

p, label {
    color: var(--muted);
}

.eyebrow {
    color: var(--blue);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 10px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #F1F5F9;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 13px;
    color: var(--muted);
    line-height: 1.7;
}

.panel-card {
    background: linear-gradient(145deg, #142137, #101A2B);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 21px;
    margin-bottom: 14px;
}

.panel-label {
    color: var(--muted);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.1px;
    font-weight: 700;
}

.panel-value {
    color: var(--text);
    font-size: 27px;
    font-weight: 800;
    margin-top: 9px;
}

.panel-note {
    font-size: 11px;
    color: var(--muted);
    margin-top: 5px;
}

.status-pill {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    margin-top: 10px;
}

.status-good {
    color: #67E8C1;
    background: rgba(16,185,129,0.12);
}

.status-warning {
    color: #FCD34D;
    background: rgba(245,158,11,0.12);
}

.status-critical {
    color: #FDA4AF;
    background: rgba(244,63,94,0.12);
}

.brand-mark {
    font-size: 22px;
    font-weight: 800;
    color: #67E8F9;
    letter-spacing: -1px;
}

.brand-subtitle {
    color: var(--muted);
    font-size: 10px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 4px;
}

.section-heading {
    font-size: 17px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
}

div[data-testid="stButton"] > button {
    background: #14243B;
    color: #DCEBFA;
    border: 1px solid #30445F;
    border-radius: 9px;
    min-height: 43px;
    font-weight: 600;
    transition: all .2s ease;
}

div[data-testid="stButton"] > button:hover {
    background: #1C3654;
    border-color: var(--blue);
    color: white;
}

div[data-testid="stChatInput"] {
    border-color: #30445F !important;
}

[data-testid="stMetric"] {
    background: #101A2B;
    padding: 15px;
    border: 1px solid var(--border);
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
}

[data-testid="stMetricValue"] {
    color: var(--text) !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #101A2B;
    border-color: #30445F;
}

hr {
    border-color: var(--border);
}

footer {
    visibility: hidden;
}

@media(max-width: 768px) {
    .hero-title {
        font-size: 27px;
    }
    .block-container {
        padding-top: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. HELPER FUNCTIONS
# =========================================================

def get_api_key():
    """Read the xAI key from Streamlit Secrets."""
    try:
        key = st.secrets.get("GROK_API_KEY", "")
        if key:
            return key
    except Exception:
        pass

    return st.session_state.get("temporary_api_key", "")


def get_efficiency_status(index):
    """Return a transparent simulation status."""
    if index < 50:
        return "Critical Capacity Gap", "status-critical"

    if index < 80:
        return "Elevated Capacity Risk", "status-warning"

    return "Adequate Capacity Coverage", "status-good"


def create_allocation_map(target):
    """Create a regional infrastructure allocation map."""

    supply = NODES["Supply Core — Lahore"]
    destination = NODES[target]

    fig = go.Figure()

    # Connection corridor
    fig.add_trace(go.Scattermap(
        lat=[supply["lat"], destination["lat"]],
        lon=[supply["lon"], destination["lon"]],
        mode="lines",
        line=dict(color="#FBBF24", width=3),
        hoverinfo="skip",
        showlegend=False
    ))

    # All regional nodes
    for name, node in NODES.items():

        is_selected = name == target
        is_supply = name == "Supply Core — Lahore"

        color = (
            "#67E8F9" if is_supply
            else "#FBBF24" if is_selected
            else "#64748B"
        )

        fig.add_trace(go.Scattermap(
            lat=[node["lat"]],
            lon=[node["lon"]],
            mode="markers+text",
            text=[name.split("—")[-1].strip()],
            textposition="top right",
            marker=dict(
                size=17 if is_selected or is_supply else 11,
                color=color
            ),
            name=name,
            hovertemplate=f"<b>{name}</b><extra></extra>"
        ))

    fig.update_layout(
        map=dict(
            style="carto-darkmatter",
            center=dict(lat=33.5, lon=74.5),
            zoom=5.2
        ),
        height=440,
        margin=dict(l=0, r=0, t=5, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#DCEBFA"),
        showlegend=False
    )

    return fig


def request_grok(api_key, conversation):
    """Submit the conversation to xAI and validate the response."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Limit conversation history to control token usage.
    recent_messages = conversation[-12:]

    payload = {
        "model": XAI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_CONTEXT},
            *recent_messages
        ],
        "temperature": 0.2,
        "max_tokens": 1800
    }

    response = requests.post(
        XAI_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=(10, 90)
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"xAI API returned HTTP {response.status_code}: "
            f"{response.text[:500]}"
        )

    data = response.json()

    choices = data.get("choices", [])

    if not choices:
        raise RuntimeError("The AI provider returned no response choices.")

    answer = choices[0].get("message", {}).get("content")

    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("The AI provider returned an empty response.")

    return answer.strip()


# =========================================================
# 4. SESSION STATE
# =========================================================

if "solution_messages" not in st.session_state:
    st.session_state.solution_messages = [
        {
            "role": "assistant",
            "content": (
                "Welcome to the EcoRoute AI advisory terminal. "
                "I can help evaluate infrastructure bottlenecks, "
                "regional resource allocation and tourism strategy. "
                "What would you like to analyze?"
            )
        }
    ]

if "temporary_api_key" not in st.session_state:
    st.session_state.temporary_api_key = ""


# =========================================================
# 5. SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding:10px 0 22px;">
            <div class="brand-mark">🐼 EcoRoute AI</div>
            <div class="brand-subtitle">Infrastructure Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("##### WORKSPACE")

    app_mode = st.radio(
        "Select workspace",
        [
            "Infrastructure Dashboard",
            "Corporate AI Advisor"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("##### SYSTEM INFORMATION")

    st.caption("Platform: EcoRoute AI")
    st.caption("Environment: Simulation")
    st.caption("Region: Northern Pakistan")

    st.divider()

    st.markdown("##### AI CONNECTION")

    if get_api_key():
        st.markdown(
            '<span class="status-pill status-good">● API KEY CONFIGURED</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<span class="status-pill status-warning">● API KEY REQUIRED</span>',
            unsafe_allow_html=True
        )

    st.caption("xAI API usage may incur charges.")


# =========================================================
# 6. WORKSPACE ONE: INFRASTRUCTURE DASHBOARD
# =========================================================

if app_mode == "Infrastructure Dashboard":

    st.markdown(
        '<div class="eyebrow">STRATEGIC INFRASTRUCTURE INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">Regional Allocation Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">'
        'Monitor simulated regional capacity, evaluate demand pressure '
        'and explore infrastructure redistribution opportunities.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # Problem statement
    st.markdown("""
    <div class="panel-card">
        <div class="eyebrow">THE BUSINESS CHALLENGE</div>
        <div class="section-heading">Uneven Regional Resource Distribution</div>
        <p style="font-size:13px;line-height:1.8;margin-bottom:0;">
        Seasonal tourism demand can create pressure on electricity,
        food distribution, waste management and transportation.
        EcoRoute AI provides a simulation environment to explore
        more balanced infrastructure and resource allocation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Optimization controls
    st.markdown(
        '<div class="section-heading">Optimization Parameters</div>',
        unsafe_allow_html=True
    )

    col_controls, col_map = st.columns([0.85, 1.5], gap="large")

    with col_controls:

        st.markdown("##### Regional Configuration")

        target_cluster = st.selectbox(
            "Target regional node",
            list(NODES.keys())[1:]
        )

        demand_load = st.slider(
            "Simulated demand pressure",
            min_value=40,
            max_value=150,
            value=95,
            help="Relative demand index. This is a simulation input."
        )

        capacity_buffer = st.slider(
            "Available supply capacity",
            min_value=10,
            max_value=100,
            value=80,
            help="Relative supply capacity index. This is a simulation input."
        )

        # Transparent ratio rather than an unvalidated efficiency claim
        coverage_ratio = round(
            (capacity_buffer / demand_load) * 100, 1
        )

        status, status_class = get_efficiency_status(coverage_ratio)

        st.markdown("---")

        st.markdown("##### Capacity Coverage")

        st.markdown(
            f'<div class="panel-value">{coverage_ratio}%</div>'
            f'<div class="panel-note">Supply capacity / demand index</div>'
            f'<span class="status-pill {status_class}">{status}</span>',
            unsafe_allow_html=True
        )

        st.progress(min(coverage_ratio / 100, 1.0))

        st.caption(
            "A ratio below 100% indicates that simulated supply "
            "capacity is below simulated demand."
        )

    with col_map:

        st.markdown(
            '<div class="section-heading">Regional Allocation Network</div>',
            unsafe_allow_html=True
        )

        st.caption("Lahore supply core → Selected regional destination")

        try:
            map_fig = create_allocation_map(target_cluster)

            st.plotly_chart(
                map_fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        except Exception as error:
            st.error(f"Map rendering error: {error}")

    # KPI section
    st.markdown("##### Operational Overview")

    k1, k2, k3 = st.columns(3)

    k1.metric("Regional Nodes", len(NODES))
    k2.metric("Demand Pressure", f"{demand_load}/150")
    k3.metric("Supply Capacity", f"{capacity_buffer}/100")

    st.caption(
        "All dashboard values are simulated. They are not verified "
        "regional infrastructure measurements or live traffic data."
    )


# =========================================================
# 7. WORKSPACE TWO: CORPORATE AI ADVISOR
# =========================================================

elif app_mode == "Corporate AI Advisor":

    st.markdown(
        '<div class="eyebrow">ENTERPRISE ADVISORY TERMINAL</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">Pandy AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">'
        'Corporate strategy, infrastructure planning and innovation advisory.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # API configuration
    api_key = get_api_key()

    if not api_key:

        with st.expander("Configure xAI API connection", expanded=True):

            st.info(
                "Add GROK_API_KEY to Streamlit Secrets for deployment, "
                "or enter a temporary key for this session."
            )

            temporary_key = st.text_input(
                "xAI API Key",
                type="password",
                placeholder="Enter your xAI API key",
                key="api_key_input"
            )

            if st.button("Connect API", use_container_width=True):

                if temporary_key.strip():
                    st.session_state.temporary_api_key = temporary_key.strip()
                    st.success("API key saved for this session.")
                    st.rerun()
                else:
                    st.warning("Enter a valid API key.")

            api_key = get_api_key()

    else:

        st.markdown(
            '<span class="status-pill status-good">● AI CONNECTION CONFIGURED</span>',
            unsafe_allow_html=True
        )

    st.write("")

    # Quick prompts
    st.markdown("##### Suggested Strategy Queries")

    quick_col1, quick_col2 = st.columns(2)

    selected_query = None

    with quick_col1:
        if st.button(
            "Overtourism & Supply Chains",
            use_container_width=True
        ):
            selected_query = (
                "Develop a comprehensive strategy to mitigate "
                "overtourism-related supply chain pressure in "
                "Northern Pakistan. Include resource redistribution, "
                "stakeholder coordination and implementation KPIs."
            )

    with quick_col2:
        if st.button(
            "Regional Economic Development",
            use_container_width=True
        ):
            selected_query = (
                "How can innovation management and public-private "
                "partnerships reduce seasonal economic volatility "
                "and localized resource inflation in tourism-dependent "
                "rural communities?"
            )

    # Conversation display
    st.markdown("---")
    st.markdown("##### Advisory Conversation")

    for message in st.session_state.solution_messages:

        avatar = "🐼" if message["role"] == "assistant" else "👤"

        with st.chat_message(
            message["role"],
            avatar=avatar
        ):
            st.markdown(message["content"])

    # Chat input
    user_input = st.chat_input(
        "Describe a business problem or infrastructure bottleneck..."
    )

    active_query = user_input or selected_query

    if active_query:

        # Prevent requests without API credentials
        if not api_key:

            st.warning(
                "Configure your xAI API key before submitting a query."
            )

        else:

            # Save user message
            st.session_state.solution_messages.append(
                {
                    "role": "user",
                    "content": active_query
                }
            )

            with st.chat_message("user", avatar="👤"):
                st.markdown(active_query)

            # Generate AI response
            with st.chat_message("assistant", avatar="🐼"):

                with st.spinner(
                    "Analyzing the business problem..."
                ):

                    try:

                        answer = request_grok(
                            api_key,
                            st.session_state.solution_messages
                        )

                        st.markdown(answer)

                        st.session_state.solution_messages.append(
                            {
                                "role": "assistant",
                                "content": answer
                            }
                        )

                    except requests.exceptions.Timeout:

                        st.error(
                            "The xAI request timed out. "
                            "Please retry with a shorter query."
                        )

                        st.session_state.solution_messages.pop()

                    except requests.exceptions.RequestException as error:

                        st.error(f"Network connection error: {error}")

                        st.session_state.solution_messages.pop()

                    except ValueError:

                        st.error(
                            "The API returned an invalid response format."
                        )

                        st.session_state.solution_messages.pop()

                    except RuntimeError as error:

                        st.error(str(error))

                        st.session_state.solution_messages.pop()

                    except Exception as error:

                        st.error(
                            f"Unexpected application error: {error}"
                        )

                        st.session_state.solution_messages.pop()

    # Conversation controls
    st.markdown("---")

    clear_col, info_col = st.columns([1, 2])

    with clear_col:

        if st.button("Clear Conversation"):

            st.session_state.solution_messages = [
                {
                    "role": "assistant",
                    "content": "Conversation reset. What would you like to analyze?"
                }
            ]

            st.rerun()

    with info_col:

        st.caption(
            "AI recommendations are generated from your supplied "
            "information and are not verified live economic research."
        )


# =========================================================
# 8. APPLICATION FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;padding:12px 0;">
        <div style="color:#67E8F9;font-size:12px;font-weight:700;">
            ECOROUTE AI
        </div>
        <div style="color:#64748B;font-size:10px;margin-top:5px;">
            Infrastructure Intelligence • Strategic Resource Allocation
        </div>
        <div style="color:#475569;font-size:10px;margin-top:5px;">
            Decision-support simulation platform
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
