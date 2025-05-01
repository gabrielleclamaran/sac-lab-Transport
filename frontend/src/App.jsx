import { useState } from "react";
import PatientForm from "./PatientForm";
import PatientList from "./PatientList";
import axios from "axios";

export default function App() {
  const [selectedAction, setSelectedAction] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const refresh = () => setRefreshTrigger(r => r + 1);

  const handleDelete = async (id) => {
    await axios.delete(`http://localhost:5050/patients/${id}`);
    refresh();
  };

  const handlePrint = (id) => {
    window.open(`http://localhost:5050/patients/${id}/pdf`, "_blank");
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial", maxWidth: "800px", margin: "0 auto", textAlign: "center" }}>
      <h1 style={{ marginBottom: "30px", color: "#2c3e50" }}>Mini Medical App</h1>
      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        <button onClick={() => setSelectedAction("create")}>Créer un patient</button>
        <button onClick={() => setSelectedAction("update")}>Mettre à jour</button>
        <button onClick={() => setSelectedAction("delete")}>Supprimer</button>
        <button onClick={() => setSelectedAction("print")}>Imprimer PDF</button>
        <button onClick={() => setSelectedAction("list")}>Afficher liste</button>
      </div>

      <div style={{ marginTop: "30px", color: "#34495e" }}>
        {selectedAction === "create" && <PatientForm refresh={refresh} />}
        {["list", "delete", "update", "print"].includes(selectedAction) &&
          <PatientList refreshTrigger={refreshTrigger} mode={selectedAction} onDelete={handleDelete} onPrint={handlePrint} />
        }
      </div>
    </div>
  );
}
