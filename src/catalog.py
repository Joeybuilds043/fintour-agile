"""Curated Pakistan destination catalogue for visitor discovery and AI context.

The catalogue is editorial, not an exhaustive official gazetteer or ranking.
Coordinates are approximate destination-cluster anchors, not navigation points.
"""
EXPERIENCE_CATEGORIES = [
    {"name": "Adventure", "symbol": "A", "short": "Trekking, climbing, rafting and outdoor challenge"},
    {"name": "Nature & wildlife", "symbol": "N", "short": "National parks, lakes, forests and landscapes"},
    {"name": "Camping & outdoors", "symbol": "C", "short": "Camping, stargazing and scenic road journeys"},
    {"name": "Culture & heritage", "symbol": "H", "short": "Architecture, living traditions, arts and history"},
    {"name": "Ecotourism", "symbol": "E", "short": "Conservation-led and community-based travel"},
    {"name": "Food & gastronomy", "symbol": "F", "short": "Regional food, markets and culinary routes"},
    {"name": "Religious & archaeology", "symbol": "R", "short": "Sacred places, archaeology and learning"},
    {"name": "Islamic & Sufi heritage", "symbol": "I", "short": "Mosques, shrines, Sufi centres and sacred architecture"},
    {"name": "Sikh pilgrimage", "symbol": "S", "short": "Gurdwaras and places associated with Sikh history"},
    {"name": "Buddhist heritage", "symbol": "B", "short": "Gandharan stupas, monasteries and Buddhist landscapes"},
    {"name": "Hindu heritage", "symbol": "H", "short": "Temples, sacred landscapes and Hindu pilgrimage"},
    {"name": "Archaeology & ancient civilizations", "symbol": "A", "short": "Indus Valley archaeology and historic settlements"},
    {"name": "Coastal & marine", "symbol": "S", "short": "Beaches, marine landscapes and coastal culture"},
    {"name": "Winter & seasonal", "symbol": "W", "short": "Snow, seasonal festivals and changing landscapes"},
    {"name": "Rural & creative", "symbol": "L", "short": "Crafts, farms, villages and local enterprise"},
]

DESTINATIONS = {
"Hunza Valley":{"region":"Gilgit-Baltistan","lat":36.3167,"lon":74.6500,"tagline":"Karakoram panoramas, historic forts and village hospitality.","overview":"A high-mountain destination known for dramatic landscapes, historic settlements, local food and routes through the Karakoram region.","culture":"Hunza's communities have distinct languages, foodways, music, craft traditions and histories. Cultural content should be developed with local contributors and should not treat the valley as one uniform culture.","experiences":["Adventure","Nature & wildlife","Camping & outdoors","Culture & heritage","Ecotourism","Food & gastronomy","Rural & creative"],"highlights":["Karimabad and Baltit Fort","Altit Fort and its historic settlement","Attabad Lake and Passu Cones","Gulmit, Ghulkin and upper Hunza village experiences"],"season":"Spring through autumn is a common visitor season; high-altitude conditions and road access vary. Confirm local conditions before departure.","access":"The Karakoram Highway is a major access corridor. Journey times depend on road conditions, weather, traffic and starting point.","responsible":"Use local guides where appropriate, respect community and photography protocols, minimise waste and choose locally owned services.","image_query":"Hunza Valley Passu Cones Attabad Lake Pakistan"},
"Skardu":{"region":"Gilgit-Baltistan","lat":35.2971,"lon":75.6333,"tagline":"Glacial valleys, turquoise lakes and gateways to the high Karakoram.","overview":"A gateway to high mountain landscapes, lakes, valleys and trekking areas. Experiences range from scenic travel to demanding high-altitude expeditions.","culture":"Baltistan has a rich regional history, languages, food traditions, architecture and community life. Present cultural interpretation with local voices and context.","experiences":["Adventure","Nature & wildlife","Camping & outdoors","Culture & heritage","Ecotourism","Food & gastronomy","Winter & seasonal"],"highlights":["Shigar Fort and Shigar Valley","Satpara Lake and Kachura Lakes","Deosai plateau, subject to seasonal access","Khaplu heritage and Balti food experiences"],"season":"Many high-altitude routes are seasonal. Access to Deosai and trekking areas depends on snow, weather and official conditions.","access":"Skardu is served by road and air connections, both subject to weather and operational conditions. Verify schedules and road status.","responsible":"Respect protected landscapes, use trained guides for remote routes, carry out waste and plan for altitude and emergencies.","image_query":"Skardu Shangrila Lower Kachura Lake Pakistan"},
"Swat Valley":{"region":"Khyber Pakhtunkhwa","lat":35.2220,"lon":72.4258,"tagline":"River valleys, forested slopes and layers of Gandhara heritage.","overview":"A varied valley destination combining rivers, forests, mountain settlements, archaeology and family-oriented nature experiences.","culture":"Swat has layered Buddhist, historical and contemporary cultural heritage. Local traditions, crafts and food vary across communities and locations.","experiences":["Nature & wildlife","Adventure","Culture & heritage","Camping & outdoors","Ecotourism","Food & gastronomy","Winter & seasonal"],"highlights":["Mingora and Saidu Sharif cultural sites","Malam Jabba mountain resort area","Kalam and Mahodand Lake landscapes","Ushu Forest and local food experiences"],"season":"Suitability varies between lower valley and higher mountain areas. Check weather, road access and local advisories.","access":"Road travel is the main access mode for most visitors. Journey times vary with traffic, route and weather.","responsible":"Follow river and trail safety guidance, respect heritage sites and select accommodation with responsible waste practices.","image_query":"Swat Valley Kalam Mahodand Lake Pakistan"},
"Chitral & Kalash Valleys":{"region":"Khyber Pakhtunkhwa","lat":35.8510,"lon":71.7864,"tagline":"Distinctive cultural landscapes beneath the Hindu Kush.","overview":"A destination cluster spanning Chitral's mountain landscapes and the Kalash valleys, where visitors can learn about local history, community life and nature.","culture":"Kalash communities have distinct cultural and religious traditions. Follow community guidance, seek consent before photographing people or ceremonies and avoid reducing living culture to a spectacle.","experiences":["Culture & heritage","Adventure","Nature & wildlife","Rural & creative","Food & gastronomy","Ecotourism"],"highlights":["Bumburet, Rumbur and Birir valleys","Chitral town and Chitral Fort","Garam Chashma and mountain landscapes","Community-approved craft and food experiences"],"season":"Road and weather conditions vary. Check festival dates, visitor access and local protocols with community and official sources.","access":"Access is by road through mountain routes; journey conditions can change quickly. Verify route status and allow contingency time.","responsible":"Prioritise community consent, cultural safeguarding, locally guided visits and fair payment for cultural work.","image_query":"Kalash Valley Bumburet Chitral Pakistan village mountains"},
"Neelum Valley":{"region":"Azad Jammu & Kashmir","lat":34.5850,"lon":73.9070,"tagline":"Forest trails, river bends and mountain villages.","overview":"A scenic mountain and river valley with forest landscapes, waterfalls, villages and opportunities for low-impact nature travel.","culture":"The valley includes varied village communities, regional food and craft traditions. Work with local hosts to represent community life accurately.","experiences":["Nature & wildlife","Camping & outdoors","Adventure","Ecotourism","Rural & creative","Food & gastronomy"],"highlights":["Keran and riverside scenery","Sharda and its historic setting","Arang Kel, subject to access and conditions","Ratti Gali Lake, subject to seasonal access"],"season":"Access is seasonal in some areas. Landslides, rain, snow and road conditions can affect travel at short notice.","access":"Road access follows the valley corridor. Check current local advisories, route status and applicable travel requirements.","responsible":"Avoid river-edge risks, take waste back, respect private land and support local accommodation and guides.","image_query":"Neelum Valley Kashmir Pakistan river forest mountains"},
"Lahore":{"region":"Punjab","lat":31.5204,"lon":74.3587,"tagline":"Mughal architecture, food streets, gardens and a living arts scene.","overview":"A major cultural city where historic architecture, museums, food streets, markets, festivals and creative life can form multi-day visitor journeys.","culture":"Lahore's identity is shaped by many historical periods and contemporary communities. Food, language, music, literature, craft and religious heritage are important parts of the city's story.","experiences":["Culture & heritage","Food & gastronomy","Religious & archaeology","Rural & creative"],"highlights":["Lahore Fort and the Walled City","Badshahi Mosque and historic surroundings","Shalimar Gardens","Museums, food streets, markets and arts spaces"],"season":"Cooler months are generally more comfortable for extensive outdoor walking. Summer heat can affect itineraries; check weather and opening hours.","access":"Lahore has major road, rail and air connections. Local journey times vary with traffic.","responsible":"Respect religious-site dress and conduct requirements, use authorised heritage guides and support local artisans.","image_query":"Badshahi Mosque Lahore Fort Pakistan sunset"},
"Taxila":{"region":"Punjab","lat":33.7460,"lon":72.8390,"tagline":"An archaeological landscape shaped by ancient trade and learning.","overview":"An important archaeological landscape with museum and site experiences suited to heritage, education and research-oriented travel.","culture":"Taxila's archaeological heritage spans multiple periods and cultural influences. Interpretation should distinguish established scholarship from popular claims and respect conservation rules.","experiences":["Religious & archaeology","Culture & heritage","Rural & creative"],"highlights":["Taxila Museum","Sirkap archaeological site","Jaulian monastery site","Other archaeological remains subject to official access"],"season":"Outdoor site visits are often more comfortable in cooler months. Confirm museum hours and site access with the responsible authority.","access":"Taxila is accessible by road from Islamabad and Rawalpindi. Check transport and opening information.","responsible":"Do not touch, climb on or remove archaeological material. Follow site rules and use qualified interpretation.","image_query":"Taxila Sirkap Buddhist archaeological ruins Pakistan"},
"Karachi & Makli–Thatta":{"region":"Sindh","lat":24.7460,"lon":67.9230,"tagline":"Coastal city energy and one of South Asia's remarkable heritage landscapes.","overview":"A linked urban and heritage cluster combining Karachi's food, arts and coastline with historic landscapes around Thatta and Makli.","culture":"Sindh's cultural traditions include languages, music, Sufi heritage, crafts, architecture and regional food. Represent communities and sacred sites with care and context.","experiences":["Culture & heritage","Food & gastronomy","Coastal & marine","Religious & archaeology","Rural & creative"],"highlights":["Karachi museums, markets and food districts","Clifton and selected coastal experiences","Makli necropolis","Thatta and Shah Jahan Mosque"],"season":"Outdoor city and heritage visits are generally more comfortable in cooler months. Check coastal weather and local access.","access":"Karachi has major air, rail and road connections. Makli and Thatta require onward road travel; verify current conditions.","responsible":"Respect religious and funerary sites, use local guides and follow coastal safety and environmental guidance.","image_query":"Makli Necropolis Thatta Shah Jahan Mosque Sindh Pakistan"},
"Bahawalpur & Cholistan":{"region":"Punjab","lat":29.3956,"lon":71.6836,"tagline":"Desert horizons, princely architecture and fort landscapes.","overview":"A southern Punjab destination cluster linking Bahawalpur's heritage with desert landscapes and cultural life of Cholistan.","culture":"The region has distinctive desert livelihoods, craft traditions, music, architecture and pastoral histories. Develop cultural experiences with local communities.","experiences":["Nature & wildlife","Culture & heritage","Camping & outdoors","Rural & creative","Adventure"],"highlights":["Noor Mahal and Bahawalpur heritage","Derawar Fort, subject to access permissions and conditions","Cholistan desert landscapes","Local crafts, food and community experiences"],"season":"Desert heat can be severe. Cooler periods are generally more suitable for outdoor activities; verify local conditions and event dates.","access":"Bahawalpur is connected by road, rail and air services. Desert excursions require reliable transport and local knowledge.","responsible":"Travel with experienced local operators, carry sufficient water, respect community land and avoid disturbing wildlife.","image_query":"Derawar Fort Cholistan desert Bahawalpur Pakistan"},
"Hingol & Gwadar Coast":{"region":"Balochistan","lat":25.1260,"lon":62.3220,"tagline":"Sculpted coastlines where desert, rock and Arabian Sea meet.","overview":"A coastal and protected-landscape cluster where dramatic geology, beaches and marine environments create opportunities for carefully managed nature tourism.","culture":"Balochistan's coastal communities have rich maritime, food, craft and cultural traditions. Local knowledge and community consent should shape tourism experiences.","experiences":["Coastal & marine","Nature & wildlife","Camping & outdoors","Adventure","Food & gastronomy","Ecotourism"],"highlights":["Hingol National Park landscapes","Princess of Hope rock formation","Makran Coastal Highway viewpoints","Gwadar coastal experiences, subject to current access and safety advice"],"season":"Hot conditions and coastal weather affect activity suitability. Check local safety, road and protected-area guidance before travel.","access":"Long-distance road travel is common for coastal circuits. Verify security advisories, fuel availability, road conditions and operator arrangements.","responsible":"Follow protected-area rules, avoid disturbing wildlife, minimise water use and use locally informed operators.","image_query":"Hingol National Park Princess of Hope Makran coast Pakistan"},
}

def _add(name, region, lat, lon, tagline, experiences, highlights, image_query, overview):
    """Add a consistently structured editorial destination cluster."""
    DESTINATIONS[name] = {
        "region": region, "lat": lat, "lon": lon, "tagline": tagline,
        "overview": overview,
        "culture": f"{name} has locally specific histories, communities and cultural practices. Visitors should use locally informed guides, seek consent before photographing people and follow site-specific customs.",
        "experiences": experiences,
        "highlights": highlights,
        "season": "Conditions vary by season, altitude and local access. Check current weather, opening information and official advisories before travelling.",
        "access": "Use current transport-provider and local-authority information to confirm routes, journey times and access. The map marker is an approximate destination-cluster anchor.",
        "responsible": "Respect local communities and protected landscapes, minimise waste, follow site rules and prioritise locally owned services where possible.",
        "image_query": image_query,
    }

# Additional well-known destination clusters across all provinces and territories.
_add("Islamabad & Margalla Hills", "Islamabad Capital Territory", 33.6844, 73.0479,
     "A green capital framed by trails, viewpoints and contemporary culture.",
     ["Nature & wildlife","Adventure","Culture & heritage","Food & gastronomy","Rural & creative"],
     ["Faisal Mosque and the National Monument","Margalla Hills trail network","Lok Virsa Museum and galleries","Rawal Lake and city viewpoints"],
     "Margalla Hills Islamabad Faisal Mosque Pakistan", "A capital-city destination combining civic architecture, museums, dining, urban parks and accessible foothill trails.")
_add("Murree & Galiyat", "Punjab / Khyber Pakhtunkhwa", 33.9070, 73.3943,
     "Pine-covered hills, colonial-era streets and cool-climate escapes.",
     ["Nature & wildlife","Winter & seasonal","Camping & outdoors","Adventure","Food & gastronomy"],
     ["Mall Road and historic hill-station streets","Nathia Gali and Dunga Gali","Ayubia National Park","Pipeline Track and forest viewpoints"],
     "Murree Nathia Gali Ayubia pine forest Pakistan", "A hill-station region with forest walks, viewpoints and seasonal visitor activity.")
_add("Naran–Kaghan Valley", "Khyber Pakhtunkhwa", 34.9090, 73.6500,
     "Alpine lakes, river corridors and summer mountain journeys.",
     ["Nature & wildlife","Adventure","Camping & outdoors","Ecotourism"],
     ["Naran and Kunhar River","Saif-ul-Malook Lake","Lalazar plateau","Babusar Pass, subject to seasonal access"],
     "Saif ul Malook Lake Naran Kaghan Pakistan", "A highland valley corridor known for alpine scenery and seasonal road journeys.")
_add("Shogran & Siri Paye", "Khyber Pakhtunkhwa", 34.6300, 73.4950,
     "Meadows and forested ridges above the Kaghan Valley.",
     ["Nature & wildlife","Adventure","Camping & outdoors","Ecotourism"],
     ["Shogran plateau","Siri Paye meadows","Forest walks and local viewpoints"],
     "Siri Paye meadows Shogran Pakistan", "A mountain meadow destination suited to short nature breaks and guided outdoor experiences.")
_add("Fairy Meadows & Raikot", "Gilgit-Baltistan", 35.3830, 74.5900,
     "A dramatic alpine meadow beneath the Nanga Parbat massif.",
     ["Adventure","Nature & wildlife","Camping & outdoors","Ecotourism"],
     ["Fairy Meadows","Nanga Parbat viewpoints","Raikot Bridge access corridor","Guided mountain walks"],
     "Fairy Meadows Nanga Parbat Pakistan", "A remote high-mountain destination requiring careful logistics, local guidance and physical preparation.")
_add("Astore & Rama Valley", "Gilgit-Baltistan", 35.3410, 74.8560,
     "Quiet mountain valleys, alpine lakes and forest landscapes.",
     ["Nature & wildlife","Adventure","Camping & outdoors","Ecotourism"],
     ["Rama Lake","Rama Meadows","Astore Valley villages","Nanga Parbat viewpoints"],
     "Rama Lake Astore Pakistan alpine", "A mountain district with alpine landscapes and access to trekking and nature experiences.")
_add("Phander & Ghizer", "Gilgit-Baltistan", 36.1800, 72.9000,
     "Blue lakes, river valleys and slower-paced mountain travel.",
     ["Nature & wildlife","Camping & outdoors","Adventure","Rural & creative","Ecotourism"],
     ["Phander Lake","Gupis and surrounding valleys","Ishkoman landscapes","Village and river experiences"],
     "Phander Lake Ghizer Gilgit Baltistan Pakistan", "A scenic upper Gilgit-Baltistan corridor with lakes, villages and seasonal outdoor travel.")
_add("Khunjerab & Upper Hunza", "Gilgit-Baltistan", 36.8500, 75.4300,
     "High-altitude landscapes along the historic Karakoram corridor.",
     ["Adventure","Nature & wildlife","Culture & heritage","Camping & outdoors"],
     ["Khunjerab National Park","Sost and upper Hunza","Passu and Gulmit landscapes","Karakoram Highway viewpoints"],
     "Khunjerab Pass National Park Pakistan Karakoram", "A high-altitude borderland landscape where access, weather and park rules require careful checking.")
_add("Khaplu & Shyok Valley", "Gilgit-Baltistan", 35.1500, 76.3350,
     "Balti heritage, mountain settlements and river landscapes.",
     ["Culture & heritage","Nature & wildlife","Adventure","Food & gastronomy","Rural & creative"],
     ["Khaplu Palace","Chaqchan Mosque","Shyok Valley villages","Local Balti food and craft experiences"],
     "Khaplu Palace Shyok Valley Baltistan Pakistan", "A heritage-led destination in eastern Baltistan with historic architecture and mountain scenery.")
_add("Deosai National Park", "Gilgit-Baltistan", 35.0000, 75.4000,
     "A vast high-altitude plateau of open skies and fragile alpine ecology.",
     ["Nature & wildlife","Camping & outdoors","Adventure","Ecotourism"],
     ["Sheosar Lake","Deosai plateau landscapes","Wildlife viewing from designated areas","Seasonal wildflower landscapes"],
     "Deosai National Park Sheosar Lake Pakistan", "A protected high-altitude plateau where seasonal access and conservation rules shape visitor experiences.")
_add("Ratti Gali & Dowarian", "Azad Jammu & Kashmir", 34.8100, 74.0700,
     "A glacial lake journey through high meadows and mountain scenery.",
     ["Adventure","Nature & wildlife","Camping & outdoors","Ecotourism"],
     ["Ratti Gali Lake","Dowarian village","High meadow trails","Guided day hikes"],
     "Ratti Gali Lake Azad Kashmir Pakistan", "A seasonal alpine lake destination requiring local transport and trail guidance.")
_add("Rawalakot & Banjosa", "Azad Jammu & Kashmir", 33.8570, 73.7600,
     "Pine forests, lakes and relaxed Poonch hill-country stays.",
     ["Nature & wildlife","Camping & outdoors","Rural & creative","Food & gastronomy"],
     ["Banjosa Lake","Toli Pir viewpoints","Rawalakot town","Village and forest walks"],
     "Banjosa Lake Rawalakot Azad Kashmir Pakistan", "A hill-country cluster offering lake, forest and community-based experiences.")
_add("Multan", "Punjab", 30.1575, 71.5249,
     "Sufi shrines, blue-tile craft, bazaars and the flavours of south Punjab.",
     ["Culture & heritage","Religious & archaeology","Food & gastronomy","Rural & creative"],
     ["Shrine of Shah Rukn-e-Alam","Shrine of Bahauddin Zakariya","Hussain Agahi Bazaar","Blue pottery and local craft workshops"],
     "Multan Shah Rukn e Alam shrine blue tiles Pakistan", "A historic city known for Sufi heritage, craft traditions, markets and regional cuisine.")
_add("Faisalabad", "Punjab", 31.4504, 73.1350,
     "A textile city with industrial heritage, markets and Punjabi food culture.",
     ["Culture & heritage","Food & gastronomy","Rural & creative"],
     ["Clock Tower and eight bazaars","Lyallpur Museum","Textile and craft heritage","Local food markets"],
     "Faisalabad Clock Tower Ghanta Ghar Pakistan", "An urban destination whose textile and commercial heritage can support industrial and cultural tourism.")
_add("Peshawar", "Khyber Pakhtunkhwa", 34.0151, 71.5249,
     "An ancient crossroads of caravan history, bazaars and cuisine.",
     ["Culture & heritage","Food & gastronomy","Religious & archaeology","Rural & creative"],
     ["Qissa Khwani Bazaar","Peshawar Museum","Bala Hisar Fort exterior and heritage context","Sethi House and traditional architecture"],
     "Peshawar Qissa Khwani Bazaar historic Pakistan", "A historic city with layered trade routes, architecture, museums and distinctive food traditions.")
_add("Mohenjo-daro", "Sindh", 27.3290, 68.1380,
     "The remarkable urban remains of the Indus Civilisation.",
     ["Religious & archaeology","Culture & heritage"],
     ["Mohenjo-daro archaeological site","Site museum, subject to opening","Conservation and interpretation areas"],
     "Mohenjo Daro archaeological site Sindh Pakistan", "A UNESCO-listed archaeological site requiring conservation-led interpretation and respect for site controls.")
_add("Ranikot Fort", "Sindh", 25.9000, 67.9000,
     "Monumental fort walls set within the Kirthar mountain landscape.",
     ["Culture & heritage","Adventure","Nature & wildlife","Camping & outdoors"],
     ["Ranikot Fort perimeter","Sann Gate","Meeri fort area","Kirthar landscape viewpoints"],
     "Ranikot Fort Great Wall of Sindh Pakistan", "A large historic fort landscape suited to heritage exploration with suitable transport and local guidance.")
_add("Keenjhar Lake & Thatta", "Sindh", 24.9500, 68.0500,
     "Wetland scenery and historic Sindhi architecture near the coast.",
     ["Nature & wildlife","Culture & heritage","Religious & archaeology","Food & gastronomy"],
     ["Keenjhar Lake","Shah Jahan Mosque","Thatta historic quarter","Wetland and birdlife viewing"],
     "Keenjhar Lake Shah Jahan Mosque Thatta Pakistan", "A lower Sindh destination combining a major lake with historic architecture and regional culture.")
_add("Khewra & Salt Range", "Punjab", 32.6500, 73.0100,
     "Geology, salt landscapes and hill-country heritage.",
     ["Nature & wildlife","Culture & heritage","Adventure"],
     ["Khewra Salt Mine, subject to official access","Katas Raj temples","Kallar Kahar lake and viewpoints","Salt Range geology"],
     "Khewra Salt Mine Pakistan salt formations", "A geological and heritage route across the Salt Range, with site access governed by local operators.")
_add("Rohtas Fort & Jhelum", "Punjab", 32.9700, 73.5800,
     "A monumental fortified landscape from the Sur period.",
     ["Culture & heritage","Religious & archaeology"],
     ["Rohtas Fort","Historic gateways and walls","Nearby village and landscape context"],
     "Rohtas Fort Jhelum Pakistan UNESCO", "A UNESCO-listed fort destination with strong architectural and military-history interest.")
_add("Ziarat & Quetta", "Balochistan", 30.3820, 67.7250,
     "Juniper forests, mountain air and Balochistan's highland heritage.",
     ["Nature & wildlife","Culture & heritage","Camping & outdoors","Rural & creative"],
     ["Ziarat Juniper Forest","Quaid-e-Azam Residency","Hanna Lake","Quetta markets and food"],
     "Ziarat Juniper Forest Quaid e Azam Residency Balochistan", "A highland destination combining juniper ecosystems, heritage architecture and Quetta's urban culture.")
_add("Ormara & Kund Malir", "Balochistan", 25.2100, 64.6500,
     "Remote Makran beaches, headlands and coastal road scenery.",
     ["Coastal & marine","Nature & wildlife","Camping & outdoors","Ecotourism"],
     ["Kund Malir beach","Ormara coastal landscapes","Makran Coastal Highway","Local fishing communities and coastal ecology"],
     "Kund Malir beach Makran Coastal Highway Pakistan", "A remote coastal cluster where visitor planning must account for long distances, access and local safety advice.")
_add("Uch Sharif & Bahawalpur Heritage", "Punjab", 29.2300, 71.0600,
     "Historic shrines, intricate tilework and southern Punjab heritage.",
     ["Culture & heritage","Religious & archaeology","Rural & creative"],
     ["Historic shrines of Uch Sharif","Bibi Jawindi tomb","Bahawalpur heritage quarter","Local craft and food traditions"],
     "Uch Sharif Bibi Jawindi tomb Pakistan", "A heritage circuit centred on historic religious architecture and the cultural landscapes of southern Punjab.")
_add("Malam Jabba", "Khyber Pakhtunkhwa", 34.8000, 72.5700,
     "A mountain resort landscape for seasonal snow and outdoor recreation.",
     ["Winter & seasonal","Adventure","Nature & wildlife","Camping & outdoors"],
     ["Malam Jabba ski area","Forest and mountain viewpoints","Seasonal outdoor activities"],
     "Malam Jabba ski resort Swat Pakistan", "A seasonal mountain recreation destination; facilities and operating schedules should be checked directly.")
_add("Kalam & Ushu Forest", "Khyber Pakhtunkhwa", 35.4900, 72.5800,
     "Alpine rivers, cedar forests and high-valley scenery.",
     ["Nature & wildlife","Adventure","Camping & outdoors","Ecotourism"],
     ["Kalam town and river","Ushu Forest","Mahodand Lake access corridor","Matiltan valley landscapes"],
     "Ushu Forest Kalam Swat Pakistan", "A forest and mountain destination with seasonal road access and opportunities for guided nature experiences.")
_add("Gorakh Hill Station", "Sindh", 26.8600, 67.0900,
     "A high plateau escape above the Sindh plains.",
     ["Nature & wildlife","Camping & outdoors","Adventure"],
     ["Gorakh Hill viewpoints","Sunrise and sunset landscapes","Guided hill-country excursions"],
     "Gorakh Hill Station Sindh Pakistan plateau", "A highland destination in Sindh where road conditions, weather and local logistics should be confirmed.")
_add("Makran Coast & Pasni", "Balochistan", 25.2600, 63.4700,
     "Fishing towns, long beaches and the open Arabian Sea.",
     ["Coastal & marine","Nature & wildlife","Food & gastronomy","Rural & creative"],
     ["Pasni coastal town","Fishing harbour and seafood culture","Makran coastline","Nearby coastal landscapes subject to access"],
     "Pasni Makran coast Balochistan Pakistan", "A coastal community destination where responsible visitor activity should support local livelihoods.")
_add("Sukkur & Rohri", "Sindh", 27.7052, 68.8574,
     "River Indus views, historic bridges and northern Sindh culture.",
     ["Culture & heritage","Nature & wildlife","Food & gastronomy","Religious & archaeology"],
     ["Sukkur Barrage viewpoints","Lansdowne Bridge","Sadhu Bela, subject to access","Indus riverfront and local markets"],
     "Sukkur Lansdowne Bridge Indus River Pakistan", "An urban river destination with engineering heritage, religious sites and regional food culture.")
_add("Kundian & Chashma Wetlands", "Punjab / Khyber Pakhtunkhwa", 32.4500, 71.4500,
     "Riverine and wetland landscapes for birdlife and nature learning.",
     ["Nature & wildlife","Ecotourism","Camping & outdoors"],
     ["Chashma Barrage surroundings","Wetland birdlife from permitted viewing areas","Indus river landscapes"],
     "Chashma Barrage wetlands Pakistan birdwatching", "A nature-oriented cluster for responsible birdwatching and wetland interpretation.")


# Dedicated religious-heritage and archaeological destination collections.
_add("Nankana Sahib & Sikh Heritage", "Punjab", 31.4504, 73.7065,
     "A major Sikh pilgrimage landscape centred on the birthplace of Guru Nanak.",
     ["Sikh pilgrimage", "Culture & heritage", "Religious & archaeology"],
     ["Gurdwara Janam Asthan", "Gurdwara Sacha Sauda at Farooqabad", "Historic gurdwaras associated with Guru Nanak"],
     "Gurdwara Janam Asthan Nankana Sahib Pakistan",
     "Nankana Sahib is an important Sikh pilgrimage destination. Plan around current site protocols, religious calendars and guidance from the responsible authorities.")
_add("Kartarpur Sahib & Narowal", "Punjab", 32.1036, 75.0265,
     "A sacred Sikh destination connected with the later life of Guru Nanak.",
     ["Sikh pilgrimage", "Culture & heritage", "Religious & archaeology"],
     ["Gurdwara Darbar Sahib Kartarpur", "Kartarpur Corridor visitor facilities", "Local heritage and community context"],
     "Gurdwara Darbar Sahib Kartarpur Pakistan",
     "Kartarpur is a major Sikh pilgrimage destination. Access arrangements, permits, visiting hours and cross-border procedures can change and must be confirmed through official channels.")
_add("Hasan Abdal & Panja Sahib", "Punjab", 33.8204, 72.6890,
     "A historic Sikh pilgrimage site in the foothills near Hasan Abdal.",
     ["Sikh pilgrimage", "Culture & heritage", "Religious & archaeology"],
     ["Gurdwara Panja Sahib", "Historic town of Hasan Abdal", "Regional heritage and pilgrimage context"],
     "Gurdwara Panja Sahib Hasan Abdal Pakistan",
     "Hasan Abdal is associated with Gurdwara Panja Sahib, a significant Sikh place of pilgrimage. Visitors should follow site protocols and verify access arrangements.")
_add("Swat Buddhist Heritage Circuit", "Khyber Pakhtunkhwa", 34.7657, 72.3679,
     "A concentrated archaeological landscape of Buddhist stupas and monastic remains.",
     ["Buddhist heritage", "Religious & archaeology", "Culture & heritage", "Archaeology & ancient civilizations"],
     ["Butkara-I Stupa and monastic remains", "Shingardar Stupa near Barikot", "Amluk Dara Stupa", "Saidu Sharif archaeological and museum context", "Udegram heritage landscape"],
     "Butkara Stupa Swat Buddhist archaeology Pakistan",
     "Swat preserves significant Buddhist archaeological remains associated with the Gandharan cultural sphere. Site condition and visitor access vary; consult official archaeology information and do not disturb protected remains.")
_add("Takht-i-Bahi & Sahr-i-Bahlol", "Khyber Pakhtunkhwa", 34.3350, 71.9430,
     "A UNESCO World Heritage monastic complex in the Gandhara region.",
     ["Buddhist heritage", "Religious & archaeology", "Culture & heritage", "Archaeology & ancient civilizations"],
     ["Main stupa court and votive stupas", "Monastic quadrangle and meditation cells", "Neighbouring fortified settlement of Sahr-i-Bahlol"],
     "Takht i Bahi Buddhist monastery Pakistan",
     "Takht-i-Bahi is an extensive Buddhist monastic complex with associated remains at Sahr-i-Bahlol. It is a protected heritage property; follow conservation and visitor rules.")
_add("Katas Raj Temples & Salt Range", "Punjab", 32.7167, 72.9990,
     "A historic Hindu temple complex around a sacred pond in the Salt Range.",
     ["Hindu heritage", "Religious & archaeology", "Culture & heritage"],
     ["Katas Raj temple complex", "Shiva, Hanuman and Ramachandra temple precincts", "Historic pond and surrounding Salt Range landscape"],
     "Katas Raj Temples Chakwal Pakistan",
     "Katas Raj is a significant Hindu heritage and pilgrimage complex. Respect active religious use, conservation requirements and local protocols.")
_add("Hinglaj Mata & Hingol", "Balochistan", 25.5010, 65.5140,
     "A Hindu pilgrimage landscape within the dramatic terrain of Hingol.",
     ["Hindu heritage", "Religious & archaeology", "Coastal & marine", "Nature & wildlife"],
     ["Hinglaj Mata temple and pilgrimage landscape", "Hingol National Park scenery", "Makran coastal and desert geology"],
     "Hinglaj Mata temple Hingol Balochistan Pakistan",
     "Hinglaj Mata is a major Hindu pilgrimage destination in a remote landscape. Travel requires current route, security, weather and local-organiser checks.")
_add("Harappa & Indus Valley Archaeology", "Punjab", 30.6315, 72.8674,
     "An archaeological landscape associated with the Indus Valley Civilization.",
     ["Archaeology & ancient civilizations", "Religious & archaeology", "Culture & heritage"],
     ["Harappa archaeological mound", "Harappa Museum", "Urban planning, craft and trade history of the Indus Valley Civilization"],
     "Harappa archaeological site museum Pakistan",
     "Harappa is a major archaeological site associated with the Indus Valley Civilization. Interpret it through archaeological evidence rather than assigning it to a modern religious tradition.")
_add("Desan Meadows & Upper Kalam", "Khyber Pakhtunkhwa", 35.5000, 72.5800,
     "A high meadow above Kalam with expansive views across upper Swat.",
     ["Nature & wildlife", "Adventure", "Camping & outdoors", "Ecotourism"],
     ["Desan Meadows, also referred to by some travel creators as Desan Top", "Upper Kalam mountain viewpoints", "Locally guided walking and meadow experiences"],
     "Desan Meadows Desan Top Kalam Swat Pakistan",
     "Travel coverage describes Desan Meadows as a mountainside destination above Kalam. Track conditions, access, exact route and the use of the name Desan Top require local confirmation.")
_add("Utror & Gabral Valleys", "Khyber Pakhtunkhwa", 35.5450, 72.4900,
     "Quieter upper-Swat valleys beyond Kalam, shaped by rivers and forested slopes.",
     ["Nature & wildlife", "Adventure", "Camping & outdoors", "Ecotourism", "Rural & creative"],
     ["Utror village and valley", "Gabral Valley and river landscapes", "Kundol Lake approach via locally guided routes"],
     "Utror Gabral Valley Kalam Swat Pakistan",
     "Utror and Gabral are upper-Swat valley destinations reached beyond Kalam. Road surfaces and access vary; confirm local conditions and use experienced local operators.")
_add("Matiltan & Mahodand Lake", "Khyber Pakhtunkhwa", 35.5000, 72.6400,
     "A forest-and-lake corridor in the upper Ushu Valley.",
     ["Nature & wildlife", "Adventure", "Camping & outdoors", "Ecotourism"],
     ["Matiltan valley landscapes", "Mahodand Lake", "Ushu Forest corridor", "Mountain viewpoints and seasonal outdoor activities"],
     "Matiltan Mahodand Lake Kalam Swat Pakistan",
     "The route beyond Kalam leads through Ushu and Matiltan toward Mahodand Lake. Terrain and seasonal conditions can make a local 4x4 and experienced driver necessary; verify before travel.")

if "Lahore" in DESTINATIONS:
    DESTINATIONS["Lahore"]["experiences"] = list(dict.fromkeys(DESTINATIONS["Lahore"]["experiences"] + ["Islamic & Sufi heritage", "Sikh pilgrimage"]))
    DESTINATIONS["Lahore"]["highlights"] += ["Wazir Khan Mosque and Data Darbar", "Gurdwara Dera Sahib and Samadhi of Ranjit Singh"]
for _name in ("Taxila", "Swat Valley"):
    if _name in DESTINATIONS:
        DESTINATIONS[_name]["experiences"] = list(dict.fromkeys(DESTINATIONS[_name]["experiences"] + ["Buddhist heritage", "Archaeology & ancient civilizations"]))
if "Swat Valley" in DESTINATIONS:
    DESTINATIONS["Swat Valley"]["highlights"] += ["Butkara-I, Shingardar and Amluk Dara Buddhist archaeological sites"]
if "Multan" in DESTINATIONS:
    DESTINATIONS["Multan"]["experiences"] = list(dict.fromkeys(DESTINATIONS["Multan"]["experiences"] + ["Islamic & Sufi heritage"]))
if "Uch Sharif & Bahawalpur Heritage" in DESTINATIONS:
    DESTINATIONS["Uch Sharif & Bahawalpur Heritage"]["experiences"] = list(dict.fromkeys(DESTINATIONS["Uch Sharif & Bahawalpur Heritage"]["experiences"] + ["Islamic & Sufi heritage"]))

_SOURCE_LINKS = {
"Nankana Sahib & Sikh Heritage":[{"label":"Punjab Government — Religious Monuments","url":"https://punjab.gov.pk/religious-monuments","type":"Official"},{"label":"TDCP — Punjab, the Land of Sacred Gurus","url":"https://webapi.tdcp.gop.pk/uploads/1769507590777-461675896.pdf","type":"Official"}],
"Kartarpur Sahib & Narowal":[{"label":"Ministry of Religious Affairs — Kartarpur Corridor","url":"https://www.mora.gov.pk/","type":"Official"}],
"Hasan Abdal & Panja Sahib":[{"label":"Punjab Government — Religious Monuments","url":"https://punjab.gov.pk/religious-monuments","type":"Official"}],
"Swat Buddhist Heritage Circuit":[{"label":"DOAM — Butkara-I","url":"https://doam.gov.pk/public/sites/3304","type":"Official archaeology record"},{"label":"DOAM — Shingardar Stupa","url":"https://doam.gov.pk/public/sites/3323","type":"Official archaeology record"},{"label":"DOAM — Amluk Dara Stupa","url":"https://doam.gov.pk/public/sites/3298","type":"Official archaeology record"},{"label":"Government of Pakistan — Swat travel booklet","url":"https://tourism.gov.pk/publications/Swat%20Booklet.pdf","type":"Official publication"}],
"Takht-i-Bahi & Sahr-i-Bahlol":[{"label":"DOAM — Takht-i-Bahi World Heritage Site","url":"https://doam.gov.pk/public/world-heritage-sites/23","type":"Official heritage record"}],
"Katas Raj Temples & Salt Range":[{"label":"Punjab Government — Archaeological Sites","url":"https://punjab.gov.pk/archeological-sites","type":"Official"},{"label":"DOAM — Heritage of Pakistan","url":"https://doam.gov.pk/public/heritage-sites","type":"Official heritage inventory"}],
"Hinglaj Mata & Hingol":[{"label":"DOAM — Heritage of Pakistan","url":"https://doam.gov.pk/public/heritage-sites","type":"Official heritage inventory"}],
"Harappa & Indus Valley Archaeology":[{"label":"Punjab Government — Archaeological Sites","url":"https://punjab.gov.pk/archeological-sites","type":"Official"},{"label":"DOAM — Heritage of Pakistan","url":"https://doam.gov.pk/public/heritage-sites","type":"Official heritage inventory"}],
"Desan Meadows & Upper Kalam":[{"label":"Explore Pakistan — Places to Visit in Kalam","url":"https://explorepakistan.live/destinations/guides/places-to-visit-in-kalam","type":"Travel editorial"},{"label":"My Travelogues — Desan Top video (2022)","url":"https://www.youtube.com/watch?v=AqdMW9pxPTo","type":"Creator video; route details need rechecking"},{"label":"Discover Swat — Kalam to Gabral guide","url":"https://discoverswat.com/blog/kalam-to-gabral-scenic-drive-guide/","type":"Travel editorial"}],
"Utror & Gabral Valleys":[{"label":"Explore Pakistan — Places to Visit in Swat","url":"https://explorepakistan.live/destinations/guides/places-to-visit-in-swat","type":"Travel editorial"},{"label":"Discover Swat — Kalam to Gabral guide","url":"https://discoverswat.com/blog/kalam-to-gabral-scenic-drive-guide/","type":"Travel editorial"}],
"Matiltan & Mahodand Lake":[{"label":"Explore Pakistan — Places to Visit in Kalam","url":"https://explorepakistan.live/destinations/guides/places-to-visit-in-kalam","type":"Travel editorial"},{"label":"Government of Pakistan — Swat travel booklet","url":"https://tourism.gov.pk/publications/Swat%20Booklet.pdf","type":"Official publication"}]
}
for _name, _sources in _SOURCE_LINKS.items():
    if _name in DESTINATIONS:
        DESTINATIONS[_name]["sources"] = _sources
