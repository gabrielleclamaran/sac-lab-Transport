from flask import Blueprint, request, jsonify, send_file
from .models import Patient
from . import db
from .pdf_utils import generate_pdf
from werkzeug.utils import secure_filename
from datetime import datetime
import os

bp = Blueprint("api", __name__)
UPLOAD_FOLDER = "zoll_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bp.route("/patients", methods=["GET"])
def get_patients():
    patients = Patient.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "sex": p.sex,
            "weight_kg": p.weight_kg,
            "transfer_call_date": p.transfer_call_date,
            "transfer_call_time": p.transfer_call_time,
            "referring_hospital": p.referring_hospital,
            "other_details": p.other_details,
            "transporting_hospital": p.transporting_hospital,
            "transfer_reason": p.transfer_reason,
            "transfer_reason_other": p.transfer_reason_other,
            "transport_team_diagnosis": p.transport_team_diagnosis,
            "secondary_diagnosis": p.secondary_diagnosis,
            "transport_team_other": p.transport_team_other,
            "comorbidities": p.comorbidities,
            "heart_rate": p.heart_rate,
            "respiratory_rate": p.respiratory_rate,
            "saturation": p.saturation,
            "fio2": p.fio2,
            "blood_pressure": p.blood_pressure,
            "temperature": p.temperature,
            "glasgow_score": p.glasgow_score,
            "departure_heart_rate": p.departure_heart_rate,
            "departure_respiratory_rate": p.departure_respiratory_rate,
            "departure_saturation": p.departure_saturation,
            "departure_fio2": p.departure_fio2,
            "departure_blood_pressure": p.departure_blood_pressure,
            "departure_temperature": p.departure_temperature,
            "departure_glasgow_score": p.departure_glasgow_score,
            "zoll_csv_filename": p.zoll_csv_filename
        } for p in patients
    ])

@bp.route("/patients", methods=["POST"])
def create_patient():
    if request.content_type.startswith("multipart/form-data"):
        data = request.form.to_dict()
        file = request.files.get("zoll_csv")
        filename = None
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
    else:
        data = request.json
        filename = None

    new_patient = Patient(
        name=data["name"],
        age=int(data["age"]),
        sex=data["sex"],
        weight_kg=float(data.get("weight_kg") or 0),
        transfer_call_date=data.get("transfer_call_date"),
        transfer_call_time=data.get("transfer_call_time"),
        referring_hospital=data.get("referring_hospital"),
        other_details=data.get("other_details"),
        transporting_hospital=data.get("transporting_hospital"),
        transfer_reason=data.get("transfer_reason"),
        transfer_reason_other=data.get("transfer_reason_other"),
        transport_team_diagnosis=data.get("transport_team_diagnosis"),
        secondary_diagnosis=data.get("secondary_diagnosis"),
        transport_team_other=data.get("transport_team_other"),
        comorbidities=data.get("comorbidities"),
        heart_rate=data.get("heart_rate"),
        respiratory_rate=data.get("respiratory_rate"),
        saturation=data.get("saturation"),
        fio2=data.get("fio2"),
        blood_pressure=data.get("blood_pressure"),
        temperature=data.get("temperature"),
        glasgow_score=data.get("glasgow_score"),
        departure_heart_rate=data.get("departure_heart_rate"),
        departure_respiratory_rate=data.get("departure_respiratory_rate"),
        departure_saturation=data.get("departure_saturation"),
        departure_fio2=data.get("departure_fio2"),
        departure_blood_pressure=data.get("departure_blood_pressure"),
        departure_temperature=data.get("departure_temperature"),
        departure_glasgow_score=data.get("departure_glasgow_score"),
        zoll_csv_filename=filename
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({ "message": "Patient created" }), 201

@bp.route("/patients/<int:id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({ "message": "Patient deleted" })

@bp.route("/patients/<int:id>/pdf", methods=["GET"])
def get_patient_pdf(id):
    patient = Patient.query.get_or_404(id)

    if not patient.zoll_csv_filename:
        return jsonify({"error": "Aucun fichier ZOLL associé à ce patient"}), 400

    csv_path = os.path.join(UPLOAD_FOLDER, patient.zoll_csv_filename.strip())

    if not os.path.exists(csv_path):
        return jsonify({"error": f"Fichier ZOLL introuvable à l'emplacement {csv_path}"}), 404

    output_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, f"rapport_patient_{id}.pdf"))
    generate_pdf(output_path, patient.name, patient.transfer_call_date or datetime.today(), csv_path)

    return send_file(
        output_path,
        as_attachment=True,
        download_name=f"rapport_patient_{id}.pdf",
        mimetype='application/pdf'
    )
