from . import db

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    weight_kg = db.Column(db.Float)

    transfer_call_date = db.Column(db.String(20))
    transfer_call_time = db.Column(db.String(20))
    referring_hospital = db.Column(db.String(100))
    other_details = db.Column(db.String(100))
    transporting_hospital = db.Column(db.String(100))

    transfer_reason = db.Column(db.String(200))
    transfer_reason_other = db.Column(db.String(200))
    transport_team_diagnosis = db.Column(db.String(200))
    secondary_diagnosis = db.Column(db.String(200))
    transport_team_other = db.Column(db.String(200))
    comorbidities = db.Column(db.String(200))

    heart_rate = db.Column(db.String(50))
    respiratory_rate = db.Column(db.String(50))
    saturation = db.Column(db.String(50))
    fio2 = db.Column(db.String(50))
    blood_pressure = db.Column(db.String(50))
    temperature = db.Column(db.String(50))
    glasgow_score = db.Column(db.String(50))

    departure_heart_rate = db.Column(db.String(50))
    departure_respiratory_rate = db.Column(db.String(50))
    departure_saturation = db.Column(db.String(50))
    departure_fio2 = db.Column(db.String(50))
    departure_blood_pressure = db.Column(db.String(50))
    departure_temperature = db.Column(db.String(50))
    departure_glasgow_score = db.Column(db.String(50))