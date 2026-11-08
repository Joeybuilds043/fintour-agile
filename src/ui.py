"""Shared editorial alpine design system and chart styling for VoyagePK."""
from __future__ import annotations

import streamlit as st


def apply_visitor_theme() -> None:
    if "voyage_theme" not in st.session_state:
        st.session_state["voyage_theme"] = "Light"
    mode = st.sidebar.selectbox("Appearance", ["Light", "Dark"], key="voyage_theme")
    dark = mode == "Dark"

    paper = "#07140F" if dark else "#F4F1E7"
    ink = "#F2F4EA" if dark else "#153A2A"
    body_ink = "#D4E8D8" if dark else "#174D34"
    surface = "rgba(17,39,29,.94)" if dark else "#FFFEF9"
    muted = "#C0D2C5" if dark else "#3F654D"
    line = "#315342" if dark else "#D8D4C6"
    sidebar = "linear-gradient(165deg,#020B07 0%,#092218 58%,#12412D 100%)" if dark else "linear-gradient(165deg,#061B12 0%,#0B3825 58%,#165238 100%)"
    header = "rgba(7,20,15,.97)" if dark else "rgba(244,241,231,.97)"
    chart_grid = "rgba(215,231,218,.13)" if dark else "rgba(25,68,45,.12)"

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Cormorant+Garamond:wght@500;600;700&display=swap');
    :root{
      --voyage-paper:PAPER;--voyage-ink:INK;--voyage-body-ink:BODYINK;
      --voyage-accent:#C7A35B;--voyage-surface:SURFACE;--voyage-muted:MUTED;
      --voyage-line:LINE;--voyage-grid:CHARTGRID;
    }
    .stApp{background:var(--voyage-paper);color:var(--voyage-ink);font-family:'Manrope',sans-serif}
    .voyage-night-sky{position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.82;
      background-image:radial-gradient(1.2px 1.2px at 8% 16%,rgba(255,255,255,.95) 55%,transparent 70%),radial-gradient(1px 1px at 18% 63%,rgba(210,232,255,.8) 55%,transparent 70%),radial-gradient(1.5px 1.5px at 32% 24%,rgba(255,255,255,.88) 55%,transparent 70%),radial-gradient(1px 1px at 46% 74%,rgba(255,255,255,.7) 55%,transparent 70%),radial-gradient(1.2px 1.2px at 61% 13%,rgba(255,255,255,.9) 55%,transparent 70%),radial-gradient(1px 1px at 73% 49%,rgba(210,232,255,.75) 55%,transparent 70%),radial-gradient(1.4px 1.4px at 86% 21%,rgba(255,255,255,.9) 55%,transparent 70%),radial-gradient(1px 1px at 94% 72%,rgba(255,255,255,.8) 55%,transparent 70%),radial-gradient(1px 1px at 54% 39%,rgba(255,255,255,.65) 55%,transparent 70%);background-size:100% 100%;background-repeat:no-repeat}
    .voyage-night-sky:after{content:"";position:absolute;top:9vh;right:11vw;width:46px;height:46px;border-radius:50%;background:radial-gradient(circle at 38% 36%,#F6E9B9 0 44%,transparent 47%);filter:drop-shadow(0 0 18px rgba(244,225,169,.34));opacity:.9}
    .stApp:before{
      content:"";position:fixed;z-index:0;pointer-events:none;left:-12vw;right:-12vw;bottom:-2vh;height:34vh;
      opacity:.075;background:linear-gradient(145deg,#174C36 0%,#347C62 48%,#C7A35B 100%);
      clip-path:polygon(0 68%,8% 47%,16% 62%,27% 24%,36% 56%,48% 8%,59% 58%,70% 22%,82% 62%,92% 39%,100% 66%,100% 100%,0 100%);
      animation:alpine-drift 34s ease-in-out infinite alternate;
    }
    @keyframes alpine-drift{0%{transform:translate3d(-2.5%,0,0) scale(1)}100%{transform:translate3d(2.5%,-2.2%,0) scale(1.035)}}
    .stApp [data-testid="stAppViewContainer"],.stApp [data-testid="stSidebar"],.stApp header{position:relative;z-index:1}
    [data-testid="stHeader"]{background:HEADER}
    [data-testid="stSidebar"]{background:SIDEBAR;border-right:1px solid rgba(199,163,91,.35)}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] strong,[data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption{color:#F0F3EA!important;opacity:1!important}
    [data-testid="stSidebar"] [data-testid="stPageLink"] a{
      color:#F5F2E9!important;border-radius:11px;padding:.56rem .72rem;
      font-family:'Manrope',sans-serif;font-size:13px;transition:all .22s ease
    }
    [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover{
      background:rgba(199,163,91,.18);color:#F3DDA9!important;transform:translateX(3px)
    }
    [data-testid="stSidebar"] hr{border-color:rgba(234,241,234,.18)}
    .block-container{max-width:1440px;padding-top:1.45rem;padding-bottom:4rem}
    h1,h2,h3{color:var(--voyage-ink)!important;font-family:'Cormorant Garamond',Georgia,serif!important;letter-spacing:-.35px}
    h1{font-size:clamp(2.5rem,4vw,3.8rem)!important;line-height:1.02!important}
    h2{font-size:clamp(2rem,3vw,2.8rem)!important}
    h3{font-size:1.65rem!important}
    p,li,label,[data-testid="stCaptionContainer"] p{color:var(--voyage-body-ink)!important;opacity:1!important}
    .stMarkdown,.stMarkdown p,.stMarkdown li{line-height:1.78}
    div[data-testid="stImage"] img{border-radius:17px;object-fit:cover;box-shadow:0 15px 38px rgba(2,16,10,.2);transition:transform .4s ease,filter .4s ease}
    div[data-testid="stImage"] img:hover{transform:translateY(-3px);filter:saturate(1.06)}
    div[data-testid="stVerticalBlockBorderWrapper"]{background:var(--voyage-surface);border-color:var(--voyage-line);border-radius:18px;backdrop-filter:blur(14px)}
    div[data-testid="stButton"]>button{border-radius:28px;background:#14583B;color:#fff;border:1px solid #C7A35B;font-weight:750;min-height:44px;letter-spacing:.15px}
    div[data-testid="stButton"]>button:hover{background:#1C7049;border-color:#E1C47C;color:#fff}
    [data-testid="stMetric"]{background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:14px;padding:13px;backdrop-filter:blur(14px)}
    [data-testid="stMetricLabel"]{color:var(--voyage-muted)!important;font-family:'Manrope',sans-serif}
    [data-testid="stMetricValue"]{color:var(--voyage-ink)!important;font-family:'Manrope',sans-serif;font-weight:800}
    [data-testid="stAlert"]{border-radius:14px}
    a{color:var(--voyage-accent)}hr{border-color:var(--voyage-line)}footer{visibility:hidden}
    .voyage-brand{font-family:'Cormorant Garamond',Georgia,serif;font-size:31px;color:#F7F3E8;font-weight:700;letter-spacing:.4px}
    .voyage-brand-sub{font-family:'Manrope',sans-serif;font-size:9px;letter-spacing:2.1px;text-transform:uppercase;color:#E4CD95;margin-top:3px}
    .horizon-flow{position:relative;overflow:hidden;border-radius:18px;background:linear-gradient(115deg,#0B2E23,#14583B 42%,#1D5B5B 72%,#263746);background-size:220% 220%;animation:horizon-current 18s ease-in-out infinite}
    @keyframes horizon-current{0%,100%{background-position:0% 45%}50%{background-position:100% 55%}}
    @media(prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important}}
    @media(max-width:700px){.block-container{padding:1rem 1rem 3rem}}
    </style>
    """.replace("PAPER",paper).replace("INK",ink).replace("BODYINK",body_ink)
       .replace("SURFACE",surface).replace("MUTED",muted).replace("LINE",line)
       .replace("CHARTGRID",chart_grid).replace("HEADER",header).replace("SIDEBAR",sidebar),
       unsafe_allow_html=True)
    if dark:
        st.markdown("<div class='voyage-night-sky' aria-hidden='true'></div>", unsafe_allow_html=True)
    st.sidebar.markdown(
        '<div class="voyage-brand">VoyagePK</div><div class="voyage-brand-sub">Pakistan Unbound</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.caption("Destination discovery · Itinerary planning · Tourism intelligence")


def style_plotly_figure(fig, *, height: int = 390):
    """Apply the same high-contrast editorial chart language in both themes."""
    dark = st.session_state.get("voyage_theme", "Light") == "Dark"
    ink = "#F0F3E9" if dark else "#173B2B"
    muted = "#C0D2C5" if dark else "#4B6855"
    grid = "rgba(215,231,218,.14)" if dark else "rgba(25,68,45,.13)"
    palette = ["#55B99A", "#D8B66E", "#63AFC0", "#B6D28C", "#D98F6D"]
    fig.update_layout(
        height=height,
        margin=dict(l=14, r=18, t=64, b=28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Manrope, sans-serif", color=ink, size=12),
        title=dict(font=dict(family="Cormorant Garamond, Georgia, serif", size=25, color=ink), x=0.015, xanchor="left"),
        colorway=palette,
        hoverlabel=dict(bgcolor="#10271D" if dark else "#173B2B", bordercolor="#C7A35B", font=dict(family="Manrope, sans-serif", color="#F7F3E8", size=12)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, bgcolor="rgba(0,0,0,0)", font=dict(color=muted)),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, showline=True, linecolor=grid, tickfont=dict(color=muted), title_font=dict(color=muted))
    fig.update_yaxes(showgrid=True, gridcolor=grid, zeroline=False, showline=False, tickfont=dict(color=muted), title_font=dict(color=muted), automargin=True)
    return fig


def apply_intelligence_theme() -> None:
    apply_visitor_theme()
    st.markdown("""
    <style>
    .block-container{max-width:1380px}
    [data-testid="stDataFrame"]{border:1px solid var(--voyage-line);border-radius:14px;overflow:hidden}
    </style>
    """, unsafe_allow_html=True)
