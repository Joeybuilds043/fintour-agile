from __future__ import annotations

import streamlit as st
import html
import re

from src.catalog import DESTINATIONS, PROVINCE_ORDER
from src.destination_gallery import DESTINATION_IMAGE_BATCHES
from src.research_register import DISCOVERY_LEADS, EVENT_RECORDS, IMAGE_CANDIDATES, RESEARCH_DESTINATIONS
from src.services.media import get_commons_image, get_display_image
from src.ui import apply_visitor_theme

# Festival/event images supplied for this section only.
ATLAS_EVENT_IMAGES = {
    "Cholistan Desert Jeep Rally": {"thumb_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcJet6WvzbSBfI0ZB0DXtovyVZXpqLmtRjgtxJaRCiysVr7PWtvQcrImw&s=10","page_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcJet6WvzbSBfI0ZB0DXtovyVZXpqLmtRjgtxJaRCiysVr7PWtvQcrImw&s=10","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Mela Chiraghan": {"thumb_url":"https://apnaorg.com/articles/news-60/dailytimes_clip_image001.jpg","page_url":"https://apnaorg.com/articles/news-60/dailytimes_clip_image001.jpg","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Vaisakhi Mela and Sikh Pilgrimage": {"thumb_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZDXAO1C6rYNZv73FHe8RyQAoFUX1tBQskaL4ItF6iyjBMDlHGMSxK3Ks&s=10","page_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZDXAO1C6rYNZv73FHe8RyQAoFUX1tBQskaL4ItF6iyjBMDlHGMSxK3Ks&s=10","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Urs of Lal Shahbaz Qalandar": {"thumb_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8fShZd9Z4WUaQPOg2Qf15MBxttmf5jO6UA10o0EwjMt63s5IKcFmyK3Bm&s=10","page_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8fShZd9Z4WUaQPOg2Qf15MBxttmf5jO6UA10o0EwjMt63s5IKcFmyK3Bm&s=10","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Thal Desert Rally & Cultural Festival": {"thumb_url":"https://i.dawn.com/primary/2017/11/5a11fcf144249.jpg","page_url":"https://i.dawn.com/primary/2017/11/5a11fcf144249.jpg","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Punjab Paragliding Championship": {"thumb_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQa1bStxoKLtg7Rm8ob87NPVRT0RgkKVG9DtWFeiMruZcUqEBpXb4EXuFw&s=10","page_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQa1bStxoKLtg7Rm8ob87NPVRT0RgkKVG9DtWFeiMruZcUqEBpXb4EXuFw&s=10","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Sindhi Cultural Day (Ekta Day)": {"thumb_url":"https://www.geo.tv/assets/uploads/updates/2022-12-04/456571_9046172_updates.jpg","page_url":"https://www.geo.tv/assets/uploads/updates/2022-12-04/456571_9046172_updates.jpg","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Urs of Data Ganj Bakhsh": {"thumb_url":"https://i.dawn.com/primary/2018/10/5bd60e6a0032d.jpg","page_url":"https://i.dawn.com/primary/2018/10/5bd60e6a0032d.jpg","artist":"Existing Data Ganj Bakhsh Urs image retained","license":"Source and reuse licence not independently verified"},
    "Waris Shah Mela": {"thumb_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBdID3hVjkfD6W8q3K9NH--gqF30hpHPxIdR9LrAQaUVGe7EFjE8Ohv4aR&s=10","page_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBdID3hVjkfD6W8q3K9NH--gqF30hpHPxIdR9LrAQaUVGe7EFjE8Ohv4aR&s=10","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Jashn-e-Baharan & Basant": {"thumb_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVkKj7cQ7RJzJ5QNOjV3wX7W7XHbVvLPe4Zek2zAEYl6l2UfaZzd-9Dn8N&s=10","page_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVkKj7cQ7RJzJ5QNOjV3wX7W7XHbVvLPe4Zek2zAEYl6l2UfaZzd-9Dn8N&s=10","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Lohri": {"thumb_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYTuAa4j5h0XGGETyg9gCH_tFyqZsRG3InuWnwhIjH5UwMxlqlRLCK4tE&s=10","page_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYTuAa4j5h0XGGETyg9gCH_tFyqZsRG3InuWnwhIjH5UwMxlqlRLCK4tE&s=10","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "National Horse & Cattle Show": {"thumb_url":"https://www.urdunews.com/sites/default/files/pictures/February/36496/2025/480693352_1209120447237906_4919564687668903105_n.jpg","page_url":"https://www.urdunews.com/node/886386","artist":"Urdu News","license":"Copyright and reuse permission not independently verified"},
    "Eid-ul-Fitr": {"thumb_url":"https://i.tribune.com.pk/media/images/618938-LahoreBadshahimosqueEidMuslimsREUTERS-1381912038/618938-LahoreBadshahimosqueEidMuslimsREUTERS-1381912038.jpg","page_url":"https://i.tribune.com.pk/media/images/618938-LahoreBadshahimosqueEidMuslimsREUTERS-1381912038/618938-LahoreBadshahimosqueEidMuslimsREUTERS-1381912038.jpg","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Eid-ul-Adha": {"thumb_url":"https://www.globaltimes.cn/Portals/0/attachment/2021/2021-05-14/7adf0b02-86d4-4088-afac-610f0328cca5.jpeg","page_url":"https://www.globaltimes.cn/Portals/0/attachment/2021/2021-05-14/7adf0b02-86d4-4088-afac-610f0328cca5.jpeg","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Eid Milad-un-Nabi": {"thumb_url":"https://i.tribune.com.pk/media/images/EId-Miladun-Nabi-main1634658140-0/EId-Miladun-Nabi-main1634658140-0.png","page_url":"https://i.tribune.com.pk/media/images/EId-Miladun-Nabi-main1634658140-0/EId-Miladun-Nabi-main1634658140-0.png","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Independence Day (Jashn-e-Azadi)": {"thumb_url":"https://i.dawn.com/primary/2025/08/141420424c6c1f6.png","page_url":"https://www.dawn.com/news/1930834","artist":"Dawn","license":"Copyright and reuse permission not independently verified"},
    "Urs of Shah Abdul Latif Bhittai": {"thumb_url":"https://www.nation.com.pk/digital_images/large/2023-09-01/annual-urs-of-shah-abdul-latif-bhittai-begins-1693548662-5559.jpg","page_url":"https://www.nation.com.pk/digital_images/large/2023-09-01/annual-urs-of-shah-abdul-latif-bhittai-begins-1693548662-5559.jpg","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Shandur Polo Festival": {"thumb_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmQ1WJQLOE34fQwTFZg3DkiQrgtR9HZxiR6Hf1Uj3dSZko-8Lg2Z2QXYrO&s=10","page_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmQ1WJQLOE34fQwTFZg3DkiQrgtR9HZxiR6Hf1Uj3dSZko-8Lg2Z2QXYrO&s=10","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Chilam Joshi Festival": {"thumb_url":"https://www.youngpioneertours.com/wp-content/uploads/2025/10/Pakistan-kalash-valley-chilam-Joshi-Festival-women.jpg","page_url":"https://www.youngpioneertours.com/wp-content/uploads/2025/10/Pakistan-kalash-valley-chilam-Joshi-Festival-women.jpg","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Kalam Summer Festival": {"thumb_url":"https://greenpaktourism.com/_next/image?url=%2Fimages%2Flicensed%2Fqaqlasht-festival-polo.jpg&w=1920&q=75","page_url":"https://greenpaktourism.com/_next/image?url=%2Fimages%2Flicensed%2Fqaqlasht-festival-polo.jpg&w=1920&q=75","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Hinglaj Mata Yatra": {"thumb_url":"https://i.redd.it/mg4pb37tifya1.png","page_url":"https://i.redd.it/mg4pb37tifya1.png","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Sibi Mela": {"thumb_url":"https://www.geo.tv/assets/uploads/updates/2019-02-21/0_4_035119_album.jpg","page_url":"https://www.geo.tv/assets/uploads/updates/2019-02-21/0_4_035119_album.jpg","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Ginani Harvest Festival": {"thumb_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1OAXcJvWhp6lgXUBD7tKWnb5T4M4vzj8PZHFYU-z9gi65AWRizDTjei50&s=10","page_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1OAXcJvWhp6lgXUBD7tKWnb5T4M4vzj8PZHFYU-z9gi65AWRizDTjei50&s=10","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Mangla Water Festival": {"thumb_url":"https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2b/05/35/d6/caption.jpg?w=800&h=800&s=1","page_url":"https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2b/05/35/d6/caption.jpg?w=800&h=800&s=1","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Leepa Valley Mela": {"thumb_url":"https://lh3.googleusercontent.com/d/13mHWrQvLvKvmSpPBmY7p-osfgKGHnOE-=w1800","page_url":"https://drive.google.com/file/d/13mHWrQvLvKvmSpPBmY7p-osfgKGHnOE-/view?usp=drive_link","artist":"User-supplied Google Drive image","license":"User-provided; sharing access and reuse rights not independently verified"},
    "Lok Virsa Folk Festival (Lok Mela)": {"thumb_url":"https://www.youlinmagazine.com/articles/lok-mela-2017-at-lok-virsa-islamabad.jpg","page_url":"https://www.youlinmagazine.com/story/lok-mela-2017-at-lok-virsa-islamabad/ODEz","artist":"Youlin Magazine","license":"Copyright and reuse permission not independently verified"},
    "Islamabad Marathon": {"thumb_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuspr_nrWU6nPfb4pUIxnr0NzoW_W2m1-6MdfbjHhKfw&s=10","page_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuspr_nrWU6nPfb4pUIxnr0NzoW_W2m1-6MdfbjHhKfw&s=10","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Uchal Festival": {"thumb_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVAUYvuxwVTFGP_H60trf_tvtWjxNwu1qi67lr4IgctgHwSZhkWrXPeqrU&s=10","page_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVAUYvuxwVTFGP_H60trf_tvtWjxNwu1qi67lr4IgctgHwSZhkWrXPeqrU&s=10","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Choimus (Chaumos) Festival": {"thumb_url":"https://i.dawn.com/primary/2016/11/58295b3c48a18.jpg","page_url":"https://i.dawn.com/primary/2016/11/58295b3c48a18.jpg","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
    "Malam Jabba Winter Sports Festival": {"thumb_url":"https://cdn-blog.zameen.com/blog/wp-content/uploads/2020/01/Cover-20-20-1.jpg","page_url":"https://cdn-blog.zameen.com/blog/wp-content/uploads/2020/01/Cover-20-20-1.jpg","artist":"User-supplied image URL","license":"Source and reuse licence not independently verified"},
}

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
.atlas-photo-frame img{display:block;width:100%;height:210px;object-fit:contain;border-radius:10px;background:linear-gradient(135deg,#E9D9B6 0%,#D7E7DE 48%,#C9DFE5 100%);padding:10px}
div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stImage"] img{padding:4px;border:1px solid rgba(199,163,91,.7);border-radius:14px;background:rgba(199,163,91,.10);box-shadow:0 10px 24px rgba(8,25,20,.12)}
.atlas-photo-placeholder{height:178px;border-radius:9px;background:linear-gradient(135deg,#123D2D,#355D62 62%,#C7A35B);display:flex;align-items:center;justify-content:center;color:#F6F2E8;font-size:10px;font-weight:800;letter-spacing:2px}
.atlas-card-meta{margin-top:12px;font-size:9px;letter-spacing:1.4px;text-transform:uppercase;color:#111A14!important;font-weight:850;min-height:28px;max-height:28px;overflow:hidden;opacity:1!important}
.atlas-event-meta{display:block;width:100%;height:34px;min-height:34px;max-height:34px;margin:10px 0 8px;overflow:hidden}
.atlas-event-date{display:flex;align-items:center;justify-content:center;box-sizing:border-box;width:100%;height:34px;min-height:34px;max-height:34px;padding:0 11px;border:1px solid #A9C5B0;border-radius:8px;background:#E8F1E9;color:#174B35!important;font-family:Inter,Arial,sans-serif;font-size:10px;line-height:1;font-weight:750;letter-spacing:.15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.atlas-record-note{padding:13px 14px;border:1px solid #285D45;border-left:4px solid #A9C5B0;border-radius:9px;background:#174B35!important;color:#FFFFFF!important;font-family:Inter,Arial,sans-serif;font-size:12px;line-height:1.65;font-weight:450}
.atlas-record-location{margin-top:9px;padding:10px 13px;border:1px solid #B8CFBD;border-radius:8px;background:#EAF2EB;color:#174B35!important;font-size:12px;line-height:1.5;font-weight:800}
.atlas-record-location strong{color:#174B35!important}
/* Festival card: keep the date directly below the event title and make the expander a clear action */
/* Keep the expander label native; only style its surface to avoid distorted glyphs. */
[class*="st-key-atlas-event-card-"] [data-testid="stExpander"] details>summary{
    background:linear-gradient(135deg,#174B35 0%,#246447 100%)!important;
    border:1px solid #174B35!important;
    border-radius:9px!important;
    padding:9px 13px!important;
    box-shadow:0 3px 9px rgba(23,75,53,.14)!important;
}
[class*="st-key-atlas-event-card-"] [data-testid="stExpander"] details>summary p{
    color:#FFFFFF!important;
}
[class*="st-key-atlas-event-card-"] [data-testid="stExpander"] details>summary:hover{
    background:#2B704F!important;
    border-color:#2B704F!important;
}
[class*="st-key-atlas-event-card-"] [data-testid="stVerticalBlockBorderWrapper"]{height:100%;min-height:470px;display:flex}
[class*="st-key-atlas-event-card-"] [data-testid="stImage"]{height:210px;min-height:210px;max-height:210px;display:flex;align-items:center;justify-content:center;overflow:hidden;background:#E9E2D4;border-radius:12px;padding:6px}
[class*="st-key-atlas-event-card-"] [data-testid="stImage"] img{width:100%;height:198px;object-fit:contain!important;background:transparent;border:0!important;box-shadow:none!important}
[class*="st-key-atlas-event-card-"] .atlas-card-title{height:54px;min-height:54px;max-height:54px;color:#111A14!important}
[class*="st-key-atlas-event-card-"] .atlas-card-copy{height:78px;min-height:78px;max-height:78px;color:#111A14!important}
[class*="st-key-atlas-event-card-"] [data-testid="stExpander"]{margin-top:auto;flex-shrink:0}
@media(max-width:700px){[class*="st-key-atlas-event-card-"] [data-testid="stVerticalBlockBorderWrapper"]{height:auto;min-height:0}[class*="st-key-atlas-event-card-"] .atlas-card-copy{height:auto;min-height:70px;max-height:95px}}
.atlas-card-title{font-family:'Cormorant Garamond',Georgia,serif;font-size:23px;line-height:1.08;font-weight:700;color:#111A14!important;margin:5px 0 7px;height:52px;min-height:52px;max-height:52px;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;opacity:1!important}
.atlas-card-copy{font-size:12px;line-height:1.55;color:#26352C!important;height:78px;min-height:78px;max-height:78px;overflow:hidden;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;opacity:1!important}
.atlas-tag-row{height:52px;min-height:52px;max-height:52px;overflow:hidden;display:block}.atlas-tag{display:inline-block;padding:4px 8px;margin:3px 3px 0 0;border:1px solid #C7D1C9;border-radius:30px;font-size:9px;color:#26352C!important;opacity:1!important}
.atlas-credit{font-size:9px;line-height:1.45;color:#26352C!important;margin:5px 2px 8px;opacity:1!important}
.atlas-record-note{padding:10px 12px;border-left:2px solid #C7A35B;background:var(--voyage-surface);border-radius:0 9px 9px 0;font-size:12px;line-height:1.6;color:var(--voyage-muted)}
div[data-testid="stVerticalBlockBorderWrapper"]{border-color:var(--voyage-line);border-radius:17px}
div[data-testid="stImage"] img{border-radius:10px;object-fit:contain;box-shadow:0 8px 20px rgba(8,25,20,.10)}
[class*="st-key-batch-gallery-card-"]{height:100%;min-height:360px;padding:13px!important;border:1px solid rgba(23,92,67,.22)!important;border-radius:18px!important;background:linear-gradient(145deg,#F3E8D0 0%,#E5F0E8 52%,#DCEAF0 100%)!important;box-shadow:0 12px 30px rgba(13,55,42,.09)!important;display:flex;flex-direction:column}
.st-key-batch-gallery-card [data-testid="stImage"]{height:224px;min-height:224px;max-height:224px;display:flex;align-items:center;justify-content:center;overflow:hidden;border-radius:13px;background:linear-gradient(135deg,#D7C59F,#C8E0D5 55%,#B8D6DF);padding:7px}
.atlas-gallery-image-slot{height:224px;min-height:224px;max-height:224px;width:100%;box-sizing:border-box;border:1px dashed rgba(23,92,67,.35);border-radius:13px;background:linear-gradient(135deg,rgba(215,197,159,.28),rgba(200,224,213,.28) 55%,rgba(184,214,223,.28))}
.atlas-gallery-image-slot--unavailable{background:linear-gradient(135deg,rgba(215,197,159,.18),rgba(200,224,213,.18) 55%,rgba(184,214,223,.18))}
.st-key-batch-gallery-card [data-testid="stImage"] img{width:100%;height:210px;object-fit:contain!important;object-position:center;background:transparent;border:0!important;border-radius:9px;box-shadow:none!important}
.st-key-batch-gallery-card .atlas-card-title{min-height:54px;margin-top:12px}
.st-key-batch-gallery-card [data-testid="stCaptionContainer"]{min-height:34px}
div[data-testid="stButton"]>button{border-radius:11px;font-weight:700;min-height:39px}
@media(max-width:700px){.atlas-card-title{font-size:21px}.atlas-lede{font-size:14px}.atlas-photo-frame img,.atlas-photo-placeholder{height:150px}}

/* Consistent destination-card geometry and readable, high-contrast copy */
[class*="st-key-atlas-destination-card-"]{height:100%}
[class*="st-key-atlas-destination-card-"] [data-testid="stVerticalBlockBorderWrapper"]{box-sizing:border-box;height:700px;min-height:700px;max-height:700px;display:flex;overflow:hidden}
[class*="st-key-atlas-destination-card-"] [data-testid="stVerticalBlock"]{box-sizing:border-box;height:100%;min-height:0;flex:1;display:flex;flex-direction:column;gap:.45rem}
[class*="st-key-atlas-destination-card-"] [data-testid="stImage"]{height:218px;min-height:218px;max-height:218px;display:flex;align-items:center;justify-content:center;overflow:hidden;border-radius:12px;background:linear-gradient(135deg,#E8E0CF,#DCEAE2 55%,#D8E8ED);padding:6px}
[class*="st-key-atlas-destination-card-"] [data-testid="stImage"] img{width:100%;height:206px;max-height:206px;object-fit:contain!important;object-position:center;background:transparent;border:0!important;box-shadow:none!important}
[class*="st-key-atlas-destination-card-"] .atlas-card-meta{height:28px;min-height:28px}
[class*="st-key-atlas-destination-card-"] .atlas-card-title{height:52px;min-height:52px}
[class*="st-key-atlas-destination-card-"] .atlas-card-copy{height:78px;min-height:78px}
[class*="st-key-atlas-destination-card-"] .atlas-tag{line-height:1.25}\n[class*="st-key-atlas-destination-card-"] [data-testid="stExpander"]{margin-top:auto;flex-shrink:0}\n[class*="st-key-atlas-destination-card-"] .stCaption{min-height:34px;max-height:34px;overflow:hidden}
[class*="st-key-atlas-reference-card-"] [data-testid="stVerticalBlockBorderWrapper"]{height:100%;min-height:450px;display:flex}
[class*="st-key-atlas-reference-card-"] [data-testid="stImage"]{height:218px;min-height:218px;display:flex;align-items:center;justify-content:center;background:#E4EAE4;border-radius:12px;padding:6px}
[class*="st-key-atlas-reference-card-"] [data-testid="stImage"] img{width:100%;height:206px;object-fit:contain!important;background:transparent;border:0!important;box-shadow:none!important}
[class*="st-key-atlas-reference-card-"] .atlas-card-title{height:54px;min-height:54px}
[class*="st-key-batch-gallery-card-"]{height:100%;min-height:365px;padding:13px!important;border:1px solid rgba(23,92,67,.22)!important;border-radius:18px!important;background:linear-gradient(145deg,#F3E8D0 0%,#E5F0E8 52%,#DCEAF0 100%)!important;box-shadow:0 12px 30px rgba(13,55,42,.09)!important}
[class*="st-key-batch-gallery-card-"] [data-testid="stImage"]{height:224px;min-height:224px;display:flex;align-items:center;justify-content:center;overflow:hidden;border-radius:13px;background:linear-gradient(135deg,#D7C59F,#C8E0D5 55%,#B8D6DF);padding:7px}
[class*="st-key-batch-gallery-card-"] [data-testid="stImage"] img{width:100%;height:210px;object-fit:contain!important;object-position:center;background:transparent;border:0!important;border-radius:9px;box-shadow:none!important}
[class*="st-key-batch-gallery-card-"] .atlas-card-title{height:54px;min-height:54px;margin-top:12px}
[class*="st-key-batch-gallery-card-"] [data-testid="stCaptionContainer"]{height:34px;min-height:34px;overflow:hidden;color:#26352C!important;opacity:1!important}
@media(max-width:700px){[class*="st-key-atlas-destination-card-"] [data-testid="stVerticalBlockBorderWrapper"]{height:auto;min-height:0;max-height:none}[class*="st-key-atlas-destination-card-"] .atlas-card-copy{height:auto;min-height:70px;max-height:90px}}



/* Atlas card alignment: consistent image boxes and left-aligned text rhythm */
.atlas-credit{display:none!important}
[class*="st-key-atlas-destination-card-"] [data-testid="stImage"]{
    box-sizing:border-box!important;width:100%!important;height:218px!important;
    min-height:218px!important;max-height:218px!important;padding:6px!important;
    display:flex!important;align-items:center!important;justify-content:center!important;
    overflow:hidden!important;border-radius:12px!important;
}
[class*="st-key-atlas-destination-card-"] [data-testid="stImage"] img{
    display:block!important;width:100%!important;height:206px!important;
    min-height:206px!important;max-height:206px!important;object-fit:contain!important;
    object-position:center!important;margin:0 auto!important;
}
[class*="st-key-atlas-destination-card-"] .atlas-card-meta,
[class*="st-key-atlas-destination-card-"] .atlas-card-title,
[class*="st-key-atlas-destination-card-"] .atlas-card-copy{
    box-sizing:border-box!important;width:100%!important;text-align:left!important;
    margin-left:0!important;margin-right:0!important;padding-left:0!important;
    padding-right:0!important;align-self:stretch!important;
}
[class*="st-key-atlas-destination-card-"] .atlas-card-title{
    height:52px!important;min-height:52px!important;max-height:52px!important;
    display:-webkit-box!important;-webkit-line-clamp:2!important;
    -webkit-box-orient:vertical!important;overflow:hidden!important;
}
[class*="st-key-atlas-destination-card-"] .atlas-card-copy{
    height:78px!important;min-height:78px!important;max-height:78px!important;
    display:-webkit-box!important;-webkit-line-clamp:4!important;
    -webkit-box-orient:vertical!important;overflow:hidden!important;
}

/* Lower atlas sections: compact, three-column cards with one shared image rhythm.
   Destination landscapes and clusters above remain deliberately untouched. */
[class*="st-key-atlas-event-card-"] [data-testid="stVerticalBlockBorderWrapper"],
[class*="st-key-atlas-reference-card-"] [data-testid="stVerticalBlockBorderWrapper"],
[class*="st-key-batch-gallery-card-"]{
    box-sizing:border-box!important;height:470px!important;min-height:470px!important;
    max-height:470px!important;display:flex!important;overflow:hidden!important;
    padding:12px!important;border:1px solid var(--voyage-line)!important;
    border-radius:16px!important;background:var(--voyage-surface)!important;
    box-shadow:0 7px 18px rgba(8,25,20,.055)!important;
}
[class*="st-key-atlas-event-card-"] [data-testid="stVerticalBlock"],
[class*="st-key-atlas-reference-card-"] [data-testid="stVerticalBlock"],
[class*="st-key-batch-gallery-card-"] [data-testid="stVerticalBlock"]{
    box-sizing:border-box!important;height:100%!important;min-height:0!important;
    flex:1!important;display:flex!important;flex-direction:column!important;gap:.38rem!important;
}
[class*="st-key-atlas-event-card-"] [data-testid="stImage"],
[class*="st-key-atlas-reference-card-"] [data-testid="stImage"],
[class*="st-key-batch-gallery-card-"] [data-testid="stImage"]{
    box-sizing:border-box!important;width:100%!important;height:184px!important;
    min-height:184px!important;max-height:184px!important;padding:5px!important;
    display:flex!important;align-items:center!important;justify-content:center!important;
    overflow:hidden!important;border-radius:12px!important;
    background:linear-gradient(135deg,#E8E0CF,#DCEAE2 55%,#D8E8ED)!important;
    border:1px solid rgba(199,163,91,.35)!important;
}
[class*="st-key-atlas-event-card-"] [data-testid="stImage"] img,
[class*="st-key-atlas-reference-card-"] [data-testid="stImage"] img,
[class*="st-key-batch-gallery-card-"] [data-testid="stImage"] img{
    display:block!important;width:100%!important;height:172px!important;
    min-height:172px!important;max-height:172px!important;object-fit:contain!important;
    object-position:center!important;margin:0 auto!important;border:0!important;
    border-radius:9px!important;box-shadow:none!important;background:transparent!important;
}
[class*="st-key-atlas-event-card-"] .atlas-card-meta,
[class*="st-key-atlas-reference-card-"] .atlas-card-meta{
    box-sizing:border-box!important;height:34px!important;min-height:34px!important;
    max-height:34px!important;overflow:hidden!important;text-align:left!important;
}
[class*="st-key-atlas-event-card-"] .atlas-card-title,
[class*="st-key-atlas-reference-card-"] .atlas-card-title,
[class*="st-key-batch-gallery-card-"] .atlas-card-title{
    box-sizing:border-box!important;height:54px!important;min-height:54px!important;
    max-height:54px!important;overflow:hidden!important;text-align:left!important;
    margin:4px 0!important;
}
[class*="st-key-atlas-event-card-"] .atlas-card-copy{
    box-sizing:border-box!important;height:88px!important;min-height:88px!important;
    max-height:88px!important;overflow:hidden!important;text-align:left!important;
    display:-webkit-box!important;-webkit-line-clamp:4!important;-webkit-box-orient:vertical!important;
}
[class*="st-key-atlas-event-card-"] [data-testid="stExpander"]{margin-top:auto!important;flex-shrink:0!important}
[class*="st-key-atlas-reference-card-"] [data-testid="stCaptionContainer"],
[class*="st-key-batch-gallery-card-"] [data-testid="stCaptionContainer"]{
    height:34px!important;min-height:34px!important;max-height:34px!important;
    overflow:hidden!important;text-align:left!important;
}
[class*="st-key-atlas-reference-card-"] [data-testid="stLinkButton"],
[class*="st-key-batch-gallery-card-"] [data-testid="stLinkButton"]{margin-top:auto!important}
[class*="st-key-atlas-next-card-"] [data-testid="stVerticalBlockBorderWrapper"]{
    box-sizing:border-box!important;min-height:112px!important;height:112px!important;
    padding:12px!important;border:1px solid var(--voyage-line)!important;
    border-radius:14px!important;background:var(--voyage-surface)!important;
}
[class*="st-key-atlas-next-card-"] .atlas-card-title{
    height:auto!important;min-height:0!important;max-height:60px!important;
    margin:0!important;font-size:19px!important;
}
@media(max-width:900px){
    [class*="st-key-atlas-event-card-"] [data-testid="stVerticalBlockBorderWrapper"],
    [class*="st-key-atlas-reference-card-"] [data-testid="stVerticalBlockBorderWrapper"],
    [class*="st-key-batch-gallery-card-"]{height:450px!important;min-height:450px!important;max-height:450px!important}
}
@media(max-width:700px){
    [class*="st-key-atlas-event-card-"] [data-testid="stVerticalBlockBorderWrapper"],
    [class*="st-key-atlas-reference-card-"] [data-testid="stVerticalBlockBorderWrapper"],
    [class*="st-key-batch-gallery-card-"]{height:auto!important;min-height:0!important;max-height:none!important}
    [class*="st-key-atlas-event-card-"] .atlas-card-copy{height:auto!important;min-height:76px!important;max-height:120px!important}
}


/* Gallery cards keep the same footprint even when a batch has only two images.
   Images are fully visible rather than cropped; titles, captions and links align. */
[class*="st-key-batch-gallery-card-"]{
    width:100%!important;min-width:0!important;
}
[class*="st-key-batch-gallery-card-"] [data-testid="stImage"] img{
    object-fit:contain!important;object-position:center!important;
}
[class*="st-key-batch-gallery-card-"] .atlas-card-title{
    display:-webkit-box!important;-webkit-line-clamp:2!important;-webkit-box-orient:vertical!important;
    white-space:normal!important;overflow:hidden!important;
}
[class*="st-key-batch-gallery-card-"] [data-testid="stCaptionContainer"]{
    display:block!important;line-height:1.4!important;
}
/* Cluster-only spacing: keep experience/category chips clear of the card edge. */
[class*="st-key-atlas-destination-card-0-"] .atlas-tag-row{
    box-sizing:border-box!important;
    height:64px!important;min-height:64px!important;max-height:64px!important;
    display:flex!important;flex-wrap:wrap!important;align-content:flex-start!important;
    align-items:flex-start!important;gap:5px!important;
    margin:0 0 12px!important;padding:2px 0 10px!important;
    overflow:hidden!important;
}
[class*="st-key-atlas-destination-card-0-"] .atlas-tag{
    box-sizing:border-box!important;display:inline-flex!important;align-items:center!important;
    line-height:1.25!important;margin:0!important;padding:5px 8px!important;
}

/* Festival cards: fixed shared geometry, compact readable copy, no clipped summaries. */
[class*="st-key-atlas-event-card-"] [data-testid="stVerticalBlockBorderWrapper"]{
    box-sizing:border-box!important;height:510px!important;min-height:510px!important;max-height:510px!important;
    display:flex!important;overflow:hidden!important;padding:13px!important;
    border:1px solid var(--voyage-line)!important;border-radius:17px!important;
    background:var(--voyage-surface)!important;box-shadow:0 9px 24px rgba(8,25,20,.075)!important;
}
[class*="st-key-atlas-event-card-"] [data-testid="stVerticalBlock"]{
    box-sizing:border-box!important;height:100%!important;min-height:0!important;
    display:flex!important;flex-direction:column!important;gap:.38rem!important;flex:1!important;
}
[class*="st-key-atlas-event-card-"] [data-testid="stImage"]{
    box-sizing:border-box!important;width:100%!important;height:218px!important;
    min-height:218px!important;max-height:218px!important;padding:6px!important;
    display:flex!important;align-items:center!important;justify-content:center!important;overflow:hidden!important;
    border-radius:12px!important;background:linear-gradient(135deg,#E8E0CF,#DCEAE2 55%,#D8E8ED)!important;
    border:1px solid rgba(199,163,91,.48)!important;
}
[class*="st-key-atlas-event-card-"] [data-testid="stImage"] img{
    display:block!important;width:100%!important;height:206px!important;
    min-height:206px!important;max-height:206px!important;object-fit:contain!important;
    object-position:center!important;margin:0 auto!important;border:0!important;
    border-radius:9px!important;box-shadow:none!important;background:transparent!important;
}
[class*="st-key-atlas-event-card-"] .atlas-card-meta{
    box-sizing:border-box!important;height:34px!important;min-height:34px!important;max-height:34px!important;
    overflow:hidden!important;text-align:left!important;color:#59695F!important;opacity:1!important;
    font-size:9px!important;font-weight:800!important;letter-spacing:.8px!important;line-height:1.25!important;
    display:-webkit-box!important;-webkit-line-clamp:2!important;-webkit-box-orient:vertical!important;
}
[class*="st-key-atlas-event-card-"] .atlas-card-title{
    box-sizing:border-box!important;height:54px!important;min-height:54px!important;max-height:54px!important;
    overflow:hidden!important;text-align:left!important;margin:2px 0!important;color:#17251D!important;opacity:1!important;
    font-family:'Cormorant Garamond',Georgia,serif!important;font-size:22px!important;font-weight:700!important;line-height:1.1!important;
    display:-webkit-box!important;-webkit-line-clamp:2!important;-webkit-box-orient:vertical!important;
}
[class*="st-key-atlas-event-card-"] .atlas-card-copy{
    box-sizing:border-box!important;height:82px!important;min-height:82px!important;max-height:82px!important;
    overflow:hidden!important;text-align:left!important;color:#34463B!important;opacity:1!important;
    font-size:12.5px!important;font-weight:500!important;line-height:1.42!important;letter-spacing:.02px!important;
    display:-webkit-box!important;-webkit-line-clamp:4!important;-webkit-box-orient:vertical!important;
}
[class*="st-key-atlas-event-card-"] [data-testid="stExpander"]{
    margin-top:auto!important;flex-shrink:0!important;
}
/* Do not override expander typography here; native Streamlit text remains legible. */
.stApp [class*="st-key-atlas-event-card-"] .atlas-record-note{
    color:var(--voyage-body-ink)!important;opacity:1!important;
    background:var(--voyage-surface)!important;font-size:12px!important;line-height:1.55!important;
}
@media(max-width:700px){
    [class*="st-key-atlas-event-card-"] [data-testid="stVerticalBlockBorderWrapper"]{
        height:auto!important;min-height:0!important;max-height:none!important;
    }
    [class*="st-key-atlas-event-card-"] .atlas-card-meta,
    [class*="st-key-atlas-event-card-"] .atlas-card-title,
    [class*="st-key-atlas-event-card-"] .atlas-card-copy{
        height:auto!important;min-height:0!important;max-height:none!important;
        display:block!important;overflow:visible!important;
    }
}

/* Final festival-detail overrides: keep the green/cream/gold palette consistent. */
.atlas-record-note{margin-bottom:18px!important;padding:13px 14px!important;border:1px solid #285D45!important;border-left:4px solid #A9C5B0!important;border-radius:9px!important;background:#174B35!important;color:#FFFFFF!important;font-family:inherit!important;font-size:12px!important;line-height:1.65!important;font-weight:450!important}
.atlas-record-note *{color:#FFFFFF!important}
.atlas-record-location{display:block!important;position:relative!important;clear:both!important;box-sizing:border-box!important;width:100%!important;margin-top:18px!important;padding:11px 13px!important;border:1px solid #B8CFBD!important;border-radius:8px!important;background:#EAF2EB!important;color:#174B35!important;font-size:12px!important;line-height:1.55!important;font-weight:800!important}
.atlas-record-location strong{color:#174B35!important}
.atlas-event-meta{display:block!important;width:100%!important;height:34px!important;min-height:34px!important;max-height:34px!important;margin:10px 0 8px!important;overflow:hidden!important}
.atlas-event-date{display:flex!important;align-items:center!important;justify-content:center!important;box-sizing:border-box!important;width:100%!important;height:34px!important;min-height:34px!important;max-height:34px!important;padding:0 11px!important;border:1px solid #A9C5B0!important;border-radius:8px!important;background:#E8F1E9!important;color:#174B35!important;font-family:Inter,Arial,sans-serif!important;font-size:10px!important;line-height:1!important;font-weight:750!important;letter-spacing:.15px!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
/* White label only; leave font family, sizing and glyph rendering to Streamlit. */
.stApp [class*="st-key-atlas-event-card-"] [data-testid="stExpander"] details>summary p{
    color:#FFFFFF!important;
}

/* Destination gallery: match the compact visual rhythm of the destination clusters. */
[class*="st-key-batch-gallery-card-"]{
    box-sizing:border-box!important;width:100%!important;height:300px!important;
    min-height:300px!important;max-height:300px!important;padding:12px!important;
    display:flex!important;flex-direction:column!important;overflow:hidden!important;
    border:1px solid var(--voyage-line)!important;border-radius:17px!important;
    background:var(--voyage-surface)!important;box-shadow:0 8px 22px rgba(8,25,20,.065)!important;
}
[class*="st-key-batch-gallery-card-"] [data-testid="stVerticalBlock"]{
    box-sizing:border-box!important;height:100%!important;min-height:0!important;
    display:flex!important;flex-direction:column!important;flex:1!important;gap:.35rem!important;
}
[class*="st-key-batch-gallery-card-"] [data-testid="stImage"]{
    box-sizing:border-box!important;width:100%!important;height:184px!important;
    min-height:184px!important;max-height:184px!important;padding:5px!important;
    display:flex!important;align-items:center!important;justify-content:center!important;
    overflow:hidden!important;border-radius:12px!important;
    background:linear-gradient(135deg,#E8E0CF,#DCEAE2 55%,#D8E8ED)!important;
    border:1px solid rgba(199,163,91,.42)!important;
}
[class*="st-key-batch-gallery-card-"] [data-testid="stImage"] img{
    display:block!important;width:100%!important;height:172px!important;
    min-height:172px!important;max-height:172px!important;object-fit:contain!important;
    object-position:center!important;margin:0 auto!important;border:0!important;
    border-radius:9px!important;box-shadow:none!important;background:transparent!important;
}
[class*="st-key-batch-gallery-card-"] .atlas-card-title{
    box-sizing:border-box!important;width:100%!important;height:54px!important;
    min-height:54px!important;max-height:54px!important;overflow:hidden!important;
    display:-webkit-box!important;-webkit-line-clamp:2!important;-webkit-box-orient:vertical!important;
    text-align:left!important;margin:7px 0 0!important;color:#17251D!important;
    font-family:'Cormorant Garamond',Georgia,serif!important;font-size:22px!important;
    font-weight:700!important;line-height:1.12!important;
}
@media(max-width:700px){
    [class*="st-key-batch-gallery-card-"]{height:auto!important;min-height:0!important;max-height:none!important}
    [class*="st-key-batch-gallery-card-"] .atlas-card-title{height:auto!important;min-height:0!important;max-height:none!important;display:block!important}
}

/* Shared visitor-facing card geometry across every Regional Atlas collection. */
[class*="st-key-atlas-destination-card-"] [data-testid="stVerticalBlockBorderWrapper"],
[class*="st-key-atlas-event-card-"] [data-testid="stVerticalBlockBorderWrapper"],
[class*="st-key-atlas-reference-card-"] [data-testid="stVerticalBlockBorderWrapper"],
[class*="st-key-batch-gallery-card-"] [data-testid="stVerticalBlockBorderWrapper"]{
 height:100%!important;min-height:0!important;padding:12px!important;
 border:1px solid #D8D4C6!important;border-radius:17px!important;
 background:#FFFFFF!important;box-shadow:0 10px 26px rgba(10,25,15,.075)!important;
}
[class*="st-key-atlas-destination-card-"] [data-testid="stImage"],
[class*="st-key-atlas-event-card-"] [data-testid="stImage"],
[class*="st-key-atlas-reference-card-"] [data-testid="stImage"]{
 height:210px!important;min-height:210px!important;max-height:210px!important;
 display:flex;align-items:center;justify-content:center;overflow:hidden;
 border-radius:12px!important;background:#E8E0CF!important;padding:6px!important;
}
[class*="st-key-atlas-destination-card-"] [data-testid="stImage"] img,
[class*="st-key-atlas-event-card-"] [data-testid="stImage"] img,
[class*="st-key-atlas-reference-card-"] [data-testid="stImage"] img{
 width:100%!important;height:198px!important;object-fit:cover!important;
 border:0!important;border-radius:9px!important;box-shadow:none!important;
}
[class*="st-key-atlas-destination-card-"] .atlas-card-title,
[class*="st-key-atlas-event-card-"] .atlas-card-title,
[class*="st-key-atlas-reference-card-"] .atlas-card-title{
 height:54px!important;min-height:54px!important;max-height:54px!important;
 margin:8px 0!important;color:#101A13!important;
}
[class*="st-key-atlas-destination-card-"] .atlas-card-copy,
[class*="st-key-atlas-event-card-"] .atlas-card-copy,
[class*="st-key-atlas-reference-card-"] .atlas-card-copy{
 height:78px!important;min-height:78px!important;max-height:78px!important;color:#17251B!important;
}
.atlas-category-shortcut{border:1px solid #D8D4C6;border-radius:10px;background:#F1F4EE;color:#174B35;padding:8px 10px}
@media(max-width:700px){
 [class*="st-key-atlas-destination-card-"] [data-testid="stImage"],
 [class*="st-key-atlas-event-card-"] [data-testid="stImage"],
 [class*="st-key-atlas-reference-card-"] [data-testid="stImage"]{height:180px!important;min-height:180px!important}
 [class*="st-key-atlas-destination-card-"] [data-testid="stImage"] img,
 [class*="st-key-atlas-event-card-"] [data-testid="stImage"] img,
 [class*="st-key-atlas-reference-card-"] [data-testid="stImage"] img{height:168px!important}
}
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
    .stApp .atlas-photo-frame{background:#080D09!important;border:1px solid #45C477!important}
    .stApp .st-key-batch-gallery-card{background:linear-gradient(145deg,#10251B 0%,#142D2D 52%,#182A3B 100%)!important;border-color:rgba(69,196,119,.45)!important;box-shadow:0 14px 34px rgba(0,0,0,.32)!important}
    .stApp .st-key-batch-gallery-card [data-testid="stImage"]{background:linear-gradient(135deg,#173D2D,#234A4C 58%,#273A4C)!important;border:1px solid rgba(69,196,119,.48)!important}
    .stApp .st-key-batch-gallery-card [data-testid="stImage"] img{background:transparent!important;border:0!important}
    .stApp [class*="st-key-batch-gallery-card-"]{height:300px!important;min-height:300px!important;max-height:300px!important;background:#080D09!important;border-color:#26372C!important;box-shadow:none!important}
    .stApp [class*="st-key-batch-gallery-card-"] [data-testid="stImage"]{height:184px!important;min-height:184px!important;max-height:184px!important;background:linear-gradient(135deg,#173D2D,#234A4C 58%,#273A4C)!important;border-color:rgba(69,196,119,.48)!important}
    .stApp [class*="st-key-batch-gallery-card-"] [data-testid="stImage"] img{height:172px!important;min-height:172px!important;max-height:172px!important}
    .stApp [class*="st-key-batch-gallery-card-"] .atlas-card-title{color:#E6EEE8!important}

    .stApp .atlas-photo-placeholder{background:#080D09!important;color:#FFFFFF!important;border:1px solid #45C477!important}
    .stApp .atlas-tag{border-color:#45C477!important;color:#BFE8CD!important}
    .stApp .atlas-record-note{border-left-color:#45C477!important}
    .stApp .atlas-eyebrow{color:#45C477!important}
    
/* Post-festival visual collections: consistent frames, readable labels and stable card rhythm. */
[class*="st-key-batch-gallery-card-"] ,
[class*="st-key-atlas-reference-card-"]{
    box-sizing:border-box!important;height:470px!important;min-height:470px!important;max-height:470px!important;
    display:flex!important;flex-direction:column!important;overflow:hidden!important;
    padding:13px!important;border:1px solid var(--voyage-line)!important;
    border-radius:17px!important;background:var(--voyage-surface)!important;
    box-shadow:0 8px 22px rgba(8,25,20,.065)!important;
}
[class*="st-key-batch-gallery-card-"] [data-testid="stVerticalBlock"],
[class*="st-key-atlas-reference-card-"] [data-testid="stVerticalBlock"]{
    box-sizing:border-box!important;height:100%!important;min-height:0!important;
    display:flex!important;flex-direction:column!important;flex:1!important;gap:.4rem!important;
}
[class*="st-key-batch-gallery-card-"] [data-testid="stImage"],
[class*="st-key-atlas-reference-card-"] [data-testid="stImage"]{
    box-sizing:border-box!important;width:100%!important;height:218px!important;
    min-height:218px!important;max-height:218px!important;padding:6px!important;
    display:flex!important;align-items:center!important;justify-content:center!important;
    overflow:hidden!important;border-radius:12px!important;
    background:linear-gradient(135deg,#E8E0CF,#DCEAE2 55%,#D8E8ED)!important;
    border:1px solid rgba(199,163,91,.42)!important;
}
[class*="st-key-batch-gallery-card-"] [data-testid="stImage"] img,
[class*="st-key-atlas-reference-card-"] [data-testid="stImage"] img{
    display:block!important;width:100%!important;height:206px!important;
    min-height:206px!important;max-height:206px!important;object-fit:contain!important;
    object-position:center!important;margin:0 auto!important;border:0!important;
    border-radius:9px!important;box-shadow:none!important;background:transparent!important;
}
[class*="st-key-batch-gallery-card-"] .atlas-card-title,
[class*="st-key-atlas-reference-card-"] .atlas-card-title{
    box-sizing:border-box!important;width:100%!important;height:56px!important;
    min-height:56px!important;max-height:56px!important;overflow:hidden!important;
    display:-webkit-box!important;-webkit-line-clamp:2!important;-webkit-box-orient:vertical!important;
    text-align:left!important;margin:3px 0!important;color:#17251D!important;
    font-size:21px!important;font-weight:700!important;line-height:1.16!important;
}
[class*="st-key-batch-gallery-card-"] [data-testid="stCaptionContainer"],
[class*="st-key-atlas-reference-card-"] [data-testid="stCaptionContainer"]{
    box-sizing:border-box!important;height:38px!important;min-height:38px!important;
    max-height:38px!important;overflow:hidden!important;text-align:left!important;
    color:#34463B!important;opacity:1!important;font-size:11px!important;line-height:1.35!important;
}
[class*="st-key-atlas-reference-card-"] [data-testid="stLinkButton"],
[class*="st-key-batch-gallery-card-"] [data-testid="stLinkButton"]{
    margin-top:auto!important;flex-shrink:0!important;
}
[class*="st-key-atlas-next-card-"] [data-testid="stVerticalBlockBorderWrapper"]{
    box-sizing:border-box!important;height:132px!important;min-height:132px!important;max-height:132px!important;
    display:flex!important;overflow:hidden!important;padding:13px!important;
    border:1px solid var(--voyage-line)!important;border-radius:15px!important;
    background:var(--voyage-surface)!important;
}
[class*="st-key-atlas-next-card-"] [data-testid="stVerticalBlock"]{
    box-sizing:border-box!important;min-height:0!important;height:100%!important;
    display:flex!important;flex-direction:column!important;justify-content:center!important;gap:.25rem!important;
}
[class*="st-key-atlas-next-card-"] .atlas-card-title{
    box-sizing:border-box!important;height:58px!important;min-height:0!important;max-height:58px!important;
    display:-webkit-box!important;-webkit-line-clamp:2!important;-webkit-box-orient:vertical!important;
    overflow:hidden!important;margin:0!important;color:#17251D!important;
    font-size:19px!important;font-weight:700!important;line-height:1.18!important;
}
[class*="st-key-atlas-next-card-"] [data-testid="stCaptionContainer"]{
    height:28px!important;min-height:28px!important;max-height:28px!important;
    overflow:hidden!important;color:#59695F!important;opacity:1!important;
}
@media(max-width:700px){
    [class*="st-key-batch-gallery-card-"],
    [class*="st-key-atlas-reference-card-"]{
        height:auto!important;min-height:0!important;max-height:none!important;
    }
    [class*="st-key-batch-gallery-card-"] .atlas-card-title,
    [class*="st-key-atlas-reference-card-"] .atlas-card-title{
        height:auto!important;min-height:0!important;max-height:none!important;
        display:block!important;overflow:visible!important;
    }
    [class*="st-key-batch-gallery-card-"] [data-testid="stCaptionContainer"],
    [class*="st-key-atlas-reference-card-"] [data-testid="stCaptionContainer"]{
        height:auto!important;min-height:0!important;max-height:none!important;
    }
}

</style>
    """, unsafe_allow_html=True)

# Exact, destination-matched photography. Broad regional photos are used only on
# their matching destination-cluster cards, never on unrelated landmark/event cards.
ATLAS_DESTINATION_IMAGES = {
    "Hunza Valley": {
        "thumb_url": "https://images.pexels.com/photos/9401114/pexels-photo-9401114.jpeg",
        "page_url": "https://images.pexels.com/photos/9401114/pexels-photo-9401114.jpeg",
        "artist": "Pexels",
        "license": "Pexels License",
    },
    "Skardu": {
        "thumb_url": "https://images.pexels.com/photos/19442073/pexels-photo-19442073.jpeg",
        "page_url": "https://images.pexels.com/photos/19442073/pexels-photo-19442073.jpeg",
        "artist": "Pexels",
        "license": "Pexels License",
    },
    "Naran–Kaghan Valley": {
        "thumb_url": "https://images.pexels.com/photos/10059879/pexels-photo-10059879.jpeg",
        "page_url": "https://images.pexels.com/photos/10059879/pexels-photo-10059879.jpeg",
        "artist": "Pexels",
        "license": "Pexels License",
    },
    "Lahore": {
        "thumb_url": "https://images.pexels.com/photos/13659051/pexels-photo-13659051.jpeg",
        "page_url": "https://images.pexels.com/photos/13659051/pexels-photo-13659051.jpeg",
        "artist": "Pexels",
        "license": "Pexels License",
    },
    "K2 & Concordia Expedition": {
        "thumb_url": "https://static.vecteezy.com/system/resources/thumbnails/058/177/333/small/mountaineers-ascending-k2-the-second-highest-mountain-on-earth-photo.jpg",
        "page_url": "https://static.vecteezy.com/system/resources/thumbnails/058/177/333/small/mountaineers-ascending-k2-the-second-highest-mountain-on-earth-photo.jpg",
        "artist": "User-supplied image URL (Vecteezy)",
        "license": "Source and reuse licence not independently verified",
    },
    "Swat Valley": {
        "thumb_url": "https://images.pexels.com/photos/37673127/pexels-photo-37673127.jpeg",
        "page_url": "https://images.pexels.com/photos/37673127/pexels-photo-37673127.jpeg",
        "artist": "Pexels",
        "license": "Pexels License",
    },
    "Chitral & Kalash Valleys": {
        "thumb_url": "https://kalashtours.com/__l5e/assets-v1/5b909362-cf4c-4fe9-a584-6828f0e2845d/dest-rumbur.webp",
        "page_url": "https://kalashtours.com/__l5e/assets-v1/5b909362-cf4c-4fe9-a584-6828f0e2845d/dest-rumbur.webp",
        "artist": "User-supplied image URL (Kalash Tours)",
        "license": "Source and reuse licence not independently verified",
    },
    "Neelum Valley": {
        "thumb_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Beautiful_Neelum_Valley_Kashmir_Pakistan.jpg?width=2000",
        "page_url": "https://commons.wikimedia.org/wiki/File:Beautiful_Neelum_Valley_Kashmir_Pakistan.jpg",
        "artist": "Azmat akbar",
        "license": "CC BY-SA 4.0",
    },
    "Taxila": {
        "thumb_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Dharmarajika%20stupa%2CTaxila.jpg?width=2000",
        "page_url": "https://commons.wikimedia.org/wiki/File:Dharmarajika_stupa,Taxila.jpg",
        "artist": "Sasha Isachenko",
        "license": "CC BY-SA 3.0",
    },
    "Karachi & Makli–Thatta": {
        "thumb_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Makli_Necropolis-11.jpg?width=2000",
        "page_url": "https://commons.wikimedia.org/wiki/File:Makli_Necropolis-11.jpg",
        "artist": "Muhammad Saqib Khan",
        "license": "CC BY-SA 3.0",
    },
    "Bahawalpur & Cholistan": {
        "thumb_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Derawar_Fort_Cholistan_Bahawalpur.jpg?width=2000",
        "page_url": "https://commons.wikimedia.org/wiki/File:Derawar_Fort_Cholistan_Bahawalpur.jpg",
        "artist": "Mhtoori",
        "license": "CC BY-SA 4.0",
    },
    "Hingol & Gwadar Coast": {
        "thumb_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Kund_Malir_Beach%2C_Hingol_National_Park%2C_Balochistan.jpg?width=2000",
        "page_url": "https://commons.wikimedia.org/wiki/File:Kund_Malir_Beach,_Hingol_National_Park,_Balochistan.jpg",
        "artist": "Furqanlw",
        "license": "CC BY-SA 4.0",
    },
    "Concordia and K2 Base Camp": {
        "thumb_url": "https://static.vecteezy.com/system/resources/thumbnails/058/177/333/small/mountaineers-ascending-k2-the-second-highest-mountain-on-earth-photo.jpg",
        "page_url": "https://static.vecteezy.com/system/resources/thumbnails/058/177/333/small/mountaineers-ascending-k2-the-second-highest-mountain-on-earth-photo.jpg",
        "artist": "User-supplied image URL (Vecteezy)",
        "license": "Source and reuse licence not independently verified",
    },
    "K2 from Concordia": {
        "thumb_url": "https://static.vecteezy.com/system/resources/thumbnails/058/177/333/small/mountaineers-ascending-k2-the-second-highest-mountain-on-earth-photo.jpg",
        "page_url": "https://static.vecteezy.com/system/resources/thumbnails/058/177/333/small/mountaineers-ascending-k2-the-second-highest-mountain-on-earth-photo.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Concordia (K2 Base Camp)": {
        "thumb_url": "https://static.vecteezy.com/system/resources/thumbnails/058/177/333/small/mountaineers-ascending-k2-the-second-highest-mountain-on-earth-photo.jpg",
        "page_url": "https://static.vecteezy.com/system/resources/thumbnails/058/177/333/small/mountaineers-ascending-k2-the-second-highest-mountain-on-earth-photo.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Katas Raj Temples": {
        "thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/16/Katas_Raj_temples_Pakistan.jpg/960px-Katas_Raj_temples_Pakistan.jpg",
        "page_url": "https://commons.wikimedia.org/wiki/File:Katas_Raj_temples_Pakistan.jpg",
        "artist": "Khadim Hussain",
        "license": "CC BY-SA 4.0",
    },
    "Katas Raj Temples & Salt Range": {
        "thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/16/Katas_Raj_temples_Pakistan.jpg/960px-Katas_Raj_temples_Pakistan.jpg",
        "page_url": "https://commons.wikimedia.org/wiki/File:Katas_Raj_temples_Pakistan.jpg",
        "artist": "Khadim Hussain",
        "license": "CC BY-SA 4.0",
    },
    "Lahore Fort (Shahi Qila)": {
        "thumb_url": "https://images.pexels.com/photos/13023314/pexels-photo-13023314.jpeg",
        "page_url": "https://images.pexels.com/photos/13023314/pexels-photo-13023314.jpeg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Tomb of Shah Rukn-e-Alam": {
        "thumb_url": "https://sacredsites.com/images/asia/pakistan/Multan-Shah-Rukn-e-Alam-01.webp",
        "page_url": "https://sacredsites.com/images/asia/pakistan/Multan-Shah-Rukn-e-Alam-01.webp",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Derawar Fort": {
        "thumb_url": "https://preview.redd.it/derawar-fort-in-the-cholistan-desert-bahawalpur-panjab-v0-213ndupt6k7e1.jpg?width=701&format=pjpg&auto=webp&s=3eac5df28f9c7f66929324f254f019179eff9e62",
        "page_url": "https://preview.redd.it/derawar-fort-in-the-cholistan-desert-bahawalpur-panjab-v0-213ndupt6k7e1.jpg?width=701&format=pjpg&auto=webp&s=3eac5df28f9c7f66929324f254f019179eff9e62",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Gurdwara Janam Asthan": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtXfew74_od9kDJLFiBbPG3d0qXVujcfdIy-cTzoiKGPnhlDIYUg4fLXI&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtXfew74_od9kDJLFiBbPG3d0qXVujcfdIy-cTzoiKGPnhlDIYUg4fLXI&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Soon Valley and Uchali Wetlands": {
        "thumb_url": "https://dialogue.earth/content/uploads/2021/01/Uc-8.jpg",
        "page_url": "https://dialogue.earth/content/uploads/2021/01/Uc-8.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Mohenjo-daro": {
        "thumb_url": "https://media.istockphoto.com/id/1485086382/photo/mohenjo-daro-main-city-indus-civilization.jpg?s=612x612&w=0&k=20&c=9iD3wruG-RsPlbi8Z_2n4XiF-WwwYmUpqkJ67PJF-Uw=",
        "page_url": "https://media.istockphoto.com/id/1485086382/photo/mohenjo-daro-main-city-indus-civilization.jpg?s=612x612&w=0&k=20&c=9iD3wruG-RsPlbi8Z_2n4XiF-WwwYmUpqkJ67PJF-Uw=",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Makli Necropolis": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQv2-4qjze3TFcyk5-tVlhnY39VSnlusTyH_ut-OB9o9A&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQv2-4qjze3TFcyk5-tVlhnY39VSnlusTyH_ut-OB9o9A&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Shrine of Lal Shahbaz Qalandar": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUWWsZ983bMFDAktwElCH7nyembgys-Yjn8X0f8vk4CA&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUWWsZ983bMFDAktwElCH7nyembgys-Yjn8X0f8vk4CA&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Karoonjhar Mountains and Jain Temples": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQV1fw-uzbpSsXbQfk_FVbKwnSyWmPROiIcC32YEHEfMS7hrcxci7EaaE&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQV1fw-uzbpSsXbQfk_FVbKwnSyWmPROiIcC32YEHEfMS7hrcxci7EaaE&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Gorakh Hill Station": {
        "thumb_url": "https://guidetourismpakistan.com/wp-content/uploads/2024/09/Gorakh-Hill-Header.png",
        "page_url": "https://guidetourismpakistan.com/wp-content/uploads/2024/09/Gorakh-Hill-Header.png",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Churna Island": {
        "thumb_url": "https://i.pinimg.com/736x/6b/33/0b/6b330ba3edc5491f0e33a80ad294e7da.jpg",
        "page_url": "https://i.pinimg.com/736x/6b/33/0b/6b330ba3edc5491f0e33a80ad294e7da.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Takht-i-Bahi and Sahr-i-Bahlol": {
        "thumb_url": "https://www.pakistanhc.lk/wp-content/uploads/2018/10/Takht-e-Bahi-960x640.jpg",
        "page_url": "https://www.pakistanhc.lk/wp-content/uploads/2018/10/Takht-e-Bahi-960x640.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Kalash Valleys: Bumburet, Rumbur and Birir": {
        "thumb_url": "https://kalashtours.com/__l5e/assets-v1/5b909362-cf4c-4fe9-a584-6828f0e2845d/dest-rumbur.webp",
        "page_url": "https://kalashtours.com/__l5e/assets-v1/5b909362-cf4c-4fe9-a584-6828f0e2845d/dest-rumbur.webp",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Kumrat Valley": {
        "thumb_url": "https://images.pexels.com/photos/15826125/pexels-photo-15826125.jpeg",
        "page_url": "https://images.pexels.com/photos/15826125/pexels-photo-15826125.jpeg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Mahodand Lake": {
        "thumb_url": "https://images.pexels.com/photos/4990600/pexels-photo-4990600.jpeg",
        "page_url": "https://images.pexels.com/photos/4990600/pexels-photo-4990600.jpeg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Shandur Pass and Polo Ground": {
        "thumb_url": "https://img.rezdy.com/PRODUCT_IMAGE/13699/Shandur_Polo_1_By_Shakir_Hussain_Yash___Own_work__CC_BY_SA_4.0__https___commons.wikimedia.org_w_index.php_curid_48504447.jpg",
        "page_url": "https://img.rezdy.com/PRODUCT_IMAGE/13699/Shandur_Polo_1_By_Shakir_Hussain_Yash___Own_work__CC_BY_SA_4.0__https___commons.wikimedia.org_w_index.php_curid_48504447.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Hingol National Park": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrKqVotrH6yUZVqvqk2EQG2n_89RBH8FXao3LiMT9VNXOpKkTzcrarCTWW&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrKqVotrH6yUZVqvqk2EQG2n_89RBH8FXao3LiMT9VNXOpKkTzcrarCTWW&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Astola Island": {
        "thumb_url": "https://i.pinimg.com/736x/40/bf/65/40bf65c7ce1e83ee3adcf120cede568d.jpg",
        "page_url": "https://i.pinimg.com/736x/40/bf/65/40bf65c7ce1e83ee3adcf120cede568d.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Ziarat Juniper Forest": {
        "thumb_url": "https://cdn-blog.zameen.com/blog/wp-content/uploads/2020/10/Your-Guide-to-Ziarat-Juniper-Forest-B-12-10-1024x640.jpg",
        "page_url": "https://cdn-blog.zameen.com/blog/wp-content/uploads/2020/10/Your-Guide-to-Ziarat-Juniper-Forest-B-12-10-1024x640.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Ziarat Residency": {
        "thumb_url": "https://tripplannerpk.com/_next/image?url=http%3A%2F%2Fapi.tripplannerpk.com%2Fimages%2Ftemp%2F47720.png&w=3840&q=75",
        "page_url": "https://tripplannerpk.com/_next/image?url=http%3A%2F%2Fapi.tripplannerpk.com%2Fimages%2Ftemp%2F47720.png&w=3840&q=75",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Moola Chotok": {
        "thumb_url": "https://i.aaj.tv/english/wp-content/uploads/2019/09/moola-chotok.jpg",
        "page_url": "https://i.aaj.tv/english/wp-content/uploads/2019/09/moola-chotok.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Concordia and K2 Base Camp": {
        "thumb_url": "https://static.vecteezy.com/system/resources/thumbnails/058/177/333/small/mountaineers-ascending-k2-the-second-highest-mountain-on-earth-photo.jpg",
        "page_url": "https://static.vecteezy.com/system/resources/thumbnails/058/177/333/small/mountaineers-ascending-k2-the-second-highest-mountain-on-earth-photo.jpg",
        "artist": "User-supplied image URL (Vecteezy)",
        "license": "Source and reuse licence not independently verified",
    },
    "Attabad Lake": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxBRSE94ks3zoq-17aZ_UkAU_xV6x8MZVf2aZdXA56lg&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxBRSE94ks3zoq-17aZ_UkAU_xV6x8MZVf2aZdXA56lg&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Khunjerab Pass": {
        "thumb_url": "https://ik.imagekit.io/traversepakistan/packages/northern-pakistan-grand-tour/cover.jpg?tr=w-3840,q-70,f-auto",
        "page_url": "https://ik.imagekit.io/traversepakistan/packages/northern-pakistan-grand-tour/cover.jpg?tr=w-3840,q-70,f-auto",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Deosai National Park": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS244N-i7BGH5ps3A3f9jKdQq-7meGz_nFROvG_ANg31uKeOEhXiMp8GZvx&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS244N-i7BGH5ps3A3f9jKdQq-7meGz_nFROvG_ANg31uKeOEhXiMp8GZvx&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Ratti Gali Lake": {
        "thumb_url": "https://dtvt.pk/wp-content/uploads/2023/01/Ratti-Gali-@KashifJaved.jpg",
        "page_url": "https://dtvt.pk/wp-content/uploads/2023/01/Ratti-Gali-@KashifJaved.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Arang Kel": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSraxWAWMVS1K_t7hODyc2caG97tt5THJ9rZ4u2QTuE4qaWIKsLXaIgxvE&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSraxWAWMVS1K_t7hODyc2caG97tt5THJ9rZ4u2QTuE4qaWIKsLXaIgxvE&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Pir Chinasi": {
        "thumb_url": "https://www.pakistanhc.lk/wp-content/uploads/2019/01/places-to-visit-in-Muzaffarabad-pir-chinasi-min-5-960x640.jpg",
        "page_url": "https://www.pakistanhc.lk/wp-content/uploads/2019/01/places-to-visit-in-Muzaffarabad-pir-chinasi-min-5-960x640.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Banjosa Lake": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8rN7oSrU65agFak34SU-KGl1RzxyRnisjcr-YIqiKnIfXTbc3j8ppfVq4&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8rN7oSrU65agFak34SU-KGl1RzxyRnisjcr-YIqiKnIfXTbc3j8ppfVq4&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Faisal Mosque": {
        "thumb_url": "https://www.pakistanhc.lk/wp-content/uploads/2018/10/0f58350048b1b544393b5651242e7eb5-shah-faisal-mosque-960x640.jpg",
        "page_url": "https://www.pakistanhc.lk/wp-content/uploads/2018/10/0f58350048b1b544393b5651242e7eb5-shah-faisal-mosque-960x640.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Pakistan Monument and Museum": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlH-L0Q8pG970bUCci3spF5S24vip9Rt4jTLEYPLBChQ&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlH-L0Q8pG970bUCci3spF5S24vip9Rt4jTLEYPLBChQ&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Margalla Hills National Park — Trail 5": {
        "thumb_url": "https://tourismguidebook.com/wp-content/uploads/2026/07/Margalla-Hills-National-Park.webp",
        "page_url": "https://tourismguidebook.com/wp-content/uploads/2026/07/Margalla-Hills-National-Park.webp",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Saidpur Village": {
        "thumb_url": "https://external-preview.redd.it/saidpur-village-5-minutes-away-from-the-heart-of-islamabad-v0-XF_L4gLEWF92hxiT_TuWpCgns_C0bv5OqWpqYmrnvug.jpg?auto=webp&s=32729fc475db5638a6812a3f0d7ffa3af4152802",
        "page_url": "https://external-preview.redd.it/saidpur-village-5-minutes-away-from-the-heart-of-islamabad-v0-XF_L4gLEWF92hxiT_TuWpCgns_C0bv5OqWpqYmrnvug.jpg?auto=webp&s=32729fc475db5638a6812a3f0d7ffa3af4152802",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },

}

# Match detailed records to the existing catalogue so imagery and cluster names stay consistent.
catalog_by_name = {name.casefold(): (name, item) for name, item in DESTINATIONS.items()}

# User-provided overrides for destination-cluster cards only.
# Kept separate from ATLAS_DESTINATION_IMAGES so detailed attraction cards remain unchanged.
ATLAS_CLUSTER_IMAGES = {
    "Hunza Valley": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJ24iX1ykpCxicbbLUFsWO4Od6HwDEkN3-ObCjriOBGxG5yYbK1THFcS_u&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJ24iX1ykpCxicbbLUFsWO4Od6HwDEkN3-ObCjriOBGxG5yYbK1THFcS_u&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Skardu": {
        "thumb_url": "https://www.imusafir.pk/blog/wp-content/uploads/2022/09/skardu-tour-pacages.jpg",
        "page_url": "https://www.imusafir.pk/blog/wp-content/uploads/2022/09/skardu-tour-pacages.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Chitral & Kalash Valleys": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRakc0-x3ZbxNe5JvOWjibAxvk3rgMijapz-yQaV5QsSA&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRakc0-x3ZbxNe5JvOWjibAxvk3rgMijapz-yQaV5QsSA&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Neelum Valley": {
        "thumb_url": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Neelum_Valley%2C_Azad_Jammu_%26_Kashmir%2C_Pakistan.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original",
        "page_url": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Neelum_Valley%2C_Azad_Jammu_%26_Kashmir%2C_Pakistan.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Lahore": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-TKQwaOdJWQuBg8_0IIRP74wZDZZD6jZDcncmzt6fRFwrUEv4zGKmvsKn&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-TKQwaOdJWQuBg8_0IIRP74wZDZZD6jZDcncmzt6fRFwrUEv4zGKmvsKn&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Taxila": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7GBZXR17OHVDiV3Qf2Jeq1VSxqafg1E_Xx1VlVVSQ1g&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7GBZXR17OHVDiV3Qf2Jeq1VSxqafg1E_Xx1VlVVSQ1g&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Karachi & Makli–Thatta": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQK6k2eWVHsRG-ob3NGAnY02iCJo1xyZicIftLO9pOLkH3rJ09gqxFt1DRO&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQK6k2eWVHsRG-ob3NGAnY02iCJo1xyZicIftLO9pOLkH3rJ09gqxFt1DRO&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Bahawalpur & Cholistan": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJDbZQeDs7kWlBjSgmTMBCZ5YiiHH5eSKq9o3laxPMwAPluXDZczgBMGkJ&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJDbZQeDs7kWlBjSgmTMBCZ5YiiHH5eSKq9o3laxPMwAPluXDZczgBMGkJ&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Hingol & Gwadar Coast": {
        "thumb_url": "https://i.dawn.com/primary/2019/02/5c7261319261b.jpg",
        "page_url": "https://i.dawn.com/primary/2019/02/5c7261319261b.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Islamabad & Margalla Hills": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNWTxmBeoqYjwE86aZj8u4nczm--1RWc53MR8Ue51gyC8HIguK-Q0DxQQ0&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNWTxmBeoqYjwE86aZj8u4nczm--1RWc53MR8Ue51gyC8HIguK-Q0DxQQ0&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Murree & Galiyat": {
        "thumb_url": "https://i0.wp.com/kumrattourism.com/wp-content/uploads/Shogran-Family-Private-Tour-Package-1-1.jpg?fit=800%2C530&ssl=1",
        "page_url": "https://i0.wp.com/kumrattourism.com/wp-content/uploads/Shogran-Family-Private-Tour-Package-1-1.jpg?fit=800%2C530&ssl=1",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Naran–Kaghan Valley": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbjQKATJ8T-V6ZRVdHAoliwoay8l2pTk8noBhN7CrcwPHftqgsa-YQ_HA&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbjQKATJ8T-V6ZRVdHAoliwoay8l2pTk8noBhN7CrcwPHftqgsa-YQ_HA&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Shogran & Siri Paye": {
        "thumb_url": "https://www.apricottours.pk/wp-content/uploads/photo-gallery/Shogran_Siri_Paye_Tour/Paye-Meadows-and-Makra-Peak.jpeg?bwg=1728646856",
        "page_url": "https://www.apricottours.pk/wp-content/uploads/photo-gallery/Shogran_Siri_Paye_Tour/Paye-Meadows-and-Makra-Peak.jpeg?bwg=1728646856",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Fairy Meadows & Raikot": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGpWcn_BZ-5c6Gn-3V1LfqotVc6b6im3l1-KIQOj0nHQ&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGpWcn_BZ-5c6Gn-3V1LfqotVc6b6im3l1-KIQOj0nHQ&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Astore & Rama Valley": {
        "thumb_url": "https://i.dawn.com/primary/2015/05/554b52d120a92.jpg?r=1342314181",
        "page_url": "https://i.dawn.com/primary/2015/05/554b52d120a92.jpg?r=1342314181",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Phander & Ghizer": {
        "thumb_url": "https://alpastravels.com/wp-content/uploads/2024/05/Ghizer-Phandar-Alpas-Travels-Pakistan-Slider.jpg.webp",
        "page_url": "https://alpastravels.com/wp-content/uploads/2024/05/Ghizer-Phandar-Alpas-Travels-Pakistan-Slider.jpg.webp",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Khunjerab & Upper Hunza": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRnBICfpOSMNurxJLjsAhVUCfUE20VgtpqICips82ZamYDGQk05T9ifqE8&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRnBICfpOSMNurxJLjsAhVUCfUE20VgtpqICips82ZamYDGQk05T9ifqE8&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Khaplu & Shyok Valley": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdt1LVAI5evwQMqscDiXe3UKMTQ9H45BEkVfdgiLRqyEcVVhMnHc1u9ng&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdt1LVAI5evwQMqscDiXe3UKMTQ9H45BEkVfdgiLRqyEcVVhMnHc1u9ng&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Ratti Gali & Dowarian": {
        "thumb_url": "https://beautyofpakistan.com/location/1000x500/Ratti-Gali-Lake-796x459-1494192289.jpeg.webp",
        "page_url": "https://beautyofpakistan.com/location/1000x500/Ratti-Gali-Lake-796x459-1494192289.jpeg.webp",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Rawalakot & Banjosa": {
        "thumb_url": "https://seepakistantours.com/wp-content/uploads/2022/04/Banjosa-Lake-480x300.jpg",
        "page_url": "https://seepakistantours.com/wp-content/uploads/2022/04/Banjosa-Lake-480x300.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Multan": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_ExNGc3MKxqDoUyT6ehf0VY2HdBbssDYeEf003UTIqePHJ63BxsCazfvE&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_ExNGc3MKxqDoUyT6ehf0VY2HdBbssDYeEf003UTIqePHJ63BxsCazfvE&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Faisalabad": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYgnHrvBt8OcnBZZ9CGS4ERh-lMo3hX7RyUvDpu0sawmXBmHQtq_3UTc1L&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYgnHrvBt8OcnBZZ9CGS4ERh-lMo3hX7RyUvDpu0sawmXBmHQtq_3UTc1L&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Peshawar": {
        "thumb_url": "https://discoveringpakistan.com/wp-content/uploads/2025/07/pexels-raqeebkhan-5838446-1-1024x663.jpg",
        "page_url": "https://discoveringpakistan.com/wp-content/uploads/2025/07/pexels-raqeebkhan-5838446-1-1024x663.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Mohenjo-daro": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTIYIWla2wE9w_xvq-_jUZ_dA1VCwIcdTv_DLK_olOHbArrJ3dOQQtJZtI&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTIYIWla2wE9w_xvq-_jUZ_dA1VCwIcdTv_DLK_olOHbArrJ3dOQQtJZtI&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Ranikot Fort": {
        "thumb_url": "https://cdn-blog.zameen.com/blog/wp-content/uploads/2020/02/Ranikot-Fort-in-Sindh-Cover-25-02.jpg",
        "page_url": "https://cdn-blog.zameen.com/blog/wp-content/uploads/2020/02/Ranikot-Fort-in-Sindh-Cover-25-02.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Keenjhar Lake & Thatta": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHiNmHd2E-tdJTONY6TnjcS3Siu7Ed-90PPEen7_58xMfXzw8ub4fef3ys&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHiNmHd2E-tdJTONY6TnjcS3Siu7Ed-90PPEen7_58xMfXzw8ub4fef3ys&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Khewra & Salt Range": {
        "thumb_url": "https://i.dawn.com/primary/2019/09/5d8b97a36920b.jpg",
        "page_url": "https://i.dawn.com/primary/2019/09/5d8b97a36920b.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Rohtas Fort & Jhelum": {
        "thumb_url": "https://webapi.tdcp.gop.pk/uploads/1776329744610-60043146.webp",
        "page_url": "https://webapi.tdcp.gop.pk/uploads/1776329744610-60043146.webp",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Ziarat & Quetta": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTd9sxXHuuCahW8_YEoneewiyByTS04ZdqsE-cnKcXvgzQPWTd7LUiTIY0f&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTd9sxXHuuCahW8_YEoneewiyByTS04ZdqsE-cnKcXvgzQPWTd7LUiTIY0f&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Ormara & Kund Malir": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgHS-oTvIgByZ8acEqVXKh074584AJEB0Jr7fCJvCfmX0xT29byVIF2n4&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgHS-oTvIgByZ8acEqVXKh074584AJEB0Jr7fCJvCfmX0xT29byVIF2n4&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Uch Sharif & Bahawalpur Heritage": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEfA97cdxRIVbpkIZh3P65unq0ORuQu0hnsPMGWWBxOQBzlYsohLN_gmTY&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEfA97cdxRIVbpkIZh3P65unq0ORuQu0hnsPMGWWBxOQBzlYsohLN_gmTY&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Malam Jabba": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTW_WEmSQaUaxl0W4ZNNmtJDm51P8HINyL7R7KAq6dfdwpuXd5Tn7QJcIqO&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTW_WEmSQaUaxl0W4ZNNmtJDm51P8HINyL7R7KAq6dfdwpuXd5Tn7QJcIqO&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Kalam & Ushu Forest": {
        "thumb_url": "https://www.imusafir.pk/blog/wp-content/uploads/2024/04/Ushu-Forest.jpg",
        "page_url": "https://www.imusafir.pk/blog/wp-content/uploads/2024/04/Ushu-Forest.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Gorakh Hill Station": {
        "thumb_url": "https://i.pinimg.com/736x/fc/5d/9e/fc5d9e2eb7b22a03aa113a2e51266fe3.jpg",
        "page_url": "https://i.pinimg.com/736x/fc/5d/9e/fc5d9e2eb7b22a03aa113a2e51266fe3.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Makran Coast & Pasni": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWaunfeJB0MuqspjwrJcFz-s-BkLTcjJFUd6bFc55Kl6Wr2mvgySdlyKT0&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWaunfeJB0MuqspjwrJcFz-s-BkLTcjJFUd6bFc55Kl6Wr2mvgySdlyKT0&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Sukkur & Rohri": {
        "thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b2/Lansdowne_Rohri%2C_Sukkur.jpg/3840px-Lansdowne_Rohri%2C_Sukkur.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=thumbnail",
        "page_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b2/Lansdowne_Rohri%2C_Sukkur.jpg/3840px-Lansdowne_Rohri%2C_Sukkur.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=thumbnail",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Kundian & Chashma Wetlands": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3tYDOuNBcUTofa6Sp4D_NR3O5a6hIxmit5fH3q79P8C9V7Ys4wTR5P4SI&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3tYDOuNBcUTofa6Sp4D_NR3O5a6hIxmit5fH3q79P8C9V7Ys4wTR5P4SI&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Nankana Sahib & Sikh Heritage": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRamxr0E5VzmKalA2bENKQ-s5wD9wSDiamgr_0v02JsvTeOEGLJq3pAghAp&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRamxr0E5VzmKalA2bENKQ-s5wD9wSDiamgr_0v02JsvTeOEGLJq3pAghAp&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Kartarpur Sahib & Narowal": {
        "thumb_url": "https://www.tribuneindia.com/sortd-service/imaginary/v22-01/jpg/large/high?url=dGhldHJpYnVuZS1zb3J0ZC1wcm8tcHJvZC1zb3J0ZC9tZWRpYTJkODY5NGMwLTc3NDgtMTFlZi1hZjA3LTliZDRjMmZlZGU4Yi5qcGc=",
        "page_url": "https://www.tribuneindia.com/sortd-service/imaginary/v22-01/jpg/large/high?url=dGhldHJpYnVuZS1zb3J0ZC1wcm8tcHJvZC1zb3J0ZC9tZWRpYTJkODY5NGMwLTc3NDgtMTFlZi1hZjA3LTliZDRjMmZlZGU4Yi5qcGc=",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Hasan Abdal & Panja Sahib": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRk8-m8vD0t8GPKbbhps4Uvxb4vbhepVcs8INFsQ3SAyHmu3ACAKVEypKM&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRk8-m8vD0t8GPKbbhps4Uvxb4vbhepVcs8INFsQ3SAyHmu3ACAKVEypKM&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Swat Buddhist Heritage Circuit": {
        "thumb_url": "https://www.imusafir.pk/blog/wp-content/uploads/2024/04/shingardar_stupa_swat.jpg",
        "page_url": "https://www.imusafir.pk/blog/wp-content/uploads/2024/04/shingardar_stupa_swat.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Takht-i-Bahi & Sahr-i-Bahlol": {
        "thumb_url": "https://fsn1.your-objectstorage.com/worldheritagesite/media/images/original_images53380119151_2689a28.2e16d0ba.fill-800x450.jpg",
        "page_url": "https://fsn1.your-objectstorage.com/worldheritagesite/media/images/original_images53380119151_2689a28.2e16d0ba.fill-800x450.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Katas Raj Temples & Salt Range": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSx3prrsmtVBt1jPQDrc6ro0TX3g5pKg0borZBFhF5QQg&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSx3prrsmtVBt1jPQDrc6ro0TX3g5pKg0borZBFhF5QQg&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Hinglaj Mata & Hingol": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQe9oo2cuc5SIFH3wZY-kyVlBAU3ecnQh7jMKVx4eMphDMsxyIoQMRke8Q9&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQe9oo2cuc5SIFH3wZY-kyVlBAU3ecnQh7jMKVx4eMphDMsxyIoQMRke8Q9&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Harappa & Indus Valley Archaeology": {
        "thumb_url": "https://sc0.blr1.digitaloceanspaces.com/large/891655-84125-grvbnkdkkb-1523855275.jpg",
        "page_url": "https://sc0.blr1.digitaloceanspaces.com/large/891655-84125-grvbnkdkkb-1523855275.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Desan Meadows & Upper Kalam": {
        "thumb_url": "https://i.pinimg.com/736x/3a/76/de/3a76de1dc6a370d6ee4814d108a92090.jpg",
        "page_url": "https://i.pinimg.com/736x/3a/76/de/3a76de1dc6a370d6ee4814d108a92090.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Utror & Gabral Valleys": {
        "thumb_url": "https://upload.wikimedia.org/wikipedia/commons/5/58/Utror_Valley%2C_Swat%2C_Khyber_Pakhtunkhwa.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original",
        "page_url": "https://upload.wikimedia.org/wikipedia/commons/5/58/Utror_Valley%2C_Swat%2C_Khyber_Pakhtunkhwa.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Matiltan & Mahodand Lake": {
        "thumb_url": "https://naturehikepakistan.pk/wp-content/uploads/2024/03/mahudand-lake-c-min.jpeg",
        "page_url": "https://naturehikepakistan.pk/wp-content/uploads/2024/03/mahudand-lake-c-min.jpeg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Andrab Lake & Anakar Valley": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3-RkiPzT99hV1XaoKYO6pgGCCryegpCdWqbPiZfSPXQ&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3-RkiPzT99hV1XaoKYO6pgGCCryegpCdWqbPiZfSPXQ&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Izmis Lake & Utror Meadows": {
        "thumb_url": "https://i.dawn.com/primary/2019/06/5d0bcd49be788.jpg",
        "page_url": "https://i.dawn.com/primary/2019/06/5d0bcd49be788.jpg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Spinkhor Lake & Upper Utror": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYWdd08GzoOmDuhz4E8RgpEZckTdcFUOv7Nro0MMlkWsbLHXMcBhPPlbkh&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYWdd08GzoOmDuhz4E8RgpEZckTdcFUOv7Nro0MMlkWsbLHXMcBhPPlbkh&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Gilgit City & Karakoram Gateway": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDPNY5483pQYwecWKeKInBlKNYCk90sua0kiI5WKYpUw&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDPNY5483pQYwecWKeKInBlKNYCk90sua0kiI5WKYpUw&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "K2 & Concordia Expedition": {
        "thumb_url": "https://trangoadventure.com/wp-content/uploads/2018/10/k2-at-night-time-scaled.jpeg",
        "page_url": "https://trangoadventure.com/wp-content/uploads/2018/10/k2-at-night-time-scaled.jpeg",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Abbottabad & Thandiani": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZXO1gc3rc8-At-IsrMQhnEDnAKQIJYl0tvnt2nVQZzWgIYORJ-MHTpTU&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZXO1gc3rc8-At-IsrMQhnEDnAKQIJYl0tvnt2nVQZzWgIYORJ-MHTpTU&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Mansehra & Kaghan Gateway": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPfQEvyaj1bj8YBSQHekrpRJB-RHcxoqQ33XIXB6NDJVHJlca5jPh-gzo&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPfQEvyaj1bj8YBSQHekrpRJB-RHcxoqQ33XIXB6NDJVHJlca5jPh-gzo&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Hyderabad & Bhit Shah": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSewDb4_sODWQ3HuuzoZ5aQIW0G6zFobMlaBIln2dig3r4VbtksmxPV4syP&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSewDb4_sODWQ3HuuzoZ5aQIW0G6zFobMlaBIln2dig3r4VbtksmxPV4syP&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Larkana & Mohenjo-daro Gateway": {
        "thumb_url": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2b/a5/dd/08/caption.jpg?w=500&h=400&s=1",
        "page_url": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2b/a5/dd/08/caption.jpg?w=500&h=400&s=1",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Sialkot": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6b-3JTKpSC7iWLt5K5exIgrDGHTEGLYZTSXZ9SQAwsDm90gvwgDAZDTKN&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6b-3JTKpSC7iWLt5K5exIgrDGHTEGLYZTSXZ9SQAwsDm90gvwgDAZDTKN&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Gujranwala": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScdXQZVvzdfJqnesbiIAsCdpBPECeGXdYgwujENZoY26FZax8lvfgC2Bpi&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScdXQZVvzdfJqnesbiIAsCdpBPECeGXdYgwujENZoY26FZax8lvfgC2Bpi&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Quetta & Hanna Lake": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSW6d9IFHAC84y1hbaI0rUwqu2jIMOa8c69MMjh9kRjqBPwqSq1KV0kLcJn&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSW6d9IFHAC84y1hbaI0rUwqu2jIMOa8c69MMjh9kRjqBPwqSq1KV0kLcJn&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
    "Kumrat Valley": {
        "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3nwIX5ngHm7u3-ol3EgxhYAH3bBR5pWYlmpq9P_efMQ&s=10",
        "page_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3nwIX5ngHm7u3-ol3EgxhYAH3bBR5pWYlmpq9P_efMQ&s=10",
        "artist": "User-supplied image URL",
        "license": "Source and reuse licence not independently verified",
    },
}

def _normalise_place_name(value: str) -> str:
    """Normalise equivalent place names so one supplied photo can be reused consistently."""
    return re.sub(r"[^a-z0-9]+", "", str(value).casefold())


_GALLERY_IMAGE_INDEX = {}
for _gallery_batch in DESTINATION_IMAGE_BATCHES.values():
    for _gallery_item in _gallery_batch:
        _gallery_name = _normalise_place_name(_gallery_item.get("destination", ""))
        _gallery_url = str(_gallery_item.get("image_url", "")).strip()
        if _gallery_name and _gallery_url:
            _GALLERY_IMAGE_INDEX.setdefault(_gallery_name, {
                "thumb_url": _gallery_url, "page_url": _gallery_url,
                "artist": "VoyagePK image collection",
                "license": "Image reuse terms not independently verified",
            })


def find_matching_destination_image(name: str):
    return (ATLAS_DESTINATION_IMAGES.get(name) or ATLAS_CLUSTER_IMAGES.get(name)
            or _GALLERY_IMAGE_INDEX.get(_normalise_place_name(name)))


def find_catalog_record(record):
    cluster = record.get("cluster", "")
    return catalog_by_name.get(cluster.casefold())

def show_photo(query: str, allow_lookup: bool = True, image_override: dict | None = None):
    # Explicit destination matches take priority; otherwise use the existing Commons lookup.
    image = image_override or (get_commons_image(query) if allow_lookup else None)
    if image and image.get("thumb_url"):
        rendered = get_display_image(image["thumb_url"], aspect_ratio=(16, 9), focal_point=(0.5, 0.5))
        st.image(rendered if rendered else image["thumb_url"], use_container_width=True)
    else:
        st.markdown('<div class="atlas-photo-frame"><div class="atlas-photo-placeholder">VOYAGEPK · PAKISTAN</div></div>', unsafe_allow_html=True)

def render_destination_card(record, index: int, detailed: bool = True):
    if detailed:
        catalog = find_catalog_record(record)
        image_query = catalog[1].get("image_query") if catalog else record.get("name", "Pakistan destination")
        # Only exact attraction names receive a destination-specific override.
        image_override = find_matching_destination_image(record.get("name", ""))
    else:
        image_query = record[1].get("image_query") or record[0]
        # Cluster cards use only an exact cluster-name match.
        image_override = find_matching_destination_image(record[0])
    with st.container(border=True, key=f"atlas-destination-card-{int(detailed)}-{index}"):
        show_photo(image_query or record.get("name", "Pakistan destination"), allow_lookup=index < 9, image_override=image_override)
        if detailed:
            st.markdown(f'<div class="atlas-card-meta">{record.get("region","")} · {record.get("type","")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="atlas-card-title">{record.get("name","")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="atlas-card-copy">{record.get("summary","")}</div>', unsafe_allow_html=True)
            tags = '<div class="atlas-tag-row">' + "".join(f'<span class="atlas-tag">{tag}</span>' for tag in record.get("categories", [])[:4]) + '</div>'
            st.markdown(tags, unsafe_allow_html=True)
        else:
            name = record[0]
            item = record[1]
            st.markdown(f'<div class="atlas-card-meta">{item.get("region","")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="atlas-card-title">{name}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="atlas-card-copy">{item.get("tagline", item.get("overview",""))}</div>', unsafe_allow_html=True)
            st.markdown('<div class="atlas-tag-row">' + "".join(f'<span class="atlas-tag">{tag}</span>' for tag in item.get("experiences", [])[:4]) + '</div>', unsafe_allow_html=True)

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
]
cols = st.columns(4)
for col, (value, label) in zip(cols, stats):
    with col:
        st.markdown(f'<div class="atlas-stat"><strong>{value}</strong><span>{label}</span></div>', unsafe_allow_html=True)

st.markdown("")
st.markdown('<div class="atlas-eyebrow">01 · START EXPLORING</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-heading">Find a place worth the journey.</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-subheading">Browse places by province and travel interest. Each listing uses a concise destination overview and a consistent photo card.</div>', unsafe_allow_html=True)

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
cluster_region = st.selectbox("Province / region", cluster_region_options, key="atlas_cluster_region")

experience_categories = sorted({tag for item in DESTINATIONS.values() for tag in item.get("experiences", [])})
category_options = ["All experiences"] + experience_categories
st.markdown('<div class="atlas-subheading">Choose the kind of place you want to visit.</div>', unsafe_allow_html=True)
for category_start in range(0, len(category_options), 4):
    category_cols = st.columns(4, gap="small")
    for category_col, category_name in zip(category_cols, category_options[category_start:category_start + 4]):
        with category_col:
            is_selected = st.session_state.get("atlas_experience_filter", "All experiences") == category_name
            if st.button(category_name, key="atlas_category_" + _normalise_place_name(category_name), use_container_width=True, type="primary" if is_selected else "secondary"):
                st.session_state["atlas_experience_filter"] = category_name
                st.rerun()
cluster_matches = []
for name, item in DESTINATIONS.items():
    item_region = item.get("region", "")
    searchable = (name + " " + item.get("tagline", "") + " " + item.get("overview", "")).casefold()
    if (cluster_region == "All regions" or cluster_region in item_region) and cluster_search.casefold() in searchable:
        cluster_matches.append((name, item))
selected_experience = st.session_state.get("atlas_experience_filter", "All experiences")
if selected_experience != "All experiences":
    cluster_matches = [(name, item) for name, item in cluster_matches if selected_experience in item.get("experiences", [])]
st.caption(f"{len(cluster_matches)} destination clusters.")
for start in range(0, len(cluster_matches), 3):
    row = st.columns(3, gap="medium")
    for offset, (col, record) in enumerate(zip(row, cluster_matches[start:start + 3])):
        with col:
            render_destination_card(record, start + offset, detailed=False)

st.divider()
st.markdown('<div class="atlas-eyebrow">03 · FESTIVALS & MAJOR EVENTS</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-heading">A calendar of culture, sport and shared traditions.</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-subheading">From Sufi gatherings and harvest celebrations to mountain polo, desert rallies and community festivals, these events offer a closer look at the places and people behind Pakistan’s travel stories.</div>', unsafe_allow_html=True)
def event_card_summary(event: dict, limit: int = 132) -> str:
    """Return a complete, compact card summary; preserve the full note in the expander."""
    raw = str(event.get("card_note") or event.get("note") or "").strip()
    compact = " ".join(raw.split())
    if len(compact) <= limit:
        return compact
    shortened = compact[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return shortened + "…"


def event_card_date(event: dict) -> str:
    """Return a concise one-line date label; full date context remains in the event details."""
    raw = " ".join(str(event.get("date") or "").split())
    compact = raw
    replacements = (
        (" (Hijri calendar; Gregorian dates shift annually)", " · Hijri dates vary"),
        (" (Hijri calendar; moon-sighting dependent)", " · Moon sighting"),
        ("; exact dates announced by Lok Virsa each year", " · Dates vary yearly"),
        ("; exact dates announced locally", " · Dates vary yearly"),
        ("; dates follow the Punjabi calendar", " · Punjabi calendar"),
        ("; pilgrimage schedules announced annually", " · Pilgrimage dates vary"),
        ("; dates follow the Hindu calendar and organiser schedule", " · Hindu calendar"),
        ("; dates follow the Kalash community calendar", " · Kalash calendar"),
        ("; exact timing follows the community calendar", " · Community calendar"),
        ("; programme dates vary by edition", " · Dates vary by edition"),
        ("; dates vary", " · Dates vary"),
        ("; 2026 expected 6 December", " · 2026: 6 Dec (expected)"),
        (" (TDCP listing); future dates announced by organiser", " · TDCP listing"),
        (" (TDCP listing)", " · TDCP listing"),
        ("; 2026 observance reported 6–8 February", " · 2026: 6–8 Feb"),
        ("; 2026 dates were 29–31 July", " · 2026: 29–31 Jul"),
        ("; Basant 2026 was held 6–8 February", " · 2026: 6–8 Feb"),
    )
    for old, new in replacements:
        compact = compact.replace(old, new)
    compact = compact.replace("Usually ", "").replace("each year", "yearly")
    compact = compact.replace("Annual fair; ", "")
    compact = compact.replace("Edition dates vary; 2025 dates supplied were ", "Dates vary · 2025: ")
    if len(compact) > 46:
        compact = compact[:45].rsplit(" ", 1)[0].rstrip(" ,;:-") + "…"
    return compact


event_query = st.text_input("Search festivals and events", placeholder="Try Urs, Polo, Lok Mela, Vaisakhi...")
event_regions = ["All regions"] + sorted({event.get("region", "") for event in EVENT_RECORDS})
event_region = st.selectbox("Event region", event_regions, key="atlas_event_region")
event_matches = [
    event for event in EVENT_RECORDS
    if (event_region == "All regions" or event.get("region") == event_region)
    and event_query.casefold() in (str(event.get("name","")) + " " + str(event.get("location","")) + " " + str(event.get("note",""))).casefold()
]

# Editorial prominence order: nationwide observances first, followed by widely
# recognised cultural, religious and major tourism events, then local/specialist events.
# This is a curated display order, not a claim of measured attendance figures.
EVENT_DISPLAY_ORDER = [
    "Eid-ul-Fitr",
    "Eid-ul-Adha",
    "Eid Milad-un-Nabi",
    "Independence Day (Jashn-e-Azadi)",
    "Shandur Polo Festival",
    "Cholistan Desert Jeep Rally",
    "Jashn-e-Baharan & Basant",
    "Urs of Data Ganj Bakhsh",
    "Urs of Lal Shahbaz Qalandar",
    "Lok Virsa Folk Festival (Lok Mela)",
    "Sindhi Cultural Day (Ekta Day)",
    "Mela Chiraghan",
    "Sibi Mela",
    "Vaisakhi Mela and Sikh Pilgrimage",
    "Hinglaj Mata Yatra",
    "Chilam Joshi Festival",
    "Choimus (Chaumos) Festival",
    "Urs of Shah Abdul Latif Bhittai",
    "National Horse & Cattle Show",
    "Waris Shah Mela",
    "Thal Desert Rally & Cultural Festival",
    "Kalam Summer Festival",
    "Malam Jabba Winter Sports Festival",
    "Ginani Harvest Festival",
    "Uchal Festival",
    "Lohri",
    "Islamabad Marathon",
    "Punjab Paragliding Championship",
    "Leepa Valley Mela",
    "Mangla Water Festival",
]
_event_rank = {name: rank for rank, name in enumerate(EVENT_DISPLAY_ORDER)}
event_matches.sort(key=lambda event: _event_rank.get(event.get("name", ""), len(EVENT_DISPLAY_ORDER)))
st.caption(f"{len(event_matches)} event records · ordered by national prominence, cultural significance and visitor recognition.")
for start in range(0, len(event_matches), 3):
    row = st.columns(3, gap="medium")
    for offset, (col, event) in enumerate(zip(row, event_matches[start:start + 3])):
        with col:
            with st.container(border=True, key=f"atlas-event-card-{event.get('id', start + offset)}"):
                event_name = event.get("name", "")
                show_photo(
                    event_name or "Pakistan festival",
                    allow_lookup=event_name in {
                        "Jashn-e-Baharan & Basant",
                        "Lohri",
                        "National Horse & Cattle Show",
                        "Urs of Data Ganj Bakhsh",
                        "Waris Shah Mela",
                        "Thal Desert Rally & Cultural Festival",
                        "Punjab Paragliding Championship",
                    },
                    image_override=ATLAS_EVENT_IMAGES.get(event_name),
                )
                st.markdown(f'<div class="atlas-card-title">{event.get("name","")}</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="atlas-event-meta"><span class="atlas-event-date">{event_card_date(event)}</span></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="atlas-card-copy">{event_card_summary(event)}</div>',
                    unsafe_allow_html=True,
                )
                with st.expander("Explore event"):
                    if event.get("date_status"):
                        st.caption(event.get("date_status",""))
                    if event.get("note"):
                        st.markdown(f'<div class="atlas-record-note">{event.get("note","")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="atlas-record-location"><strong>Location</strong> · {event.get("location","")}</div>', unsafe_allow_html=True)

st.divider()
st.markdown('<div class="atlas-eyebrow">04 · DESTINATION IMAGE GALLERY</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-heading">Pakistan, through the places themselves.</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-subheading">A visual journey through Pakistan’s landmarks, landscapes and heritage.</div>', unsafe_allow_html=True)
for batch_index, (batch_name, batch_images) in enumerate(DESTINATION_IMAGE_BATCHES.items()):
    st.markdown(f'<div class="atlas-card-meta">{batch_name}</div>', unsafe_allow_html=True)
    for start in range(0, len(batch_images), 3):
        image_row = batch_images[start:start + 3]
        if len(image_row) == 2:
            row = st.columns([1, 2, 2, 1], gap="medium")
            card_columns = row[1:3]
        elif len(image_row) == 1:
            row = st.columns([1, 2, 1], gap="medium")
            card_columns = [row[1]]
        else:
            row = st.columns(3, gap="medium")
            card_columns = row
        for offset, (col, image_record) in enumerate(zip(card_columns, image_row)):
            with col:
                with st.container(border=True, key=f"batch-gallery-card-{batch_index}-{start + offset}"):
                    image_url = str(image_record.get("image_url", "")).strip()
                    destination_name = str(image_record.get("destination", "Destination")).strip()
                    if image_url:
                        safe_url = html.escape(image_url, quote=True)
                        safe_name = html.escape(destination_name, quote=True)
                        st.markdown(
                            f'<div style="width:100%;height:218px;min-height:218px;max-height:218px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;overflow:hidden;border:1px solid rgba(199,163,91,.42);border-radius:12px;padding:6px;background:linear-gradient(135deg,#E8E0CF,#DCEAE2 55%,#D8E8ED)">'
                            f'<img src="{safe_url}" alt="{safe_name}" loading="lazy" style="display:block;width:100%;height:206px;max-height:206px;object-fit:contain;object-position:center;border:0;border-radius:9px;background:transparent">'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown('<div class="atlas-gallery-image-slot atlas-gallery-image-slot--unavailable"></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="atlas-card-title">{html.escape(destination_name)}</div>', unsafe_allow_html=True)

st.divider()
st.markdown('<div class="atlas-eyebrow">05 · MORE DESTINATION PHOTOGRAPHY</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-heading">More places to explore.</div>', unsafe_allow_html=True)
st.markdown('<div class="atlas-subheading">Explore additional destination photography from across Pakistan.</div>', unsafe_allow_html=True)
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
            with st.container(border=True, key=f"atlas-reference-card-{start + offset}"):
                if item.get("page"):
                    show_photo(
                        item["subject"],
                        image_override=ATLAS_DESTINATION_IMAGES.get(item.get("subject")) or {
                            "IMG-PB-001": ATLAS_DESTINATION_IMAGES.get("Lahore Fort (Shahi Qila)"),
                            "IMG-PB-002": ATLAS_DESTINATION_IMAGES.get("Derawar Fort"),
                            "IMG-PB-003": ATLAS_DESTINATION_IMAGES.get("Katas Raj Temples"),
                            "IMG-SD-002": ATLAS_DESTINATION_IMAGES.get("Makli Necropolis"),
                            "IMG-SD-003": ATLAS_DESTINATION_IMAGES.get("Shrine of Lal Shahbaz Qalandar"),
                        }.get(item.get("id")),
                    )
                else:
                    st.markdown('<div class="atlas-photo-frame"><div class="atlas-photo-placeholder">IMAGE SOURCE PENDING</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="atlas-card-meta">{item.get("region","")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="atlas-card-title">{item.get("subject","")}</div>', unsafe_allow_html=True)

st.divider()
st.markdown('<div class="atlas-eyebrow">06 · THE NEXT DISCOVERIES</div>', unsafe_allow_html=True)
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
                    with st.container(border=True, key=f"atlas-next-card-{lead_regions.index(region_name)}-{start + leads.index(lead)}"):
                        st.markdown(f'<div class="atlas-card-title">{lead}</div>', unsafe_allow_html=True)
                        st.caption("Discovery lead · " + region_name)

st.divider()
st.caption("Check local access, schedules, permits and image permissions before travel or reuse.")
