import { useState } from "react";
import PatientForm from "./components/PatientForm";
import PatientList from "./components/PatientList";

function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  const triggerRefresh = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <img
        src="/logo.jpeg"
        alt="Logo"
        style={{ height: "150px", marginBottom: "10px" }}
      />
      <h1 style={{ marginBottom: "30px" }}>Mini Medical App</h1>

      <PatientForm refresh={triggerRefresh} />
      <PatientList refreshTrigger={refreshKey} />
    </div>
  );
}

export default App;

