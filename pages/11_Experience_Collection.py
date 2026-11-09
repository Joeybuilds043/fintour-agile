from __future__ import annotations

import streamlit as st

from src.catalog import DESTINATIONS
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
            ]),
            ("Religious gatherings & annual observances", [
                ("Raiwind Tablighi Ijtema", "Raiwind, near Lahore, Punjab", "A large annual Tablighi Jamaat gathering. Dates, access arrangements and crowd-management instructions change each year; verify official announcements."),
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
                ("Taxila", "Rawalpindi region, Punjab", "A multi-period archaeological landscape shaped by trade, urban settlement and Buddhist learning."),
                ("Mehrgarh", "Bolan region, Balochistan", "A key Neolithic and Chalcolithic archaeological site informing the early history of settled communities in South Asia."),
                ("Makli Necropolis", "Thatta, Sindh", "A vast funerary landscape containing monuments from several centuries of Sindh’s history."),
                ("Rohtas Fort", "Jhelum, Punjab", "A 16th-century fortified complex built under Sher Shah Suri and recognised as a UNESCO World Heritage Site."),
            ]),
        ],
    },
}

key = st.session_state.get("selected_experience_collection", "northern_landscapes")
collection = COLLECTIONS.get(key, COLLECTIONS["northern_landscapes"])

if st.button("← Back to VoyagePK home"):
    st.switch_page("app.py")

st.markdown('<div class="atlas-kicker">VOYAGEPK · PLACE-BASED COLLECTION</div>', unsafe_allow_html=True)
st.title(collection["title"])
st.write(collection["intro"])

for section_title, places in collection["sections"]:
    st.subheader(section_title)
    cols = st.columns(2, gap="large")
    for index, place in enumerate(places):
        with cols[index % 2]:
            with st.container(border=True):
                if key == "northern_landscapes":
                    name, detail, location = place
                else:
                    name, location, detail = place
                st.markdown(f"**{name}**")
                st.caption(location)
                st.write(detail)

if key == "northern_landscapes":
    st.divider()
    st.subheader("Browse the destination catalogue")
    candidates = [
        (name, item) for name, item in DESTINATIONS.items()
        if any(tag in item.get("experiences", []) for tag in ("Nature & wildlife", "Adventure", "Camping & outdoors"))
    ]
    candidates.sort(key=lambda pair: pair[0])
    st.caption(f"{len(candidates)} destination clusters tagged for nature, adventure or outdoor travel.")
    for start in range(0, len(candidates), 3):
        cols = st.columns(3)
        for col, (name, item) in zip(cols, candidates[start:start + 3]):
            with col:
                with st.container(border=True):
                    st.markdown(f"**{name}**")
                    st.caption(item.get("province", item["region"]))
                    st.write(item["tagline"])
                    if st.button("Open destination guide", key=f"north_{name}"):
                        st.session_state["selected_destination"] = name
                        st.switch_page("pages/02_Destination_Guide.py")

st.caption("This is a curated editorial collection, not an exhaustive gazetteer. Verify current access, permits, opening arrangements, safety and local guidance before travelling.")
