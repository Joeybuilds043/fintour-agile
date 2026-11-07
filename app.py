from __future__ import annotations

import math
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk
import streamlit as st

st.set_page_config(
    page_title="FinTour Agile | Strategic Tourism & Finance Lab",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

BG = "#0B0F19"
PANEL = "#111827"
CYAN = "#00F2FE"
GOLD = "#D4AF37"
MUTED = "#94A3B8"
WHITE = "#F8FAFC"
RED = "#FB7185"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    :root {{ color-scheme: dark; }}
    html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}
    .stApp {{ background: radial-gradient(ellipse at 12% 0%, #14263a 0%, {BG} 42%); color: {WHITE}; }}
    [data-testid="stHeader"] {{ background: rgba(11,15,25,.72); }}
    [data-testid="stSidebar"] {{ background: rgba(10,15,26,.96); border-right: 1px solid rgba(0,242,254,.16); }}
    [data-testid="stMetric"] {{
      background: linear-gradient(145deg, rgba(24,36,54,.88), rgba(12,18,30,.86));
      border: 1px solid rgba(0,242,254,.18); border-radius: 16px;
      padding: 16px 18px; box-shadow: 0 12px 34px rgba(0,0,0,.22);
    }}
    [data-testid="stMetricLabel"] {{ color: {MUTED}; }}
    [data-testid="stMetricValue"] {{ color: {WHITE}; font-family: 'Space Grotesk', sans-serif; }}
    .hero {{
      padding: 28px 30px; border: 1px solid rgba(0,242,254,.28); border-radius: 22px;
      background: linear-gradient(115deg, rgba(16,34,51,.92), rgba(17,24,39,.78));
      box-shadow: 0 18px 55px rgba(0,0,0,.28); backdrop-filter: blur(18px);
      margin-bottom: 22px;
    }}
    .eyebrow {{ color: {CYAN}; letter-spacing: .19em; text-transform: uppercase; font-size: .72rem; font-weight: 700; }}
    .hero h1 {{ font-family: 'Space Grotesk', sans-serif; font-size: clamp(2rem,4vw,3.25rem); margin: 8px 0; color: {WHITE}; }}
    .hero p {{ color: #B7C4D6; max-width: 850px; margin-bottom: 0; }}
    .section-title {{ font-family: 'Space Grotesk',sans-serif; font-size: 1.35rem; font-weight: 700; margin: 8px 0 4px; }}
    .subtle {{ color: {MUTED}; font-size: .9rem; }}
    .glass {{
      background: rgba(17,24,39,.72); border: 1px solid rgba(212,175,55,.18);
      border-radius: 17px; padding: 18px 20px; backdrop-filter: blur(14px);
    }}
    .gold {{ color: {GOLD}; }} .cyan {{ color: {CYAN}; }}
    .chat-user {{ background: rgba(0,242,254,.09); border: 1px solid rgba(0,242,254,.2); border-radius: 14px 14px 4px 14px; padding: 12px 15px; margin: 8px 0 8px 12%; }}
    .chat-ai {{ background: rgba(212,175,55,.08); border: 1px solid rgba(212,175,55,.2); border-radius: 14px 14px 14px 4px; padding: 12px 15px; margin: 8px 12% 8px 0; }}
    .stButton > button, .stDownloadButton > button {{
      border: 1px solid rgba(0,242,254,.45); border-radius: 10px;
      background: linear-gradient(100deg, rgba(0,242,254,.12), rgba(212,175,55,.08));
      color: {WHITE}; font-weight: 600;
    }}
    .stButton > button:hover {{ border-color: {CYAN}; color: {CYAN}; }}
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, .stTextArea textarea {{
      background: #0F1725; border-color: rgba(148,163,184,.25); color: {WHITE};
    }}
    hr {{ border-color: rgba(148,163,184,.15); }}
    footer {{ visibility: hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def money(value: float, currency: str = "$") -> str:
    return f"{currency}{value:,.2f}"


def bond_price(
    face: float,
    coupon_rate: float,
    market_yield: float,
    years: int,
    frequency: int = 2,
) -> float:
    periods = max(1, int(years * frequency))
    periodic_yield = market_yield / frequency
    coupon = face * coupon_rate / frequency

    if periodic_yield <= -1:
        return float("nan")

    return (
        sum(
            coupon / (1 + periodic_yield) ** t
            for t in range(1, periods + 1)
        )
        + face / (1 + periodic_yield) ** periods
    )


def haversine_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    radius = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    )
    return 2 * radius * math.asin(math.sqrt(a))


def optimize_route(
    data: pd.DataFrame,
    start_index: int,
) -> tuple[list[int], float]:
    remaining = set(data.index.tolist())
    route: list[int] = []
    current = start_index
    total = 0.0

    while remaining:
        remaining.remove(current)
        route.append(current)

        if not remaining:
            break

        next_index = min(
            remaining,
            key=lambda idx: haversine_km(
                float(data.loc[current, "latitude"]),
                float(data.loc[current, "longitude"]),
                float(data.loc[idx, "latitude"]),
                float(data.loc[idx, "longitude"]),
            ),
        )

        total += haversine_km(
            float(data.loc[current, "latitude"]),
            float(data.loc[current, "longitude"]),
            float(data.loc[next_index, "latitude"]),
            float(data.loc[next_index, "longitude"]),
        )
        current = next_index

    return route, total


def pandy_reply(
    prompt: str,
    inventory: float,
    demand: float,
    lead_time: float,
    capacity: float,
) -> str:
    coverage = inventory / max(demand, 0.01)
    utilization = demand / max(capacity, 0.01) * 100

    if coverage < lead_time:
        action = (
            "Expedite the highest-priority replenishment and allocate scarce "
            "stock to the highest-margin or service-critical destinations."
        )
        risk = "Stockout exposure is elevated."
    elif utilization > 90:
        action = (
            "Smooth demand into available capacity, stagger dispatch windows, "
            "and confirm carrier slots before accepting incremental orders."
        )
        risk = "Capacity is the binding constraint."
    else:
        action = (
            "Maintain the replenishment cadence, monitor supplier variance, "
            "and keep a small buffer for demand spikes."
        )
        risk = "The entered scenario is within the basic operating envelope."

    return (
        f"Scenario readout: {risk} Estimated inventory cover is "
        f"{coverage:.1f} demand-days versus {lead_time:.1f} lead-time days; "
        f"capacity utilization is {utilization:.1f}%. Recommended next action: "
        f"{action} This is a rules-based demonstration using the values "
        f"entered in this session, not a live ERP feed or an autonomous "
        f"operational decision."
    )


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        (
            "assistant",
            "I am Pandy-AI, a supply-chain scenario assistant. Enter operating "
            "assumptions and ask about stockouts, lead times, capacity, or "
            "service levels. This demo does not connect to live supplier systems.",
        )
    ]


with st.sidebar:
    st.markdown(
        "## <span class='cyan'>✦ FINTOUR</span> "
        "<span class='gold'>AGILE</span>",
        unsafe_allow_html=True,
    )
    st.caption("Strategic Tourism • Finance • Operations")

    page = st.radio(
        "WORKSPACE",
        [
            "Executive Overview",
            "Yield Simulator",
            "Tourism Research Map",
            "Pandy-AI Operations",
        ],
        label_visibility="visible",
    )

    st.divider()
    st.caption("PROJECT OWNER")
    st.markdown("**Muhammad Asad**")
    st.caption("BS Hospitality | Financial markets research")
    st.caption(f"Session · {datetime.now().strftime('%d %b %Y, %H:%M')}")
    st.markdown("---")
    st.caption(
        "Research and educational decision-support prototype. "
        "Not investment advice."
    )


st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Strategic intelligence workspace / 01</div>
      <h1>FinTour <span style="color:#00F2FE">Agile</span></h1>
      <p>Connecting financial-market thinking, destination intelligence and
      operational resilience in one analytical workspace.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


if page == "Executive Overview":
    st.markdown(
        '<div class="section-title">Academic & professional snapshot</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtle">Profile figures are displayed as supplied by '
        'the project owner and should be reconciled against official '
        'transcripts and certificates before external publication.</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    records = [
        ("Matriculation", "1,010 / 1,100", "91.82%"),
        ("Intermediate", "921 / 1,100", "83.73%"),
        ("Undergraduate CGPA", "3.75", "As supplied"),
        ("Additional learning", "Harvard ALP", "Certificate / programme"),
    ]

    for col, (label, value, detail) in zip(cols, records):
        with col:
            st.metric(label, value)
            st.caption(detail)

    st.markdown("")
    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown(
            '<div class="section-title">Project thesis</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="glass">
              <div class="eyebrow">Applied research proposition</div>
              <h3 style="margin:8px 0;color:#F8FAFC">
                Tourism systems are capital-allocation systems.
              </h3>
              <p style="color:#B7C4D6">
                Destination performance depends on demand quality, seasonality,
                access, infrastructure capacity, visitor flows and the cost of
                capital. FinTour Agile turns these connected variables into
                transparent, inspectable scenarios rather than unsupported
                forecasts.
              </p>
              <p class="subtle">
                Research lineage: strategic financial-market analysis associated
                with Yale SOM and Robert J. Shiller's work on expectations,
                valuation and long-horizon market behaviour. This project is
                independent and is not affiliated with Yale or Professor Shiller.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            '<div class="section-title">Analytical modules</div>',
            unsafe_allow_html=True,
        )

        for title, desc in [
            (
                "01 / Yield sensitivity",
                "Bond pricing, duration-style sensitivity and inflation scenarios.",
            ),
            (
                "02 / Destination routing",
                "Upload geocoded research locations and calculate a heuristic visit sequence.",
            ),
            (
                "03 / Operational resilience",
                "Translate inventory, demand, lead-time and capacity assumptions into actions.",
            ),
        ]:
            st.markdown(
                f"<div class='glass' style='margin-bottom:10px'>"
                f"<b class='gold'>{title}</b><br>"
                f"<span class='subtle'>{desc}</span></div>",
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">Research integrity & data provenance</div>',
        unsafe_allow_html=True,
    )
    st.info(
        "No ResearchGate profile, publication metadata, transcript, or "
        "certificate file is connected to this repository. Upload source data "
        "in the relevant module; the dashboard does not invent citations, "
        "credentials, or live market observations."
    )


elif page == "Yield Simulator":
    st.markdown(
        '<div class="section-title">Strategic finance yield simulator</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtle">A Shiller-inspired long-horizon scenario tool. '
        'It is not a Yale product, a market-data terminal, or a forecast.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        face = st.number_input(
            "Bond face value",
            min_value=100.0,
            max_value=10000000.0,
            value=1000.0,
            step=100.0,
        )
        coupon = st.slider(
            "Annual coupon rate (%)",
            0.0,
            15.0,
            5.0,
            0.25,
        ) / 100

    with c2:
        years = st.slider("Time to maturity (years)", 1, 40, 10)
        base_yield = st.slider(
            "Base market yield (%)",
            0.1,
            20.0,
            4.5,
            0.1,
        ) / 100

    with c3:
        inflation = st.slider(
            "Expected inflation (%)",
            -2.0,
            15.0,
            2.5,
            0.1,
        ) / 100
        shock = st.slider(
            "Yield shock (%)",
            -5.0,
            8.0,
            1.0,
            0.1,
        ) / 100

    current_price = bond_price(face, coupon, base_yield, years)
    shocked_price = bond_price(face, coupon, base_yield + shock, years)
    real_yield = base_yield - inflation
    price_change = (
        (shocked_price / current_price - 1) * 100
        if current_price
        else 0
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        "Modelled bond price",
        money(current_price),
        f"{(current_price / face - 1) * 100:+.2f}% vs par",
    )
    m2.metric(
        "Price after yield shock",
        money(shocked_price),
        f"{price_change:+.2f}%",
    )
    m3.metric("Approx. real yield", f"{real_yield * 100:.2f}%")
    m4.metric("Nominal yield", f"{base_yield * 100:.2f}%")

    yields = np.linspace(
        max(-0.005, base_yield - 0.05),
        base_yield + 0.08,
        100,
    )
    prices = [
        bond_price(face, coupon, float(y), years)
        for y in yields
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=yields * 100,
            y=prices,
            mode="lines",
            name="Bond price",
            line=dict(color=CYAN, width=3),
            fill="tozeroy",
            fillcolor="rgba(0,242,254,.08)",
        )
    )
    fig.add_vline(
        x=base_yield * 100,
        line_dash="dash",
        line_color=GOLD,
        annotation_text="Base yield",
    )
    fig.add_vline(
        x=(base_yield + shock) * 100,
        line_dash="dot",
        line_color=RED,
        annotation_text="Scenario yield",
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,.35)",
        height=390,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Market yield (%)",
        yaxis_title="Present value",
        legend=dict(orientation="h"),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="section-title">Scenario interpretation</div>',
        unsafe_allow_html=True,
    )

    direction = (
        "rises"
        if price_change > 0
        else "falls"
        if price_change < 0
        else "is broadly unchanged"
    )
    color_class = "cyan" if price_change >= 0 else "gold"

    st.markdown(
        f"<div class='glass'>A {shock * 100:+.2f} percentage-point "
        f"parallel yield shock changes the modelled bond price by "
        f"<b class='{color_class}'>{price_change:+.2f}%</b>. Under this "
        f"fixed-cash-flow model, price {direction} as the discount rate "
        f"changes. The real-yield proxy is nominal yield minus the "
        f"user-entered expected inflation assumption "
        f"({inflation * 100:.2f}%). It is not a market-quoted real yield.</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "Model assumptions: fixed coupon, semi-annual payments, no default, "
        "no tax, no liquidity premium, no reinvestment risk, and a flat "
        "discount curve. Actual bond valuation requires instrument terms "
        "and market curves."
    )


elif page == "Tourism Research Map":
    st.markdown(
        '<div class="section-title">Tourism research geospatial lab</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtle">Upload a CSV exported or prepared from your '
        'research. ResearchGate does not provide an assumed public '
        'geospatial feed; coordinates must be present in your source data.</div>',
        unsafe_allow_html=True,
    )

    template = pd.DataFrame(
        columns=[
            "location_name",
            "latitude",
            "longitude",
            "category",
            "research_note",
        ]
    )

    st.download_button(
        "Download CSV template",
        template.to_csv(index=False).encode("utf-8"),
        "fintour_research_locations_template.csv",
        "text/csv",
    )

    upload = st.file_uploader(
        "Upload research locations (CSV)",
        type=["csv"],
    )

    if upload is None:
        st.markdown(
            "<div class='glass'><b class='gold'>Awaiting source data</b>"
            "<p class='subtle'>Required columns: location_name, latitude, "
            "longitude. Optional columns: category, research_note. No map "
            "markers or route are fabricated when no dataset is supplied.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        try:
            locations = pd.read_csv(upload)
            required = {
                "location_name",
                "latitude",
                "longitude",
            }
            missing = required.difference(locations.columns)

            if missing:
                st.error(
                    "Missing required columns: "
                    + ", ".join(sorted(missing))
                )
            else:
                locations["latitude"] = pd.to_numeric(
                    locations["latitude"],
                    errors="coerce",
                )
                locations["longitude"] = pd.to_numeric(
                    locations["longitude"],
                    errors="coerce",
                )
                locations = locations.dropna(
                    subset=["latitude", "longitude"]
                ).copy()

                locations = locations[
                    locations["latitude"].between(-90, 90)
                    & locations["longitude"].between(-180, 180)
                ].reset_index(drop=True)

                if len(locations) < 2:
                    st.warning(
                        "At least two valid coordinate rows are required "
                        "for route optimization."
                    )
                else:
                    if "category" not in locations:
                        locations["category"] = "Research location"
                    if "research_note" not in locations:
                        locations["research_note"] = ""

                    st.caption(
                        f"{len(locations)} valid locations loaded."
                    )

                    start_name = st.selectbox(
                        "Route starting point",
                        locations["location_name"].astype(str).tolist(),
                    )

                    start_idx = int(
                        locations.index[
                            locations["location_name"].astype(str)
                            == start_name
                        ][0]
                    )

                    order, distance = optimize_route(
                        locations,
                        start_idx,
                    )
                    routed = locations.loc[order].copy().reset_index(
                        drop=True
                    )
                    routed["sequence"] = np.arange(
                        1,
                        len(routed) + 1,
                    )

                    st.metric(
                        "Heuristic route distance",
                        f"{distance:,.1f} km",
                        "Straight-line estimate; not road distance",
                    )

                    st.dataframe(
                        routed[
                            [
                                "sequence",
                                "location_name",
                                "category",
                                "latitude",
                                "longitude",
                                "research_note",
                            ]
                        ],
                        use_container_width=True,
                        hide_index=True,
                    )

                    layer = pdk.Layer(
                        "ScatterplotLayer",
                        data=locations,
                        get_position="[longitude, latitude]",
                        get_radius=500,
                        get_fill_color=[0, 242, 254, 190],
                        pickable=True,
                    )

                    path_data = (
                        routed[["longitude", "latitude"]]
                        .values.tolist()
                    )

                    route_layer = pdk.Layer(
                        "PathLayer",
                        data=[{"path": path_data}],
                        get_path="path",
                        get_color=[212, 175, 55, 220],
                        width_scale=20,
                        width_min_pixels=3,
                        get_width=5,
                    )

                    view = pdk.ViewState(
                        latitude=float(locations["latitude"].mean()),
                        longitude=float(locations["longitude"].mean()),
                        zoom=8,
                        pitch=35,
                    )

                    st.pydeck_chart(
                        pdk.Deck(
                            layers=[route_layer, layer],
                            initial_view_state=view,
                            tooltip={"text": "{location_name}"},
                            map_style=(
                                "https://basemaps.cartocdn.com/gl/"
                                "dark-matter-gl-style/style.json"
                            ),
                        ),
                        use_container_width=True,
                    )

                    st.caption(
                        "The route uses a nearest-neighbour heuristic and "
                        "great-circle distances. It is not a globally optimal "
                        "route and does not account for road networks, travel "
                        "time, opening hours, traffic, safety, or transport mode."
                    )

        except Exception as exc:
            st.error(f"Could not read the uploaded CSV: {exc}")


elif page == "Pandy-AI Operations":
    st.markdown(
        '<div class="section-title">Pandy-AI | Supply-chain scenario desk</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtle">Interactive rules-based demonstration. It does '
        'not access live inventory, suppliers, ERP, logistics APIs, or '
        'external AI services.</div>',
        unsafe_allow_html=True,
    )

    a, b, c, d = st.columns(4)

    with a:
        inventory = st.number_input(
            "Available inventory (units)",
            min_value=0.0,
            value=1200.0,
            step=50.0,
        )
    with b:
        demand = st.number_input(
            "Daily demand (units)",
            min_value=1.0,
            value=300.0,
            step=10.0,
        )
    with c:
        lead_time = st.number_input(
            "Supplier lead time (days)",
            min_value=0.0,
            value=5.0,
            step=0.5,
        )
    with d:
        capacity = st.number_input(
            "Daily fulfilment capacity",
            min_value=1.0,
            value=400.0,
            step=10.0,
        )

    coverage = inventory / max(demand, 0.01)
    utilization = demand / max(capacity, 0.01) * 100

    x1, x2, x3 = st.columns(3)
    x1.metric("Inventory cover", f"{coverage:.1f} days")
    x2.metric("Capacity utilization", f"{utilization:.1f}%")
    x3.metric(
        "Lead-time gap",
        f"{coverage - lead_time:+.1f} days",
        "Cover less supplier lead time",
    )

    st.markdown(
        "<div class='glass'><span class='eyebrow'>PANDY-AI / "
        "DECISION SUPPORT</span><h3 style='margin:8px 0'>Operational "
        "scenario assistant</h3><span class='subtle'>Ask a question using "
        "the assumptions above. The response is generated by transparent "
        "local rules.</span></div>",
        unsafe_allow_html=True,
    )

    for role, message in st.session_state.chat_history:
        css = "chat-user" if role == "user" else "chat-ai"
        label = "YOU" if role == "user" else "PANDY-AI"

        st.markdown(
            f"<div class='{css}'><b class='"
            f"{'cyan' if role == 'user' else 'gold'}'>{label}</b><br>"
            f"{message}</div>",
            unsafe_allow_html=True,
        )

    with st.form("pandy_chat_form", clear_on_submit=True):
        prompt = st.text_input(
            "Message Pandy-AI",
            placeholder="How can I reduce stockout risk this week?",
        )
        submitted = st.form_submit_button("Analyse scenario")

    if submitted and prompt.strip():
        st.session_state.chat_history.append(
            ("user", prompt.strip())
        )
        response = pandy_reply(
            prompt.strip(),
            inventory,
            demand,
            lead_time,
            capacity,
        )
        st.session_state.chat_history.append(
            ("assistant", response)
        )
        st.rerun()

    if st.button("Reset conversation"):
        st.session_state.chat_history = []
        st.rerun()


st.markdown("---")
st.markdown(
    f"<div style='display:flex;justify-content:space-between;gap:12px;"
    f"flex-wrap:wrap;color:{MUTED};font-size:.78rem'>"
    f"<span>FINTOUR AGILE · STRATEGIC TOURISM & FINANCE LAB</span>"
    f"<span>Built as an independent research prototype · "
    f"{datetime.now(timezone.utc).year}</span></div>",
    unsafe_allow_html=True,
)
