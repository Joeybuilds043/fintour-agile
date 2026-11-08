"""Shared visual systems for visitor discovery and tourism intelligence."""
from __future__ import annotations
import streamlit as st

def apply_visitor_theme() -> None:
    """Premium editorial travel theme with a dark, legible navigation rail."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
    :root{--horizon-paper:#F4F0E7;--horizon-ink:#173B3A;--horizon-accent:#B77B54;--horizon-surface:#FFFCF6;--horizon-muted:#657875;--horizon-line:#E4DCCE}
    .stApp{background:var(--horizon-paper);color:var(--horizon-ink);font-family:'DM Sans',sans-serif}
    [data-testid="stHeader"]{background:rgba(244,240,231,.94)}
    [data-testid="stSidebar"]{background:linear-gradient(165deg,#102F31 0%,#174342 58%,#1B4D4A 100%);border-right:1px solid #315A58}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,[data-testid="stSidebar"] strong,[data-testid="stSidebar"] label,[data-testid="stSidebar"] .stCaption{color:#E8E6DC!important}
    [data-testid="stSidebar"] [data-testid="stPageLink"] a{color:#F4F0E7!important;border-radius:10px;padding:.48rem .62rem;transition:all .22s ease}
    [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover{background:rgba(217,167,126,.16);color:#F2C9A7!important;transform:translateX(3px)}
    [data-testid="stSidebar"] hr{border-color:rgba(232,230,220,.18)}
    .block-container{max-width:1440px;padding-top:1.25rem;padding-bottom:4rem}
    h1,h2,h3{color:var(--horizon-ink)!important;font-family:'Playfair Display',Georgia,serif!important}
    p,li,label,.stCaption{color:var(--horizon-muted)}
    div[data-testid="stImage"] img{border-radius:17px;object-fit:cover;box-shadow:0 10px 28px rgba(23,59,58,.10);transition:transform .35s ease,box-shadow .35s ease}
    div[data-testid="stImage"] img:hover{transform:translateY(-2px);box-shadow:0 16px 34px rgba(23,59,58,.15)}
    div[data-testid="stVerticalBlockBorderWrapper"]{background:var(--horizon-surface);border-color:var(--horizon-line);border-radius:18px}
    div[data-testid="stButton"]>button{border-radius:28px;background:#173B3A;color:#FFFCF6;border:1px solid #173B3A;font-weight:650;min-height:42px;transition:all .2s ease}
    div[data-testid="stButton"]>button:hover{background:#B77B54;border-color:#B77B54;color:#fff;transform:translateY(-1px)}
    [data-testid="stMetric"]{background:var(--horizon-surface);border:1px solid var(--horizon-line);border-radius:14px;padding:12px}
    a{color:#98613F}hr{border-color:var(--horizon-line)}footer{visibility:hidden}
    .horizon-brand{font-family:'Playfair Display',Georgia,serif;font-size:29px;color:#F4F0E7;font-weight:700}
    .horizon-brand-sub{font-size:9px;letter-spacing:1.8px;text-transform:uppercase;color:#B9CCC4;margin-top:2px}
    .horizon-flow{position:relative;overflow:hidden;border-radius:18px;background:linear-gradient(115deg,#123638,#1B4D4A 42%,#2C6660 72%,#173B3A);background-size:220% 220%;animation:horizon-current 18s ease-in-out infinite}
    .horizon-flow:after{content:"";position:absolute;inset:0;pointer-events:none;opacity:.23;background:repeating-linear-gradient(164deg,transparent 0 34px,rgba(221,239,226,.16) 35px,transparent 37px,transparent 68px);background-size:180% 180%;animation:horizon-river 24s linear infinite}
    @keyframes horizon-current{0%,100%{background-position:0% 45%}50%{background-position:100% 55%}}
    @keyframes horizon-river{from{background-position:0 0}to{background-position:240px 120px}}
    @media(prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important}}
    @media(max-width:700px){.block-container{padding:1rem 1rem 3rem}}
    </style>
    """, unsafe_allow_html=True)

def apply_intelligence_theme() -> None:
    """Apply the brand palette in a denser analytical workspace."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
    :root{--horizon-paper:#F1EEE6;--horizon-ink:#173B3A;--horizon-accent:#B77B54;--horizon-surface:#FFFCF6;--horizon-line:#E1D9CC}
    .stApp{background:var(--horizon-paper);color:var(--horizon-ink);font-family:'DM Sans',sans-serif}
    [data-testid="stHeader"]{background:rgba(241,238,230,.96)}
    [data-testid="stSidebar"]{background:linear-gradient(165deg,#102F31,#174342);border-right:1px solid #315A58}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,[data-testid="stSidebar"] label,[data-testid="stSidebar"] .stCaption{color:#E8E6DC!important}
    [data-testid="stSidebar"] [data-testid="stPageLink"] a{color:#F4F0E7!important;border-radius:10px}
    [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover{background:rgba(217,167,126,.16);color:#F2C9A7!important}
    .block-container{max-width:1380px;padding-top:1.3rem;padding-bottom:4rem}
    h1,h2,h3{color:var(--horizon-ink)!important;font-weight:650}
    [data-testid="stMetric"]{background:var(--horizon-surface);border:1px solid var(--horizon-line);border-radius:12px;padding:13px}
    div[data-testid="stVerticalBlockBorderWrapper"]{background:var(--horizon-surface);border-color:var(--horizon-line);border-radius:14px}
    div[data-testid="stButton"]>button{background:var(--horizon-ink);color:#fff;border:1px solid var(--horizon-ink);border-radius:8px;font-weight:650}
    div[data-testid="stButton"]>button:hover{background:var(--horizon-accent);border-color:var(--horizon-accent);color:#fff}
    div[data-testid="stDataFrame"]{border:1px solid var(--horizon-line);border-radius:10px;overflow:hidden}
    hr{border-color:var(--horizon-line)}footer{visibility:hidden}.stCaption{color:#657875}
    </style>
    """, unsafe_allow_html=True)
