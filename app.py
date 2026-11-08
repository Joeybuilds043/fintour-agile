from __future__ import annotations
import os
import streamlit as st
from src.catalog import DESTINATIONS, EXPERIENCE_CATEGORIES
from src.services.media import get_commons_image

st.set_page_config(page_title="Horizon Tourism | Discover Pakistan", page_icon="✦", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
:root{--ink:#172b35;--muted:#64777b;--cream:#f7f5ef;--teal:#176b67}
.stApp{background:var(--cream);color:var(--ink);font-family:'DM Sans',sans-serif}
[data-testid="stHeader"]{background:rgba(247,245,239,.92)}
[data-testid="stSidebar"]{background:#f0eee6;border-right:1px solid #deded3}
.block-container{max-width:1440px;padding-top:1.7rem;padding-bottom:4rem}
h1,h2,h3{color:var(--ink)!important}
.hero-title{font-family:'Playfair Display',serif;font-size:clamp(38px,5vw,68px);line-height:1.03;letter-spacing:-1.7px;color:#17333a;margin:10px 0 14px}
.hero-copy{font-size:16px;line-height:1.8;color:#5c7072;max-width:600px}
.eyebrow{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--teal);font-weight:800}
.section-title{font-family:'Playfair Display',serif;font-size:32px;color:#19343a;margin:4px 0}
.soft-card{background:#fffefa;border:1px solid #e6e3d9;border-radius:17px;padding:16px;height:100%}
div[data-testid="stButton"]>button{border-radius:30px;border:1px solid #176b67;background:#176b67;color:white;font-weight:700;min-height:42px}
div[data-testid="stButton"]>button:hover{background:#0e5552;border-color:#0e5552;color:white}
[data-testid="stMetric"]{background:#fffefa;border:1px solid #e6e3d9;border-radius:14px;padding:12px}
hr{border-color:#e3e0d6}footer{visibility:hidden}
@media(max-width:700px){.hero-title{font-size:39px}.block-container{padding-top:1rem}}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## HORIZON")
    st.caption("DISCOVER PAKISTAN")
    st.markdown("A destination discovery and tourism intelligence prototype.")
    st.divider()
    st.page_link("app.py", label="Home", icon="🏡")
    st.page_link("pages/01_Discover_Pakistan.py", label="Discover Pakistan", icon="🧭")
    st.page_link("pages/02_Destination_Guide.py", label="Destination guides", icon="📍")
    st.page_link("pages/03_Trip_Planner.py", label="Plan a journey", icon="🗺️")
    st.page_link("pages/04_Explore_Map.py", label="Explore map", icon="🌐")
    st.caption("Discover responsibly · Travel thoughtfully · Support local")

hero = None if os.getenv("HORIZON_DISABLE_REMOTE_MEDIA") == "1" else get_commons_image("Hunza Valley Pakistan mountains lake")
left, right = st.columns([1.08, 1], gap="large", vertical_alignment="center")
with left:
    st.markdown('<div class="eyebrow">A NEW WAY TO EXPERIENCE PAKISTAN</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Find your place<br>in Pakistan.</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-copy">From high mountain trails and quiet valleys to living heritage, coastal landscapes and unforgettable food — discover the experiences that make Pakistan extraordinary.</div>', unsafe_allow_html=True)
    st.page_link("pages/01_Discover_Pakistan.py", label="Explore destinations →", icon="🧭")
    st.caption("Discover responsibly · Travel thoughtfully · Support local")
with right:
    if hero:
        st.image(hero["thumb_url"], use_container_width=True)
        st.caption(f'{hero["title"]} · {hero["license"]} · {hero["artist"]} · [Source]({hero["page_url"]})')
    else:
        st.markdown('<div style="background:linear-gradient(135deg,#d6e6df,#a9c8bf);border-radius:22px;padding:70px 25px;text-align:center;color:#214c4b"><div style="font-size:54px">🏔️</div><h2>Pakistan, waiting to be explored</h2><p>Destination photography loads from openly licensed Wikimedia Commons media.</p></div>', unsafe_allow_html=True)

st.markdown('<div class="eyebrow">CHOOSE YOUR KIND OF JOURNEY</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Travel by experience</div>', unsafe_allow_html=True)
st.caption("Destinations can offer several types of tourism at once.")
cols = st.columns(5)
for i, category in enumerate(EXPERIENCE_CATEGORIES):
    with cols[i % 5]:
        st.markdown(f'<div class="soft-card" style="margin-bottom:12px"><div style="font-size:25px">{category["icon"]}</div><div style="font-weight:700;margin-top:7px">{category["name"]}</div><div style="font-size:11px;color:#718184;margin-top:4px">{category["short"]}</div></div>', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">START EXPLORING</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Featured destinations</div>', unsafe_allow_html=True)
st.caption("Ten pilot destination clusters selected for geographic and experience diversity, not ranked by visitor numbers.")
cols = st.columns(4)
for col, name in zip(cols, ["Hunza Valley", "Skardu", "Lahore", "Chitral & Kalash Valleys"]):
    item = DESTINATIONS[name]
    with col:
        image = None if os.getenv("HORIZON_DISABLE_REMOTE_MEDIA") == "1" else get_commons_image(item["image_query"])
        if image:
            st.image(image["thumb_url"], use_container_width=True)
            st.caption(f'{image["license"]} · [Image source]({image["page_url"]})')
        st.markdown(f'**{name}**')
        st.caption(item["tagline"])
        st.page_link("pages/02_Destination_Guide.py", label="Explore guide →", icon="📍")
st.markdown('<div class="soft-card"><div class="eyebrow">THE HORIZON IDEA</div><div class="section-title">Discover more. Travel better. Grow tourism responsibly.</div><p>Horizon connects visitor discovery with destination knowledge and investment thinking. It aims to help visitors make informed choices while helping local businesses and destination managers understand tourism opportunities and constraints.</p></div>', unsafe_allow_html=True)
st.caption("Horizon is an independent prototype, not an official government tourism service. Verify travel, safety, access and booking details with responsible local authorities and providers.")
