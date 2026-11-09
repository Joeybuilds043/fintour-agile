from __future__ import annotations

import json
import streamlit as st

from src.catalog import DESTINATIONS
from src.services.media import get_commons_image, get_display_image
from src.services.weather import get_weather
from src.ui import apply_visitor_theme

st.set_page_config(page_title="VoyagePK | Pakistan Unbound", page_icon=None, layout="wide")

apply_visitor_theme()
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
.section-copy{color:var(--voyage-body-ink)!important;opacity:1!important;font-size:14px;line-height:1.8;max-width:720px}
.soft-panel{background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:20px;padding:20px;height:100%}
.category-tile{background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:15px;padding:16px 14px;min-height:105px}
.category-letter{width:27px;height:27px;border-radius:50%;background:#E8E1D5;color:#173B3A;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;margin-bottom:10px}
.category-name{font-weight:700;font-size:14px;color:var(--voyage-ink)}
.category-copy{font-size:11px;color:#657875;line-height:1.5;margin-top:4px}
.destination-name{color:var(--voyage-ink);font-family:"Cormorant Garamond",Georgia,serif;font-weight:700;font-size:25px;line-height:1.12;min-height:58px;display:flex;align-items:flex-end;margin:8px 0 6px}
.destination-meta{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#657875}
.destination-copy{font-size:13px;line-height:1.65;color:var(--voyage-body-ink)!important;opacity:1!important;min-height:64px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.hero-note{border-left:2px solid #C7A35B;padding:6px 0 6px 14px;color:var(--voyage-body-ink)!important;font-size:11px;line-height:1.8;margin-top:14px;letter-spacing:.25px}.hero-image-caption{display:flex;justify-content:space-between;gap:12px;padding:10px 4px 0;color:var(--voyage-body-ink);font-family:"Manrope",sans-serif;font-size:9px;letter-spacing:1.8px;font-weight:800}.hero-image-caption span:first-child{color:#C39B50}
.weather-chip{display:inline-block;margin:6px 0 2px;padding:6px 10px;border-radius:20px;background:rgba(24,89,60,.14);color:var(--voyage-ink);font-size:11px;font-weight:600}
@media(max-width:700px){.display-title{font-size:36px}.section-title{font-size:31px}.voyage-masthead-kicker{font-size:18px}.hero-image-caption{font-size:8px;letter-spacing:1.1px}}
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
# The homepage uses the two exact image URLs supplied by the site owner.
# Appearance mode selects one image; no collage or Islamabad skyline is used here.
dark_mode = st.session_state.get("voyage_theme", "Light") == "Dark"
if dark_mode:
    st.markdown("""
    <style>
    .stApp .voyage-masthead,.stApp .hero-copy-panel,.stApp .soft-panel,
    .stApp .category-tile,.stApp .category-letter,.stApp .weather-chip{
        background:#050505!important;color:#FFFFFF!important;border:1px solid #292929!important;box-shadow:none!important
    }
    .stApp .hero-copy-panel .lede,.stApp .hero-copy-panel .hero-note,
    .stApp .voyage-masthead-kicker,.stApp .voyage-masthead-sub,
    .stApp .kicker,.stApp .section-title,.stApp .section-copy,
    .stApp .destination-name,.stApp .destination-copy,.stApp .destination-meta,
    .stApp .hero-image-caption,.stApp .category-name,.stApp .category-copy{
        color:#FFFFFF!important
    }
    .stApp .masthead-divider,.stApp .hero-image-caption span:first-child{color:#FFFFFF!important}
    .stApp .category-letter{background:#FFFFFF!important;color:#000000!important}
    .stApp .hero-note{border-left-color:#FFFFFF!important}
    .stApp [data-testid="stImage"] img{border-color:#FFFFFF!important}
    </style>
    """, unsafe_allow_html=True)

hero_asset = asset_manifest["assets"]["night_islamabad_cityscape"] if dark_mode else asset_manifest["assets"]["daytime_northern_pakistan"]
hero_image = hero_asset["url"]
hero_edition = "NIGHT EDITION" if dark_mode else "CITY EDITION"
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
        f'<div class="hero-image-caption"><span>{hero_edition}</span><span>PAKISTAN · UNBOUND</span></div>',
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
            with st.container(border=True):
                rendered = get_display_image(asset["url"], aspect_ratio=(16, 9), focal_point=tuple(asset.get("focal_point", [0.5, 0.48])))
                st.image(rendered if rendered else asset["url"], use_container_width=True)
                st.caption(f'{asset["author"]} · {asset["license"]} · [Image source]({asset["page_url"]})')
                st.markdown(f'<div class="destination-name">{asset["title"]}</div><div class="destination-copy">{asset["description"]}</div>', unsafe_allow_html=True)
                if st.button(f'Explore {asset["title"]}', key=f'collection_{asset["key"]}', use_container_width=True):
                    st.session_state["selected_experience_collection"] = asset["key"]
                    st.switch_page("pages/11_Experience_Collection.py")
st.write("")
st.markdown('<div class="kicker">EDITORIAL DESTINATION SELECTION</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Journeys worth discovering</div>', unsafe_allow_html=True)
st.markdown('<div class="section-copy">A cross-section of Pakistan’s mountain, coastal, cultural and urban experiences. This is an editorial selection, not a popularity ranking.</div>', unsafe_allow_html=True)
featured = ["Hunza Valley", "Skardu", "Naran–Kaghan Valley", "Lahore", "K2 & Concordia Expedition", "Swat Valley"]
for start in range(0, len(featured), 3):
    cols = st.columns(3, gap="large")
    for col, name in zip(cols, featured[start:start+3]):
        item = DESTINATIONS.get(name)
        if item is None:
            st.warning(f"Destination profile temporarily unavailable: {name}. The rest of the atlas can still be used.")
            continue
        with col:
            image = get_commons_image(item["image_query"])
            if image:
                st.image(get_display_image(image["thumb_url"], aspect_ratio=(16, 9), focal_point=(0.5, 0.5)) or image["thumb_url"], use_container_width=True)
                st.caption(f'{image["artist"]} · {image["license"]} · [Image details]({image["page_url"]})' + (' · Illustrative regional reference' if image.get('illustrative') else ''))
            else:
                st.markdown('<div style="height:190px;border-radius:17px;background:linear-gradient(135deg,#EEE9DF,#D9C8B7);display:flex;align-items:center;justify-content:center;color:#183B3B;font-family:Georgia,serif">A place worth discovering</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="destination-meta">{item["region"]}</div><div class="destination-name">{name}</div><div class="destination-copy">{item["tagline"]}</div>', unsafe_allow_html=True)
            weather = get_weather(item["lat"], item["lon"])
            if weather and weather.get("current"):
                current = weather["current"]
                st.markdown(f'<div class="weather-chip">Current forecast · {current.get("temperature_2m", "—")}°C · Wind {current.get("wind_speed_10m", "—")} km/h</div>', unsafe_allow_html=True)
            else:
                st.caption("Live weather temporarily unavailable")
            if st.button("Explore this place", key=f"home_guide_{name}", use_container_width=True):
                st.session_state["selected_destination"] = name
                st.switch_page("pages/02_Destination_Guide.py")

st.write("")
a, b, c = st.columns([1, 1, 1], gap="large")
with a:
    st.markdown('<div class="soft-panel"><div class="kicker">PLAN WITH CONTEXT</div><div class="section-title">Make the journey yours.</div><p>Shape a trip around your time, interests and budget. Use destination guides to understand seasons, access and responsible travel considerations before you go.</p></div>', unsafe_allow_html=True)
    st.page_link("pages/03_Trip_Planner.py", label="Build a trip plan")
with b:
    st.markdown('<div class="soft-panel"><div class="kicker">REGIONAL DISCOVERY</div><div class="section-title">Explore the full atlas.</div><p>Search detailed attractions, regional destination clusters, festivals, image sources and the next places being researched.</p></div>', unsafe_allow_html=True)
    st.page_link("pages/00_Regional_Atlas.py", label="Open regional atlas")
with c:
    st.markdown('<div class="soft-panel"><div class="kicker">SEE THE BIGGER PICTURE</div><div class="section-title">Travel is also an economy.</div><p>Explore the tourism intelligence workspace: destination evidence, investment scenarios, local value and the data gaps that matter for better decisions.</p></div>', unsafe_allow_html=True)
    st.page_link("pages/05_Destination_Intelligence.py", label="Explore tourism intelligence")

st.caption("VoyagePK is an independent prototype, not an official government tourism service. Destination descriptions and approximate map anchors require local review. Verify travel, safety, access, permits and booking details with responsible local authorities and providers.")
