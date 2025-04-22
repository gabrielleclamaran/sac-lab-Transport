from reportlab.pdfgen import canvas
from io import BytesIO

def generate_patient_pdf(patient):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Patient Information")
    y = 770

    c.setFont("Helvetica", 12)
    c.drawString(100, y, f"Name: {patient.name}"); y -= 20
    c.drawString(100, y, f"Age: {patient.age}"); y -= 20
    c.drawString(100, y, f"Sex: {patient.sex}"); y -= 20
    c.drawString(100, y, f"Weight (kg): {patient.weight_kg or 'N/A'}"); y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, "Transport"); y -= 25
    c.setFont("Helvetica", 12)
    c.drawString(100, y, f"Date: {patient.transfer_call_date} - Time: {patient.transfer_call_time}"); y -= 20
    c.drawString(100, y, f"Referring Hospital: {patient.referring_hospital}"); y -= 20
    c.drawString(100, y, f"Other: {patient.other_details}"); y -= 20
    c.drawString(100, y, f"Transporting Hospital: {patient.transporting_hospital}"); y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, "Diagnostic"); y -= 25
    c.setFont("Helvetica", 12)
    c.drawString(100, y, f"Reason (CH référent): {patient.transfer_reason}"); y -= 20
    c.drawString(100, y, f"Other (référent): {patient.transfer_reason_other}"); y -= 20
    c.drawString(100, y, f"Diagnostic transport: {patient.transport_team_diagnosis}"); y -= 20
    c.drawString(100, y, f"Secondary: {patient.secondary_diagnosis}"); y -= 20
    c.drawString(100, y, f"Other (transport): {patient.transport_team_other}"); y -= 20
    c.drawString(100, y, f"Comorbidities: {patient.comorbidities}"); y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, "Signes vitaux à l’arrivée au CH référent"); y -= 25
    c.setFont("Helvetica", 12)
    c.drawString(100, y, f"FC: {patient.heart_rate}, RR: {patient.respiratory_rate}, Sat: {patient.saturation}, FiO2: {patient.fio2}"); y -= 20
    c.drawString(100, y, f"TA: {patient.blood_pressure}, Température: {patient.temperature}, Glasgow: {patient.glasgow_score}"); y -= 20

    c.save()
    buffer.seek(0)
    return buffer