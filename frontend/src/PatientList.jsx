import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const hospitalOptions = ["CHU Sainte-Justine", "CHUL", "CHUS", "HME", "Autre"];
const diagnosisOptions = ["Trauma crânien", "Sepsis", "Crise épileptique", "Insuffisance respiratoire", "Autre"];

export default function PatientList({ refreshTrigger, mode, onDelete, onPrint }) {
  const [patients, setPatients] = useState([]);
  const [searchId, setSearchId] = useState("");
  const [searchHospital, setSearchHospital] = useState("");
  const [searchDiagnosis, setSearchDiagnosis] = useState("");
  const [searchDate, setSearchDate] = useState("");
  const [showFilters, setShowFilters] = useState(false);

  const navigate = useNavigate();

  const fetchPatients = async () => {
    const res = await axios.get("http://localhost:5050/patients");
    setPatients(res.data);
  };

  useEffect(() => {
    fetchPatients();
  }, [refreshTrigger]);

  const filteredPatients = patients.filter((p) => {
    return (
      (searchId === "" || p.id.toString() === searchId) &&
      (searchHospital === "" || p.referring_hospital === searchHospital) &&
      (searchDiagnosis === "" || p.transfer_reason === searchDiagnosis) &&
      (searchDate === "" || p.transfer_call_date === searchDate)
    );
  });

  return (
    <div style={containerStyle}>
      {mode === "list" && (
        <>
          <button
            onClick={() => setShowFilters(!showFilters)}
            style={filterButtonStyle}
          >
            🔍 Filtres
          </button>

          {showFilters && (
            <div style={filterBoxStyle}>
              <input
                type="text"
                placeholder="Rechercher par ID"
                value={searchId}
                onChange={(e) => setSearchId(e.target.value)}
                style={inputStyle}
              />

              <select value={searchHospital} onChange={(e) => setSearchHospital(e.target.value)} style={inputStyle}>
                <option value="">-- CH Référent --</option>
                {hospitalOptions.map((h, i) => <option key={i} value={h}>{h}</option>)}
              </select>

              <select value={searchDiagnosis} onChange={(e) => setSearchDiagnosis(e.target.value)} style={inputStyle}>
                <option value="">-- Diagnostic --</option>
                {diagnosisOptions.map((d, i) => <option key={i} value={d}>{d}</option>)}
              </select>

              <input
                type="date"
                value={searchDate}
                onChange={(e) => setSearchDate(e.target.value)}
                style={inputStyle}
              />
            </div>
          )}
        </>
      )}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {filteredPatients.map((p) => (
          <li key={p.id} style={cardStyle}>
            <strong style={{ fontSize: "18px", color: "#083464" }}>{p.name}</strong><br />
            <span>ID: {p.id}, Âge: {p.age}, Sexe: {p.sex}, Poids: {p.weight_kg ?? "N/A"} kg</span>

            <div style={buttonContainerStyle}>
              {mode === "list" && (
                <button onClick={() => navigate(`/view/${p.id}`)} style={actionButtonStyle}>
                  Voir
                </button>
              )}
              {mode === "print" && (
                <button onClick={() => onPrint(p.id)} style={actionButtonStyle}>
                  Imprimer PDF
                </button>
              )}
              {mode === "delete" && (
                <button onClick={() => onDelete(p.id)} style={deleteButtonStyle}>
                  Supprimer
                </button>
              )}
              {mode === "update" && (
                <button onClick={() => navigate(`/update/${p.id}`)} style={actionButtonStyle}>
                  Modifier
                </button>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

/* === Styles === */
const containerStyle = {
  maxWidth: "900px",
  margin: "0 auto",
  textAlign: "center",
  fontFamily: "Arial, sans-serif"
};

const filterButtonStyle = {
  marginBottom: "15px",
  padding: "8px 16px",
  cursor: "pointer",
  fontSize: "16px",
  backgroundColor: "#083464",
  color: "white",
  border: "none",
  borderRadius: "8px"
};

const filterBoxStyle = {
  marginBottom: "20px",
  display: "flex",
  flexDirection: "column",
  gap: "10px",
  padding: "15px",
  border: "2px solid #083464",
  borderRadius: "10px",
  backgroundColor: "#f9faff"
};

const inputStyle = {
  padding: "8px",
  border: "1px solid #ccc",
  borderRadius: "6px",
  width: "100%",
  maxWidth: "300px",
  margin: "0 auto"
};

const cardStyle = {
  marginBottom: "25px",
  border: "2px solid #083464",
  borderRadius: "12px",
  padding: "20px",
  backgroundColor: "white",
  boxShadow: "0 2px 6px rgba(0,0,0,0.05)"
};

const buttonContainerStyle = {
  marginTop: "15px",
  display: "flex",
  gap: "10px",
  justifyContent: "center",
  flexWrap: "wrap"
};

const actionButtonStyle = {
  backgroundColor: "#083464",
  color: "white",
  border: "none",
  borderRadius: "8px",
  padding: "8px 14px",
  cursor: "pointer"
};

const deleteButtonStyle = {
  backgroundColor: "#dc3545",
  color: "white",
  border: "none",
  borderRadius: "8px",
  padding: "8px 14px",
  cursor: "pointer"
};
