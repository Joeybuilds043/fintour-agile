"""Shared premium visitor and tourism-intelligence themes for VoyagePK."""
from __future__ import annotations
import streamlit as st


def apply_visitor_theme() -> None:
    if "voyage_theme" not in st.session_state:
        st.session_state["voyage_theme"] = "Light"
    mode = st.sidebar.selectbox("Appearance", ["Light", "Dark"], key="voyage_theme")
    dark = mode == "Dark"
    paper = "#0B1713" if dark else "#F4F2E9"
    ink = "#EAF1EA" if dark else "#18372C"
    surface = "rgba(23,43,35,.88)" if dark else "#FFFEF9"
    muted = "#B6C8BC" if dark else "#5D7166"
    line = "#2C493B" if dark else "#DDDCCF"
    sidebar = "linear-gradient(165deg,#061810 0%,#103A2A 58%,#1A4A37 100%)" if dark else "linear-gradient(165deg,#08291D 0%,#104631 58%,#1B6042 100%)"
    header = "rgba(11,23,19,.96)" if dark else "rgba(244,242,233,.96)"
    accent = "#C7A35B"
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
    :root{--voyage-paper:PAPER;--voyage-ink:INK;--voyage-accent:ACCENT;--voyage-surface:SURFACE;--voyage-muted:MUTED;--voyage-line:LINE}
    .stApp{background:var(--voyage-paper);color:var(--voyage-ink);font-family:'DM Sans',sans-serif}
    [data-testid="stHeader"]{background:HEADER}
    [data-testid="stSidebar"]{background:SIDEBAR;border-right:1px solid rgba(199,163,91,.35)}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,[data-testid="stSidebar"] strong,[data-testid="stSidebar"] label,[data-testid="stSidebar"] .stCaption{color:#EAF1EA!important}
    [data-testid="stSidebar"] [data-testid="stPageLink"] a{color:#F5F2E9!important;border-radius:11px;padding:.52rem .68rem;font-family:'DM Sans',sans-serif;font-size:13px;transition:all .22s ease}
    [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover{background:rgba(199,163,91,.18);color:#E9D6A7!important;transform:translateX(3px)}
    [data-testid="stSidebar"] hr{border-color:rgba(234,241,234,.18)}
    .block-container{max-width:1440px;padding-top:1.25rem;padding-bottom:4rem}
    h1,h2,h3{color:var(--voyage-ink)!important;font-family:'Playfair Display',Georgia,serif!important}
    p,li,label,.stCaption{color:var(--voyage-muted)}
    div[data-testid="stImage"] img{border-radius:17px;object-fit:cover;box-shadow:0 12px 30px rgba(4,24,16,.18);transition:transform .35s ease}
    div[data-testid="stImage"] img:hover{transform:translateY(-2px)}
    div[data-testid="stVerticalBlockBorderWrapper"]{background:var(--voyage-surface);border-color:var(--voyage-line);border-radius:18px;backdrop-filter:blur(14px)}
    div[data-testid="stButton"]>button{border-radius:28px;background:#14583B;color:#fff;border:1px solid #C7A35B;font-weight:650;min-height:42px}
    div[data-testid="stButton"]>button:hover{background:#1C7049;border-color:#D7B86E;color:#fff}
    [data-testid="stMetric"]{background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:14px;padding:12px;backdrop-filter:blur(14px)}
    a{color:var(--voyage-accent)}hr{border-color:var(--voyage-line)}footer{visibility:hidden}
    .voyage-brand{font-family:'Playfair Display',Georgia,serif;font-size:28px;color:#F7F3E8;font-weight:700}
    .voyage-brand-sub{font-family:'DM Sans',sans-serif;font-size:9px;letter-spacing:2.1px;text-transform:uppercase;color:#D9C58F;margin-top:3px}
    .horizon-flow{position:relative;overflow:hidden;border-radius:18px;background:linear-gradient(115deg,#0B2E23,#14583B 42%,#1D5B5B 72%,#263746);background-size:220% 220%;animation:horizon-current 18s ease-in-out infinite}
    @keyframes horizon-current{0%,100%{background-position:0% 45%}50%{background-position:100% 55%}}
    @media(prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important}}
    @media(max-width:700px){.block-container{padding:1rem 1rem 3rem}}
    </style>
    """.replace("PAPER",paper).replace("INK",ink).replace("ACCENT",accent).replace("SURFACE",surface).replace("MUTED",muted).replace("LINE",line).replace("HEADER",header).replace("SIDEBAR",sidebar), unsafe_allow_html=True)
    st.sidebar.markdown('<div class="voyage-brand">VoyagePK</div><div class="voyage-brand-sub">Pakistan Unbound</div>', unsafe_allow_html=True)
    st.sidebar.caption("Destination discovery · Itinerary planning · Tourism intelligence")


def apply_intelligence_theme() -> None:
    apply_visitor_theme()
    st.markdown("""
    <style>
    .block-container{max-width:1380px}
    [data-testid="stMetric"] label{font-family:'DM Sans',sans-serif;font-size:11px;letter-spacing:.5px}
    [data-testid="stMetricValue"]{font-family:'IBM Plex Mono',monospace!important;font-variant-numeric:tabular-nums}
    div[data-testid="stDataFrame"]{border:1px solid var(--voyage-line);border-radius:14px;overflow:hidden}
    </style>
    """, unsafe_allow_html=True)
