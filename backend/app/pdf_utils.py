from io import BytesIO
import os
import csv

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_patient_pdf(patient):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

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

    # Add CSV as table if available
    if patient.zoll_csv_filename:
        csv_path = os.path.join("zoll_uploads", patient.zoll_csv_filename)
        if os.path.exists(csv_path):
            try:
                with open(csv_path, newline="") as csvfile:
                    reader = csv.reader(csvfile)
                    data = list(reader)

                if data:
                    elements.append(Paragraph("Zoll Data (CSV Table)", styles['Heading2']))

                    usable_width = 500
                    num_cols = len(data[0])
                    col_width = usable_width / num_cols if num_cols else 60

                    table = Table(data, colWidths=[col_width] * num_cols, repeatRows=1)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                        ('FONTSIZE', (0, 0), (-1, -1), 6),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ]))
                    elements.append(table)
            except Exception as e:
                elements.append(Paragraph(f"[Error rendering CSV table: {str(e)}]", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer
