"""Shared visual systems for visitor discovery and tourism intelligence."""
from __future__ import annotations

import streamlit as st


def apply_visitor_theme() -> None:
    """Apply the visitor-facing 60/30/10 palette: ivory, deep teal, copper."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
    :root{
      --horizon-paper:#F5F1E8;       /* 60%: warm limestone */
      --horizon-ink:#183B3B;         /* 30%: deep evergreen teal */
      --horizon-accent:#C47A50;     /* 10%: restrained copper */
      --horizon-surface:#FFFCF6;
      --horizon-muted:#687976;
      --horizon-line:#E5DED2;
    }
    .stApp{background:var(--horizon-paper);color:var(--horizon-ink);font-family:'DM Sans',sans-serif}
    [data-testid="stHeader"]{background:rgba(245,241,232,.96)}
    [data-testid="stSidebar"]{background:#EEE9DF;border-right:1px solid var(--horizon-line)}
    .block-container{max-width:1440px;padding-top:1.25rem;padding-bottom:4rem}
    h1,h2,h3{color:var(--horizon-ink)!important;font-family:'Playfair Display',Georgia,serif!important}
    p,li,label,.stCaption{color:var(--horizon-muted)}
    div[data-testid="stImage"] img{border-radius:18px;object-fit:cover;filter:saturate(1.06) contrast(1.035)}
    div[data-testid="stVerticalBlockBorderWrapper"]{background:var(--horizon-surface);border-color:var(--horizon-line);border-radius:18px}
    div[data-testid="stButton"]>button{border-radius:28px;background:var(--horizon-ink);color:#FFFCF6;border:1px solid var(--horizon-ink);font-weight:650;min-height:42px}
    div[data-testid="stButton"]>button:hover{background:var(--horizon-accent);border-color:var(--horizon-accent);color:#fff}
    [data-testid="stPageLink"] a{border-radius:28px}
    [data-testid="stMetric"]{background:var(--horizon-surface);border:1px solid var(--horizon-line);border-radius:14px;padding:12px}
    a{color:#A85F3C}
    hr{border-color:var(--horizon-line)}footer{visibility:hidden}
    @media(max-width:700px){.block-container{padding:1rem 1rem 3rem}}
    </style>
    """, unsafe_allow_html=True)


def apply_intelligence_theme() -> None:
    """Use the same brand colours in a denser, analytical workspace."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
    :root{--horizon-paper:#F3F0E9;--horizon-ink:#183B3B;--horizon-accent:#C47A50;--horizon-surface:#FFFCF6;--horizon-line:#E2DBD0}
    .stApp{background:var(--horizon-paper);color:var(--horizon-ink);font-family:'DM Sans',sans-serif}
    [data-testid="stHeader"]{background:rgba(243,240,233,.96)}
    [data-testid="stSidebar"]{background:#EAE5DC;border-right:1px solid var(--horizon-line)}
    .block-container{max-width:1380px;padding-top:1.3rem;padding-bottom:4rem}
    h1,h2,h3{color:var(--horizon-ink)!important;font-weight:650}
    [data-testid="stMetric"]{background:var(--horizon-surface);border:1px solid var(--horizon-line);border-radius:12px;padding:13px}
    div[data-testid="stVerticalBlockBorderWrapper"]{background:var(--horizon-surface);border-color:var(--horizon-line);border-radius:14px}
    div[data-testid="stButton"]>button{background:var(--horizon-ink);color:#fff;border:1px solid var(--horizon-ink);border-radius:8px;font-weight:650}
    div[data-testid="stButton"]>button:hover{background:var(--horizon-accent);border-color:var(--horizon-accent);color:#fff}
    div[data-testid="stDataFrame"]{border:1px solid var(--horizon-line);border-radius:10px;overflow:hidden}
    hr{border-color:var(--horizon-line)}footer{visibility:hidden}
    .stCaption{color:#687976}
    </style>
    """, unsafe_allow_html=True)
