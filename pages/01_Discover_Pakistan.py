from __future__ import annotations

import streamlit as st

from src.catalog import DESTINATIONS, EXPERIENCE_CATEGORIES
from src.services.media import get_commons_image, get_display_image
from src.ui import apply_visitor_theme

st.set_page_config(page_title="Discover Pakistan | VoyagePK", page_icon=None, layout="wide")
apply_visitor_theme()

st.markdown("""
<style>
.atlas-kicker{font-size:10px;letter-spacing:2.2px;text-transform:uppercase;color:#C7A35B;font-weight:800}
.atlas-lede{max-width:900px;font-size:15px;line-height:1.8;color:var(--voyage-body-ink)}
.atlas-section{font-family:'Cormorant Garamond',Georgia,serif;font-size:clamp(32px,3.2vw,44px);font-weight:700;line-height:1.05;color:var(--voyage-ink);margin:0}
.atlas-section-copy{max-width:850px;color:var(--voyage-body-ink);font-size:13px;line-height:1.75}
.atlas-card-title{font-family:'Cormorant Garamond',Georgia,serif;font-size:25px;line-height:1.08;font-weight:700;color:var(--voyage-ink);min-height:54px;margin:8px 0 4px}
.atlas-card-meta{font-size:9px;letter-spacing:1.45px;text-transform:uppercase;color:var(--voyage-muted);font-weight:800}
.atlas-card-copy{font-size:12px;line-height:1.65;color:var(--voyage-body-ink);min-height:60px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.atlas-tags{font-size:10px;line-height:1.5;color:var(--voyage-muted);min-height:30px;margin-top:8px}
.atlas-card-image{height:190px;overflow:hidden;border-radius:13px}
div[data-testid="stImage"] img{height:190px;object-fit:cover;border-radius:13px}
div[data-testid="stVerticalBlockBorderWrapper"]{height:100%;background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:18px}
div[data-testid="stButton"]>button{width:100%;min-height:42px;border-radius:24px}
.atlas-tradition{border:1px solid var(--voyage-line);border-radius:15px;background:var(--voyage-surface);padding:14px 16px;min-height:105px}
.atlas-tradition-name{font-family:'Cormorant Garamond',Georgia,serif;font-size:21px;font-weight:700;color:var(--voyage-ink)}
.atlas-tradition-count{font-size:10px;letter-spacing:1.1px;color:var(--voyage-muted);text-transform:uppercase}
@media(max-width:700px){.atlas-card-title{font-size:22px}.atlas-section{font-size:32px}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="atlas-kicker">VOYAGEPK · PAKISTAN UNBOUND</div>', unsafe_allow_html=True)
st.title("Discover Pakistan")
st.markdown('<div class="atlas-lede">Start with the kind of journey you want: historic cities, mountain country, lakes and forests, coastlines, food and living culture. Then explore religious and sacred heritage in its own dedicated collection.</div>', unsafe_allow_html=True)
st.write("")

with st.container(border=True):
    f1, f2, f3 = st.columns([1.0, 1.0, 1.5], gap="medium")
    with f1:
        province_options = ["All provinces & territories"] + [
            province for province in __import__("src.catalog", fromlist=["PROVINCE_ORDER"]).PROVINCE_ORDER
            if any(d.get("province") == province for d in DESTINATIONS.values())
        ]
        selected_province = st.selectbox("Province / territory", province_options)
    with f2:
        excluded = {"Islamic & Sufi heritage", "Sikh pilgrimage", "Buddhist heritage", "Hindu heritage", "Religious & archaeology"}
        experiences = ["All travel types"] + [x["name"] for x in EXPERIENCE_CATEGORIES if x["name"] not in excluded]
        selected_experience = st.selectbox("Travel type", experiences)
    with f3:
        query = st.text_input("Search destinations", placeholder="Hunza, K2, Lahore, lakes, forts, food…")

RELIGIOUS_ONLY = {
    "Nankana Sahib & Sikh Heritage", "Kartarpur Sahib & Narowal",
    "Hasan Abdal & Panja Sahib", "Swat Buddhist Heritage Circuit",
    "Takht-i-Bahi & Sahr-i-Bahlol", "Katas Raj Temples & Salt Range",
    "Hinglaj Mata & Hingol",
}
PROVINCE_SECTIONS = [
    province for province in __import__("src.catalog", fromlist=["PROVINCE_ORDER"]).PROVINCE_ORDER
    if any(item.get("province") == province for item in DESTINATIONS.values())
]
for section_index, province in enumerate(PROVINCE_SECTIONS):
    items = [(n, d) for n, d in DESTINATIONS.items()
             if d.get("province", d["region"]) == province and matches(n, d)]
    if not items:
        continue
    st.write("")
    st.markdown(
        f'<div class="atlas-kicker">DESTINATION COLLECTION · 0{section_index+1}</div>'
        f'<div class="atlas-section">{province}</div>'
        f'<div class="atlas-section-copy">Explore destination clusters across {province}. '
        'Individual places may offer several types of experience.</div>',
        unsafe_allow_html=True,
    )
    items.sort(key=lambda pair: pair[0])
    for start in range(0, len(items), 3):
        cols = st.columns(3, gap="large")
        for col, (name, item) in zip(cols, items[start:start+3]):
            destination_card(col, name, item, f"province_{section_index}")

