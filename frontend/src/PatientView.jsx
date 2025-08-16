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

  if (!patient) return <p style={{ textAlign: "center", color: "#083464" }}>Chargement...</p>;

  return (
    <div style={containerStyle}>
      <h2 style={titleStyle}>Dossier du patient : {patient.name}</h2>

      <Section title="Informations générales">
        <p><strong>ID :</strong> {patient.id}</p>
        <p><strong>Âge :</strong> {patient.age}</p>
        <p><strong>Sexe :</strong> {patient.sex}</p>
        <p><strong>Poids :</strong> {patient.weight_kg ?? "N/A"} kg</p>
      </Section>

      <Section title="Transport">
        <p><strong>Date :</strong> {patient.transfer_call_date}</p>
        <p><strong>Heure :</strong> {patient.transfer_call_time}</p>
        <p><strong>CH Référent :</strong> {patient.referring_hospital}</p>
        <p><strong>Autre :</strong> {patient.other_details}</p>
        <p><strong>CH Transporteur :</strong> {patient.transporting_hospital}</p>
      </Section>

      <Section title="Diagnostic">
        <p><strong>Diagnostic CH Référent :</strong> {patient.transfer_reason}</p>
        <p><strong>Autre (référent) :</strong> {patient.transfer_reason_other}</p>
        <p><strong>Diagnostic transport :</strong> {patient.transport_team_diagnosis}</p>
        <p><strong>Secondaire :</strong> {patient.secondary_diagnosis}</p>
        <p><strong>Autre (transport) :</strong> {patient.transport_team_other}</p>
        <p><strong>Co-morbidités :</strong> {patient.comorbidities}</p>
      </Section>

      <Section title="Signes vitaux à l’arrivée">
        <p>FC: {patient.heart_rate}, RR: {patient.respiratory_rate}, Sat: {patient.saturation}, FiO2: {patient.fio2}</p>
        <p>TA: {patient.blood_pressure}, Temp: {patient.temperature}, Glasgow: {patient.glasgow_score}</p>
      </Section>

      <Section title="Signes vitaux au départ">
        <p>FC: {patient.departure_heart_rate}, RR: {patient.departure_respiratory_rate}, Sat: {patient.departure_saturation}, FiO2: {patient.departure_fio2}</p>
        <p>TA: {patient.departure_blood_pressure}, Temp: {patient.departure_temperature}, Glasgow: {patient.departure_glasgow_score}</p>
      </Section>

      {patient.notes && patient.notes.trim() !== "" && (
        <Section title="Notes du médecin">
          <p style={{ whiteSpace: "pre-wrap" }}>{patient.notes}</p>
        </Section>
      )}

      {patient.zoll_csv_filename && (
        <Section title="Fichier Zoll">
          <p><em>{patient.zoll_csv_filename}</em></p>
        </Section>
      )}

      <div style={{ textAlign: "center", marginTop: "30px" }}>
        <button 
          onClick={() => navigate("/list")} 
          style={buttonStyle}
        >
          ← Retour à la liste
        </button>
      </div>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <fieldset style={sectionStyle}>
      <legend style={legendStyle}>{title}</legend>
      {children}
    </fieldset>
  );
}

/* === Styles === */
const containerStyle = {
  maxWidth: "900px",
  margin: "0 auto",
  padding: "30px",
  fontFamily: "Arial, sans-serif",
  backgroundColor: "white",
  borderRadius: "12px",
  boxShadow: "0 4px 12px rgba(0,0,0,0.1)"
};

const titleStyle = {
  color: "#083464",
  textAlign: "center",
  marginBottom: "25px"
};

const sectionStyle = {
  border: "2px solid #083464",
  borderRadius: "12px",
  padding: "15px 20px",
  marginBottom: "20px",
  backgroundColor: "#f9faff"
};

const legendStyle = {
  fontWeight: "bold",
  fontSize: "1.1rem",
  color: "#083464",
  padding: "0 8px"
};

const buttonStyle = {
  backgroundColor: "#083464",
  color: "white",
  border: "none",
  borderRadius: "8px",
  padding: "12px 20px",
  fontSize: "16px",
  cursor: "pointer"
};
