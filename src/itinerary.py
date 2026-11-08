"""Deterministic itinerary structure and print-ready PDF export."""
from __future__ import annotations

from io import BytesIO
from urllib.parse import quote_plus

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
import qrcode

FOOD_GUIDE = {
    "Hunza Valley": {
        "breakfast": "Hunza bread (ghilmindi) with apricot jam; local tea",
        "lunch": "Chapshuro, a regional meat-filled pastry",
        "dinner": "Mamtu dumplings with seasonal vegetables",
        "snack": "Dried apricots, walnuts and local fruit",
    },
    "Skardu": {
        "breakfast": "Balti khambir bread with butter tea",
        "lunch": "Balti-style pulao or locally prepared trout where available",
        "dinner": "Mamtu or locally prepared Balti stew",
        "snack": "Apricots and local nuts",
    },
    "Lahore": {
        "breakfast": "Halwa puri or channay from a reputable local breakfast shop",
        "lunch": "Chicken or beef karahi with fresh naan",
        "dinner": "Walled City food-street specialities; choose a hygienic, busy vendor",
        "snack": "Falooda or seasonal street-side fruit from a clean outlet",
    },
    "Islamabad & Margalla Hills": {
        "breakfast": "Nihari or paratha with chai at a well-reviewed local restaurant",
        "lunch": "Chapli kebab or a seasonal Pakistani thali",
        "dinner": "Traditional barbecue and daal with fresh roti",
        "snack": "Pakistani chai and bakery snacks",
    },
    "Multan": {
        "breakfast": "Sohan halwa tasting with a light local breakfast",
        "lunch": "Multani sajji or regional pulao",
        "dinner": "Traditional mutton or chicken curry with naan",
        "snack": "Sohan halwa from an established producer",
    },
    "default": {
        "breakfast": "Local paratha, eggs and chai from a clean, established café",
        "lunch": "A regional rice or bread-based speciality recommended by a local host",
        "dinner": "Seasonal regional curry, vegetables and fresh roti",
        "snack": "Seasonal fruit, nuts or a locally made snack",
    },
}

SLOT_TITLES = {
    "Morning": "08:00–11:30",
    "Afternoon": "12:00–16:30",
    "Evening": "17:00–20:30",
}


def build_itinerary(destination: str, highlights: list[str], days: int, pace: str) -> list[dict]:
    """Create morning/afternoon/evening slots without implying verified travel times."""
    capacity = {"Relaxed": 1, "Balanced": 2, "Full days": 3}[pace]
    slots = ["Morning", "Afternoon", "Evening"]
    food = FOOD_GUIDE.get(destination, FOOD_GUIDE["default"])
    result, cursor = [], 0
    for day in range(1, days + 1):
        activities = {}
        for slot in slots:
            if slot == "Evening" and pace == "Relaxed":
                activity = "Unstructured time, sunset viewpoint or a short local cultural experience"
            elif cursor < len(highlights) and (slot != "Evening" or capacity == 3):
                activity = highlights[cursor]
                cursor += 1
            else:
                activity = "Flexible time: rest, explore locally or confirm a community-led activity"
            activities[slot] = {
                "time": SLOT_TITLES[slot],
                "activity": activity,
                "food": food[{"Morning": "breakfast", "Afternoon": "lunch", "Evening": "dinner"}[slot]],
            }
        result.append({"day": day, "title": f"Day {day}: {destination}", "slots": activities,
                       "snack": food["snack"]})
    return result


def build_itinerary_pdf(destination: str, itinerary: list[dict], travellers: int,
                        budget_pkr: float, interests: list[str]) -> bytes:
    """Build A4 itinerary with per-day QR links to destination map search."""
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4, rightMargin=17*mm, leftMargin=17*mm,
                            topMargin=16*mm, bottomMargin=16*mm,
                            title=f"VoyagePK itinerary — {destination}")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="VoyageTitle", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=24, leading=28, textColor=colors.HexColor("#263746"),
                              alignment=TA_CENTER, spaceAfter=5*mm))
    styles.add(ParagraphStyle(name="VoyageSub", parent=styles["Normal"], fontSize=9,
                              textColor=colors.HexColor("#536675"), alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="DayHead", parent=styles["Heading2"], fontSize=15,
                              textColor=colors.HexColor("#2A7778"), spaceBefore=4*mm))
    styles.add(ParagraphStyle(name="Slot", parent=styles["Normal"], fontSize=9, leading=13,
                              textColor=colors.HexColor("#263746")))
    story = [
        Paragraph("VOYAGEPK", styles["VoyageSub"]),
        Paragraph("Pakistan Unbound", styles["VoyageTitle"]),
        Paragraph(f"{destination} · {len(itinerary)} days · {travellers} traveller(s)", styles["VoyageSub"]),
        Paragraph(f"Planning budget: PKR {budget_pkr:,.0f} · Interests: {', '.join(interests) if interests else 'Open discovery'}", styles["VoyageSub"]),
        Spacer(1, 8*mm),
        Paragraph("YOUR JOURNEY", styles["Heading1"]),
        Paragraph("A planning draft, not a verified route or booking. Confirm access, opening hours, weather, permits and provider details before departure.", styles["BodyText"]),
        Spacer(1, 3*mm),
    ]
    for day in itinerary:
        qr_url = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(destination)
        qr = qrcode.QRCode(box_size=3, border=1)
        qr.add_data(qr_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="#263746", back_color="white")
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        from reportlab.platypus import Image as RLImage
        rows = [[Paragraph(f"DAY {day['day']:02d} — {destination}", styles["DayHead"]), RLImage(qr_buffer, width=22*mm, height=22*mm)]]
        for slot, detail in day["slots"].items():
            rows.append([Paragraph(
                f"<b>{slot} · {detail['time']}</b><br/>{detail['activity']}<br/><font color='#2A7778'>Food:</font> {detail['food']}",
                styles["Slot"]), ""])
        rows.append([Paragraph(f"<i>Local snack idea: {day['snack']}</i>", styles["Slot"]), ""])
        table = Table(rows, colWidths=[150*mm, 25*mm])
        table.setStyle(TableStyle([
            ("SPAN", (1, 1), (1, len(rows)-1)),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF3F1")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5DFDA")),
            ("INNERGRID", (0, 1), (0, -1), 0.25, colors.HexColor("#E5E9E6")),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.extend([KeepTogether([table]), Spacer(1, 4*mm)])
    story.extend([
        Spacer(1, 4*mm),
        Paragraph("TRAVEL RESPONSIBLY", styles["Heading2"]),
        Paragraph("Respect local customs and protected areas. Seek consent before photographing people. Choose local guides and businesses where appropriate. Verify road, weather and safety conditions with local authorities.", styles["BodyText"]),
        Paragraph("VoyagePK is an independent travel-planning prototype and is not an official government service.", styles["Italic"]),
    ])
    doc.build(story)
    return output.getvalue()
