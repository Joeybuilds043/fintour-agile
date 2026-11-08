from __future__ import annotations
import os
import streamlit as st
from src.catalog import DESTINATIONS,EXPERIENCE_CATEGORIES
from src.services.media import get_commons_image

st.set_page_config(page_title="Discover Pakistan | Horizon",page_icon="🧭",layout="wide")
st.title("Discover Pakistan")
st.write("Find a destination through the experience you want — not just by looking at a list of cities.")
choices=["All experiences"]+[x["name"] for x in EXPERIENCE_CATEGORIES]
selected=st.selectbox("What would you like to experience?",choices)
region=st.selectbox("Explore by region",["All regions"]+sorted({d["region"] for d in DESTINATIONS.values()}))
query=st.text_input("Search destinations",placeholder="Try Hunza, heritage, coast or mountains")
results=[]
for name,item in DESTINATIONS.items():
    haystack=" ".join([name,item["region"],item["tagline"],item["overview"]," ".join(item["experiences"])]).lower()
    if selected!="All experiences" and selected not in item["experiences"]: continue
    if region!="All regions" and region!=item["region"]: continue
    if query.strip() and query.strip().lower() not in haystack: continue
    results.append((name,item))
st.caption(f"{len(results)} destination clusters match your selection. This is a curated pilot collection, not a national ranking.")
for start in range(0,len(results),3):
    cols=st.columns(3)
    for col,(name,item) in zip(cols,results[start:start+3]):
        with col:
            image=None if os.getenv("HORIZON_DISABLE_REMOTE_MEDIA")=="1" else get_commons_image(item["image_query"])
            if image:
                st.image(image["thumb_url"],use_container_width=True)
                st.caption(f'{image["license"]} · {image["artist"]} · [Licence]({image["license_url"]}) · [Image source]({image["page_url"]})')
            st.subheader(name)
            st.caption(item["region"])
            st.write(item["tagline"])
            st.markdown(" · ".join(item["experiences"][:4]))
            st.page_link("pages/02_Destination_Guide.py",label="Open destination guide →")
if not results: st.info("No destination matches those filters. Try a broader search.")
