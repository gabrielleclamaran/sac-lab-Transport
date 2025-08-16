import { Routes, Route, useNavigate } from "react-router-dom";
import PatientForm from "./PatientForm";
import PatientList from "./PatientList";
import { useState } from "react";
import BackButton from "./BackButton";
import PatientView from "./PatientView";
import logo from "./assets/logo.png"; // logo dans src/assets/

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
    <div style={appContainer}>
      <main style={mainCard}>
        {/* Header avec logo + titre dans la carte */}
        <header style={headerStyle}>
          <img src={logo} alt="CHU Sainte-Justine" style={logoStyle} />
          <h1 style={titleStyle}>Gestion des Transferts Pédiatriques</h1>
        </header>

        <Routes>
          <Route path="/" element={
            <div style={menuGrid}>
              <MenuButton text="Créer un patient" onClick={() => navigate("/create")} />
              <MenuButton text="Mettre à jour" onClick={() => navigate("/update")} />
              <MenuButton text="Supprimer" onClick={() => navigate("/delete")} />
              <MenuButton text="Imprimer PDF" onClick={() => navigate("/print")} />
              <MenuButton text="Afficher liste" onClick={() => navigate("/list")} />
            </div>
          } />

          <Route path="/create" element={<><BackButton /><PatientForm refresh={() => setRefresh((r) => !r)} /></>} />
          <Route path="/update/:id" element={<><BackButton /><PatientForm refresh={() => setRefresh((r) => !r)} /></>} />
          <Route path="/view/:id" element={<><BackButton /><PatientView /></>} />
          <Route path="/list" element={<><BackButton /><PatientList refreshTrigger={refresh} mode="list" /></>} />
          <Route path="/delete" element={<><BackButton /><PatientList refreshTrigger={refresh} mode="delete" onDelete={handleDelete} /></>} />
          <Route path="/update" element={<><BackButton /><PatientList refreshTrigger={refresh} mode="update" /></>} />
          <Route path="/print" element={<><BackButton /><PatientList refreshTrigger={refresh} mode="print" onPrint={handlePrint} /></>} />
        </Routes>
      </main>
    </div>
  );
}

function MenuButton({ text, onClick }) {
  return (
    <button 
      onClick={onClick} 
      style={menuButtonStyle}
      onMouseOver={(e) => e.currentTarget.style.transform = "scale(1.05)"}
      onMouseOut={(e) => e.currentTarget.style.transform = "scale(1)"}
    >
      {text}
    </button>
  );
}

/* === Styles globaux === */
const appContainer = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",   // ✅ centrage vertical + horizontal
  minHeight: "100vh",
  backgroundColor: "#f5f7fa",
  padding: "20px"
};

const mainCard = {
  backgroundColor: "white",
  padding: "40px",
  borderRadius: "12px",
  boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
  width: "100%",
  maxWidth: "600px",     // ✅ rendu compact centré
  textAlign: "center",   // ✅ contenu centré
  display: "flex",
  flexDirection: "column",
  alignItems: "center"
};

const headerStyle = {
  textAlign: "center",
  marginBottom: "20px"
};

const logoStyle = {
  height: "70px",
  marginBottom: "10px"
};

const titleStyle = {
  color: "#083464",
  margin: "10px 0",
  fontSize: "1.8rem",
  fontWeight: "bold"
};

const menuGrid = {
  display: "grid",
  gridTemplateColumns: "1fr",
  gap: "20px",
  justifyContent: "center",
  width: "100%"
};

const menuButtonStyle = {
  backgroundColor: "#083464",
  color: "white",
  border: "none",
  borderRadius: "12px",
  padding: "20px",
  fontSize: "16px",
  fontWeight: "bold",
  cursor: "pointer",
  boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
  transition: "transform 0.15s ease-in-out",
  width: "100%"
};
