from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import matplotlib.pyplot as plt
import os
import csv

LOGO_PATH = "static/logo.png"
UPLOAD_FOLDER = "zoll_uploads"


def generate_bpm_chart_from_csv(filepath: str) -> BytesIO:
    timestamps = []
    bpms = []

    with open(filepath, encoding="ISO-8859-1") as f:
        next(f)
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 3:
                continue
            date_str, time_str, bpm_raw = parts[0], parts[1], parts[2]
            try:
                fr_months = {
                    "janv.": "Jan", "févr.": "Feb", "mars": "Mar", "avr.": "Apr",
                    "mai": "May", "juin": "Jun", "juil.": "Jul", "août": "Aug",
                    "sept.": "Sep", "oct.": "Oct", "nov.": "Nov", "déc.": "Dec"
                }
                for fr, en in fr_months.items():
                    date_str = date_str.replace(fr, en)
                ts = datetime.strptime(f"{date_str} {time_str}", "%d-%b-%y %H:%M")
                bpm = int("".join(filter(str.isdigit, bpm_raw)))
                timestamps.append(ts)
                bpms.append(bpm)
            except:
                continue

    if not timestamps:
        raise ValueError("No valid BPM data found")

    plt.figure(figsize=(10, 3))
    plt.plot(timestamps, bpms, marker="o", linestyle="-")
    plt.title("Heart Rate (BPM) Over Time")
    plt.xlabel("Time")
    plt.ylabel("BPM")
    plt.grid(True)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def generate_patient_pdf(patient):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    if os.path.exists(LOGO_PATH):
        elements.append(Image(LOGO_PATH, width=180, height=80))
        elements.append(Spacer(1, 20))

    # Patient info
    elements.append(Paragraph("Patient Information", styles['Heading1']))
    elements.append(Paragraph(f"Name: {patient.name}", styles['Normal']))
    elements.append(Paragraph(f"Age: {patient.age}", styles['Normal']))
    elements.append(Paragraph(f"Sex: {patient.sex}", styles['Normal']))
    elements.append(Paragraph(f"Weight (kg): {patient.weight_kg or 'N/A'}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Transport info
    elements.append(Paragraph("Transport", styles['Heading2']))
    elements.append(Paragraph(f"Date: {patient.transfer_call_date} - Time: {patient.transfer_call_time}", styles['Normal']))
    elements.append(Paragraph(f"Referring Hospital: {patient.referring_hospital}", styles['Normal']))
    elements.append(Paragraph(f"Other: {patient.other_details}", styles['Normal']))
    elements.append(Paragraph(f"Transporting Hospital: {patient.transporting_hospital}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Diagnostic
    elements.append(Paragraph("Diagnostic", styles['Heading2']))
    elements.append(Paragraph(f"Reason (CH référent): {patient.transfer_reason}", styles['Normal']))
    elements.append(Paragraph(f"Other (référent): {patient.transfer_reason_other}", styles['Normal']))
    elements.append(Paragraph(f"Diagnostic transport: {patient.transport_team_diagnosis}", styles['Normal']))
    elements.append(Paragraph(f"Secondary: {patient.secondary_diagnosis}", styles['Normal']))
    elements.append(Paragraph(f"Other (transport): {patient.transport_team_other}", styles['Normal']))
    elements.append(Paragraph(f"Comorbidities: {patient.comorbidities}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Vital signs
    elements.append(Paragraph("Signes vitaux à l’arrivée au CH référent", styles['Heading2']))
    elements.append(Paragraph(f"FC: {patient.heart_rate}, RR: {patient.respiratory_rate}, Sat: {patient.saturation}, FiO2: {patient.fio2}", styles['Normal']))
    elements.append(Paragraph(f"TA: {patient.blood_pressure}, Température: {patient.temperature}, Glasgow: {patient.glasgow_score}", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Signes vitaux au départ du CH référent", styles['Heading2']))
    elements.append(Paragraph(f"FC: {patient.departure_heart_rate}, RR: {patient.departure_respiratory_rate}, Sat: {patient.departure_saturation}, FiO2: {patient.departure_fio2}", styles['Normal']))
    elements.append(Paragraph(f"TA: {patient.departure_blood_pressure}, Température: {patient.departure_temperature}, Glasgow: {patient.departure_glasgow_score}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # CSV trend chart (BPM)
    if patient.zoll_csv_filename:
        chart_path = os.path.join(UPLOAD_FOLDER, patient.zoll_csv_filename)
        if os.path.exists(chart_path):
            try:
                elements.append(Paragraph("Heart Rate Trend (from CSV)", styles['Heading2']))
                chart = generate_bpm_chart_from_csv(chart_path)
                elements.append(Image(chart, width=480, height=150))
                elements.append(Spacer(1, 20))
            except Exception as e:
                elements.append(Paragraph(f"[Error generating chart: {str(e)}]", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer
