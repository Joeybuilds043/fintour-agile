from __future__ import annotations

import streamlit as st

from src.catalog import DESTINATIONS, PROVINCE_ORDER
from src.destination_gallery import DESTINATION_IMAGE_BATCHES, get_destination_gallery_image
from src.research_register import DISCOVERY_LEADS, EVENT_RECORDS, IMAGE_CANDIDATES, RESEARCH_DESTINATIONS
from src.services.media import get_commons_image, get_display_image
from src.ui import apply_visitor_theme

st.set_page_config(page_title="Regional Atlas | VoyagePK", page_icon=None, layout="wide")
apply_visitor_theme()

st.markdown("""
<style>
.atlas-eyebrow{font-size:10px;letter-spacing:2.2px;text-transform:uppercase;color:#C7A35B;font-weight:850}
.atlas-lede{max-width:940px;font-size:15px;line-height:1.8;color:var(--voyage-body-ink)}
.atlas-heading{font-family:'Cormorant Garamond',Georgia,serif;font-size:clamp(30px,3vw,40px);line-height:1.05;font-weight:700;color:var(--voyage-ink);margin:0}
.atlas-subheading{font-size:13px;line-height:1.7;color:var(--voyage-muted);max-width:850px}
.atlas-stat{padding:15px 17px;border:1px solid var(--voyage-line);border-radius:16px;background:var(--voyage-surface);min-height:88px}
.atlas-stat strong{display:block;font-family:'Cormorant Garamond',Georgia,serif;font-size:31px;line-height:1.05;color:var(--voyage-ink)}
.atlas-stat span{display:block;margin-top:5px;font-size:10px;letter-spacing:1px;text-transform:uppercase;color:var(--voyage-muted);font-weight:750}
.atlas-card{height:100%;padding:12px;border:1px solid var(--voyage-line);border-radius:17px;background:var(--voyage-surface);box-shadow:0 8px 22px rgba(8,25,20,.055)}
.atlas-photo-frame{padding:5px;border:1px solid rgba(199,163,91,.55);border-radius:14px;background:linear-gradient(145deg,rgba(199,163,91,.13),rgba(255,255,255,.35))}
.atlas-photo-frame img{display:block;width:100%;height:178px;object-fit:cover;border-radius:9px}
div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stImage"] img{padding:4px;border:1px solid rgba(199,163,91,.7);border-radius:14px;background:rgba(199,163,91,.10);box-shadow:0 10px 24px rgba(8,25,20,.12)}
.atlas-photo-placeholder{height:178px;border-radius:9px;background:linear-gradient(135deg,#123D2D,#355D62 62%,#C7A35B);display:flex;align-items:center;justify-content:center;color:#F6F2E8;font-size:10px;font-weight:800;letter-spacing:2px}
.atlas-card-meta{margin-top:12px;font-size:9px;letter-spacing:1.4px;text-transform:uppercase;color:var(--voyage-muted);font-weight:850}
.atlas-card-title{font-family:'Cormorant Garamond',Georgia,serif;font-size:23px;line-height:1.08;font-weight:700;color:var(--voyage-ink);margin:5px 0 7px;min-height:48px}
.atlas-card-copy{font-size:12px;line-height:1.65;color:var(--voyage-body-ink);min-height:60px}
.atlas-tag{display:inline-block;padding:4px 8px;margin:3px 3px 0 0;border:1px solid var(--voyage-line);border-radius:30px;font-size:9px;color:var(--voyage-muted)}
.atlas-credit{font-size:9px;line-height:1.45;color:var(--voyage-muted);margin:5px 2px 8px}
.atlas-record-note{padding:10px 12px;border-left:2px solid #C7A35B;background:var(--voyage-surface);border-radius:0 9px 9px 0;font-size:12px;line-height:1.6;color:var(--voyage-muted)}
div[data-testid="stVerticalBlockBorderWrapper"]{border-color:var(--voyage-line);border-radius:17px}
div[data-testid="stImage"] img{border-radius:10px;object-fit:cover;box-shadow:0 8px 20px rgba(8,25,20,.10)}
div[data-testid="stButton"]>button{border-radius:11px;font-weight:700;min-height:39px}
@media(max-width:700px){.atlas-card-title{font-size:21px}.atlas-lede{font-size:14px}.atlas-photo-frame img,.atlas-photo-placeholder{height:150px}}
</style>
""", unsafe_allow_html=True)


if st.session_state.get("voyage_theme", "Light") == "Dark":
    st.markdown("""
    <style>
    .stApp .atlas-eyebrow,.stApp .atlas-lede,.stApp .atlas-heading,
    .stApp .atlas-subheading,.stApp .atlas-stat strong,.stApp .atlas-stat span,
    .stApp .atlas-card-meta,.stApp .atlas-card-title,.stApp .atlas-card-copy,
    .stApp .atlas-tag,.stApp .atlas-credit,.stApp .atlas-record-note{
        color:#E6EEE8!important
    }
    .stApp .atlas-stat,.stApp .atlas-card,.stApp .atlas-record-note,
    .stApp [data-testid="stVerticalBlockBorderWrapper"]{
        background:#080D09!important;border-color:#26372C!important;box-shadow:none!important
    }
    .stApp .atlas-photo-frame{background:#050705!important;border:1px solid #45C477!important}
    .stApp .atlas-photo-placeholder{background:#080D09!important;color:#FFFFFF!important;border:1px solid #45C477!important}
    .stApp .atlas-tag{border-color:#45C477!important;color:#BFE8CD!important}
    .stApp .atlas-record-note{border-left-color:#45C477!important}
    .stApp .atlas-eyebrow{color:#45C477!important}
    </style>
    """, unsafe_allow_html=True)

# Match detailed records to the existing catalogue so imagery and cluster names stay consistent.
catalog_by_name = {name.casefold(): (name, item) for name, item in DESTINATIONS.items()}

def find_catalog_record(record):
    cluster = record.get("cluster", "")
    return catalog_by_name.get(cluster.casefold())

def show_photo(query: str, allow_lookup: bool = True):
    # Only the first few cards in each section trigger remote image discovery.
    image = get_destination_gallery_image(query) or (get_commons_image(query) if allow_lookup else None)
    if image and image.get("thumb_url"):
        rendered = get_display_image(image["thumb_url"], aspect_ratio=(16, 9), focal_point=(0.5, 0.5))
        st.image(rendered if rendered else image["thumb_url"], use_container_width=True)
        credit = f'{image.get("artist", "Creator not listed")} · {image.get("license", "Licence not listed")}'
        if image.get("page_url"):
            st.markdown(f'<div class="atlas-credit"><a href="{image["page_url"]}" target="_blank">Image source</a> · {credit}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="atlas-credit">{credit}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="atlas-photo-frame"><div class="atlas-photo-placeholder">VOYAGEPK · PAKISTAN</div></div>', unsafe_allow_html=True)

def render_destination_card(record, index: int, detailed: bool = True):
    if detailed:
        catalog = find_catalog_record(record)
        image_query = catalog[1].get("image_query") if catalog else record.get("name", "Pakistan destination")
    else:
        image_query = record[1].get("image_query") or record[0]
    with st.container(border=True):
        show_photo(image_query or record.get("name", "Pakistan destination"), allow_lookup=index < 9)
        if detailed:
            st.markdown(f'<div class="atlas-card-meta">{record.get("region","")} · {record.get("type","")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="atlas-card-title">{record.get("name","")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="atlas-card-copy">{record.get("summary","")}</div>', unsafe_allow_html=True)
            tags = "".join(f'<span class="atlas-tag">{tag}</span>' for tag in record.get("categories", [])[:4])
            st.markdown(tags, unsafe_allow_html=True)
            st.caption("Catalogue cluster: " + record.get("cluster", "Not assigned"))
            with st.expander("Research notes and source"):
                st.markdown(f'<div class="atlas-record-note">{record.get("note","")}</div>', unsafe_allow_html=True)
                if record.get("source"):
                    st.link_button("Open source", record["source"])
        else:
            name = record[0]
            item = record[1]
            st.markdown(f'<div class="atlas-card-meta">{item.get("region","")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="atlas-card-title">{name}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="atlas-card-copy">{item.get("tagline", item.get("overview",""))}</div>', unsafe_allow_html=True)
            st.markdown("".join(f'<span class="atlas-tag">{tag}</span>' for tag in item.get("experiences", [])[:4]), unsafe_allow_html=True)

st.markdown('<div class="atlas-eyebrow">VOYAGEPK · PAKISTAN UNBOUND</div>', unsafe_allow_html=True)
st.title("Regional Atlas")
st.markdown(
    '<div class="atlas-lede">Explore Pakistan region by region. Discover signature destinations, detailed attractions, '
    'living heritage, seasonal festivals and visual references in one organised atlas.</div>',
    unsafe_allow_html=True,
)

stats = [
    (len(DESTINATIONS), "Destination clusters"),
    (len(RESEARCH_DESTINATIONS), "Detailed attractions"),
    (len(EVENT_RECORDS), "Festival & event records"),
    (len(IMAGE_CANDIDATES), "Image candidates"),
]
cols = st.columns(4)
for col, (value, label) in zip(cols, stats):
    with col:
        st.markdown(f'<div class="atlas-stat"><strong>{value}</strong><span>{label}</span></div>', unsafe_allow_html=True)

st.markdown("")
st.markdown('<div class="atlas-eyebrow">01 · START EXPLORING</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-heading">Find a place worth the journey.</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-subheading">Search across detailed destination records and filter by region. Each destination is presented as a framed visual card with its own summary, categories and source notes.</div>', unsafe_allow_html=True)

f1, f2 = st.columns([1.5, 1])
with f1:
    search_text = st.text_input("Search destinations and attractions", placeholder="Try Hunza, Makli, Kalash, lake, fort...")
with f2:
    region_options = ["All regions"] + sorted({item["region"] for item in RESEARCH_DESTINATIONS})
    selected_region = st.selectbox("Region", region_options, key="atlas_region_filter")

destination_matches = []
for record in RESEARCH_DESTINATIONS:
    haystack = " ".join([
        str(record.get("name", "")), str(record.get("region", "")), str(record.get("cluster", "")),
        str(record.get("type", "")), str(record.get("summary", "")),
        " ".join(record.get("categories", [])), str(record.get("note", "")),
    ]).casefold()
    if (selected_region == "All regions" or record["region"] == selected_region) and search_text.casefold() in haystack:
        destination_matches.append(record)

st.caption(f"{len(destination_matches)} detailed records match your search.")
for start in range(0, len(destination_matches), 3):
    row = st.columns(3, gap="medium")
    for offset, (col, record) in enumerate(zip(row, destination_matches[start:start + 3])):
        with col:
            render_destination_card(record, start + offset)

st.divider()
st.markdown('<div class="atlas-eyebrow">02 · THE NATIONAL COLLECTION</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-heading">Explore destination clusters.</div>', unsafe_allow_html=True)
cluster_search = st.text_input("Search the wider destination catalogue", placeholder="Search all destination clusters", key="atlas_cluster_search")
cluster_region_options = ["All regions"] + PROVINCE_ORDER
cluster_region = st.selectbox("Catalogue region", cluster_region_options, key="atlas_cluster_region")
cluster_matches = []
for name, item in DESTINATIONS.items():
    item_region = item.get("region", "")
    searchable = (name + " " + item.get("tagline", "") + " " + item.get("overview", "")).casefold()
    if (cluster_region == "All regions" or cluster_region in item_region) and cluster_search.casefold() in searchable:
        cluster_matches.append((name, item))
st.caption(f"{len(cluster_matches)} destination clusters.")
for start in range(0, len(cluster_matches), 3):
    row = st.columns(3, gap="medium")
    for offset, (col, record) in enumerate(zip(row, cluster_matches[start:start + 3])):
        with col:
            render_destination_card(record, start + offset, detailed=False)

st.divider()
st.markdown('<div class="atlas-eyebrow">03 · FESTIVAL SEASONS</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-heading">Culture has its own calendar.</div>', unsafe_allow_html=True)
event_query = st.text_input("Search festivals and events", placeholder="Try Urs, Polo, Lok Mela, Vaisakhi...")
event_regions = ["All regions"] + sorted({event.get("region", "") for event in EVENT_RECORDS})
event_region = st.selectbox("Event region", event_regions, key="atlas_event_region")
event_matches = [
    event for event in EVENT_RECORDS
    if (event_region == "All regions" or event.get("region") == event_region)
    and event_query.casefold() in (str(event.get("name","")) + " " + str(event.get("location","")) + " " + str(event.get("note",""))).casefold()
]
st.caption(f"{len(event_matches)} event records.")
for start in range(0, len(event_matches), 2):
    row = st.columns(2, gap="medium")
    for offset, (col, event) in enumerate(zip(row, event_matches[start:start + 2])):
        with col:
            with st.container(border=True):
                show_photo(event.get("name", "Pakistan festival"), allow_lookup=start + offset < 6)
                st.markdown(f'<div class="atlas-card-meta">{event.get("region","")} · {event.get("id","")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="atlas-card-title">{event.get("name","")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="atlas-card-copy">{event.get("location","")} · {event.get("date","")}</div>', unsafe_allow_html=True)
                st.info(event.get("date_status", "Date information is retained from the research intake."))
                with st.expander("Event context and source"):
                    st.markdown(f'<div class="atlas-record-note">{event.get("note","")}</div>', unsafe_allow_html=True)
                    if event.get("source"):
                        st.link_button("Open event source", event["source"])

st.divider()
st.markdown('<div class="atlas-eyebrow">04 · DESTINATION IMAGE GALLERY</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-heading">Pakistan, through the places themselves.</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-subheading">The following destination photographs are displayed from the exact URLs supplied for batches 1–8. The original URLs are preserved; source and reuse rights should be checked before commercial or promotional reuse.</div>', unsafe_allow_html=True)
for batch_name, batch_images in DESTINATION_IMAGE_BATCHES.items():
    st.markdown(f'<div class="atlas-card-meta">{batch_name}</div>', unsafe_allow_html=True)
    for start in range(0, len(batch_images), 3):
        row = st.columns(3, gap="medium")
        for col, image_record in zip(row, batch_images[start:start + 3]):
            with col:
                with st.container(border=True):
                    st.image(image_record["image_url"], use_container_width=True)
                    st.markdown(f'<div class="atlas-card-title">{image_record["destination"]}</div>', unsafe_allow_html=True)
                    st.caption("Supplied image URL · original link preserved")
                    st.link_button("Open original image", image_record["image_url"])

st.divider()
st.markdown('<div class="atlas-eyebrow">05 · VISUAL REFERENCE LIBRARY</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-heading">Images, with their source context.</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-subheading">Image candidates are displayed as framed subject cards. A source-page candidate is not automatically a cleared production asset; review the creator and licence before reuse.</div>', unsafe_allow_html=True)
image_query = st.text_input("Search image subjects", placeholder="Faisal Mosque, Astola Island, Makli...")
image_matches = [
    item for item in IMAGE_CANDIDATES
    if image_query.casefold() in (str(item.get("subject","")) + " " + str(item.get("region","")) + " " + str(item.get("id") or "")).casefold()
]
st.caption(f"{len(image_matches)} image candidates.")
for start in range(0, len(image_matches), 3):
    row = st.columns(3, gap="medium")
    for offset, (col, item) in enumerate(zip(row, image_matches[start:start + 3])):
        with col:
            with st.container(border=True):
                if item.get("page") and start + offset < 6:
                    show_photo(item["subject"])
                else:
                    st.markdown('<div class="atlas-photo-frame"><div class="atlas-photo-placeholder">IMAGE SOURCE PENDING</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="atlas-card-meta">{item.get("region","")} · {item.get("id") or item.get("intake_ref","Candidate")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="atlas-card-title">{item.get("subject","")}</div>', unsafe_allow_html=True)
                if item.get("creator"):
                    st.caption("Creator: " + item["creator"])
                if item.get("licence"):
                    st.caption("Licence: " + item["licence"])
                if item.get("page"):
                    st.link_button("Review image source", item["page"])
                else:
                    st.caption(item.get("note", "Original source-page details were not retained."))

st.divider()
st.markdown('<div class="atlas-eyebrow">05 · THE NEXT DISCOVERIES</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-heading">More places to explore.</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-subheading">A region-by-region discovery queue of additional sites and experiences. These are kept visible for future expansion of the atlas.</div>', unsafe_allow_html=True)
lead_regions = list(DISCOVERY_LEADS.keys())
for region_name in lead_regions:
    leads = DISCOVERY_LEADS.get(region_name) or []
    with st.expander(f"{region_name}  ·  {len(leads)} places", expanded=False):
        for start in range(0, len(leads), 3):
            row = st.columns(3, gap="small")
            for col, lead in zip(row, leads[start:start + 3]):
                with col:
                    with st.container(border=True):
                        st.markdown(f'<div class="atlas-card-title">{lead}</div>', unsafe_allow_html=True)
                        st.caption("Discovery lead · " + region_name)

st.divider()
st.caption("VoyagePK is an independent tourism discovery prototype. Listings do not guarantee current access, event schedules, permits, safety conditions or image reuse rights. Confirm time-sensitive details with the responsible authority and local community before travel.")
