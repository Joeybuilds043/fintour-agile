from __future__ import annotations

import streamlit as st

from src.catalog import DESTINATIONS, EXPERIENCE_CATEGORIES
from src.services.media import get_commons_image, get_display_image

st.set_page_config(page_title="Discover Pakistan | Horizon", page_icon=None, layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
.stApp{background:#F5F1E8;font-family:'DM Sans',sans-serif;color:#183B3B}
.block-container{max-width:1480px;padding-top:1.4rem}
h1,h2,h3{color:#183B3B!important;font-family:'Playfair Display',Georgia,serif!important}
.kicker{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#A85F3C;font-weight:700}
.lede{font-size:15px;line-height:1.8;color:#687976;max-width:800px}
.card-title{font-family:'Playfair Display',Georgia,serif;font-size:23px;color:#183B3B;margin:7px 0 2px}
.card-meta{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#687976}
.card-copy{font-size:13px;line-height:1.65;color:#687976;min-height:42px}
.card-tags{font-size:11px;color:#183B3B;line-height:1.6}
div[data-testid="stImage"] img{border-radius:15px;object-fit:cover;filter:saturate(1.08) contrast(1.04)}
div[data-testid="stVerticalBlockBorderWrapper"]{background:#FFFCF6;border-color:#E5DED2;border-radius:18px}
div[data-testid="stButton"]>button{border-radius:30px;background:#183B3B;color:white;border:1px solid #183B3B}
@media(max-width:700px){.block-container{padding:1rem}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="kicker">THE HORIZON DESTINATION COLLECTION</div>', unsafe_allow_html=True)
st.title("Find the Pakistan you want to experience.")
st.markdown('<div class="lede">Explore mountain valleys, living heritage, desert landscapes, coastal communities and cities shaped by food and culture. Filter by the kind of journey you have in mind, then open a field guide for context before you travel.</div>', unsafe_allow_html=True)
st.write("")

with st.container(border=True):
    f1, f2, f3 = st.columns([1.1, 1.1, 1.5], gap="medium")
    with f1:
        experience = st.selectbox("Travel experience", ["All experiences"] + [x["name"] for x in EXPERIENCE_CATEGORIES])
    with f2:
        regions = ["All regions"] + sorted({d["region"] for d in DESTINATIONS.values()})
        region = st.selectbox("Region", regions)
    with f3:
        query = st.text_input("Search places and experiences", placeholder="Try Multan, beaches, forts, trekking or food")

results = []
for name, item in DESTINATIONS.items():
    searchable = " ".join([
        name, item["region"], item["tagline"], item["overview"],
        item["culture"], " ".join(item["experiences"]),
        " ".join(item["highlights"]),
    ]).casefold()
    if experience != "All experiences" and experience not in item["experiences"]:
        continue
    if region != "All regions" and region != item["region"]:
        continue
    if query.strip() and query.strip().casefold() not in searchable:
        continue
    results.append((name, item))

results.sort(key=lambda pair: pair[0])
st.markdown(f"**{len(results)} destinations**  ·  {len({d['region'] for _, d in results})} regions represented")
st.caption("An expanding editorial collection of destination clusters, not an official exhaustive gazetteer or ranking. Map pins are approximate area anchors.")
if not results:
    st.info("No destination matches those filters. Try a broader place name or experience.")
else:
    for start in range(0, len(results), 3):
        columns = st.columns(3, gap="large")
        for column, (name, item) in zip(columns, results[start:start + 3]):
            with column:
                with st.container(border=True):
                    image = get_commons_image(item["image_query"])
                    if image:
                        st.image(get_display_image(image["thumb_url"]) or image["thumb_url"], use_container_width=True)
                        st.caption(f'{image["artist"]} · {image["license"]} · [File details & attribution]({image["page_url"]})' + (' · Illustrative regional reference' if image.get('illustrative') else ''))
                    else:
                        st.markdown('<div style="height:190px;border-radius:15px;background:linear-gradient(135deg,#EEE9DF,#D9C8B7);display:flex;align-items:center;justify-content:center;color:#183B3B;font-family:Georgia,serif">Destination image unavailable</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-meta">{item["region"]}</div><div class="card-title">{name}</div><div class="card-copy">{item["tagline"]}</div><div class="card-tags">{ " · ".join(item["experiences"][:4]) }</div>', unsafe_allow_html=True)
                    if st.button("Open destination", key=f"discover_guide_{name}", use_container_width=True):
                        st.session_state["selected_destination"] = name
                        st.switch_page("pages/02_Destination_Guide.py")

st.write("")
st.markdown("### A note on travelling well")
st.markdown("Pakistan’s destinations are not interchangeable backdrops. Local customs, seasonal access, environmental limits and community priorities differ by place. Read the destination notes, verify current conditions with local sources and choose experiences that create value for local communities.")
