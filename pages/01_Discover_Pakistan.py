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
        region_options = ["All regions"] + sorted({d["region"] for d in DESTINATIONS.values()})
        selected_region = st.selectbox("Region", region_options)
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
GENERAL_SECTIONS = [
    ("Heritage & historic cities", "Forts, old quarters, archaeological landscapes and cities shaped by centuries of exchange.",
     lambda n,d: "Culture & heritage" in d["experiences"] or "Archaeology & ancient civilizations" in d["experiences"]),
    ("Northern Pakistan", "Karakoram, Himalaya and Hindu Kush journeys — from accessible valleys to specialist high-altitude expeditions.",
     lambda n,d: d["region"] in {"Gilgit-Baltistan","Khyber Pakhtunkhwa","Azad Jammu & Kashmir"} and ("Nature & wildlife" in d["experiences"] or "Adventure" in d["experiences"])),
    ("Lakes, forests & wilderness", "Alpine lakes, forests, wetlands, plateaus and protected landscapes.",
     lambda n,d: "Nature & wildlife" in d["experiences"] or "Ecotourism" in d["experiences"]),
    ("Coast, desert & open landscapes", "Arabian Sea coastlines, desert routes and dramatic geological scenery.",
     lambda n,d: "Coastal & marine" in d["experiences"] or ("Camping & outdoors" in d["experiences"] and any(k in n.lower() for k in ["desert","cholistan","hingol","makran","kund","coast"]))),
    ("Food, craft & living culture", "Regional cuisine, markets, crafts and community-led cultural experiences.",
     lambda n,d: "Food & gastronomy" in d["experiences"] or "Rural & creative" in d["experiences"]),
]

def matches(name, item):
    if name in RELIGIOUS_ONLY:
        return False
    if selected_region != "All regions" and item["region"] != selected_region:
        return False
    if selected_experience != "All travel types" and selected_experience not in item["experiences"]:
        return False
    search_text = " ".join([name,item["region"],item["tagline"],item["overview"]," ".join(item["highlights"]), " ".join(item["experiences"])]).casefold()
    return not query.strip() or query.strip().casefold() in search_text

def destination_card(column, name, item, key_prefix):
    with column:
        with st.container(border=True):
            image = get_commons_image(item["image_query"])
            if image:
                rendered = get_display_image(image["thumb_url"], aspect_ratio=(16,9), focal_point=(0.5,0.5))
                st.image(rendered if rendered else image["thumb_url"], use_container_width=True)
                st.caption(f'{image["artist"]} · {image["license"]} · [Image source]({image["page_url"]})')
            else:
                st.markdown('<div class="atlas-card-image" style="background:linear-gradient(135deg,#173E2E,#456D66,#C7A35B);display:flex;align-items:center;justify-content:center;color:#F5F1E7">VOYAGEPK · DESTINATION ATLAS</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="atlas-card-meta">{item["region"]}</div><div class="atlas-card-title">{name}</div><div class="atlas-card-copy">{item["tagline"]}</div><div class="atlas-tags">{" · ".join(item["experiences"][:3])}</div>', unsafe_allow_html=True)
            if st.button("Explore destination", key=f"{key_prefix}_{name}", use_container_width=True):
                st.session_state["selected_destination"] = name
                st.switch_page("pages/02_Destination_Guide.py")

for section_index, (heading, description, selector) in enumerate(GENERAL_SECTIONS):
    items = [(n,d) for n,d in DESTINATIONS.items() if selector(n,d) and matches(n,d)]
    if not items:
        continue
    st.write("")
    st.markdown(f'<div class="atlas-kicker">EXPLORE BY JOURNEY · 0{section_index+1}</div><div class="atlas-section">{heading}</div><div class="atlas-section-copy">{description}</div>', unsafe_allow_html=True)
    items.sort(key=lambda pair: pair[0])
    for start in range(0,len(items),3):
        cols=st.columns(3,gap="large")
        for col,(name,item) in zip(cols,items[start:start+3]):
            destination_card(col,name,item,f"atlas_{section_index}")

st.caption(f"{len(DESTINATIONS)} destination clusters in the catalogue. Collections can overlap because one place may offer more than one type of experience.")

st.write("")
st.divider()
st.markdown('<div class="atlas-kicker">SACRED PLACES & RELIGIOUS HERITAGE</div><div class="atlas-section">Explore by faith and tradition</div><div class="atlas-section-copy">A dedicated collection for living sacred places, pilgrimage routes and religious archaeology. These are separated from general heritage and nature collections to avoid duplicate or misleading labels.</div>', unsafe_allow_html=True)
tradition_labels = {
    "Islamic & Sufi heritage": "Mosques, shrines, Sufi centres and sacred architecture",
    "Sikh pilgrimage": "Gurdwaras and places associated with Sikh history",
    "Buddhist heritage": "Gandharan monasteries, stupas and Buddhist landscapes",
    "Hindu heritage": "Temples, sacred landscapes and Hindu pilgrimage",
}
tradition_cols=st.columns(4,gap="medium")
for col,(tradition,desc) in zip(tradition_cols,tradition_labels.items()):
    names=[n for n,d in DESTINATIONS.items() if tradition in d["experiences"]]
    with col:
        st.markdown(f'<div class="atlas-tradition"><div class="atlas-tradition-name">{tradition}</div><div class="atlas-tradition-count">{len(names)} destination references</div><div class="atlas-card-copy">{desc}</div></div>',unsafe_allow_html=True)

for tradition in tradition_labels:
    names=[(n,d) for n,d in DESTINATIONS.items() if tradition in d["experiences"]]
    names.sort(key=lambda pair:pair[0])
    st.write("")
    st.markdown(f'<div class="atlas-kicker">{tradition.upper()}</div><div class="atlas-section">{tradition}</div>',unsafe_allow_html=True)
    for start in range(0,len(names),3):
        cols=st.columns(3,gap="large")
        for col,(name,item) in zip(cols,names[start:start+3]):
            destination_card(col,name,item,"faith_"+tradition.split()[0].lower())

st.write("")
st.markdown("### Travel advisory and access checks")
st.markdown("Destination discovery is not a safety clearance. Conditions can change quickly, particularly in remote mountain, border, coastal and security-sensitive areas. Check official government advisories, local administration notices, weather and road status immediately before travel.")
advisory_cols=st.columns(3,gap="medium")
with advisory_cols[0]:
    st.markdown("**UK Foreign Office (FCDO)**")
    st.link_button("Pakistan regional travel advice","https://www.gov.uk/foreign-travel-advice/pakistan/regional-risks",use_container_width=True)
with advisory_cols[1]:
    st.markdown("**US Department of State**")
    st.link_button("Pakistan travel advisory","https://travel.state.gov/en/international-travel/travel-advisories/pakistan.html",use_container_width=True)
with advisory_cols[2]:
    st.markdown("**Gilgit-Baltistan Tourism Department**")
    st.link_button("Official tourism updates","https://e-tourism.visitgilgitbaltistan.gov.pk/plan-trip/news-and-updates",use_container_width=True)

st.caption("VoyagePK is an independent discovery prototype, not an official tourism or security authority. Destination clusters and map anchors are editorial approximations. Never interpret a destination listing as confirmation that travel is currently safe, open or permitted.")
