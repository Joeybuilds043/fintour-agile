from __future__ import annotations

import streamlit as st

from src.catalog import DESTINATIONS, EXPERIENCE_CATEGORIES
from src.services.media import get_commons_image, get_display_image
from src.services.weather import get_weather
from src.ui import apply_visitor_theme

st.set_page_config(page_title="VoyagePK | Pakistan Unbound", page_icon=None, layout="wide")

apply_visitor_theme()
st.markdown("""
<style>
.display-title{font-family:'Playfair Display',Georgia,serif;font-size:clamp(43px,5.6vw,76px);line-height:1.02;letter-spacing:-1.8px;color:#173B3A;margin:10px 0 18px}
.lede{font-size:16px;line-height:1.85;color:#657875;max-width:610px}
.kicker{font-size:10px;letter-spacing:2.3px;text-transform:uppercase;color:#98613F;font-weight:700}
.section-title{font-family:'Playfair Display',Georgia,serif;font-size:clamp(28px,3vw,38px);line-height:1.12;margin:4px 0 7px;color:#173B3A}
.section-copy{color:#657875;font-size:14px;line-height:1.7;max-width:720px}
.soft-panel{background:#FFFCF6;border:1px solid #E4DCCE;border-radius:20px;padding:20px;height:100%}
.category-tile{background:#FFFCF6;border:1px solid #E4DCCE;border-radius:15px;padding:16px 14px;min-height:105px}
.category-letter{width:27px;height:27px;border-radius:50%;background:#E8E1D5;color:#173B3A;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;margin-bottom:10px}
.category-name{font-weight:700;font-size:14px;color:#173B3A}
.category-copy{font-size:11px;color:#657875;line-height:1.5;margin-top:4px}
.destination-name{font-family:'Playfair Display',Georgia,serif;font-size:22px;color:#173B3A;margin:8px 0 2px}
.destination-meta{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#657875}
.destination-copy{font-size:13px;line-height:1.65;color:#657875;min-height:43px}
.hero-note{border-left:2px solid #D9A77E;padding:4px 0 4px 13px;color:#657875;font-size:11px;line-height:1.6}
.weather-chip{display:inline-block;margin:6px 0 2px;padding:6px 10px;border-radius:20px;background:#E8F0EA;color:#234D47;font-size:11px;font-weight:600}
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

hero = get_commons_image("Hunza Valley Passu Cones Attabad Lake Pakistan")
st.markdown('<div class="horizon-flow" style="padding:10px 16px;margin:0 0 20px;color:#F4F0E7;font-size:10px;letter-spacing:2px;text-transform:uppercase">A living atlas of landscapes, culture and journeys across Pakistan</div><div class="kicker">PAKISTAN, CLOSER THAN YOU THINK</div>', unsafe_allow_html=True)
left, right = st.columns([0.92, 1.28], gap="large", vertical_alignment="center")
with left:
    st.markdown('<div class="display-title">A country of a thousand journeys.</div>', unsafe_allow_html=True)
    st.markdown('<div class="lede">Follow the curve of a mountain road. Find a courtyard hidden in an old city. Taste a region through its food. VoyagePK brings Pakistan’s landscapes, heritage and local experiences into one considered travel guide.</div>', unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/01_Discover_Pakistan.py", label="Explore Pakistan")
    st.markdown('<div class="hero-note">From the Karakoram to the Arabian Sea · 39 curated destination clusters · One connected travel atlas</div>', unsafe_allow_html=True)
with right:
    if hero:
        st.image(get_display_image(hero["thumb_url"], aspect_ratio=(16, 9), focal_point=(0.52, 0.48)) or hero["thumb_url"], use_container_width=True)
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
st.markdown('<div class="kicker">A FEW PLACES TO BEGIN</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Journeys worth discovering</div>', unsafe_allow_html=True)
st.markdown('<div class="section-copy">A cross-section of Pakistan’s mountain, coastal, cultural and urban experiences. This is an editorial selection, not a popularity ranking.</div>', unsafe_allow_html=True)
featured = ["Hunza Valley", "Lahore", "Neelum Valley", "Multan", "Hingol & Gwadar Coast", "Skardu"]
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
