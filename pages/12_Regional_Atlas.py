from __future__ import annotations

import streamlit as st

from src.catalog import DESTINATIONS, PROVINCE_ORDER
from src.research_register import (
    DISCOVERY_LEADS,
    EVENT_RECORDS,
    IMAGE_CANDIDATES,
    RESEARCH_DESTINATIONS,
)
from src.ui import apply_visitor_theme

st.set_page_config(page_title="Regional Atlas & Events | VoyagePK", page_icon=None, layout="wide")
apply_visitor_theme()

st.markdown("""
<style>
.atlas-kicker{font-size:11px;letter-spacing:2.1px;text-transform:uppercase;color:var(--voyage-accent);font-weight:800}
.atlas-intro{max-width:980px;font-size:16px;line-height:1.8;color:var(--voyage-body-ink)}
.atlas-stat{padding:16px 18px;border:1px solid var(--voyage-line);border-radius:16px;background:var(--voyage-surface)}
.atlas-stat strong{display:block;font-family:'Cormorant Garamond',Georgia,serif;font-size:32px;line-height:1.1;color:var(--voyage-ink)}
.atlas-stat span{font-size:12px;color:var(--voyage-muted);letter-spacing:.5px}
.record-title{font-family:'Cormorant Garamond',Georgia,serif;font-size:25px;line-height:1.12;font-weight:700;color:var(--voyage-ink)}
.record-meta{font-size:12px;letter-spacing:1px;text-transform:uppercase;color:var(--voyage-muted);font-weight:750}
.record-copy{font-size:15px;line-height:1.75;color:var(--voyage-body-ink)}
.record-note{font-size:13px;line-height:1.65;color:var(--voyage-muted)}
.tag{display:inline-block;padding:5px 9px;margin:3px 4px 3px 0;border:1px solid var(--voyage-line);border-radius:30px;font-size:11px;color:var(--voyage-body-ink)}
@media(max-width:700px){.atlas-intro{font-size:14px}.record-title{font-size:22px}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="atlas-kicker">VOYAGEPK · REGIONAL INTELLIGENCE</div>', unsafe_allow_html=True)
st.title("Pakistan regional atlas")
st.markdown(
    '<p class="atlas-intro">A searchable layer of destination research, festivals, image-source candidates and regional discovery leads. '
    'Browse the existing destination catalogue alongside the detailed research intake. All records remain visible; evidence notes are shown rather than used to hide content.</p>',
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
for col, value, label in [
    (m1, len(DESTINATIONS), "Existing destination clusters"),
    (m2, len(RESEARCH_DESTINATIONS), "Detailed destination records"),
    (m3, len(EVENT_RECORDS), "Festival and event records"),
    (m4, len(IMAGE_CANDIDATES), "Image-source candidates"),
]:
    with col:
        st.markdown(f'<div class="atlas-stat"><strong>{value}</strong><span>{label}</span></div>', unsafe_allow_html=True)

st.caption("The existing Discover Pakistan page continues to show the full destination-cluster catalogue. This page adds the structured research intake and discovery leads.")

tab_dest, tab_events, tab_images, tab_leads = st.tabs(
    ["Destination intelligence", "Festivals & events", "Image source register", "More places to research"]
)

with tab_dest:
    st.subheader("Detailed destination records")
    regions = ["All regions"] + sorted({r["region"] for r in RESEARCH_DESTINATIONS})
    f1, f2 = st.columns([1.4, 1])
    with f1:
        q = st.text_input("Search destinations, attractions or descriptions", placeholder="e.g. Makli, Kalash, lake, Buddhist...")
    with f2:
        region = st.selectbox("Filter by region", regions)
    matches = []
    for item in RESEARCH_DESTINATIONS:
        haystack = " ".join([item["name"], item["region"], item["cluster"], item["type"], item["summary"], " ".join(item["categories"])])
        if (region == "All regions" or item["region"] == region) and q.casefold() in haystack.casefold():
            matches.append(item)
    st.caption(f"Showing {len(matches)} of {len(RESEARCH_DESTINATIONS)} detailed research records.")
    for item in matches:
        with st.container(border=True):
            st.markdown(f'<div class="record-meta">{item["region"]} · {item["type"]} · {item["id"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="record-title">{item["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="record-copy">{item["summary"]}</div>', unsafe_allow_html=True)
            st.caption("Catalogue cluster: " + item["cluster"])
            st.markdown("".join(f'<span class="tag">{tag}</span>' for tag in item["categories"]), unsafe_allow_html=True)
            st.markdown(f'<div class="record-note">Editorial note: {item["note"]}</div>', unsafe_allow_html=True)
            st.link_button("Open source page", item["source"], use_container_width=False)

    st.divider()
    st.subheader("Existing destination clusters")
    cluster_query = st.text_input("Search all catalogue clusters", key="cluster_query", placeholder="Search the full 63-cluster catalogue")
    cluster_regions = ["All regions"] + PROVINCE_ORDER
    selected_region = st.selectbox("Catalogue region", cluster_regions, key="cluster_region")
    cluster_matches = []
    for name, item in DESTINATIONS.items():
        item_region = item.get("region", "")
        if (selected_region == "All regions" or selected_region in item_region) and cluster_query.casefold() in (name + " " + item.get("tagline", "") + " " + item.get("overview", "")).casefold():
            cluster_matches.append((name, item))
    st.caption(f"Showing {len(cluster_matches)} matching catalogue clusters.")
    cols = st.columns(2)
    for index, (name, item) in enumerate(cluster_matches):
        with cols[index % 2]:
            with st.container(border=True):
                st.markdown(f'<div class="record-title">{name}</div>', unsafe_allow_html=True)
                st.caption(item.get("region", ""))
                st.write(item.get("tagline", ""))
                st.write(" · ".join(item.get("highlights", [])[:4]))

with tab_events:
    st.subheader("Festival and event calendar")
    event_regions = ["All regions"] + sorted({e["region"] for e in EVENT_RECORDS})
    e1, e2 = st.columns([1.3, 1])
    with e1:
        event_q = st.text_input("Search events", placeholder="e.g. Urs, polo, Mela...")
    with e2:
        event_region = st.selectbox("Event region", event_regions)
    event_matches = [
        e for e in EVENT_RECORDS
        if (event_region == "All regions" or e["region"] == event_region)
        and event_q.casefold() in (e["name"] + " " + e["location"] + " " + e["note"]).casefold()
    ]
    st.caption(f"Showing {len(event_matches)} of {len(EVENT_RECORDS)} event records. Duplicate Shandur references are consolidated into one cross-regional event.")
    for event in event_matches:
        with st.container(border=True):
            st.markdown(f'<div class="record-meta">{event["region"]} · {event["id"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="record-title">{event["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="record-copy">{event["location"]} · {event["date"]}</div>', unsafe_allow_html=True)
            st.info(event["date_status"])
            st.markdown(f'<div class="record-note">{event["note"]}</div>', unsafe_allow_html=True)
            st.link_button("Open event source", event["source"])

with tab_images:
    st.subheader("Image source register")
    st.warning(
        "These are source-page candidates, not cleared production assets. A Commons page URL alone does not verify the exact image, creator, licence, attribution or commercial-use rights. "
        "Do not publish or crop an asset until its file page and licence are checked."
    )
    image_q = st.text_input("Search image subjects", placeholder="e.g. Faisal Mosque, Astola, Makli...")
    image_matches = [x for x in IMAGE_CANDIDATES if image_q.casefold() in (x["subject"] + " " + x["region"] + " " + x["id"]).casefold()]
    st.caption(f"{len(image_matches)} image-source candidates currently have enough retained metadata to list on this page.")
    for item in image_matches:
        with st.container(border=True):
            asset_ref = item.get("id") or item.get("intake_ref", "Unassigned source candidate")
            st.markdown(f'<div class="record-meta">{item["region"]} · {asset_ref}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="record-title">{item["subject"]}</div>', unsafe_allow_html=True)
            if item.get("creator"):
                st.caption("Creator recorded: " + item["creator"])
            if item.get("licence"):
                st.caption("Licence note: " + item["licence"])
            if item.get("page"):
                st.link_button("Review source page", item["page"])
            else:
                st.warning(item.get("note", "Original source metadata is missing; this candidate is retained but not cleared for use."))
                st.caption(item.get("intake_ref", "Original batch candidate"))
    st.caption("All 27 image candidates from the retained batch count are represented. Where original file-page metadata was not recoverable, the subject remains listed without an invented URL, creator or licence.")

with tab_leads:
    st.subheader("Additional destination discovery leads")
    st.markdown("These names are retained as research leads so they are not lost. They are not yet full destination records.")
    lead_regions = list(DISCOVERY_LEADS)
    selected_lead_region = st.selectbox("Lead region", lead_regions)
    leads = DISCOVERY_LEADS[selected_lead_region]
    for start in range(0, len(leads), 2):
        cols = st.columns(2)
        for offset, lead in enumerate(leads[start:start + 2]):
            with cols[offset]:
                with st.container(border=True):
                    st.markdown(f'<div class="record-title">{lead}</div>', unsafe_allow_html=True)
                    st.caption("Discovery lead · " + selected_lead_region)

st.divider()
st.caption(
    "VoyagePK is an independent tourism discovery prototype, not an official tourism, safety or booking authority. "
    "A listing does not guarantee current access, operating status, event dates, permits or image rights. "
    "Check current information with the responsible authority and local community before travel."
)
