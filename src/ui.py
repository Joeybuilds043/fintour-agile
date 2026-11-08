"""Shared visual systems for VoyagePK visitor and tourism intelligence experiences."""
from __future__ import annotations
import streamlit as st

def apply_visitor_theme() -> None:
    if "voyage_theme" not in st.session_state:
        st.session_state["voyage_theme"] = "Light"
    mode = st.sidebar.selectbox("Appearance", ["Light", "Dark"], key="voyage_theme")
    dark = mode == "Dark"
    paper = "#101D2B" if dark else "#F5F1E8"
    ink = "#EAF0F3" if dark else "#263746"
    surface = "rgba(30,46,61,.82)" if dark else "#FFFCF6"
    muted = "#B6C5CC" if dark else "#657875"
    line = "#344B5B" if dark else "#E4DCCE"
    sidebar = "linear-gradient(165deg,#0B1724,#172B3C,#203B4B)" if dark else "linear-gradient(165deg,#17334A,#24566A,#2A7778)"
    header = "rgba(16,29,43,.94)" if dark else "rgba(245,241,232,.94)"
    accent = "#C3A66B" if dark else "#2A7778"
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
    :root{--voyage-paper:PAPER;--voyage-ink:INK;--voyage-accent:ACCENT;--voyage-surface:SURFACE;--voyage-muted:MUTED;--voyage-line:LINE}
    .stApp{background:var(--voyage-paper);color:var(--voyage-ink);font-family:'DM Sans',sans-serif}
    [data-testid="stHeader"]{background:HEADER}
    [data-testid="stSidebar"]{background:SIDEBAR;border-right:1px solid LINE}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,[data-testid="stSidebar"] strong,[data-testid="stSidebar"] label,[data-testid="stSidebar"] .stCaption{color:#EAF0F3!important}
    [data-testid="stSidebar"] [data-testid="stPageLink"] a{color:#F5F1E8!important;border-radius:10px;padding:.48rem .62rem;transition:all .22s ease}
    [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover{background:rgba(195,166,107,.17);color:#E8D6A8!important;transform:translateX(3px)}
    [data-testid="stSidebar"] hr{border-color:rgba(232,240,243,.18)}
    .block-container{max-width:1440px;padding-top:1.25rem;padding-bottom:4rem}
    h1,h2,h3{color:var(--voyage-ink)!important;font-family:'Playfair Display',Georgia,serif!important}
    p,li,label,.stCaption{color:var(--voyage-muted)}
    div[data-testid="stImage"] img{border-radius:17px;object-fit:cover;box-shadow:0 10px 28px rgba(9,24,37,.16);transition:transform .35s ease}
    div[data-testid="stImage"] img:hover{transform:translateY(-2px)}
    div[data-testid="stVerticalBlockBorderWrapper"]{background:var(--voyage-surface);border-color:var(--voyage-line);border-radius:18px;backdrop-filter:blur(14px)}
    div[data-testid="stButton"]>button{border-radius:28px;background:ACCENT;color:#fff;border:1px solid ACCENT;font-weight:650;min-height:42px}
    [data-testid="stMetric"]{background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:14px;padding:12px;backdrop-filter:blur(14px)}
    a{color:ACCENT}hr{border-color:var(--voyage-line)}footer{visibility:hidden}
    .horizon-brand,.voyage-brand{font-family:'Playfair Display',Georgia,serif;font-size:27px;color:#F5F1E8;font-weight:700}
    .horizon-brand-sub,.voyage-brand-sub{font-size:9px;letter-spacing:1.8px;text-transform:uppercase;color:#C6D5D9;margin-top:3px}
    .horizon-flow{position:relative;overflow:hidden;border-radius:18px;background:linear-gradient(115deg,#17334A,#24566A 42%,#2A7778 72%,#263746);background-size:220% 220%;animation:horizon-current 18s ease-in-out infinite}
    @keyframes horizon-current{0%,100%{background-position:0% 45%}50%{background-position:100% 55%}}
    @media(prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important}}
    @media(max-width:700px){.block-container{padding:1rem 1rem 3rem}}
    </style>
    """.replace("PAPER",paper).replace("INK",ink).replace("ACCENT",accent).replace("SURFACE",surface).replace("MUTED",muted).replace("LINE",line).replace("HEADER",header).replace("SIDEBAR",sidebar), unsafe_allow_html=True)
    st.sidebar.markdown('<div class="voyage-brand">VoyagePK</div><div class="voyage-brand-sub">Pakistan Unbound</div>', unsafe_allow_html=True)
    st.sidebar.caption("Travel discovery · Planning · Tourism intelligence")

def apply_intelligence_theme() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
    .stApp{background:#F1EEE6;color:#263746;font-family:'DM Sans',sans-serif}
    [data-testid="stSidebar"]{background:linear-gradient(165deg,#10283A,#1C5260);border-right:1px solid #315A68}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,[data-testid="stSidebar"] label,[data-testid="stSidebar"] .stCaption{color:#E8EEF0!important}
    .block-container{max-width:1380px;padding-top:1.3rem;padding-bottom:4rem}
    h1,h2,h3{color:#263746!important;font-weight:650}
    [data-testid="stMetric"]{background:#FFFCF6;border:1px solid #E1D9CC;border-radius:12px;padding:13px}
    div[data-testid="stVerticalBlockBorderWrapper"]{background:#FFFCF6;border-color:#E1D9CC;border-radius:14px}
    div[data-testid="stButton"]>button{background:#263746;color:#fff;border:1px solid #263746;border-radius:8px;font-weight:650}
    div[data-testid="stButton"]>button:hover{background:#2A7778;border-color:#2A7778;color:#fff}
    hr{border-color:#E1D9CC}footer{visibility:hidden}
    .voyage-brand{font-family:'Playfair Display',Georgia,serif;font-size:27px;color:#F5F1E8;font-weight:700}
    .voyage-brand-sub{font-size:9px;letter-spacing:1.8px;text-transform:uppercase;color:#C6D5D9;margin-top:3px}
    </style>
    """, unsafe_allow_html=True)
    st.sidebar.markdown('<div class="voyage-brand">VoyagePK</div><div class="voyage-brand-sub">Pakistan Unbound · Intelligence</div>', unsafe_allow_html=True)
