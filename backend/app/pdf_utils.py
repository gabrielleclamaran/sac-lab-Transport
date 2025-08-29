from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader

from datetime import datetime
import csv
import os

# ---------- Styles ----------
_base = getSampleStyleSheet()
H1Blue = ParagraphStyle(
    name="H1Blue",
    parent=_base["Heading1"],
    textColor=colors.HexColor("#003366"),
    fontSize=14,
    leading=16,
    alignment=1,  # center
    spaceAfter=10,
)
H2Blue = ParagraphStyle(
    name="H2Blue",
    parent=_base["Heading2"],
    textColor=colors.HexColor("#003366"),
    fontSize=12,
    leading=14,
    spaceAfter=8,
)
NormalBold10 = ParagraphStyle(
    name="NormalBold10",
    parent=_base["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=12,
    spaceAfter=4,
)

# ---------- Config ----------
LOGO_PATH = "static/logo.png"  # optionnel
MARGIN_LR = 40
MARGIN_T = 80
MARGIN_B = 50

# ---------- Utils ----------
def clean(val):
    if val is None:
        return "N/A"
    s = str(val).strip()
    if s == "" or s == "---":
        return "N/A"
    return s.replace("[", "").replace("]", "").strip()

def _parse_hhmm(hhmm: str):
    try:
        parts = hhmm.strip().split(":")
        if len(parts) < 2:
            return None
        h = int(parts[0]); m = int(parts[1])
        if 0 <= h <= 23 and 0 <= m <= 59:
            return h, m
    except Exception:
        pass
    return None

def _sample_every_3_minutes(rows):
    """
    Garde 1 mesure toutes les 3 minutes (minute % 3 == 0). 
    Si plusieurs lignes pour la même minute, garde la dernière.
    """
    buckets = {}
    keys = set()
    for row in rows:
        hhmm = clean(row.get("Heure (HH:MM)", ""))
        parsed = _parse_hhmm(hhmm)
        if not parsed:
            continue
        h, m = parsed
        if m % 3 != 0:
            continue
        key = (h, m)
        buckets[key] = row    # garde la dernière vue
        keys.add(key)
    ordered = sorted(keys, key=lambda x: (x[0], x[1]))
    return [buckets[k] for k in ordered]

def _read_csv_resilient(csv_path):
    # Certains exports peuvent être UTF-8 ou ISO-8859-1
    for enc in ("utf-8", "ISO-8859-1"):
        try:
            with open(csv_path, encoding=enc) as f:
                return list(csv.DictReader(f, delimiter=","))
        except UnicodeDecodeError:
            continue
    # Dernier recours
    with open(csv_path, "rb") as f:
        data = f.read().decode("utf-8", errors="ignore")
    return list(csv.DictReader(data.splitlines(), delimiter=","))

def _draw_header_footer(c: canvas.Canvas, doc, patient_name: str):
    width, height = letter
    # Bandeau haut
    c.setFillColor(colors.HexColor("#003366"))
    c.rect(0, height - 50, width, 50, fill=True, stroke=False)

    # Titre (sans logo)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 30, f"Rapport de transport – {patient_name}")

    # Pied de page : numéro de page
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.black)
    c.drawRightString(width - 40, 30, f"Page {c.getPageNumber()}")

def _build_patient_info_block(patient, patient_name, transfer_date):
    elems = []
    elems.append(Paragraph("Informations Patient", H1Blue))
    if patient:
        elems.append(Paragraph(f"<b>Nom :</b> {clean(patient.name)}", _base["Normal"]))
        elems.append(Paragraph(f"<b>Âge :</b> {clean(patient.age)} ans", _base["Normal"]))
        elems.append(Paragraph(f"<b>Sexe :</b> {clean(patient.sex)}", _base["Normal"]))
        elems.append(Paragraph(f"<b>Poids :</b> {clean(patient.weight_kg)} kg", _base["Normal"]))
        elems.append(Paragraph(f"<b>CH Référent :</b> {clean(patient.referring_hospital)}", _base["Normal"]))
        elems.append(Paragraph(f"<b>CH Transporteur :</b> {clean(patient.transporting_hospital)}", _base["Normal"]))
        elems.append(Paragraph(f"<b>Date d'appel :</b> {clean(patient.transfer_call_date)}", _base["Normal"]))
    else:
        elems.append(Paragraph(f"<b>Nom :</b> {clean(patient_name)}", _base["Normal"]))
        elems.append(Paragraph(f"<b>Date de transfert :</b> {clean(transfer_date)}", _base["Normal"]))
    elems.append(Spacer(1, 12))
    return elems

# ---------- Main ----------
def generate_pdf(output_path, patient_name, transfer_date, csv_path, patient=None):
    """
    Génère le PDF de rapport patient.
    """
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        rightMargin=MARGIN_LR, leftMargin=MARGIN_LR,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B
    )

    elements = []

    # --- Logo (dans le corps du document, pas dans l'en-tête)
    if os.path.exists(LOGO_PATH):
        try:
            img = ImageReader(LOGO_PATH)
            iw, ih = img.getSize()
            target_w = 200  # largeur max
            target_h = 70   # hauteur max
            ratio = min(target_w / iw, target_h / ih)  # conserve le ratio
            final_w, final_h = iw * ratio, ih * ratio
            elements.append(Image(LOGO_PATH, width=final_w, height=final_h))
            elements.append(Spacer(1, 12))
        except Exception:
            pass

    # Bloc infos patient
    elements += _build_patient_info_block(patient, patient_name, transfer_date)

    # Lecture CSV + échantillonnage 1/3 min
    table_data = [["Heure", "Fréquence cardiaque", "SpO₂", "TA (Sys/Dia)"]]
    if not os.path.exists(csv_path):
        elements.append(Paragraph(f"⚠️ Fichier ZOLL introuvable : {csv_path}", _base["Normal"]))
    else:
        reader_rows = _read_csv_resilient(csv_path)
        sampled = _sample_every_3_minutes(reader_rows)
        for row in sampled:
            heure = clean(row.get("Heure (HH:MM)", ""))
            fc = clean(row.get("FC/FP (BPM)", ""))
            spo2 = clean(row.get("SpO2 (%)", ""))
            sys_ = clean(row.get("PNI (mm Hg) (Sys)", ""))
            dia_ = clean(row.get("PNI (mm Hg) (Dia)", ""))
            ta = f"{sys_}/{dia_}" if sys_ != "N/A" and dia_ != "N/A" else "N/A"
            if any(v != "N/A" for v in (fc, spo2, ta)):
                table_data.append([heure, fc, spo2, ta])

        elements.append(Paragraph("Signes vitaux extraits du moniteur (1 mesure / 3 min)", H2Blue))
        if len(table_data) == 1:
            elements.append(Paragraph("Aucune mesure disponible après échantillonnage.", _base["Normal"]))
        else:
            table = Table(table_data, colWidths=[90, 150, 100, 160], repeatRows=1)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6F0FF")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("TOPPADDING", (0, 0), (-1, 0), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
            ]))
            elements.append(table)
        elements.append(Spacer(1, 16))

    # Notes du médecin (si disponibles)
    if patient and getattr(patient, "notes", None):
        elements.append(Paragraph("Notes du médecin", H2Blue))
        elements.append(Paragraph(clean(patient.notes), _base["Normal"]))
        elements.append(Spacer(1, 12))

    # Build avec en-tête/pied de page
    doc.build(
        elements,
        onFirstPage=lambda c, d: _draw_header_footer(c, d, patient_name),
        onLaterPages=lambda c, d: _draw_header_footer(c, d, patient_name),
    )
