from __future__ import annotations

import json
import html
import base64
import streamlit as st

from src.catalog import DESTINATIONS
from src.destination_gallery import get_destination_gallery_image
from src.services.media import get_commons_image, get_display_image
from src.services.weather import get_weather
from src.ui import apply_visitor_theme

st.set_page_config(page_title="VoyagePK | Pakistan Unbound", page_icon=None, layout="wide")

apply_visitor_theme()
st.markdown("""<style>
@media (max-width: 700px) {
  .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
  [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: 0.75rem !important; }
  [data-testid="column"] { min-width: min(100%, 280px) !important; flex: 1 1 100% !important; }
  img { max-width: 100%; }
}
</style>""", unsafe_allow_html=True)
st.markdown("""
<style>
.voyage-masthead{display:flex;align-items:center;gap:15px;padding:12px 16px;margin:0 0 18px;border-radius:16px;background:linear-gradient(110deg,#0B2E23 0%,#174D39 62%,#233B45 100%);box-shadow:0 12px 30px rgba(5,28,20,.2)}
.pakistan-flag{width:74px;height:45px;flex:none;filter:drop-shadow(0 3px 6px rgba(0,0,0,.22))}
.voyage-masthead-kicker{font-family:"Cormorant Garamond",Georgia,serif;color:#F6F2E8;font-size:22px;font-weight:700;letter-spacing:2.2px}
.voyage-masthead-sub{font-family:"Manrope",sans-serif;color:#D8C58F;font-size:9px;letter-spacing:2px;margin-top:5px}.masthead-divider{color:#C7A35B;padding:0 5px}
.category-photo-fallback{height:170px;border-radius:12px;background:linear-gradient(135deg,#123D2E,#1C4C57,#C2A25E);display:flex;align-items:center;justify-content:center;color:#F6F2E8;font-size:11px;letter-spacing:2px}
div[data-testid="stImage"] img{border:1px solid rgba(199,163,91,.32);border-radius:17px;box-shadow:0 18px 38px rgba(2,16,10,.24)}
.hero-frame:after{content:"";position:absolute;inset:8px;pointer-events:none;border:1px solid rgba(255,255,255,.58);background:linear-gradient(90deg,transparent 61.6%,rgba(255,255,255,.22) 61.8%,transparent 62%),linear-gradient(0deg,transparent 38%,rgba(255,255,255,.18) 38.2%,transparent 38.4%)} 
.hero-frame img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;object-position:61.8% 38.2%;border-radius:12px} 
.display-title{color:#FFFFFF!important;font-family:"Cormorant Garamond",Georgia,serif;font-weight:700;font-size:clamp(34px,3.2vw,44px);line-height:1.08;letter-spacing:-.55px;margin:0 0 13px;text-shadow:0 2px 20px rgba(0,0,0,.22)}
.hero-copy-panel{background:linear-gradient(145deg,rgba(7,35,25,.97),rgba(17,67,47,.94) 68%,rgba(30,67,72,.94));border:1px solid rgba(199,163,91,.42);border-radius:22px;padding:clamp(22px,3vw,36px);min-height:100%;box-shadow:0 22px 52px rgba(2,16,10,.2)}
.hero-copy-panel .lede{font-size:15px;line-height:1.78;color:#F0F4EB!important;opacity:1!important;max-width:680px;font-weight:500;letter-spacing:.05px}
.hero-copy-panel .hero-note{color:#F0E5C8!important}
.voyage-masthead-kicker{color:#FFFFFF!important;font-size:24px;letter-spacing:2px}
.voyage-masthead-sub{color:#FFFFFF!important;font-size:10px;letter-spacing:1.7px;font-weight:700}
.kicker{font-size:10px;letter-spacing:2.3px;text-transform:uppercase;color:#C7A35B;font-weight:700}
.section-title{color:var(--voyage-ink)!important;font-family:"Cormorant Garamond",Georgia,serif;font-weight:700;font-size:clamp(32px,3.2vw,44px);line-height:1.02;margin:4px 0 9px}
.section-copy{color:#26352C!important;-webkit-text-fill-color:#26352C!important;opacity:1!important;font-size:14px;line-height:1.8;max-width:720px;font-weight:550}
.section-title{color:#14251B!important;-webkit-text-fill-color:#14251B!important}

.soft-panel{background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:20px;padding:20px;height:100%}
.category-tile{background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:15px;padding:16px 14px;min-height:105px}
.category-letter{width:27px;height:27px;border-radius:50%;background:#E8E1D5;color:#173B3A;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;margin-bottom:10px}
.experience-collection-card{height:100%;min-height:455px;display:flex;flex-direction:column}
.experience-collection-card [data-testid="stVerticalBlockBorderWrapper"]{height:100%;min-height:455px;display:flex;flex-direction:column}
.experience-collection-card [data-testid="stImage"]{height:auto}
.experience-collection-card [data-testid="stImage"] img{width:100%;aspect-ratio:16/9;object-fit:cover}
.experience-credit{height:38px;min-height:38px;max-height:38px;overflow:hidden;font-size:10px;line-height:1.45;color:var(--voyage-muted);margin:7px 1px 4px}
.experience-credit a{font-weight:750}
.experience-collection-card .destination-name{min-height:58px;max-height:58px;overflow:hidden;align-items:center;margin:5px 0 6px}
.experience-collection-card .destination-copy{min-height:66px;max-height:66px}
.experience-collection-card [data-testid="stButton"]{margin-top:auto}
[class*="st-key-experience-collection-"] [data-testid="stButton"] button,
[class*="st-key-experience-collection-"] [data-testid="stButton"] button p,
[class*="st-key-experience-collection-"] [data-testid="stButton"] button span{
    color:#FFFFFF!important;
    font-weight:750!important;
}
[class*="st-key-experience-collection-"] [data-testid="stButton"] button{
    background:#167A43!important;
    border:1px solid #219653!important;
}
[class*="st-key-experience-collection-"] [data-testid="stButton"] button:hover{
    background:#219653!important;
    border-color:#45C477!important;
}
.category-letter{background:#167A43;color:#FFFFFF}
.weather-chip{background:#167A43;color:#FFFFFF!important;border:1px solid #219653}
@media(max-width:900px){.experience-collection-card,.experience-collection-card [data-testid="stVerticalBlockBorderWrapper"]{min-height:0}}
.category-name{font-weight:700;font-size:14px;color:var(--voyage-ink)}
.category-copy{font-size:11px;color:#657875;line-height:1.5;margin-top:4px}
.destination-name{color:var(--voyage-ink);font-family:"Cormorant Garamond",Georgia,serif;font-weight:700;font-size:25px;line-height:1.12;min-height:58px;display:flex;align-items:flex-end;margin:8px 0 6px}
.destination-meta{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#657875}
.destination-copy{font-size:13px;line-height:1.65;color:var(--voyage-body-ink)!important;opacity:1!important;min-height:64px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.hero-note{border-left:2px solid #C7A35B;padding:6px 0 6px 14px;color:var(--voyage-body-ink)!important;font-size:11px;line-height:1.8;margin-top:14px;letter-spacing:.25px}.hero-image-caption{display:flex;justify-content:space-between;gap:12px;padding:10px 4px 0;color:var(--voyage-body-ink);font-family:"Manrope",sans-serif;font-size:9px;letter-spacing:1.8px;font-weight:800}.hero-image-caption span:first-child{color:#C39B50}
.weather-chip{display:inline-block;margin:6px 0 2px;padding:6px 10px;border-radius:20px;background:rgba(24,89,60,.14);color:var(--voyage-ink);font-size:11px;font-weight:600}
.featured-image-frame{height:190px;width:100%;display:flex;align-items:center;justify-content:center;overflow:hidden;border-radius:13px;background:linear-gradient(135deg,#E8E2D6,#D8E6DF,#D7E3E9);color:#31564A;font:600 11px Manrope,sans-serif;letter-spacing:1.2px}
.featured-image-frame img{width:100%;height:190px;object-fit:cover;border-radius:13px}
.featured-image-credit{height:34px;min-height:34px;max-height:34px;overflow:hidden;font-size:9px;line-height:1.4;color:var(--voyage-muted,#657875);padding:6px 2px 0}
.featured-image-credit a{font-weight:700}
.featured-region{height:22px;min-height:22px;overflow:hidden;font-size:9px;letter-spacing:1.35px;text-transform:uppercase;color:#657875;padding-top:3px}
.featured-title{height:62px;min-height:62px;max-height:62px;display:flex;align-items:center;overflow:hidden;color:var(--voyage-ink);font-family:"Cormorant Garamond",Georgia,serif;font-size:24px;font-weight:700;line-height:1.1;margin:2px 0 5px}
.featured-description{height:70px;min-height:70px;max-height:70px;overflow:hidden;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;font-size:12px;line-height:1.55;color:var(--voyage-body-ink)}
.featured-weather{height:38px;min-height:38px;max-height:38px;display:flex;align-items:center;overflow:hidden;font-size:10px;line-height:1.35;color:var(--voyage-body-ink);margin:5px 0}
[class*="st-key-featured-destination-"] [data-testid="stVerticalBlockBorderWrapper"]{height:570px;min-height:570px;display:flex;flex-direction:column}
[class*="st-key-featured-destination-"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"]{height:100%;display:flex;flex-direction:column}
[class*="st-key-featured-destination-"] [data-testid="stButton"]{margin-top:auto}
[class*="st-key-featured-destination-"] [data-testid="stButton"] button{min-height:42px}
/* Featured destination cards: dark, high-contrast editorial panels */
[class*="st-key-featured-destination-"] [data-testid="stVerticalBlockBorderWrapper"]{
    background:linear-gradient(155deg,#101713 0%,#080D0A 100%)!important;
    border:1px solid #314438!important;
    border-radius:18px!important;
    padding:12px!important;
    box-shadow:0 12px 28px rgba(0,0,0,.16)!important;
}
[class*="st-key-featured-destination-"] .featured-image-credit,
[class*="st-key-featured-destination-"] .featured-image-credit a,
[class*="st-key-featured-destination-"] .featured-region,
[class*="st-key-featured-destination-"] .featured-title,
[class*="st-key-featured-destination-"] .featured-description,
[class*="st-key-featured-destination-"] .featured-weather{
    color:#F5F8F5!important;
}
[class*="st-key-featured-destination-"] .featured-region{color:#B8D5C1!important}
[class*="st-key-featured-destination-"] .featured-image-credit{opacity:.88}
[class*="st-key-featured-destination-"] [data-testid="stButton"] button{
    color:#FFFFFF!important;background:#167A43!important;border:1px solid #35A765!important;
    font-weight:750!important;border-radius:10px!important;
}
[class*="st-key-featured-destination-"] [data-testid="stButton"] button p,
[class*="st-key-featured-destination-"] [data-testid="stButton"] button span{color:#FFFFFF!important}
[class*="st-key-featured-destination-"] [data-testid="stButton"] button:hover{background:#219653!important}
/* Unified homepage typography: use the closing-panel title and body styles consistently. */
.featured-title,.destination-name,.category-name,.section-title,
.experience-collection-card .destination-name{
    color:#101A13!important;
    -webkit-text-fill-color:#101A13!important;
    font-family:"Cormorant Garamond",Georgia,serif!important;
    font-size:26px!important;
    font-weight:700!important;
    line-height:1.08!important;
}
.featured-description,.destination-copy,.category-copy,.section-copy,
.experience-credit,.featured-image-credit,.featured-weather,.destination-meta,
.featured-region,.hero-note,.hero-copy-panel .lede{
    color:#17251B!important;
    -webkit-text-fill-color:#17251B!important;
    font-family:Manrope,Arial,sans-serif!important;
    font-size:12px!important;
    font-weight:750!important;
    line-height:1.55!important;
    opacity:1!important;
}
/* Three closing action panels share the same geometry and typography */
/* Strong contrast for the Journeys section heading on the light page surface. */

/* Equal, prominent green navigation actions beneath all three closing panels. */
[class*="st-key-bottom-action-link-"] [data-testid="stPageLink-NavLink"]{
    min-height:52px;height:52px;width:100%;box-sizing:border-box;
    display:flex!important;align-items:center!important;justify-content:center!important;
    padding:10px 14px!important;margin-top:12px!important;
    background:#167A43!important;border:1px solid #219653!important;
    border-radius:12px!important;text-decoration:none!important;
    box-shadow:0 8px 18px rgba(13,75,42,.16)!important;
    transition:background .18s ease,transform .18s ease,box-shadow .18s ease;
}
[class*="st-key-bottom-action-link-"] [data-testid="stPageLink-NavLink"]:hover{
    background:#219653!important;transform:translateY(-2px);
    box-shadow:0 11px 22px rgba(13,75,42,.22)!important;
}
[class*="st-key-bottom-action-link-"] [data-testid="stPageLink-NavLink"] p,
[class*="st-key-bottom-action-link-"] [data-testid="stPageLink-NavLink"] span{
    color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;
    font-family:Manrope,Arial,sans-serif!important;font-size:12px!important;
    font-weight:800!important;letter-spacing:.25px!important;text-align:center!important;
    line-height:1.25!important;margin:0!important;
}

.kicker + .section-title{color:#14251B!important;-webkit-text-fill-color:#14251B!important}
.kicker + .section-title + .section-copy{color:#26352C!important;-webkit-text-fill-color:#26352C!important;opacity:1!important}
/* Closing action panels: clean white cards with concise, high-contrast copy. */
.bottom-feature-card{
    height:208px;min-height:208px;max-height:208px;box-sizing:border-box;
    display:flex;flex-direction:column;justify-content:flex-start;
    padding:20px 22px;border-radius:18px;
    background:#FFFFFF!important;
    border:1px solid #D8D4C6;box-shadow:0 12px 28px rgba(10,25,15,.08);
    overflow:hidden;
}
.bottom-feature-card .bottom-card-kicker{
    color:#267348!important;font:800 9px/1.4 Manrope,sans-serif;letter-spacing:2px;
    text-transform:uppercase;margin:0 0 10px;min-height:14px;
}
.bottom-feature-card .bottom-card-title{
    color:#101A13!important;font:700 26px/1.08 "Cormorant Garamond",Georgia,serif;
    min-height:58px;height:58px;margin:0 0 8px;display:flex;align-items:center;
}
.bottom-feature-card .bottom-card-copy{
    color:#17251B!important;font:750 12px/1.55 Manrope,sans-serif;
    min-height:56px;height:56px;margin:0;overflow:hidden;
    display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
}
@media(max-width:900px){.bottom-feature-card{height:auto;min-height:190px;max-height:none}.bottom-feature-card .bottom-card-title{height:auto;min-height:54px}.bottom-feature-card .bottom-card-copy{height:auto;min-height:50px}}
@media(max-width:900px){[class*="st-key-featured-destination-"] [data-testid="stVerticalBlockBorderWrapper"]{height:auto;min-height:0}.featured-image-frame,.featured-image-frame img{height:190px}}
@media(max-width:700px){.display-title{font-size:36px}.section-title{font-size:31px}.voyage-masthead-kicker{font-size:18px}.hero-image-caption{font-size:8px;letter-spacing:1.1px}}
/* Featured destination cards use the same white-panel / dark-type treatment as the closing cards. */
[class*="st-key-featured-destination-"] [data-testid="stVerticalBlockBorderWrapper"]{
    background:#FFFFFF!important;
    border:1px solid #D8D4C6!important;
    box-shadow:0 12px 28px rgba(10,25,15,.08)!important;
}
[class*="st-key-featured-destination-"] .featured-image-credit,
[class*="st-key-featured-destination-"] .featured-image-credit *,
[class*="st-key-featured-destination-"] .featured-region,
[class*="st-key-featured-destination-"] .featured-title,
[class*="st-key-featured-destination-"] .featured-description,
[class*="st-key-featured-destination-"] .featured-weather{
    color:#17251B!important;
    -webkit-text-fill-color:#17251B!important;
    opacity:1!important;
}
[class*="st-key-featured-destination-"] .featured-region{color:#267348!important;-webkit-text-fill-color:#267348!important}
[class*="st-key-featured-destination-"] .featured-title{color:#101A13!important;-webkit-text-fill-color:#101A13!important}
[class*="st-key-featured-destination-"] [data-testid="stButton"] button,
[class*="st-key-featured-destination-"] [data-testid="stButton"] button *{
    color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;
}

/* Explicit contrast for the six experience collection cards and their green actions. */
[class*="st-key-experience-collection-"] [data-testid="stButton"] button,
[class*="st-key-experience-collection-"] [data-testid="stButton"] button *{
    color:#FFFFFF!important;
    opacity:1!important;
    -webkit-text-fill-color:#FFFFFF!important;
}
[class*="st-key-experience-collection-"] [data-testid="stButton"] button{
    background:#167A43!important;border-color:#219653!important;
}
[class*="st-key-experience-collection-"] [data-testid="stButton"] button:hover{
    background:#219653!important;
}
[class*="st-key-featured-destination-"] .featured-image-credit,
[class*="st-key-featured-destination-"] .featured-image-credit *,
[class*="st-key-featured-destination-"] .featured-region,
[class*="st-key-featured-destination-"] .featured-title,
[class*="st-key-featured-destination-"] .featured-description,
[class*="st-key-featured-destination-"] .featured-weather{
    color:#F5F8F5!important;opacity:1!important;
}
.bottom-feature-card,.bottom-feature-card *{
    color:#17251B!important;
}
.bottom-feature-card .bottom-card-kicker{color:#267348!important}
.bottom-feature-card .bottom-card-title{color:#101A13!important}
.bottom-feature-card .bottom-card-copy{color:#17251B!important;font-weight:750!important}

/* Hero copy sits on a deep-green surface: preserve clear white contrast. */
.hero-copy-panel .lede,
.hero-copy-panel .hero-note{
    color:#FFFFFF!important;
    -webkit-text-fill-color:#FFFFFF!important;
    opacity:1!important;
    font-family:Manrope,Arial,sans-serif!important;
    font-weight:650!important;
}
.hero-copy-panel .hero-note{
    border-left-color:#D7C58F!important;
}
</style>
""", unsafe_allow_html=True)



with st.sidebar:
    st.markdown('<div class="voyage-sidebar-note">A considered guide to Pakistan</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="horizon-sidebar-kicker">THE DESTINATION ATLAS</div>', unsafe_allow_html=True)
    st.page_link("pages/00_Regional_Atlas.py", label="Regional Atlas")
    st.page_link("app.py", label="National destination atlas")
    st.page_link("pages/01_Discover_Pakistan.py", label="Explore destinations")
    st.page_link("pages/02_Destination_Guide.py", label="Destination field guides")
    st.page_link("pages/03_Trip_Planner.py", label="Build an itinerary")
    st.page_link("pages/04_Explore_Map.py", label="Explore the atlas")
    st.divider()
    st.markdown('<div class="horizon-sidebar-kicker">INTELLIGENCE & PLANNING</div>', unsafe_allow_html=True)
    st.page_link("pages/05_Destination_Intelligence.py", label="Destination intelligence")
    st.page_link("pages/06_Investment_Studio.py", label="Investment studio")
    st.page_link("pages/08_AI_Travel_Concierge.py", label="Travel concierge")
    st.page_link("pages/09_AI_Strategy_Advisor.py", label="Strategy advisor")
    st.page_link("pages/10_Growth_Scenario_Planner.py", label="Growth scenarios")
    st.divider()
    st.caption("Independent destination discovery prototype. Travel thoughtfully and verify local conditions.")

with open("assets/manifest.json", encoding="utf-8") as asset_file:
    asset_manifest = json.load(asset_file)
# Homepage hero photography is selected by appearance mode: daytime landscape in Light,
# illuminated heritage architecture in Dark.
dark_mode = st.session_state.get("voyage_theme", "Light") == "Dark"
if dark_mode:
    st.markdown("""
    <style>
    .stApp .voyage-masthead,.stApp .hero-copy-panel,.stApp .soft-panel,
    .stApp .category-tile,.stApp .category-letter,.stApp .weather-chip{
        background:#080D09!important;color:#FFFFFF!important;border:1px solid #26372C!important;box-shadow:none!important
    }
    .stApp .hero-copy-panel .lede,.stApp .hero-copy-panel .hero-note,
    .stApp .voyage-masthead-kicker,.stApp .voyage-masthead-sub,
    .stApp .kicker,.stApp .section-title,.stApp .section-copy,
    .stApp .destination-name,.stApp .destination-copy,.stApp .destination-meta,
    .stApp .hero-image-caption,.stApp .category-name,.stApp .category-copy{
        color:#E6EEE8!important
    }
    .stApp .masthead-divider,.stApp .hero-image-caption span:first-child{color:#45C477!important}
    .stApp .category-letter{background:#167A43!important;color:#FFFFFF!important;border-color:#45C477!important}
    .stApp .hero-note{border-left-color:#45C477!important}
    .stApp [data-testid="stImage"] img{border-color:#45C477!important}
    </style>
    """, unsafe_allow_html=True)

hero_asset = asset_manifest["assets"]["night_islamabad_cityscape"] if dark_mode else asset_manifest["assets"]["daytime_northern_pakistan"]
hero_image = hero_asset["url"]
hero_edition = "ILLUMINATED MOUNTAIN CITYSCAPE" if dark_mode else "SHANGRILA RESORT · SKARDU"
st.markdown(
    '<div class="voyage-masthead"><svg viewBox="0 0 92 56" role="img" aria-label="Flag of Pakistan" class="pakistan-flag"><rect width="92" height="56" rx="4" fill="#01411C"/><rect width="20" height="56" fill="#FFFFFF"/><circle cx="57" cy="27" r="17" fill="#FFFFFF"/><circle cx="63" cy="22" r="14" fill="#01411C"/><path d="M70 7l3.2 7.4 8 .7-6.1 5.2 1.8 7.8-6.9-4.1-6.9 4.1 1.8-7.8-6.1-5.2 8-.7z" fill="#FFFFFF"/></svg><div><div class="voyage-masthead-kicker">VOYAGEPK <span class="masthead-divider">/</span> PAKISTAN UNBOUND</div><div class="voyage-masthead-sub">LANDSCAPES · LIVING CULTURES · HERITAGE · PLACE-BASED TRAVEL</div></div></div><div class="kicker">A FIELD GUIDE TO THE EXTRAORDINARY</div>',
    unsafe_allow_html=True,
)
left, right = st.columns([1, 1], gap="large", vertical_alignment="center")
with left:
    st.markdown("""<div class='hero-copy-panel'><div class='display-title'>A country of peaks, pathways and living heritage.</div><div class='lede'>From the high Karakoram to historic cities and the Arabian Sea, Pakistan rewards the curious traveller with extraordinary landscapes, layered histories and cultures rooted in place. VoyagePK brings considered destination guides, practical journey planning and tourism insight together in one editorial travel atlas.</div><div class='hero-note'>Karakoram to coast · Ancient cities to living culture · Travel with context</div></div>""", unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/01_Discover_Pakistan.py", label="Explore Pakistan")

with right:
    hero_rendered = get_display_image(hero_image, aspect_ratio=(16, 10), focal_point=tuple(hero_asset.get("focal_point", [0.52, 0.72])))
    st.image(hero_rendered if hero_rendered else hero_image, use_container_width=True)
    st.markdown(
        f'<div class="hero-image-caption"><span>{hero_edition}</span><span>{hero_asset.get("author", "PEXELS CONTRIBUTOR")} · PEXELS</span><span>PAKISTAN · UNBOUND</span></div>',
        unsafe_allow_html=True,
    )
st.markdown('<div class="kicker">EXPLORE THE COUNTRY THROUGH DISTINCTIVE JOURNEYS</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">A richer way to experience Pakistan.</div>', unsafe_allow_html=True)
st.markdown('<div class="section-copy">Explore the country through mountain environments, spiritual and religious heritage, historic cities and cultural landscapes. Each collection links to destination-level field notes and visitor planning.</div>', unsafe_allow_html=True)
photo_collections = asset_manifest["experience_collections"]
for start_index in range(0, len(photo_collections), 3):
    cols = st.columns(3, gap="large")
    for col, asset in zip(cols, photo_collections[start_index:start_index + 3]):
        with col:
            with st.container(border=False, key=f'experience-collection-{asset["key"]}'):
                with st.container(border=True):
                    rendered = get_display_image(asset["url"], aspect_ratio=(16, 9), focal_point=tuple(asset.get("focal_point", [0.5, 0.48])))
                    st.image(rendered if rendered else asset["url"], use_container_width=True)
                    credit_author = str(asset.get("author") or "").strip()
                    credit_license = str(asset.get("license") or "").strip()
                    credit_page = str(asset.get("page_url") or "").strip()
                    missing_credit = any(term in (credit_author + " " + credit_license).lower() for term in ("not provided", "not confirmed", "unverified", "not independently"))
                    if credit_author and credit_license and credit_page and not missing_credit:
                        st.markdown(
                            f'<div class="experience-credit">{html.escape(credit_author)} · {html.escape(credit_license)} · <a href="{html.escape(credit_page, quote=True)}" target="_blank" rel="noopener">Image source</a></div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.caption("Credit details to be added.")
                    st.markdown(f'<div class="destination-name">{asset["title"]}</div><div class="destination-copy">{asset["description"]}</div>', unsafe_allow_html=True)
                    if st.button(f'Explore {asset["title"]}', key=f'collection_{asset["key"]}', use_container_width=True):
                        st.session_state["selected_experience_collection"] = asset["key"]
                        st.switch_page("pages/11_Experience_Collection.py")
st.write("")
st.markdown('<div class="kicker">EDITORIAL DESTINATION SELECTION</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Journeys worth discovering</div>', unsafe_allow_html=True)
st.markdown('<div class="section-copy">A cross-section of Pakistan’s mountain, coastal, cultural and urban experiences. This is an editorial selection, not a popularity ranking.</div>', unsafe_allow_html=True)
featured = ["Hunza Valley", "Skardu", "Naran–Kaghan Valley", "Lahore", "K2 & Concordia Expedition", "Swat Valley"]
# User-selected Pexels photography takes priority over catalogue/Commons fallbacks.
featured_image_overrides = {
    "Hunza Valley": {
        "thumb_url": "https://images.pexels.com/photos/9401114/pexels-photo-9401114.jpeg",
        "artist": "Pexels",
        "license": "Pexels License",
        "page_url": "https://images.pexels.com/photos/9401114/pexels-photo-9401114.jpeg",
    },
    "Skardu": {
        "thumb_url": "https://images.pexels.com/photos/19442073/pexels-photo-19442073.jpeg",
        "artist": "Pexels",
        "license": "Pexels License",
        "page_url": "https://images.pexels.com/photos/19442073/pexels-photo-19442073.jpeg",
    },
    "Naran–Kaghan Valley": {
        "thumb_url": "https://images.pexels.com/photos/10059879/pexels-photo-10059879.jpeg",
        "artist": "Pexels",
        "license": "Pexels License",
        "page_url": "https://images.pexels.com/photos/10059879/pexels-photo-10059879.jpeg",
    },
    "Lahore": {
        "thumb_url": "https://images.pexels.com/photos/13659051/pexels-photo-13659051.jpeg",
        "artist": "Pexels",
        "license": "Pexels License",
        "page_url": "https://images.pexels.com/photos/13659051/pexels-photo-13659051.jpeg",
    },
    "K2 & Concordia Expedition": {
        "thumb_url": "https://images.pexels.com/photos/31410274/pexels-photo-31410274.jpeg",
        "artist": "Pexels",
        "license": "Pexels License",
        "page_url": "https://images.pexels.com/photos/31410274/pexels-photo-31410274.jpeg",
    },
    "Swat Valley": {
        "thumb_url": "https://images.pexels.com/photos/37673127/pexels-photo-37673127.jpeg",
        "artist": "Pexels",
        "license": "Pexels License",
        "page_url": "https://images.pexels.com/photos/37673127/pexels-photo-37673127.jpeg",
    },
}
for start in range(0, len(featured), 3):
    cols = st.columns(3, gap="large")
    for offset, (col, name) in enumerate(zip(cols, featured[start:start + 3])):
        item = DESTINATIONS.get(name)
        if item is None:
            with col:
                st.warning(f"Destination profile temporarily unavailable: {name}. The rest of the atlas can still be used.")
            continue
        with col:
            with st.container(border=False, key=f"featured-destination-{start + offset}"):
                with st.container(border=True):
                    image = featured_image_overrides.get(name) or get_destination_gallery_image(name) or get_commons_image(item["image_query"])
                    if image:
                        image_data = get_display_image(image["thumb_url"], aspect_ratio=(16, 9), focal_point=(0.5, 0.5))
                        if isinstance(image_data, (bytes, bytearray)):
                            image_src = "data:image/jpeg;base64," + base64.b64encode(image_data).decode("ascii")
                        else:
                            image_src = str(image["thumb_url"])
                        st.markdown(
                            f'<div class="featured-image-frame"><img src="{html.escape(image_src, quote=True)}" alt="{html.escape(str(name), quote=True)}"></div>',
                            unsafe_allow_html=True,
                        )
                        image_credit = f'{image.get("artist", "Image contributor")} · {image.get("license", "Licence details")} · <a href="{html.escape(image.get("page_url", "#"), quote=True)}" target="_blank" rel="noopener">Image details</a>'
                        if image.get("illustrative"):
                            image_credit += " · Illustrative regional reference"
                    else:
                        st.markdown('<div class="featured-image-frame">DESTINATION IMAGE UNAVAILABLE</div>', unsafe_allow_html=True)
                        image_credit = "Image reference temporarily unavailable"
                    st.markdown(f'<div class="featured-image-credit">{image_credit}</div>', unsafe_allow_html=True)
                    st.markdown(
                        f'<div class="featured-region">{html.escape(str(item.get("region", "Pakistan")))}</div>'
                        f'<div class="featured-title">{html.escape(name)}</div>'
                        f'<div class="featured-description">{html.escape(str(item.get("tagline", "")))}</div>',
                        unsafe_allow_html=True,
                    )
                    weather = get_weather(item["lat"], item["lon"])
                    if weather and weather.get("current"):
                        current = weather["current"]
                        weather_text = f'Current forecast · {current.get("temperature_2m", "—")}°C · Wind {current.get("wind_speed_10m", "—")} km/h'
                    else:
                        weather_text = "Live weather temporarily unavailable"
                    st.markdown(f'<div class="featured-weather">{html.escape(weather_text)}</div>', unsafe_allow_html=True)
                    if st.button("Explore this place", key=f"home_guide_{name}", use_container_width=True):
                        st.session_state["selected_destination"] = name
                        st.switch_page("pages/02_Destination_Guide.py")

st.write("")
a, b, c = st.columns([1, 1, 1], gap="large")
with a:
    st.markdown('<div class="bottom-feature-card"><div class="bottom-card-kicker">PLAN WITH CONTEXT</div><div class="bottom-card-title">Make the journey yours.</div><p class="bottom-card-copy">Plan around your time, interests and budget. Check seasons, access and local guidance before you go.</p></div>', unsafe_allow_html=True)
    with st.container(border=False, key="bottom-action-link-plan"):
        st.page_link("pages/03_Trip_Planner.py", label="Build a trip plan")
with b:
    st.markdown('<div class="bottom-feature-card"><div class="bottom-card-kicker">REGIONAL DISCOVERY</div><div class="bottom-card-title">Explore the full atlas.</div><p class="bottom-card-copy">Browse regional destinations, attractions and festivals. Discover the places shaping Pakistan’s travel story.</p></div>', unsafe_allow_html=True)
    with st.container(border=False, key="bottom-action-link-atlas"):
        st.page_link("pages/00_Regional_Atlas.py", label="Open regional atlas")
with c:
    st.markdown('<div class="bottom-feature-card"><div class="bottom-card-kicker">SEE THE BIGGER PICTURE</div><div class="bottom-card-title">Travel is also an economy.</div><p class="bottom-card-copy">Explore tourism data, local value and investment scenarios. See where evidence can guide better decisions.</p></div>', unsafe_allow_html=True)
    with st.container(border=False, key="bottom-action-link-intelligence"):
        st.page_link("pages/05_Destination_Intelligence.py", label="Explore tourism intelligence")

st.caption("VoyagePK is an independent prototype, not an official government tourism service. Destination descriptions and approximate map anchors require local review. Verify travel, safety, access, permits and booking details with responsible local authorities and providers.")
