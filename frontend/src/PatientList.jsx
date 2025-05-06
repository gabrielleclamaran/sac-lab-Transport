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
    <div style={{ maxWidth: "800px", margin: "0 auto", textAlign: "left" }}>
      {mode === "list" && (
        <>
          <button
            onClick={() => setShowFilters(!showFilters)}
            style={{
              marginBottom: "15px",
              padding: "6px 12px",
              cursor: "pointer",
              fontSize: "16px"
            }}
          >
            🔍 Filters
          </button>

          {showFilters && (
            <div style={{ marginBottom: "20px", display: "flex", flexDirection: "column", gap: "10px" }}>
              <input
                type="text"
                placeholder="Search by ID"
                value={searchId}
                onChange={(e) => setSearchId(e.target.value)}
                style={{ padding: "8px", width: "100%", maxWidth: "300px" }}
              />

              <select value={searchHospital} onChange={(e) => setSearchHospital(e.target.value)}>
                <option value="">-- Filter by Referring Hospital --</option>
                {hospitalOptions.map((h, i) => <option key={i} value={h}>{h}</option>)}
              </select>

              <select value={searchDiagnosis} onChange={(e) => setSearchDiagnosis(e.target.value)}>
                <option value="">-- Filter by Diagnosis --</option>
                {diagnosisOptions.map((d, i) => <option key={i} value={d}>{d}</option>)}
              </select>

              <input
                type="date"
                value={searchDate}
                onChange={(e) => setSearchDate(e.target.value)}
                style={{ padding: "8px", maxWidth: "300px" }}
              />
            </div>
          )}
        </>
      )}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {filteredPatients.map((p) => (
          <li key={p.id} style={{
            marginBottom: "40px",
            borderBottom: "1px solid #444",
            paddingBottom: "20px",
            paddingTop: "20px"
          }}>
            <strong style={{ fontSize: "18px" }}>{p.name}</strong><br />
            ID: {p.id}, Age: {p.age}, Sex: {p.sex}, Weight: {p.weight_kg ?? "N/A"} kg

            <div style={{ marginTop: "15px", display: "flex", gap: "10px", flexWrap: "wrap" }}>
              {mode === "list" && (
                <button onClick={() => navigate(`/view/${p.id}`)}>View</button>
              )}
              {mode === "print" && (
                <button onClick={() => onPrint(p.id)}>Print PDF</button>
              )}
              {mode === "delete" && (
                <button onClick={() => onDelete(p.id)}>Delete</button>
              )}
              {mode === "update" && (
                <button onClick={() => navigate(`/update/${p.id}`)}>Edit</button>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
