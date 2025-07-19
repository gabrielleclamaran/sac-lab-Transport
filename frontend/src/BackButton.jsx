import { useNavigate } from "react-router-dom";

export default function BackButton() {
  const navigate = useNavigate();

  return (
    <div style={{ marginBottom: "20px", textAlign: "left" }}>
      <button onClick={() => navigate("/")} style={{ padding: "8px 16px" }}>
        ← Retour à l’accueil
      </button>
    </div>
  );
}
