import { useNavigate } from "react-router-dom";

export default function BackButton() {
  const navigate = useNavigate();

  return (
    <div style={{ marginBottom: "20px", textAlign: "center" }}>
      <button 
        onClick={() => navigate("/")} 
        style={buttonStyle}
        onMouseOver={(e) => e.currentTarget.style.backgroundColor = "#e6ebf5"}
        onMouseOut={(e) => e.currentTarget.style.backgroundColor = "#f5f7fa"}
      >
        ← Retour à l’accueil
      </button>
    </div>
  );
}

const buttonStyle = {
  backgroundColor: "#f5f7fa",
  color: "#083464",
  border: "1px solid #083464",
  borderRadius: "8px",
  padding: "10px 18px",
  fontSize: "15px",
  fontWeight: "bold",
  cursor: "pointer",
  transition: "background-color 0.2s ease-in-out"
};
