from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os
import csv

LOGO_PATH = "static/logo.png"
UPLOAD_FOLDER = "zoll_uploads"

def clean(val):
    if not val or val.strip() == "---":
        return "N/A"
    return val.replace("[", "").replace("]", "").strip()

def parse_csv_to_table(csv_path):
    table_data = [["Heure", "Fréquence cardiaque", "SpO₂", "TA (Sys/Dia)"]]

    try:
        with open(csv_path, encoding="ISO-8859-1") as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                heure = clean(row.get("Heure (HH:MM)", ""))
                fc = clean(row.get("FC/FP (BPM)", ""))
                spo2 = clean(row.get("SpO2 (%)", ""))
                sys = clean(row.get("PNI (mm Hg) (Sys)", ""))
                dia = clean(row.get("PNI (mm Hg) (Dia)", ""))
                ta = f"{sys}/{dia}" if sys != "N/A" and dia != "N/A" else "N/A"

                if any(val != "N/A" for val in [fc, spo2, ta]):
                    table_data.append([heure, fc, spo2, ta])
    except Exception as e:
        table_data.append([f"Erreur : {str(e)}", "", "", ""])

    return table_data

def generate_pdf(output_path, patient_name, transport_date, csv_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    # Logo
    if os.path.exists(LOGO_PATH):
        elements.append(Image(LOGO_PATH, width=150, height=60))
        elements.append(Spacer(1, 12))

    # En-tête
    elements.append(Paragraph("<b>Résumé de transport pédiatrique</b>", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Nom du patient : {patient_name}", normal))

    if isinstance(transport_date, str):
        try:
            transport_date = datetime.strptime(transport_date, "%Y-%m-%d")
        except:
            transport_date = datetime.today()
    elements.append(Paragraph(f"Date du transport : {transport_date.strftime('%d/%m/%Y')}", normal))
    elements.append(Spacer(1, 12))

    # Données cliniques
    table_data = parse_csv_to_table(csv_path)
    table = Table(table_data, colWidths=[80, 130, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
    ]))

    elements.append(Paragraph("Signes vitaux extraits du moniteur :", styles["Heading2"]))
    elements.append(table)

    doc.build(elements)
