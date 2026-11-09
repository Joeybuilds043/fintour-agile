from __future__ import annotations

import streamlit as st

from src.catalog import DESTINATIONS, PROVINCE_ORDER
from src.services.media import get_commons_image, get_display_image
from src.ui import apply_visitor_theme

st.set_page_config(page_title="Discover Pakistan | VoyagePK", page_icon=None, layout="wide")
apply_visitor_theme()

st.markdown("""
<style>
.atlas-kicker{font-size:10px;letter-spacing:2.2px;text-transform:uppercase;color:#C7A35B;font-weight:800}
.atlas-lede{max-width:900px;font-size:15px;line-height:1.8;color:var(--voyage-body-ink)}
.atlas-section{font-family:'Cormorant Garamond',Georgia,serif;font-size:clamp(30px,3vw,42px);font-weight:700;line-height:1.08;color:var(--voyage-ink);margin:0}
.atlas-section-copy{max-width:850px;color:var(--voyage-body-ink);font-size:13px;line-height:1.75}
.atlas-card-title{font-family:'Cormorant Garamond',Georgia,serif;font-size:24px;line-height:1.08;font-weight:700;color:var(--voyage-ink);min-height:52px;margin:8px 0 4px}
.atlas-card-meta{font-size:9px;letter-spacing:1.45px;text-transform:uppercase;color:var(--voyage-muted);font-weight:800}
.atlas-card-copy{font-size:12px;line-height:1.65;color:var(--voyage-body-ink);min-height:54px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.atlas-tags{font-size:10px;line-height:1.5;color:var(--voyage-muted);min-height:30px;margin-top:8px}
.atlas-card-image{height:190px;overflow:hidden;border-radius:13px}
div[data-testid="stImage"] img{height:190px;object-fit:cover;border-radius:13px}
div[data-testid="stVerticalBlockBorderWrapper"]{height:100%;background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:16px}
div[data-testid="stButton"]>button{width:100%;min-height:42px;border-radius:12px;white-space:normal}
.category-tile{border:1px solid var(--voyage-line);border-radius:15px;background:var(--voyage-surface);padding:13px 14px;min-height:112px}
.category-icon{font-size:23px;margin-bottom:5px}
.category-name{font-size:14px;font-weight:750;color:var(--voyage-ink);line-height:1.3}
.category-count{font-size:10px;color:var(--voyage-muted);margin-top:6px}
@media(max-width:700px){.atlas-card-title{font-size:21px}.atlas-section{font-size:30px}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="atlas-kicker">VOYAGEPK · PAKISTAN UNBOUND</div>', unsafe_allow_html=True)
st.title("Discover Pakistan")
st.markdown(
    '<div class="atlas-lede">Start with the kind of journey you want. Explore destinations by tourism type, '
    'then narrow the results by province or search for a specific place.</div>',
    unsafe_allow_html=True,
)

# Visitor-facing taxonomy is deliberately broader than the catalogue's internal experience tags.
TOURISM_TYPES = [
    {"name": "Nature Tourism", "icon": "🌿", "description": "Valleys, lakes, forests, wildlife and landscapes", "tags": {"Nature & wildlife"}},
    {"name": "Adventure Tourism", "icon": "🥾", "description": "Trekking, climbing, rafting and mountain challenges", "tags": {"Adventure"}},
    {"name": "Religious & Pilgrimage Tourism", "icon": "🕌", "description": "Sacred places, pilgrimage routes and religious heritage", "tags": {"Religious & archaeology", "Islamic & Sufi heritage", "Sikh pilgrimage", "Buddhist heritage", "Hindu heritage"}},
    {"name": "Cultural & Heritage Tourism", "icon": "🏛️", "description": "Historic cities, architecture, archaeology, arts and traditions", "tags": {"Culture & heritage", "Archaeology & ancient civilizations"}},
    {"name": "Ecotourism", "icon": "🌱", "description": "Conservation, low-impact travel and community benefit", "tags": {"Ecotourism"}},
    {"name": "Food & Culinary Tourism", "icon": "🍲", "description": "Regional cuisine, food streets, markets and local flavours", "tags": {"Food & gastronomy"}},
    {"name": "Coastal & Marine Tourism", "icon": "🌊", "description": "Beaches, coastlines, marine landscapes and boating", "tags": {"Coastal & marine"}},
    {"name": "Rural & Community Tourism", "icon": "🧵", "description": "Village life, crafts, farms and locally hosted experiences", "tags": {"Rural & creative"}},
    {"name": "Camping & Outdoor Tourism", "icon": "⛺", "description": "Camping, stargazing and scenic outdoor journeys", "tags": {"Camping & outdoors"}},
    {"name": "Winter & Seasonal Tourism", "icon": "❄️", "description": "Snow landscapes, winter escapes and seasonal events", "tags": {"Winter & seasonal"}},
]

def destination_matches_type(item: dict, tourism_type: dict) -> bool:
    return bool(tourism_type["tags"].intersection(item.get("experiences", [])))

def destination_card(column, name: str, item: dict, key_prefix: str) -> None:
    with column:
        with st.container(border=True):
            image = get_commons_image(item["image_query"])
            if image:
                rendered = get_display_image(image["thumb_url"], aspect_ratio=(16, 9), focal_point=(0.5, 0.5))
                st.image(rendered if rendered else image["thumb_url"], use_container_width=True)
                credit = f'{image["artist"]} · {image["license"]} · [Image source]({image["page_url"]})'
                if image.get("illustrative"):
                    credit += " · Illustrative regional reference"
                st.caption(credit)
            else:
                st.markdown(
                    '<div class="atlas-card-image" style="background:linear-gradient(135deg,#173E2E,#456D66,#C7A35B);'
                    'display:flex;align-items:center;justify-content:center;color:#F5F1E7">VOYAGEPK · DESTINATION ATLAS</div>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                f'<div class="atlas-card-meta">{item.get("province", item["region"])}</div>'
                f'<div class="atlas-card-title">{name}</div>'
                f'<div class="atlas-card-copy">{item["tagline"]}</div>'
                f'<div class="atlas-tags">{" · ".join(item["experiences"][:3])}</div>',
                unsafe_allow_html=True,
            )
            if st.button("Explore destination", key=f"{key_prefix}_{name}", use_container_width=True):
                st.session_state["selected_destination"] = name
                st.switch_page("pages/02_Destination_Guide.py")

st.markdown('<div class="atlas-kicker">EXPLORE BY INTEREST</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-section">Choose your tourism type</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="atlas-section-copy">These are discovery categories, not an official ranking. '
    'A destination can belong to several tourism types.</div>',
    unsafe_allow_html=True,
)

if "discover_tourism_type" not in st.session_state:
    st.session_state["discover_tourism_type"] = "All tourism types"

# Category tiles are real buttons: selecting one filters the destination collection below.
for row_start in range(0, len(TOURISM_TYPES), 5):
    cols = st.columns(5, gap="small")
    for col, tourism_type in zip(cols, TOURISM_TYPES[row_start:row_start + 5]):
        count = sum(destination_matches_type(item, tourism_type) for item in DESTINATIONS.values())
        with col:
            st.markdown(
                f'<div class="category-tile"><div class="category-icon">{tourism_type["icon"]}</div>'
                f'<div class="category-name">{tourism_type["name"]}</div>'
                f'<div class="category-count">{count} destination clusters</div></div>',
                unsafe_allow_html=True,
            )
            if st.button("Explore this type", key="type_" + tourism_type["name"], use_container_width=True):
                st.session_state["discover_tourism_type"] = tourism_type["name"]
                st.rerun()

st.write("")
selected_type_name = st.session_state["discover_tourism_type"]
selected_type = next((t for t in TOURISM_TYPES if t["name"] == selected_type_name), None)
with st.container(border=True):
    f1, f2, f3 = st.columns([1.1, 1.0, 1.5], gap="medium")
    with f1:
        available_provinces = [
            p for p in PROVINCE_ORDER
            if any(d.get("province", d["region"]) == p for d in DESTINATIONS.values())
        ]
        selected_province = st.selectbox(
            "Province / territory",
            ["All provinces & territories"] + available_provinces,
        )
    with f2:
        options = ["All tourism types"] + [t["name"] for t in TOURISM_TYPES]
        current_index = options.index(selected_type_name) if selected_type_name in options else 0
        chosen_type = st.selectbox("Selected tourism type", options, index=current_index)
        if chosen_type != selected_type_name:
            st.session_state["discover_tourism_type"] = chosen_type
            st.rerun()
    with f3:
        query = st.text_input(
            "Search destinations",
            placeholder="Hunza, Lahore, lakes, forts, food…",
        )

selected_type = next(
    (t for t in TOURISM_TYPES if t["name"] == st.session_state["discover_tourism_type"]),
    None,
)

results = []
for name, item in DESTINATIONS.items():
    if selected_province != "All provinces & territories" and item.get("province", item["region"]) != selected_province:
        continue
    if selected_type and not destination_matches_type(item, selected_type):
        continue
    searchable = " ".join([
        name, item["region"], item.get("province", ""), item["tagline"], item["overview"],
        " ".join(item["highlights"]), " ".join(item["experiences"]),
    ]).casefold()
    if query.strip() and query.strip().casefold() not in searchable:
        continue
    results.append((name, item))

st.write("")
if selected_type:
    st.markdown(f'<div class="atlas-kicker">{selected_type["icon"]} SELECTED TOURISM TYPE</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="atlas-section">{selected_type["name"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="atlas-section-copy">{selected_type["description"]}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="atlas-kicker">DESTINATION COLLECTION</div>', unsafe_allow_html=True)
    st.markdown('<div class="atlas-section">All destinations</div>', unsafe_allow_html=True)

st.caption(f"{len(results)} matching destination clusters")
if not results:
    st.info("No destinations match these filters. Try another tourism type, province or search term.")
else:
    results.sort(key=lambda pair: (pair[1].get("province", pair[1]["region"]), pair[0]))
    grouped = {}
    for name, item in results:
        province = item.get("province", item["region"])
        grouped.setdefault(province, []).append((name, item))
    for section_index, (province, items) in enumerate(grouped.items(), start=1):
        st.write("")
        st.markdown(
            f'<div class="atlas-kicker">DESTINATION COLLECTION · {section_index:02d}</div>'
            f'<div class="atlas-section">{province}</div>',
            unsafe_allow_html=True,
        )
        for start in range(0, len(items), 3):
            cols = st.columns(3, gap="large")
            for col, (name, item) in zip(cols, items[start:start + 3]):
                destination_card(col, name, item, f"discover_{section_index}")

st.write("")
st.divider()
st.markdown('<div class="atlas-kicker">SACRED PLACES & RELIGIOUS HERITAGE</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-section">Explore by faith and tradition</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="atlas-section-copy">A dedicated lens within Religious & Pilgrimage Tourism, '
    'covering living sacred places, pilgrimage routes and religious archaeology.</div>',
    unsafe_allow_html=True,
)
traditions = {
    "Islamic & Sufi heritage": "Mosques, shrines, Sufi centres and sacred architecture",
    "Sikh pilgrimage": "Gurdwaras and places associated with Sikh history",
    "Buddhist heritage": "Gandharan monasteries, stupas and Buddhist landscapes",
    "Hindu heritage": "Temples, sacred landscapes and Hindu pilgrimage",
}
tradition_cols = st.columns(4, gap="medium")
for col, (tradition, description) in zip(tradition_cols, traditions.items()):
    names = [n for n, d in DESTINATIONS.items() if tradition in d["experiences"]]
    with col:
        st.markdown(
            f'<div class="category-tile"><div class="category-name">{tradition}</div>'
            f'<div class="category-count">{len(names)} destination references</div>'
            f'<div class="atlas-card-copy">{description}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")
st.markdown("### Travel advisory and access checks")
st.markdown(
    "Destination discovery is not a safety clearance. Conditions can change quickly, particularly in remote "
    "mountain, border, coastal and security-sensitive areas. Check official government advisories, local "
    "administration notices, weather and road status immediately before travel."
)
advisory_cols = st.columns(3, gap="medium")
with advisory_cols[0]:
    st.markdown("**UK Foreign Office (FCDO)**")
    st.link_button("Pakistan regional travel advice", "https://www.gov.uk/foreign-travel-advice/pakistan/regional-risks", use_container_width=True)
with advisory_cols[1]:
    st.markdown("**US Department of State**")
    st.link_button("Pakistan travel advisory", "https://travel.state.gov/en/international-travel/travel-advisories/pakistan.html", use_container_width=True)
with advisory_cols[2]:
    st.markdown("**Gilgit-Baltistan Tourism Department**")
    st.link_button("Official tourism updates", "https://e-tourism.visitgilgitbaltistan.gov.pk/plan-trip/news-and-updates", use_container_width=True)

st.caption(
    "VoyagePK is an independent discovery prototype, not an official tourism or security authority. "
    "Destination clusters and map anchors are editorial approximations. A listing does not confirm current safety, access or permits."
)
