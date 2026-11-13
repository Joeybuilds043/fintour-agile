from __future__ import annotations

import streamlit as st

from src.catalog import DESTINATIONS
from src.destination_gallery import get_destination_gallery_image
from src.services.media import get_commons_image, get_display_image
from src.ui import apply_visitor_theme

st.set_page_config(page_title="Experience Collection | VoyagePK", page_icon=None, layout="wide")
apply_visitor_theme()

COLLECTIONS = {
    "northern_landscapes": {
        "title": "Northern landscapes",
        "intro": "Explore northern Pakistan through mountain systems, glaciers, river valleys, streams, alpine lakes, protected areas, high plateaus and cold deserts. Access is seasonal in many places.",
        "sections": [
            ("Mountains, peaks & glaciers", [
                ("K2 & Concordia", "Baltoro Glacier and the high Karakoram; a demanding expedition environment requiring licensed, experienced operators.", "Gilgit-Baltistan"),
                ("Nanga Parbat & Fairy Meadows", "High mountain scenery and the Raikot approach to the Nanga Parbat massif; trekking requires local guidance.", "Gilgit-Baltistan"),
                ("Rakaposhi & Minapin", "A prominent Karakoram peak above Nagar, with village and trekking viewpoints.", "Gilgit-Baltistan"),
                ("Passu & Batura region", "Passu Cones, the Hunza River corridor and views toward the Batura glacier system.", "Gilgit-Baltistan"),
            ]),
            ("Valleys, rivers & streams", [
                ("Hunza Valley", "Historic settlements, river landscapes, orchards and high mountain villages.", "Gilgit-Baltistan"),
                ("Neelum Valley", "Forest slopes, the Neelum River, waterfalls and mountain settlements.", "Azad Jammu & Kashmir"),
                ("Swat & Kalam", "The Swat River corridor, forested valleys and upper mountain landscapes.", "Khyber Pakhtunkhwa"),
                ("Naran–Kaghan", "Kunhar River, alpine side valleys and seasonal highland routes.", "Khyber Pakhtunkhwa"),
                ("Chitral & Kalash Valleys", "Hindu Kush landscapes and distinct living cultural traditions; visit with community respect.", "Khyber Pakhtunkhwa"),
            ]),
            ("Lakes, meadows & alpine water", [
                ("Attabad Lake", "A striking lake in upper Hunza formed after a major landslide; boating and road access depend on local conditions.", "Gilgit-Baltistan"),
                ("Saif-ul-Malook", "A high-altitude lake above Naran, reached by a route whose availability is seasonal.", "Khyber Pakhtunkhwa"),
                ("Mahodand Lake", "An alpine lake in upper Swat, commonly accessed from Kalam when routes permit.", "Khyber Pakhtunkhwa"),
                ("Rama Lake & Meadows", "Astore’s forest and alpine-meadow landscape beneath surrounding peaks.", "Gilgit-Baltistan"),
                ("Satpara & Kachura Lakes", "Lake landscapes around Skardu, including the well-known Kachura area.", "Gilgit-Baltistan"),
            ]),
            ("National parks, plateaus & protected landscapes", [
                ("Deosai National Park", "A high-altitude plateau ecosystem known for open grasslands, seasonal flowers and wildlife habitat.", "Gilgit-Baltistan"),
                ("Khunjerab National Park", "A high-altitude protected landscape around Khunjerab Pass and the Karakoram corridor.", "Gilgit-Baltistan"),
                ("Central Karakoram National Park", "A vast mountain protected area encompassing major glaciers and high peaks.", "Gilgit-Baltistan"),
                ("Ayubia National Park", "Forest ecosystems and walking trails in the Galiyat region.", "Khyber Pakhtunkhwa"),
                ("Hingol National Park", "A large protected landscape of coastal, desert and geological features.", "Balochistan"),
            ]),
            ("Cold deserts & winter landscapes", [
                ("Katpana Cold Desert", "A high-altitude sand-dune landscape near Skardu.", "Gilgit-Baltistan"),
                ("Sarfaranga Cold Desert", "A high-altitude desert landscape in the Shigar area, associated with seasonal events and scenic drives.", "Gilgit-Baltistan"),
                ("Shigar Valley", "A cold-desert and mountain setting with historic settlements and access toward the Karakoram.", "Gilgit-Baltistan"),
                ("Malam Jabba", "A mountain resort area known for winter recreation and seasonal snow conditions.", "Khyber Pakhtunkhwa"),
            ]),
        ],
    },
    "islamic_sufi": {
        "title": "Islamic & Sufi Heritage",
        "intro": "A geographically organised guide to major mosques, Sufi shrines and religious gatherings. This is a curated starting point, not a complete register of every mosque or shrine in Pakistan.",
        "sections": [
            ("Famous mosques", [
                ("Badshahi Mosque", "Lahore, Punjab", "A major Mughal-era congregational mosque facing Lahore Fort, known for its monumental courtyard and red sandstone architecture."),
                ("Wazir Khan Mosque", "Walled City, Lahore, Punjab", "A 17th-century mosque celebrated for its tilework, frescoes and historic urban setting."),
                ("Faisal Mosque", "Islamabad Capital Territory", "A contemporary national landmark at the foot of the Margalla Hills, with a distinctive tent-inspired design."),
                ("Mahabat Khan Mosque", "Peshawar, Khyber Pakhtunkhwa", "A prominent Mughal-period mosque in Peshawar’s historic city centre."),
                ("Shah Jahan Mosque", "Thatta, Sindh", "A 17th-century mosque known for extensive tile decoration and distinctive architectural design."),
                ("Bhong Mosque", "Bhong, Rahim Yar Khan, Punjab", "An ornate mosque complex recognised for elaborate decorative craftsmanship."),
                ("Sargana Mosque", "Multan region, Punjab", "A historic mosque highlighted in regional tourism planning for its courtyard and decorative details."),
                ("Sunehri Mosque", "Lahore, Punjab", "An 18th-century mosque in Lahore’s historic centre, known for its gilded domes."),
                ("Mariam Zamani Mosque", "Lahore Fort area, Punjab", "A Mughal-era mosque associated with Mariam-uz-Zamani, located near Lahore Fort."),
                ("Shahi Eid Gah Mosque", "Multan, Punjab", "A historic congregational mosque in Multan, associated with the city’s religious and architectural heritage."),
            ]),
            ("Famous Sufi shrines", [
                ("Data Darbar — Ali Hujwiri", "Lahore, Punjab", "One of Lahore’s best-known Sufi shrines, associated with the 11th-century scholar and mystic Ali Hujwiri."),
                ("Mian Mir Shrine", "Lahore, Punjab", "A major Sufi heritage site associated with the Qadiri saint Mian Mir."),
                ("Baba Farid Shrine", "Pakpattan, Punjab", "A major Chishti Sufi centre associated with Fariduddin Ganjshakar."),
                ("Shah Rukn-e-Alam Shrine", "Multan, Punjab", "A 14th-century octagonal mausoleum and defining monument of Multan’s Sufi heritage."),
                ("Bahauddin Zakariya Shrine", "Multan, Punjab", "The shrine of an influential Suhrawardi Sufi master whose legacy shaped Multan’s spiritual history."),
                ("Shah Shams Sabzwari Shrine", "Multan, Punjab", "A historic Sufi shrine within Multan’s wider sacred landscape."),
                ("Bibi Jawindi Tomb", "Uch Sharif, Punjab", "A celebrated 15th-century funerary monument within Uch Sharif’s historic Sufi and architectural landscape."),
                ("Jalaluddin Surkh-Posh Bukhari Shrine", "Uch Sharif, Punjab", "A major shrine associated with the Suhrawardi Sufi tradition and Uch Sharif’s religious history."),
                ("Lal Shahbaz Qalandar Shrine", "Sehwan Sharif, Sindh", "A major Sufi pilgrimage centre associated with the 13th-century saint Lal Shahbaz Qalandar."),
                ("Shah Abdul Latif Bhittai Shrine", "Bhit Shah, Sindh", "A major shrine and cultural centre associated with Sindh’s celebrated Sufi poet."),
                ("Sachal Sarmast Shrine", "Daraza Sharif, Khairpur, Sindh", "A shrine honouring the Sindhi Sufi poet known for multilingual devotional poetry."),
                ("Sakhi Sarwar Shrine", "Dera Ghazi Khan, Punjab", "A regional pilgrimage centre associated with the saint Sakhi Sarwar."),
                ("Baba Bulleh Shah Shrine", "Kasur, Punjab", "A major shrine associated with the Punjabi Sufi poet Bulleh Shah."),
                ("Khawaja Ghulam Farid Shrine", "Kot Mithan, Rajanpur, Punjab", "A shrine associated with the Sufi poet Khawaja Ghulam Farid and the Rohi/Cholistan literary tradition."),
                ("Sultan Bahu Shrine", "Garh Maharaja, Jhang, Punjab", "A pilgrimage site associated with the Sufi poet and scholar Sultan Bahu."),
                ("Shah Yusuf Gardezi Shrine", "Multan, Punjab", "A historic shrine within Multan’s wider Sufi heritage landscape."),
                ("Musa Pak Shaheed Shrine", "Multan, Punjab", "A prominent shrine in Multan administered within the Punjab Auqaf shrine network."),
                ("Abdullah Shah Ghazi Shrine", "Karachi, Sindh", "A major coastal-city shrine associated with Karachi’s religious and cultural history."),
                ("Shah Inayat Shaheed Shrine", "Jhok Sharif, Thatta, Sindh", "A shrine associated with the 18th-century Sufi figure Shah Inayat Shaheed."),
            ]),
            ("Religious gatherings & annual observances", [
                ("Raiwind Tablighi Ijtima (Ijtema)", "Raiwind, near Lahore, Punjab", "A large annual Tablighi Jamaat gathering. Dates, access arrangements and crowd-management instructions change each year; verify official announcements."),
                ("Urs of Lal Shahbaz Qalandar", "Sehwan Sharif, Sindh", "An annual Urs gathering associated with the shrine; event dates and visitor arrangements should be checked locally."),
                ("Urs of Shah Abdul Latif Bhittai", "Bhit Shah, Sindh", "An annual commemoration bringing devotional music, poetry and visitors to the shrine."),
                ("Urs of Baba Farid", "Pakpattan, Punjab", "An annual religious observance centred on Baba Farid’s shrine; follow local administration guidance."),
            ]),
        ],
    },
    "sikhism_sites": {
        "title": "Sikhism Sites",
        "intro": "Pakistan contains important Sikh pilgrimage places associated with Guru Nanak and Sikh history. Access rules, corridor arrangements and pilgrimage dates must be checked before travel.",
        "sections": [
            ("Major gurdwaras & pilgrimage sites", [
                ("Gurdwara Janam Asthan", "Nankana Sahib, Punjab", "A highly revered gurdwara marking the birthplace traditionally associated with Guru Nanak; Nankana Sahib contains a wider group of historic gurdwaras."),
                ("Gurdwara Darbar Sahib", "Kartarpur, Narowal, Punjab", "The sacred site associated with Guru Nanak’s final years; the Kartarpur Corridor has a separate access and documentation process."),
                ("Gurdwara Panja Sahib", "Hasan Abdal, Punjab", "A major pilgrimage gurdwara associated with the tradition of Guru Nanak’s visit and the preserved rock bearing a hand impression."),
                ("Gurdwara Dera Sahib", "Lahore, Punjab", "A major Sikh site associated with Guru Arjan Dev, near Lahore Fort and the Samadhi of Maharaja Ranjit Singh."),
                ("Gurdwara Sacha Sauda", "Farooqabad, Sheikhupura, Punjab", "A historic site associated with a formative episode in the life of Guru Nanak."),
                ("Gurdwara Rori Sahib", "Aimanabad, Gujranwala, Punjab", "A historic gurdwara associated with Guru Nanak’s travels and Sikh heritage in the region."),
                ("Gurdwara Chowa Sahib", "Rohtas area, Jhelum, Punjab", "A historic Sikh site associated with Guru Nanak and the wider Rohtas heritage landscape."),
            ]),
        ],
    },
    "hinduism_sites": {
        "title": "Hinduism Sites",
        "intro": "A curated guide to Hindu temples and pilgrimage landscapes in Pakistan. Religious-site access and preservation conditions can change; respect local custodians and community protocols.",
        "sections": [
            ("Temples & sacred landscapes", [
                ("Katas Raj Temples", "Chakwal, Punjab", "A complex of historic temples around a sacred pond, including shrines associated with Shiva, Ramachandra and Hanuman."),
                ("Hinglaj Mata Mandir", "Hingol National Park, Balochistan", "A major Hindu pilgrimage site set within the Hingol landscape; the annual Hinglaj Yatra draws pilgrims from across the region."),
                ("Shri Swaminarayan Mandir", "Karachi, Sindh", "A historic Hindu temple complex in Karachi associated with the Swaminarayan tradition."),
                ("Shri Varun Dev Mandir", "Manora, Karachi, Sindh", "A coastal temple dedicated to Varuna, associated with Karachi’s Hindu maritime heritage."),
                ("Umarkot Shiv Mandir", "Umerkot, Sindh", "A significant Hindu temple and pilgrimage site in the Umerkot region."),
                ("Panchmukhi Hanuman Mandir", "Karachi, Sindh", "A historic Hanuman temple in Karachi, recognised for its religious and community significance."),
                ("Sadhu Bela Temple Complex", "Sukkur, Sindh", "A Hindu temple complex on an island in the Indus River, associated with pilgrimage and the Udasi tradition."),
            ]),
        ],
    },
    "buddhist_heritage": {
        "title": "Buddhist Heritage",
        "intro": "Explore Gandharan Buddhist art, monasteries, stupas and archaeological landscapes, especially across Taxila, the Peshawar Valley and Swat.",
        "sections": [
            ("Stupas, monasteries & archaeological landscapes", [
                ("Dharmarajika Stupa", "Taxila, Punjab", "A major Buddhist stupa and monastic complex within the Taxila archaeological landscape."),
                ("Jaulian Monastery", "Taxila, Punjab", "A hilltop Buddhist monastery known for remains of stupas, chapels and sculptural details."),
                ("Takht-i-Bahi", "Mardan, Khyber Pakhtunkhwa", "A remarkably preserved Buddhist monastic complex on a hill and a UNESCO World Heritage Site."),
                ("Butkara Stupa", "Saidu Sharif, Swat, Khyber Pakhtunkhwa", "An important Buddhist stupa complex associated with the development of Gandharan Buddhist art."),
                ("Shingardar Stupa", "Barikot, Swat, Khyber Pakhtunkhwa", "A prominent Buddhist stupa in the Swat Valley archaeological landscape."),
            ]),
        ],
    },
    "ancient_civilizations": {
        "title": "Ancient Civilizations",
        "intro": "Discover archaeological sites and historic settlements that reveal Pakistan’s place in the Indus Valley, Gandharan and later regional histories.",
        "sections": [
            ("Archaeological sites & ancient settlements", [
                ("Mohenjo-daro", "Larkana, Sindh", "A major urban centre of the Indus Civilization, known for planned streets, drainage and baked-brick architecture."),
                ("Harappa", "Sahiwal, Punjab", "A principal Indus Civilization site with extensive archaeological remains and an associated museum."),
                ("Taxila", "Taxila, Punjab", "A multi-period archaeological landscape shaped by trade, urban settlement and Buddhist learning."),
                ("Mehrgarh", "Bolan region, Balochistan", "A key Neolithic and Chalcolithic archaeological site informing the early history of settled communities in South Asia."),
                ("Makli Necropolis", "Thatta, Sindh", "A vast funerary landscape containing monuments from several centuries of Sindh’s history."),
                ("Rohtas Fort", "Jhelum, Punjab", "A 16th-century fortified complex built under Sher Shah Suri and recognised as a UNESCO World Heritage Site."),
            ]),
        ],
    },
}

key = st.session_state.get("selected_experience_collection", "northern_landscapes")
collection = COLLECTIONS.get(key, COLLECTIONS["northern_landscapes"])

st.markdown("""
<style>
.experience-hero{padding:26px 30px;border:1px solid rgba(185,151,91,.34);border-radius:22px;background:linear-gradient(115deg,#102D22 0%,#1D4B38 58%,#304D50 100%);margin:4px 0 20px;box-shadow:0 16px 38px rgba(8,35,25,.13)}
.experience-kicker{font:800 10px Manrope,Arial,sans-serif;letter-spacing:2.5px;color:#D8C18D;text-transform:uppercase}
.experience-hero h1{font:700 clamp(32px,3.4vw,46px) 'Cormorant Garamond',Georgia,serif;color:#FFF;margin:8px 0 6px;line-height:1.05}
.experience-hero p{font:500 14px/1.75 Manrope,Arial,sans-serif;color:#F1F4EC;margin:0;max-width:900px}
.experience-filter-note{font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:#8A7652;font-weight:800;margin:8px 0}
[class*="st-key-experience-atlas-card-"]{height:100%}
[class*="st-key-experience-atlas-card-"] [data-testid="stVerticalBlockBorderWrapper"]{height:560px;min-height:560px;max-height:560px;display:flex;overflow:hidden;border:1px solid rgba(23,92,67,.22)!important;border-radius:18px!important;background:linear-gradient(145deg,#F7F1E5 0%,#E8F0E9 58%,#E5EEF0 100%)!important;padding:13px!important;box-shadow:0 12px 28px rgba(13,55,42,.08)!important}
[class*="st-key-experience-atlas-card-"] [data-testid="stVerticalBlock"]{height:100%;min-height:0;display:flex;flex-direction:column;gap:.35rem}
[class*="st-key-experience-atlas-card-"] [data-testid="stImage"]{height:210px;min-height:210px;max-height:210px;display:flex;align-items:center;justify-content:center;overflow:hidden;border-radius:12px;background:linear-gradient(135deg,#D7C59F,#C8E0D5 55%,#B8D6DF);padding:6px}
[class*="st-key-experience-atlas-card-"] [data-testid="stImage"] img{width:100%;height:198px;max-height:198px;object-fit:contain!important;object-position:center;border:0!important;box-shadow:none!important;border-radius:8px}
.experience-card-meta{font:800 9px/1.4 Manrope,Arial,sans-serif;letter-spacing:1.5px;text-transform:uppercase;color:#537063;min-height:25px}
.experience-card-title{font:700 24px/1.08 'Cormorant Garamond',Georgia,serif;color:#14251B;min-height:54px;max-height:54px;overflow:hidden}
.experience-card-location{font:800 10px/1.4 Manrope,Arial,sans-serif;letter-spacing:.7px;color:#765D34;min-height:28px}
.experience-card-copy{font:500 12px/1.6 Manrope,Arial,sans-serif;color:#26352C;height:82px;max-height:82px;overflow:hidden}
.experience-card-credit{font:500 9px/1.35 Manrope,Arial,sans-serif;color:#62756B;height:31px;max-height:31px;overflow:hidden}
.experience-tag{display:inline-block;margin:2px 4px 2px 0;padding:4px 8px;border-radius:999px;background:#DCE9DE;color:#23523A;font:800 9px Manrope,Arial,sans-serif;letter-spacing:.3px}
@media(max-width:850px){[class*="st-key-experience-atlas-card-"] [data-testid="stVerticalBlockBorderWrapper"]{height:auto;min-height:0;max-height:none}.experience-card-copy{height:auto;max-height:100px}}
</style>
""", unsafe_allow_html=True)

if st.button("← Back to VoyagePK home"):
    st.switch_page("app.py")

st.markdown(
    f'<div class="experience-hero"><div class="experience-kicker">VOYAGEPK · CURATED DESTINATION ATLAS</div>'
    f'<h1>{collection["title"]}</h1><p>{collection["intro"]}</p></div>',
    unsafe_allow_html=True,
)

def _place_fields(place):
    if key == "northern_landscapes":
        name, detail, location = place
    else:
        name, location, detail = place
    return name, location, detail

def _city_name(location):
    parts = [part.strip() for part in location.split(",") if part.strip()]
    first = parts[0] if parts else "Unclassified"
    if first.casefold() in {"walled city", "lahore fort area"}:
        return "Lahore"
    if first.casefold() == "multan region":
        return "Multan"
    if first.casefold() == "rawalpindi region":
        return "Taxila / Rawalpindi region"
    if first.casefold() == "hingol national park":
        return "Hingol / Lasbela"
    if first.casefold() == "bolan region":
        return "Bolan / Kachhi"
    return first

records = []
for section_title, places in collection["sections"]:
    for place in places:
        name, location, detail = _place_fields(place)
        records.append({
            "name": name, "location": location, "city": _city_name(location),
            "detail": detail, "category": section_title,
        })

cities = ["All cities"] + sorted({item["city"] for item in records})
categories = ["All tourism themes"] + [title for title, _ in collection["sections"]]
filter_cols = st.columns([1.1, 1.1, 1.6], gap="medium")
with filter_cols[0]:
    selected_city = st.selectbox("Browse by city / area", cities, key=f"exp_city_{key}")
with filter_cols[1]:
    selected_category = st.selectbox("Tourism category", categories, key=f"exp_category_{key}")
with filter_cols[2]:
    search_text = st.text_input("Find a destination", placeholder="Search a place, city or experience…", key=f"exp_search_{key}")

matches = [
    item for item in records
    if (selected_city == "All cities" or item["city"] == selected_city)
    and (selected_category == "All tourism themes" or item["category"] == selected_category)
    and search_text.casefold() in f'{item["name"]} {item["location"]} {item["detail"]} {item["category"]}'.casefold()
]
st.markdown(
    f'<div class="experience-filter-note">{len(matches)} curated places · grouped by tourism theme · filterable by city</div>',
    unsafe_allow_html=True,
)

for section_title, _ in collection["sections"]:
    section_matches = [item for item in matches if item["category"] == section_title]
    if not section_matches:
        continue
    st.subheader(section_title)
    for start_index in range(0, len(section_matches), 3):
        columns = st.columns(3, gap="large")
        for offset, (column, item) in enumerate(zip(columns, section_matches[start_index:start_index + 3])):
            with column:
                card_index = start_index + offset
                with st.container(border=True, key=f"experience-atlas-card-{key}-{section_title[:10]}-{card_index}"):
                    supplied = get_destination_gallery_image(item["name"] + " " + item["location"])
                    photo = supplied or get_commons_image(item["name"] + " " + item["location"])
                    if photo and photo.get("thumb_url"):
                        rendered = get_display_image(photo["thumb_url"], aspect_ratio=(16, 9))
                        if rendered:
                            st.image(rendered, use_container_width=True)
                        else:
                            st.image(photo["thumb_url"], use_container_width=True)
                        credit = (
                            f'{photo.get("artist", "Image source")} · {photo.get("license", "Attribution unavailable")}'
                            + (f' · [Source]({photo["page_url"]})' if photo.get("page_url") else "")
                        )
                    else:
                        st.markdown('<div style="height:198px;border-radius:10px;background:linear-gradient(135deg,#D7C59F,#C8E0D5 55%,#B8D6DF);display:flex;align-items:center;justify-content:center;color:#31564A;font-size:11px;font-weight:800;letter-spacing:1.5px">VOYAGEPK DESTINATION</div>', unsafe_allow_html=True)
                        credit = "Photography reference not yet assigned"
                    st.markdown(f'<div class="experience-card-meta">{item["category"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="experience-card-title">{item["name"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="experience-card-location">{item["city"]} · {item["location"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="experience-card-copy">{item["detail"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="experience-card-credit">{credit}</div>', unsafe_allow_html=True)

st.divider()
st.subheader("Reference sources")
st.markdown(
    "- [Punjab Auqaf Department — shrine directory](https://auqaf.punjab.gov.pk/shrines)\n"
    "- [Punjab Portal — religious monuments and gurdwaras](https://punjab.gov.pk/religious-monuments)\n"
    "- [Department of Archaeology & Museums — Katas Raj Temples](https://doam.gov.pk/public/sites/6750)\n"
    "- [Government of Pakistan — Raiwind Tablighi Ijtima reference](https://pid.gov.pk/site/press_detail/27048)\n"
    "- [TDCP — Sikh pilgrimage guide](https://webapi.tdcp.gop.pk/uploads/1769507590777-461675896.pdf)"
)
st.caption("This is a curated editorial collection, not an exhaustive gazetteer. Verify current access, permits, opening arrangements, safety and local guidance before travelling.")
