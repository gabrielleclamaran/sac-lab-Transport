import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const hospitalOptions = ["CHU Sainte-Justine", "CHUL", "CHUS", "HME", "Autre"];
const transportOptions = ["01-MCH", "02-HSJ", "03-CHUS", "04-CHUL", "05-Centre référant", "06-EVAQ", "07-Autre"];
const diagnosisOptions = ["Trauma crânien", "Sepsis", "Crise épileptique", "Insuffisance respiratoire", "Autre"];

export default function PatientForm({ refresh }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEditMode = Boolean(id);

  const [form, setForm] = useState({
    name: "", age: "", sex: "Male", weight_kg: "",
    transfer_call_date: "", transfer_call_time: "",
    referring_hospital: "", other_details: "", transporting_hospital: "",
    transfer_reason: "", transfer_reason_other: "",
    transport_team_diagnosis: "", secondary_diagnosis: "",
    transport_team_other: "", comorbidities: "",
    heart_rate: "", respiratory_rate: "", saturation: "", fio2: "",
    blood_pressure: "", temperature: "", glasgow_score: "",
    departure_heart_rate: "", departure_respiratory_rate: "", departure_saturation: "", departure_fio2: "",
    departure_blood_pressure: "", departure_temperature: "", departure_glasgow_score: "",
    notes: ""
  });

  const [csvFile, setCsvFile] = useState(null);

  useEffect(() => {
    if (isEditMode) {
      axios.get(`http://localhost:5050/patients`)
        .then((res) => {
          const patient = res.data.find(p => p.id === parseInt(id));
          if (patient) {
            setForm({ ...patient, notes: patient.notes ?? "" });
          } else {
            alert("Patient introuvable");
            navigate("/update");
          }
        });
    }
  }, [id]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  const handleFileChange = (e) => setCsvFile(e.target.files[0]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    Object.entries(form).forEach(([key, val]) => formData.append(key, val ?? ""));
    if (csvFile) formData.append("zoll_csv", csvFile);

    try {
      if (isEditMode) {
        await axios.put(`http://localhost:5050/patients/${id}`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        alert("Patient mis à jour");
      } else {
        await axios.post("http://localhost:5050/patients", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        alert("Patient ajouté");
      }
      refresh();
      navigate("/list");
    } catch (err) {
      console.error("Erreur lors de l'envoi du formulaire:", err);
    }
  };

  return (
    <div style={cardContainer}>
      <form 
        onSubmit={handleSubmit} 
        style={{ display: "flex", flexDirection: "column", gap: "20px" }}
      >
        <fieldset style={fieldsetStyle}>
          <legend style={legendStyle}>Identification</legend>
          <div style={rowStyle}>
            <input name="name" value={form.name} onChange={handleChange} placeholder="Nom du patient" required />
            <input name="age" type="number" value={form.age} onChange={handleChange} placeholder="Âge" required />
            <select name="sex" value={form.sex} onChange={handleChange}>
              <option>Male</option><option>Female</option><option>Other</option>
            </select>
            <input name="weight_kg" type="number" step="0.1" value={form.weight_kg} onChange={handleChange} placeholder="Poids (kg)" />
          </div>
        </fieldset>

        <fieldset style={fieldsetStyle}>
          <legend style={legendStyle}>Transport</legend>
          <div style={rowStyle}>
            <input name="transfer_call_date" type="date" value={form.transfer_call_date} onChange={handleChange} />
            <input name="transfer_call_time" type="time" value={form.transfer_call_time} onChange={handleChange} />
            <select name="referring_hospital" value={form.referring_hospital} onChange={handleChange}>
              <option value="">-- CH référent --</option>
              {hospitalOptions.map((h, i) => <option key={i} value={h}>{h}</option>)}
            </select>
            <input name="other_details" value={form.other_details} onChange={handleChange} placeholder="Autre (si précisé)" />
            <select name="transporting_hospital" value={form.transporting_hospital} onChange={handleChange}>
              <option value="">-- CH transporteur --</option>
              {transportOptions.map((t, i) => <option key={i} value={t}>{t}</option>)}
            </select>
          </div>
        </fieldset>

        <fieldset style={fieldsetStyle}>
          <legend style={legendStyle}>Diagnostic</legend>
          <div style={{ display: "flex", flexDirection: "column", gap: "10px", alignItems: "center" }}>
            <select name="transfer_reason" value={form.transfer_reason} onChange={handleChange}>
              <option value="">-- Diagnostic CH Référent --</option>
              {diagnosisOptions.map((d, i) => <option key={i} value={d}>{d}</option>)}
            </select>
            <input name="transfer_reason_other" value={form.transfer_reason_other} onChange={handleChange} placeholder="Si autre (référent)" />
            <select name="transport_team_diagnosis" value={form.transport_team_diagnosis} onChange={handleChange}>
              <option value="">-- Diagnostic Transport --</option>
              {diagnosisOptions.map((d, i) => <option key={i} value={d}>{d}</option>)}
            </select>
            <select name="secondary_diagnosis" value={form.secondary_diagnosis} onChange={handleChange}>
              <option value="">-- Diagnostic Secondaire --</option>
              {diagnosisOptions.map((d, i) => <option key={i} value={d}>{d}</option>)}
            </select>
            <input name="transport_team_other" value={form.transport_team_other} onChange={handleChange} placeholder="Si autre (transport)" />
            <textarea name="comorbidities" value={form.comorbidities} onChange={handleChange} placeholder="Co-morbidités" />
          </div>
        </fieldset>

        <div style={{ display: "flex", gap: "20px", flexWrap: "wrap", justifyContent: "space-between" }}>
          <fieldset style={{ ...fieldsetStyle, flex: "1 1 45%" }}>
            <legend style={legendStyle}>Signes vitaux à l'arrivée</legend>
            <div style={columnStyle}>
              <input name="heart_rate" value={form.heart_rate} onChange={handleChange} placeholder="Fréquence cardiaque" />
              <input name="respiratory_rate" value={form.respiratory_rate} onChange={handleChange} placeholder="Rythme respiratoire" />
              <input name="saturation" value={form.saturation} onChange={handleChange} placeholder="Saturation" />
              <input name="fio2" value={form.fio2} onChange={handleChange} placeholder="FiO2" />
              <input name="blood_pressure" value={form.blood_pressure} onChange={handleChange} placeholder="Tension artérielle" />
              <input name="temperature" value={form.temperature} onChange={handleChange} placeholder="Température" />
              <input name="glasgow_score" value={form.glasgow_score} onChange={handleChange} placeholder="Score de Glasgow" />
            </div>
          </fieldset>

          <fieldset style={{ ...fieldsetStyle, flex: "1 1 45%" }}>
            <legend style={legendStyle}>Signes vitaux au départ</legend>
            <div style={columnStyle}>
              <input name="departure_heart_rate" value={form.departure_heart_rate} onChange={handleChange} placeholder="Fréquence cardiaque" />
              <input name="departure_respiratory_rate" value={form.departure_respiratory_rate} onChange={handleChange} placeholder="Rythme respiratoire" />
              <input name="departure_saturation" value={form.departure_saturation} onChange={handleChange} placeholder="Saturation" />
              <input name="departure_fio2" value={form.departure_fio2} onChange={handleChange} placeholder="FiO2" />
              <input name="departure_blood_pressure" value={form.departure_blood_pressure} onChange={handleChange} placeholder="Tension artérielle" />
              <input name="departure_temperature" value={form.departure_temperature} onChange={handleChange} placeholder="Température" />
              <input name="departure_glasgow_score" value={form.departure_glasgow_score} onChange={handleChange} placeholder="Score de Glasgow" />
            </div>
          </fieldset>
        </div>

        <fieldset style={fieldsetStyle}>
          <legend style={legendStyle}>Notes</legend>
          <textarea
            name="notes"
            value={form.notes}
            onChange={handleChange}
            placeholder="Observations, interventions, remarques"
            rows={6}
            style={{ width: "100%", padding: "10px" }}
          />
        </fieldset>

        <fieldset style={fieldsetStyle}>
          <legend style={legendStyle}>Fichier Zoll (CSV)</legend>
          <input type="file" accept=".csv" onChange={handleFileChange} />
        </fieldset>

        <button 
          type="submit" 
          style={submitButtonStyle}
        >
          {isEditMode ? "Mettre à jour" : "Ajouter"}
        </button>
      </form>
    </div>
  );
}

/* === Styles === */
const cardContainer = {
  backgroundColor: "white",
  padding: "25px",
  borderRadius: "12px",
  boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
  margin: "0 auto",
  maxWidth: "1000px"
};

const fieldsetStyle = {
  border: "2px solid #083464",
  borderRadius: "12px",
  padding: "20px",
  backgroundColor: "#f9faff"
};

const legendStyle = {
  textAlign: "center",
  fontWeight: "bold",
  fontSize: "1.2rem",
  color: "#083464"
};

const rowStyle = {
  display: "flex",
  flexWrap: "wrap",
  gap: "10px",
  justifyContent: "center"
};

const columnStyle = {
  display: "flex",
  flexDirection: "column",
  gap: "10px"
};

const submitButtonStyle = {
  width: "220px",
  alignSelf: "center",
  marginTop: "20px",
  backgroundColor: "#083464",
  color: "white",
  border: "none",
  borderRadius: "8px",
  padding: "12px",
  fontSize: "16px",
  cursor: "pointer"
};
