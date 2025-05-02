import { Routes, Route, useNavigate } from "react-router-dom";
import PatientForm from "./PatientForm";
import PatientList from "./PatientList";
import { useState } from "react";

export default function App() {
  const navigate = useNavigate();
  const [refresh, setRefresh] = useState(false);

  const handleDelete = async (id) => {
    await fetch(`http://localhost:5050/patients/${id}`, { method: "DELETE" });
    setRefresh((prev) => !prev);
  };

  const handlePrint = (id) => {
    window.open(`http://localhost:5050/patients/${id}/pdf`, "_blank");
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial", maxWidth: "800px", margin: "0 auto", textAlign: "center" }}>
      <h1 style={{ marginBottom: "30px", color: "#2c3e50" }}>
        Mini Medical App
      </h1>

      <Routes>
        <Route path="/" element={
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <button onClick={() => navigate("/create")}>Créer un patient</button>
            <button onClick={() => navigate("/update")}>Mettre à jour</button>
            <button onClick={() => navigate("/delete")}>Supprimer</button>
            <button onClick={() => navigate("/print")}>Imprimer PDF</button>
            <button onClick={() => navigate("/list")}>Afficher liste</button>
          </div>
        } />

        <Route path="/create" element={<PatientForm refresh={() => setRefresh((r) => !r)} />} />
        <Route path="/list" element={<PatientList refreshTrigger={refresh} mode="list" />} />
        <Route path="/delete" element={<PatientList refreshTrigger={refresh} mode="delete" onDelete={handleDelete} />} />
        <Route path="/update" element={<PatientList refreshTrigger={refresh} mode="update" />} />
        <Route path="/print" element={<PatientList refreshTrigger={refresh} mode="print" onPrint={handlePrint} />} />
      </Routes>
    </div>
  );
}
