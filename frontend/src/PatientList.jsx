import { useState, useEffect } from "react";
import axios from "axios";

export default function PatientList({ refreshTrigger, mode, onDelete, onPrint }) {
  const [patients, setPatients] = useState([]);
  const [editPatient, setEditPatient] = useState(null);
  const [updatedName, setUpdatedName] = useState("");
  const [searchId, setSearchId] = useState("");

  const fetchPatients = async () => {
    const res = await axios.get("http://localhost:5050/patients");
    setPatients(res.data);
  };

  useEffect(() => {
    fetchPatients();
  }, [refreshTrigger]);

  const handleUpdate = async (id) => {
    await axios.put(`http://localhost:5050/patients/${id}`, { name: updatedName });
    setEditPatient(null);
    fetchPatients();
  };

  const filteredPatients = searchId
    ? patients.filter((p) => p.id.toString() === searchId)
    : patients;

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", textAlign: "left" }}>
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Rechercher par ID"
          value={searchId}
          onChange={(e) => setSearchId(e.target.value)}
          style={{ padding: "8px", width: "100%", maxWidth: "300px" }}
        />
      </div>

      <ul style={{ listStyle: "none", padding: 0 }}>
        {filteredPatients.map((p) => (
          <li key={p.id} style={{
            marginBottom: "40px",
            borderBottom: "1px solid #444",
            paddingBottom: "20px",
            paddingTop: "20px"
          }}>
            <strong style={{ fontSize: "18px" }}>{p.name}</strong><br />
            ID: {p.id}, Âge: {p.age}, Sexe: {p.sex}, Poids: {p.weight_kg ?? "N/A"} kg

            <div style={{ marginTop: "15px" }}>
              {mode === "print" && (
                <button onClick={() => onPrint(p.id)}>Imprimer PDF</button>
              )}

              {mode === "delete" && (
                <button onClick={() => onDelete(p.id)}>Supprimer</button>
              )}

              {mode === "update" && (
                <>
                  {editPatient === p.id ? (
                    <>
                      <input
                        value={updatedName}
                        onChange={(e) => setUpdatedName(e.target.value)}
                        placeholder="Nouveau nom"
                      />
                      <button onClick={() => handleUpdate(p.id)}>Valider</button>
                      <button onClick={() => setEditPatient(null)}>Annuler</button>
                    </>
                  ) : (
                    <button onClick={() => {
                      setEditPatient(p.id);
                      setUpdatedName(p.name);
                    }}>Modifier</button>
                  )}
                </>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
