import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

export default function PatientView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [patient, setPatient] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:5050/patients")
      .then((res) => {
        const found = res.data.find((p) => p.id === parseInt(id));
        if (found) {
          setPatient(found);
        } else {
          alert("Patient introuvable");
          navigate("/list");
        }
      });
  }, [id]);

  if (!patient) return <p>Chargement...</p>;

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "30px", textAlign: "left" }}>
      <h2>Dossier du patient : {patient.name}</h2>

      <p><strong>ID :</strong> {patient.id}</p>
      <p><strong>Âge :</strong> {patient.age}</p>
      <p><strong>Sexe :</strong> {patient.sex}</p>
      <p><strong>Poids :</strong> {patient.weight_kg ?? "N/A"} kg</p>

      <h3>Transport</h3>
      <p><strong>Date :</strong> {patient.transfer_call_date}</p>
      <p><strong>Heure :</strong> {patient.transfer_call_time}</p>
      <p><strong>CH Référent :</strong> {patient.referring_hospital}</p>
      <p><strong>Autre :</strong> {patient.other_details}</p>
      <p><strong>CH Transporteur :</strong> {patient.transporting_hospital}</p>

      <h3>Diagnostic</h3>
      <p><strong>Diagnostic CH Référent :</strong> {patient.transfer_reason}</p>
      <p><strong>Autre (référent) :</strong> {patient.transfer_reason_other}</p>
      <p><strong>Diagnostic transport :</strong> {patient.transport_team_diagnosis}</p>
      <p><strong>Secondaire :</strong> {patient.secondary_diagnosis}</p>
      <p><strong>Autre (transport) :</strong> {patient.transport_team_other}</p>
      <p><strong>Co-morbidités :</strong> {patient.comorbidities}</p>

      <h3>Signes vitaux à l’arrivée</h3>
      <p>FC: {patient.heart_rate}, RR: {patient.respiratory_rate}, Sat: {patient.saturation}, FiO2: {patient.fio2}</p>
      <p>TA: {patient.blood_pressure}, Temp: {patient.temperature}, Glasgow: {patient.glasgow_score}</p>

      <h3>Signes vitaux au départ</h3>
      <p>FC: {patient.departure_heart_rate}, RR: {patient.departure_respiratory_rate}, Sat: {patient.departure_saturation}, FiO2: {patient.departure_fio2}</p>
      <p>TA: {patient.departure_blood_pressure}, Temp: {patient.departure_temperature}, Glasgow: {patient.departure_glasgow_score}</p>

      {patient.zoll_csv_filename && (
        <>
          <h3>Fichier Zoll</h3>
          <p><em>{patient.zoll_csv_filename}</em></p>
        </>
      )}

      <button onClick={() => navigate("/list")} style={{ marginTop: "20px" }}>Retour à la liste</button>
    </div>
  );
}
