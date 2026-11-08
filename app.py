from __future__ import annotations

import json
import streamlit as st

from src.catalog import DESTINATIONS, EXPERIENCE_CATEGORIES
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
.display-title{color:var(--voyage-ink)!important;font-family:"Cormorant Garamond",Georgia,serif;font-weight:700;font-size:clamp(48px,5.4vw,78px);line-height:.98;letter-spacing:-1.2px;margin:10px 0 20px}
.lede{font-size:16px;line-height:1.85;color:var(--voyage-muted);max-width:680px}
.kicker{font-size:10px;letter-spacing:2.3px;text-transform:uppercase;color:#C7A35B;font-weight:700}
.section-title{color:var(--voyage-ink)!important;font-family:"Cormorant Garamond",Georgia,serif;font-weight:700;font-size:clamp(32px,3.2vw,44px);line-height:1.02;margin:4px 0 9px}
.section-copy{color:var(--voyage-muted);font-size:14px;line-height:1.7;max-width:720px}
.soft-panel{background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:20px;padding:20px;height:100%}
.category-tile{background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:15px;padding:16px 14px;min-height:105px}
.category-letter{width:27px;height:27px;border-radius:50%;background:#E8E1D5;color:#173B3A;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;margin-bottom:10px}
.category-name{font-weight:700;font-size:14px;color:var(--voyage-ink)}
.category-copy{font-size:11px;color:#657875;line-height:1.5;margin-top:4px}
.destination-name{color:var(--voyage-ink);font-family:"Cormorant Garamond",Georgia,serif;font-weight:700;font-size:27px;margin:8px 0 2px}
.destination-meta{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#657875}
.destination-copy{font-size:13px;line-height:1.65;color:var(--voyage-muted);min-height:43px}
.hero-note{border-left:2px solid #C7A35B;padding:6px 0 6px 14px;color:var(--voyage-muted);font-size:11px;line-height:1.7;margin-top:14px;letter-spacing:.25px}.mosaic-label{display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin:5px 0 0;color:var(--voyage-ink);font-family:"Cormorant Garamond",Georgia,serif;font-size:22px;font-weight:700}.mosaic-label small{font-family:"Manrope",sans-serif;font-size:9px;letter-spacing:1.4px;text-transform:uppercase;color:var(--voyage-muted);font-weight:600}.mosaic-label-small{font-size:18px}.mosaic-subtitle{font-family:"Manrope",sans-serif;font-size:9px;letter-spacing:1.3px;text-transform:uppercase;color:var(--voyage-muted);margin:0 0 7px}
.weather-chip{display:inline-block;margin:6px 0 2px;padding:6px 10px;border-radius:20px;background:rgba(24,89,60,.14);color:var(--voyage-ink);font-size:11px;font-weight:600}
@media(max-width:700px){.display-title{font-size:48px}.section-title{font-size:31px}.voyage-masthead-kicker{font-size:18px}.mosaic-label{font-size:19px}}
</style>
""", unsafe_allow_html=True)



with st.sidebar:
    st.markdown('<div class="voyage-sidebar-note">A considered guide to Pakistan</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="horizon-sidebar-kicker">THE DESTINATION ATLAS</div>', unsafe_allow_html=True)
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
# The homepage hero is an editorial destination collage in both appearance modes.
# Avoid the former Islamabad night skyline: the first impression should sell Pakistan's
# landscape and cultural variety, not read as a generic city-at-night banner.
hero_photos = [
    ("Passu Cones · Hunza", "Passu Hunza", "Karakoram landscapes"),
    ("Badshahi Mosque · Lahore", "Badshahi Mosque Lahore", "Living heritage"),
    ("Kund Malir · Balochistan", "Kund Malir Beach Hingol", "Arabian Sea coast"),
]
st.markdown(
    '<div class="voyage-masthead"><svg viewBox="0 0 92 56" role="img" aria-label="Flag of Pakistan" class="pakistan-flag"><rect width="92" height="56" rx="4" fill="#01411C"/><rect width="20" height="56" fill="#FFFFFF"/><circle cx="57" cy="27" r="17" fill="#FFFFFF"/><circle cx="63" cy="22" r="14" fill="#01411C"/><path d="M70 7l3.2 7.4 8 .7-6.1 5.2 1.8 7.8-6.9-4.1-6.9 4.1 1.8-7.8-6.1-5.2 8-.7z" fill="#FFFFFF"/></svg><div><div class="voyage-masthead-kicker">VOYAGEPK <span class="masthead-divider">/</span> PAKISTAN UNBOUND</div><div class="voyage-masthead-sub">LANDSCAPES · LIVING CULTURES · HERITAGE · PLACE-BASED TRAVEL</div></div></div><div class="kicker">THE COUNTRY, IN ALL ITS CONTRASTS</div>',
    unsafe_allow_html=True,
)
left, right = st.columns([0.88, 1.32], gap="large", vertical_alignment="center")
with left:
    st.markdown('<div class="display-title">Pakistan is more than a destination. It is a world of journeys.</div>', unsafe_allow_html=True)
    st.markdown('<div class="lede">From the high Karakoram to historic cities and the Arabian Sea, discover a country shaped by extraordinary landscapes, living cultures and layered histories. VoyagePK brings destination guides, thoughtful trip planning and tourism intelligence into one considered travel experience — grounded in place, context and responsible exploration.</div>', unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/01_Discover_Pakistan.py", label="Explore Pakistan")
    st.markdown('<div class="hero-note">Karakoram to coast · Sacred places to ancient cities · One connected travel atlas</div>', unsafe_allow_html=True)
with right:
    main_photo = get_commons_image(hero_photos[0][1])
    side_photos = [get_commons_image(hero_photos[1][1]), get_commons_image(hero_photos[2][1])]
    mosaic_main, mosaic_side = st.columns([1.18, 1], gap="small")
    with mosaic_main:
        if main_photo:
            rendered = get_display_image(main_photo["thumb_url"], aspect_ratio=(4, 5), focal_point=(0.53, 0.5))
            st.image(rendered if rendered else main_photo["thumb_url"], use_container_width=True)
            st.markdown(f'<div class="mosaic-label"><span>{hero_photos[0][0]}</span></div><div class="mosaic-subtitle">{hero_photos[0][2]}</div>', unsafe_allow_html=True)
            st.caption(f'{main_photo["artist"]} · {main_photo["license"]} · [Source]({main_photo["page_url"]})')
    with mosaic_side:
        for asset, meta in zip(side_photos, hero_photos[1:]):
            if asset:
                rendered = get_display_image(asset["thumb_url"], aspect_ratio=(5, 4), focal_point=(0.5, 0.48))
                st.image(rendered if rendered else asset["thumb_url"], use_container_width=True)
                st.markdown(f'<div class="mosaic-label mosaic-label-small"><span>{meta[0]}</span></div><div class="mosaic-subtitle">{meta[2]}</div>', unsafe_allow_html=True)
                st.caption(f'{asset["artist"]} · {asset["license"]} · [Source]({asset["page_url"]})')
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
                st.page_link("pages/01_Discover_Pakistan.py", label=f'Explore {asset["category"]}')
st.write("")
st.markdown('<div class="kicker">EDITORIAL DESTINATION SELECTION</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Journeys worth discovering</div>', unsafe_allow_html=True)
st.markdown('<div class="section-copy">A cross-section of Pakistan’s mountain, coastal, cultural and urban experiences. This is an editorial selection, not a popularity ranking.</div>', unsafe_allow_html=True)
featured = ["Hunza Valley", "Lahore", "Nankana Sahib & Sikh Heritage", "Swat Buddhist Heritage Circuit", "Desan Meadows & Upper Kalam", "Skardu"]
for start in range(0, len(featured), 3):
    cols = st.columns(3, gap="large")
    for col, name in zip(cols, featured[start:start+3]):
        item = DESTINATIONS[name]
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
a, b = st.columns([1, 1], gap="large")
with a:
    st.markdown('<div class="soft-panel"><div class="kicker">PLAN WITH CONTEXT</div><div class="section-title">Make the journey yours.</div><p>Shape a trip around your time, interests and budget. Use destination guides to understand seasons, access and responsible travel considerations before you go.</p></div>', unsafe_allow_html=True)
    st.page_link("pages/03_Trip_Planner.py", label="Build a trip plan")
with b:
    st.markdown('<div class="soft-panel"><div class="kicker">SEE THE BIGGER PICTURE</div><div class="section-title">Travel is also an economy.</div><p>Explore the tourism intelligence workspace: destination evidence, investment scenarios, local value and the data gaps that matter for better decisions.</p></div>', unsafe_allow_html=True)
    st.page_link("pages/05_Destination_Intelligence.py", label="Explore tourism intelligence")

st.caption("VoyagePK is an independent prototype, not an official government tourism service. Destination descriptions and approximate map anchors require local review. Verify travel, safety, access, permits and booking details with responsible local authorities and providers.")
