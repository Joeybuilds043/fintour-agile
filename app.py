from __future__ import annotations

import streamlit as st

from src.catalog import DESTINATIONS, EXPERIENCE_CATEGORIES
from src.services.media import get_commons_image, get_display_image

st.set_page_config(page_title="Horizon Tourism | Pakistan, closer than you think", page_icon=None, layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root{--ink:#183B3B;--muted:#687976;--paper:#F5F1E8;--white:#FFFCF6;--sea:#C47A50;--ice:#EEE9DF;--sand:#C47A50;--line:#E5DED2}
.stApp{background:var(--paper);color:var(--ink);font-family:'DM Sans',sans-serif}
[data-testid="stHeader"]{background:rgba(247,245,239,.94)}
[data-testid="stSidebar"]{background:#EEE9DF;border-right:1px solid var(--line)}
.block-container{max-width:1480px;padding-top:1.15rem;padding-bottom:4rem}
h1,h2,h3{color:var(--ink)!important}
h1,.display-title,.section-title{font-family:'Playfair Display',Georgia,serif!important}
.display-title{font-size:clamp(43px,5.6vw,76px);line-height:1.02;letter-spacing:-1.8px;color:#183B3B;margin:10px 0 18px}
.lede{font-size:16px;line-height:1.85;color:#687976;max-width:610px}
.kicker{font-size:10px;letter-spacing:2.3px;text-transform:uppercase;color:#A85F3C;font-weight:700}
.section-title{font-size:clamp(28px,3vw,38px);line-height:1.12;margin:4px 0 7px}
.section-copy{color:#687976;font-size:14px;line-height:1.7;max-width:720px}
.brandmark{font-family:'Playfair Display',serif;font-size:26px;letter-spacing:.3px;color:#183B3B;font-weight:700}
.brand-sub{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#687976}
.soft-panel{background:var(--white);border:1px solid var(--line);border-radius:20px;padding:20px;height:100%}
.category-tile{background:#FFFCF6;border:1px solid #E5DED2;border-radius:15px;padding:16px 14px;min-height:105px}
.category-letter{width:27px;height:27px;border-radius:50%;background:#EEE9DF;color:#183B3B;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;margin-bottom:10px}
.category-name{font-weight:700;font-size:14px;color:#183B3B}
.category-copy{font-size:11px;color:#687976;line-height:1.5;margin-top:4px}
.destination-name{font-family:'Playfair Display',Georgia,serif;font-size:22px;color:#1b3940;margin:8px 0 2px}
.destination-meta{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#687976}
.destination-copy{font-size:13px;line-height:1.65;color:#68797d;min-height:43px}
.hero-note{border-left:2px solid #D9C8B7;padding:4px 0 4px 13px;color:#687976;font-size:11px;line-height:1.6}
div[data-testid="stImage"] img{border-radius:17px;object-fit:cover;filter:saturate(1.08) contrast(1.035)}
div[data-testid="stButton"]>button{border-radius:30px;border:1px solid #183B3B;background:#183B3B;color:white;font-weight:700;min-height:42px;padding:0 20px}
div[data-testid="stButton"]>button:hover{background:#C47A50;border-color:#C47A50;color:white}
div[data-testid="stPageLink"] a{border-radius:30px}
[data-testid="stMetric"]{background:#FFFCF6;border:1px solid var(--line);border-radius:14px;padding:12px}
hr{border-color:var(--line)}footer{visibility:hidden}
@media(max-width:700px){.display-title{font-size:43px}.block-container{padding:1rem 1rem 3rem}.section-title{font-size:29px}}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="brandmark">Horizon</div><div class="brand-sub">Pakistan travel & tourism intelligence</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown("**DISCOVER**")
    st.page_link("app.py", label="The journey starts here")
    st.page_link("pages/01_Discover_Pakistan.py", label="Explore destinations")
    st.page_link("pages/02_Destination_Guide.py", label="Destination field guides")
    st.page_link("pages/03_Trip_Planner.py", label="Build an itinerary")
    st.page_link("pages/04_Explore_Map.py", label="Explore the atlas")
    st.divider()
    st.markdown("**TOURISM INSIGHTS**")
    st.page_link("pages/05_Destination_Intelligence.py", label="Destination intelligence")
    st.page_link("pages/06_Investment_Studio.py", label="Investment studio")
    st.page_link("pages/07_Data_Observatory.py", label="Data observatory")
    st.page_link("pages/08_AI_Travel_Concierge.py", label="Travel concierge")
    st.page_link("pages/09_AI_Strategy_Advisor.py", label="Strategy advisor")
    st.page_link("pages/10_Growth_Scenario_Planner.py", label="Growth scenarios")
    st.divider()
    st.caption("Independent destination discovery prototype. Travel thoughtfully and verify local conditions.")

hero = get_commons_image("Hunza Valley Passu Cones Attabad Lake Pakistan")
st.markdown('<div class="kicker">PAKISTAN, CLOSER THAN YOU THINK</div>', unsafe_allow_html=True)
left, right = st.columns([0.92, 1.28], gap="large", vertical_alignment="center")
with left:
    st.markdown('<div class="display-title">A country of a thousand journeys.</div>', unsafe_allow_html=True)
    st.markdown('<div class="lede">Follow the curve of a mountain road. Find a courtyard hidden in an old city. Taste a region through its food. Horizon brings Pakistan’s landscapes, heritage and local experiences into one considered travel guide.</div>', unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/01_Discover_Pakistan.py", label="Explore Pakistan")
    st.markdown('<div class="hero-note">From the Karakoram to the Arabian Sea · 39 curated destination clusters · One connected travel atlas</div>', unsafe_allow_html=True)
with right:
    if hero:
        st.image(get_display_image(hero["thumb_url"]) or hero["thumb_url"], use_container_width=True)
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
                st.image(get_display_image(image["thumb_url"]) or image["thumb_url"], use_container_width=True)
                st.caption(f'{image["artist"]} · {image["license"]} · [Image details]({image["page_url"]})' + (' · Illustrative regional reference' if image.get('illustrative') else ''))
            else:
                st.markdown('<div style="height:190px;border-radius:17px;background:linear-gradient(135deg,#EEE9DF,#D9C8B7);display:flex;align-items:center;justify-content:center;color:#183B3B;font-family:Georgia,serif">A place worth discovering</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="destination-meta">{item["region"]}</div><div class="destination-name">{name}</div><div class="destination-copy">{item["tagline"]}</div>', unsafe_allow_html=True)
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

st.caption("Horizon is an independent prototype, not an official government tourism service. Destination descriptions and approximate map anchors require local review. Verify travel, safety, access, permits and booking details with responsible local authorities and providers.")
