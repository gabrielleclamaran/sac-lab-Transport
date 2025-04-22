import { useState, useEffect } from "react";
import axios from "axios";

export default function PatientList({ refreshTrigger }) {
  const [patients, setPatients] = useState([]);

  const fetchPatients = async () => {
    const res = await axios.get("http://localhost:5050/patients");
    setPatients(res.data);
  };

  useEffect(() => {
    fetchPatients();
  }, [refreshTrigger]);

  const deletePatient = async (id) => {
    await axios.delete(`http://localhost:5050/patients/${id}`);
    fetchPatients();
  };

  const downloadPDF = (id) => {
    window.open(`http://localhost:5050/patients/${id}/pdf`, "_blank");
  };

  return (
    <div style={{ maxWidth: "1000px", margin: "0 auto", textAlign: "center" }}>
      <h3>Patients</h3>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {patients.map((p) => (
          <li key={p.id} style={{
            marginBottom: "40px",
            borderBottom: "1px solid #444",
            paddingBottom: "20px",
            paddingTop: "20px"
          }}>
            <strong style={{ fontSize: "18px" }}>{p.name}</strong><br />
            Âge: {p.age}, Sexe: {p.sex}, Poids: {p.weight_kg ?? "N/A"} kg

            <div style={{ marginTop: "15px" }}>
              <button onClick={() => downloadPDF(p.id)}>PDF</button>
              <button onClick={() => deletePatient(p.id)} style={{ marginLeft: "10px" }}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}