import { useState } from "react";
import Sidebar from "./components/config/Sidebar";
import { SAMPLE_LOT_SAN_LUIS } from "./data/mockData";
import "./styles/config.css";
import DecisionBoard from "./decision/DecisionBoard.jsx";

export default function App() {
  // Estado de configuración del lote (Dev 1)
  const [config, setConfig] = useState({
    coords: SAMPLE_LOT_SAN_LUIS.coords,
    currentCrop: "Soja",
    irrigation: "lluvia",
    priorities: {
      water: true,
      nutrients: true,
      erosion: true,
      forageProfit: false
    },
    lotName: SAMPLE_LOT_SAN_LUIS.name
  });

  const [isLoading, setIsLoading] = useState(false);
  // Configuración con la que se simuló por última vez (la consume el Tablero de Decisión)
  const [simParams, setSimParams] = useState(null);

  // Acción del botón principal "Simular Rotaciones"
  const handleSimulate = () => {
    setIsLoading(true);
    // Pequeño retardo para simular la consulta satelital
    setTimeout(() => {
      setSimParams({ ...config });
      setIsLoading(false);
    }, 700);
  };

  return (
    <div className="app-container">
      {/* BLOQUE 1: Panel Lateral de Configuración (Tu parte - Dev 1) */}
      <Sidebar
        config={config}
        onConfigChange={setConfig}
        onSimulate={handleSimulate}
        isLoading={isLoading}
      />

      {/* BLOQUES 2 y 3: Área Principal / Tablero de Decisión (Para tu amigo - Dev 2) */}
      <main className="main-dashboard">
        <header className="dashboard-header">
          <div className="dashboard-title">
            <h2>Tablero de Decisión Agronómica</h2>
            <p>
              Campo evaluado: <strong>{config.lotName || "Lote seleccionado"}</strong> (
              {config.coords.lat}, {config.coords.lng}) &bull; Cultivo actual:{" "}
              <strong>{config.currentCrop}</strong>
            </p>
          </div>
          <div className="nasa-tag">
            <span>🛰️</span> Modelos NASA SMAP &bull; ECOSTRESS &bull; GPM
          </div>
        </header>

        {/* Bloques 2 y 3: tablero de decisión + evidencia NASA + timeline (Dev 2) */}
        <DecisionBoard params={simParams} />
      </main>
    </div>
  );
}
