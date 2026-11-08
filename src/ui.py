"""Shared visual systems: visitor discovery and tourism intelligence."""
from __future__ import annotations

import streamlit as st


def apply_visitor_theme() -> None:
    """Editorial travel-magazine visual language for visitor-facing pages."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
    .stApp{background:#f7f5ef;color:#172f38;font-family:'DM Sans',sans-serif}
    [data-testid="stHeader"]{background:rgba(247,245,239,.94)}
    [data-testid="stSidebar"]{background:#f0eee7;border-right:1px solid #e7e2d8}
    .block-container{max-width:1420px;padding-top:1.25rem;padding-bottom:4rem}
    h1,h2,h3{color:#18343c!important;font-family:'Playfair Display',Georgia,serif!important}
    div[data-testid="stImage"] img{border-radius:17px;object-fit:cover;filter:saturate(1.08) contrast(1.04)}
    div[data-testid="stVerticalBlockBorderWrapper"]{background:#fffefa;border-color:#e7e2d8;border-radius:18px}
    div[data-testid="stButton"]>button{border-radius:30px;background:#176b70;color:white;border:1px solid #176b70;font-weight:700}
    [data-testid="stMetric"]{background:#fffefa;border:1px solid #e7e2d8;border-radius:14px;padding:12px}
    hr{border-color:#e7e2d8}footer{visibility:hidden}
    @media(max-width:700px){.block-container{padding:1rem}}
    </style>
    """, unsafe_allow_html=True)


def apply_intelligence_theme() -> None:
    """Restrained analytical visual language for tourism-industry workspaces."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
    .stApp{background:#f2f5f7;color:#172d3a;font-family:'DM Sans',sans-serif}
    [data-testid="stHeader"]{background:rgba(242,245,247,.95)}
    [data-testid="stSidebar"]{background:#e9eef1;border-right:1px solid #d6e0e5}
    .block-container{max-width:1380px;padding-top:1.3rem;padding-bottom:4rem}
    h1,h2,h3{color:#173447!important;font-weight:650}
    [data-testid="stMetric"]{background:#fff;border:1px solid #dce5e9;border-radius:12px;padding:13px}
    div[data-testid="stVerticalBlockBorderWrapper"]{background:#fff;border-color:#dce5e9;border-radius:14px}
    div[data-testid="stButton"]>button{background:#174b66;color:#fff;border:1px solid #174b66;border-radius:8px;font-weight:650}
    div[data-testid="stDataFrame"]{border:1px solid #dce5e9;border-radius:10px;overflow:hidden}
    hr{border-color:#dce5e9}footer{visibility:hidden}
    .stCaption{color:#607580}
    </style>
    """, unsafe_allow_html=True)
