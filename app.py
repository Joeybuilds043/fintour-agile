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
.voyage-masthead-kicker{font-family:Georgia,serif;color:#F6F2E8;font-size:16px;letter-spacing:1.4px}
.voyage-masthead-sub{font-family:Arial,sans-serif;color:#D8C58F;font-size:9px;letter-spacing:1.5px;margin-top:4px}
.category-photo-fallback{height:170px;border-radius:12px;background:linear-gradient(135deg,#123D2E,#1C4C57,#C2A25E);display:flex;align-items:center;justify-content:center;color:#F6F2E8;font-size:11px;letter-spacing:2px}
div[data-testid="stImage"] img{border:5px solid #C7A35B;border-radius:17px;box-shadow:0 15px 35px rgba(7,28,21,.2)}
.hero-frame:after{content:"";position:absolute;inset:8px;pointer-events:none;border:1px solid rgba(255,255,255,.58);background:linear-gradient(90deg,transparent 61.6%,rgba(255,255,255,.22) 61.8%,transparent 62%),linear-gradient(0deg,transparent 38%,rgba(255,255,255,.18) 38.2%,transparent 38.4%)} 
.hero-frame img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;object-position:61.8% 38.2%;border-radius:12px} 
.display-title{color:var(--voyage-ink)!important;font-family:'Playfair Display',Georgia,serif;font-size:clamp(43px,5.6vw,76px);line-height:1.02;letter-spacing:-1.8px;color:#173B3A;margin:10px 0 18px}
.lede{font-size:16px;line-height:1.85;color:var(--voyage-muted);max-width:680px}
.kicker{font-size:10px;letter-spacing:2.3px;text-transform:uppercase;color:#C7A35B;font-weight:700}
.section-title{color:var(--voyage-ink)!important;font-family:'Playfair Display',Georgia,serif;font-size:clamp(28px,3vw,38px);line-height:1.12;margin:4px 0 7px;color:#173B3A}
.section-copy{color:var(--voyage-muted);font-size:14px;line-height:1.7;max-width:720px}
.soft-panel{background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:20px;padding:20px;height:100%}
.category-tile{background:var(--voyage-surface);border:1px solid var(--voyage-line);border-radius:15px;padding:16px 14px;min-height:105px}
.category-letter{width:27px;height:27px;border-radius:50%;background:#E8E1D5;color:#173B3A;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;margin-bottom:10px}
.category-name{font-weight:700;font-size:14px;color:var(--voyage-ink)}
.category-copy{font-size:11px;color:#657875;line-height:1.5;margin-top:4px}
.destination-name{color:var(--voyage-ink);font-family:'Playfair Display',Georgia,serif;font-size:22px;color:#173B3A;margin:8px 0 2px}
.destination-meta{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#657875}
.destination-copy{font-size:13px;line-height:1.65;color:var(--voyage-muted);min-height:43px}
.hero-note{border-left:2px solid #D9A77E;padding:4px 0 4px 13px;color:var(--voyage-muted);font-size:11px;line-height:1.6}
.weather-chip{display:inline-block;margin:6px 0 2px;padding:6px 10px;border-radius:20px;background:rgba(24,89,60,.14);color:var(--voyage-ink);font-size:11px;font-weight:600}
@media(max-width:700px){.display-title{font-size:43px}.section-title{font-size:29px}}
</style>
""", unsafe_allow_html=True)



with st.sidebar:
    st.markdown('<div class="voyage-sidebar-note">A considered guide to Pakistan</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="horizon-sidebar-kicker">Discover</div>', unsafe_allow_html=True)
    st.page_link("app.py", label="The journey starts here")
    st.page_link("pages/01_Discover_Pakistan.py", label="Explore destinations")
    st.page_link("pages/02_Destination_Guide.py", label="Destination field guides")
    st.page_link("pages/03_Trip_Planner.py", label="Build an itinerary")
    st.page_link("pages/04_Explore_Map.py", label="Explore the atlas")
    st.divider()
    st.markdown('<div class="horizon-sidebar-kicker">Tourism insights</div>', unsafe_allow_html=True)
    st.page_link("pages/05_Destination_Intelligence.py", label="Destination intelligence")
    st.page_link("pages/06_Investment_Studio.py", label="Investment studio")
    st.page_link("pages/07_Data_Observatory.py", label="Data observatory")
    st.page_link("pages/08_AI_Travel_Concierge.py", label="Travel concierge")
    st.page_link("pages/09_AI_Strategy_Advisor.py", label="Strategy advisor")
    st.page_link("pages/10_Growth_Scenario_Planner.py", label="Growth scenarios")
    st.divider()
    st.caption("Independent destination discovery prototype. Travel thoughtfully and verify local conditions.")

with open("assets/manifest.json", encoding="utf-8") as asset_file:
    asset_manifest = json.load(asset_file)
active_theme = st.session_state.get("voyage_theme", "Light")
hero_asset = asset_manifest["assets"]["night_islamabad_cityscape" if active_theme == "Dark" else "daytime_northern_pakistan"]
hero = {"url": hero_asset["url"], "title": hero_asset["caption"], "artist": hero_asset.get("author", "Creator listed on source page"), "license": hero_asset.get("license", "See source page"), "page_url": hero_asset["page_url"], "focal_point": tuple(hero_asset.get("focal_point", [0.618, 0.382]))}
st.markdown('<div class="voyage-masthead"><svg viewBox="0 0 92 56" role="img" aria-label="Flag of Pakistan" class="pakistan-flag"><rect width="92" height="56" rx="4" fill="#01411C"/><rect width="20" height="56" fill="#FFFFFF"/><circle cx="57" cy="27" r="17" fill="#FFFFFF"/><circle cx="63" cy="22" r="14" fill="#01411C"/><path d="M70 7l3.2 7.4 8 .7-6.1 5.2 1.8 7.8-6.9-4.1-6.9 4.1 1.8-7.8-6.1-5.2 8-.7z" fill="#FFFFFF"/></svg><div><div class="voyage-masthead-kicker">PAKISTAN · DESTINATION ATLAS</div><div class="voyage-masthead-sub">LANDSCAPES · LIVING CULTURES · HERITAGE · PLACE-BASED TRAVEL</div></div></div><div class="kicker">A NATIONAL DESTINATION DISCOVERY PLATFORM</div>', unsafe_allow_html=True)
left, right = st.columns([0.92, 1.28], gap="large", vertical_alignment="center")
with left:
    st.markdown('<div class="display-title">Discover Pakistan through its places, people and living heritage.</div>', unsafe_allow_html=True)
    st.markdown('<div class="lede">VoyagePK approaches tourism as an interconnected destination system: landscapes, cultural assets, historic places, local enterprise and visitor experiences are understood in relation to one another. The platform brings destination discovery, itinerary planning and tourism intelligence into a single digital environment, with an emphasis on place-based interpretation, responsible visitor management and the long-term stewardship of Pakistan’s natural and cultural heritage.</div>', unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/01_Discover_Pakistan.py", label="Explore Pakistan")
    st.markdown('<div class="hero-note">From the Karakoram to the Arabian Sea · A curated, expanding destination collection · One connected travel atlas</div>', unsafe_allow_html=True)
with right:
    if hero:
        hero_image = get_display_image(hero["url"], aspect_ratio=(16, 9), focal_point=hero["focal_point"])
        st.image(hero_image if hero_image else hero["url"], use_container_width=True, caption=None)
        st.caption(f'{hero["title"]} · {hero["artist"]} · {hero["license"]} · [Image source]({hero["page_url"]})' + (' · Illustrative regional reference' if hero.get('illustrative') else ''))
    else:
        st.markdown('<div class="soft-panel" style="min-height:390px;display:flex;align-items:center;justify-content:center;background:linear-gradient(145deg,#EEE9DF,#D9C8B7)"><div><div class="section-title">The mountains are only the beginning.</div><p>A regional image is not available for this destination yet.</p></div></div>', unsafe_allow_html=True)

st.write("")
st.markdown('<div class="kicker">CHOOSE YOUR OWN WAY THROUGH THE COUNTRY</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">What does travel look like to you?</div>', unsafe_allow_html=True)
st.markdown('<div class="section-copy">A place can be many things at once. Explore by the experience you want, then discover the destinations that bring it to life.</div>', unsafe_allow_html=True)
cols = st.columns(5, gap="small")
for i, category in enumerate(EXPERIENCE_CATEGORIES):
    with cols[i % 5]:
        st.markdown(f'<div class="category-tile"><div class="category-letter">{category["symbol"]}</div><div class="category-name">{category["name"]}</div><div class="category-copy">{category["short"]}</div></div>', unsafe_allow_html=True)

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
