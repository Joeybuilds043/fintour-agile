"""Owner-supplied destination photography grouped by research batch.

The image URLs are intentionally preserved verbatim. Source pages and reuse
licences were not supplied for every image, so the UI labels them accordingly.
"""

DESTINATION_IMAGE_BATCHES = {
    "Sindh · Batch 1": [
        {"destination": "Mohenjo Daro", "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/07/Mohenjo-daro_RV.jpg"},
        {"destination": "Mazar-e-Quaid, Karachi", "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/fe/Mazar-e-Quaid_Karachi.jpg"},
    ],
    "Punjab · Batch 2": [
        {"destination": "Badshahi Mosque, Lahore", "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/74/Badshahi_Mosque_July_1_2005_pic32_by_Ali_Imran.jpg"},
        {"destination": "Minar-e-Pakistan, Lahore", "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/44/Minar_e_Pakistan_Lahore.jpg"},
    ],
    "Cholistan & South Punjab · Batch 3": [
        {"destination": "Derawar Fort", "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Derawar_Fort_Cholistan_Desert_Bahawalpur.jpg"},
        {"destination": "Noor Mahal, Bahawalpur", "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/52/Noor_Mahal_Bahawalpur_Pakistan.jpg"},
    ],
    "Balochistan · Batch 4": [
        {"destination": "Hingol National Park (Princess of Hope)", "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/f7/Princess_of_hope_Balochistan.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original"},
        {"destination": "Astola Island", "image_url": "https://i.dawn.com/primary/2016/12/58651575af419.jpg"},
        {"destination": "Ziarat Residency", "image_url": "https://realpakistan.com.pk/wp-content/uploads/2025/08/Quaid-Residency-scaled-1920x1080.webp"},
    ],
    "Gilgit-Baltistan · Batch 5": [
        {"destination": "Concordia (K2 Base Camp)", "image_url": "https://trangoadventure.com/wp-content/uploads/2018/10/k2-8611-meters-scaled.jpeg"},
        {"destination": "Attabad Lake, Hunza", "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/52/Attabad.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original"},
        {"destination": "Khunjerab Pass", "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0a/China_Border%2C_Pakistan.jpg/1280px-China_Border%2C_Pakistan.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=thumbnail"},
        {"destination": "Deosai National Park", "image_url": "https://i.dawn.com/primary/2019/12/5df769a3a7d69.jpg"},
    ],
    "Azad Jammu & Kashmir · Batch 6": [
        {"destination": "Arang Kel", "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/40/Arang_Kel_Morning.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original"},
        {"destination": "Ratti Gali Lake", "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/30/Ratti_Gali_Lake_.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original"},
    ],
    "Islamabad Capital Territory · Batch 7": [
        {"destination": "Faisal Mosque", "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e0/Ali_Mujtaba_WLM2017_FAISAL_MOSQUE_019.jpg/1280px-Ali_Mujtaba_WLM2017_FAISAL_MOSQUE_019.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=thumbnail"},
        {"destination": "Pakistan Monument", "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/cf/Blue_Hour_at_Pakistan_Monument.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original"},
    ],
    "Khyber Pakhtunkhwa · Batch 8": [
        {"destination": "Malam Jabba Ski Resort, Swat", "image_url": "https://malamjabbaskiresort.com/wp-content/uploads/2025/11/PC-Hotel-Winter.webp"},
        {"destination": "Katora Lake, Kumrat Valley", "image_url": "https://upload.wikimedia.org/wikipedia/commons/1/10/Katora_lake_dir.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original"},
        {"destination": "Lake Saif-ul-Malook, Naran", "image_url": "https://www.pakistanhc.lk/wp-content/uploads/2018/10/Saif-ul-Malook-960x640.jpg"},
        {"destination": "Kalash Valley", "image_url": "https://vceela.com/web/image/product.template/26957/image_1024?unique=a6d92dd"},
    ],
}

def get_destination_gallery_image(query: str) -> dict | None:
    """Return an exact owner-supplied image when its destination is mentioned."""
    import re
    q = re.sub(r"[^a-z0-9]+", " ", (query or "").casefold()).strip()
    aliases = {
        "Mohenjo Daro": ("mohenjo", "moenjodaro"),
        "Mazar-e-Quaid, Karachi": ("mazar e quaid", "mazar quaid", "karachi mausoleum"),
        "Badshahi Mosque, Lahore": ("badshahi",),
        "Minar-e-Pakistan, Lahore": ("minar e pakistan", "minar pakistan"),
        "Derawar Fort": ("derawar",),
        "Noor Mahal, Bahawalpur": ("noor mahal",),
        "Hingol National Park (Princess of Hope)": ("princess of hope", "hingol"),
        "Astola Island": ("astola",),
        "Ziarat Residency": ("ziarat residency", "quaid residency"),
        "Concordia (K2 Base Camp)": ("concordia", "k2 base camp"),
        "Attabad Lake, Hunza": ("attabad",),
        "Khunjerab Pass": ("khunjerab",),
        "Deosai National Park": ("deosai",),
        "Arang Kel": ("arang kel",),
        "Ratti Gali Lake": ("ratti gali",),
        "Faisal Mosque": ("faisal mosque",),
        "Pakistan Monument": ("pakistan monument",),
        "Malam Jabba Ski Resort, Swat": ("malam jabba",),
        "Katora Lake, Kumrat Valley": ("katora lake",),
        "Lake Saif-ul-Malook, Naran": ("saif ul malook", "saif-ul-malook", "saif ul muluk"),
        "Kalash Valley": ("kalash",),
    }
    for batch, records in DESTINATION_IMAGE_BATCHES.items():
        for record in records:
            terms = aliases.get(record["destination"], ())
            if any(term in q for term in terms):
                return {
                    "title": record["destination"],
                    "thumb_url": record["image_url"],
                    "page_url": record["image_url"],
                    "artist": "User-supplied image URL",
                    "license": "Source and reuse licence not independently verified",
                    "provider": "User-supplied",
                }
    return None
