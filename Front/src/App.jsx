import { useState } from "react";
import Sidebar from "./components/config/Sidebar";
import { SAMPLE_LOT_SAN_LUIS } from "./data/mockData";
import "./styles/config.css";
import DecisionBoard from "./decision/DecisionBoard.jsx";
import { simulateRotations } from "./services/simulationService.js";

const REGION_LABELS = {
  norte: "Región Norte",
  centro: "Región Centro",
  sur: "Región Sur",
};

export default function App() {
  // Estado de configuración del lote (con región por defecto vacía "---")
  const [config, setConfig] = useState({
    region: "",
    currentCrop: "Soja",
    irrigation: "lluvia",
    priorities: {
      water: true,
      nutrients: true,
      erosion: true,
      forageProfit: false,
    },
    lotName: SAMPLE_LOT_SAN_LUIS.name,
  });

  const [isLoading, setIsLoading] = useState(false);
  const [simulationData, setSimulationData] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Ejecuta la llamada al servicio de simulación de la API
  const runSimulation = async (paramsToSimulate) => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const data = await simulateRotations(paramsToSimulate);
      setSimulationData(data);
    } catch (err) {
      console.error("Error al conectar con la API de simulación:", err);
      setErrorMessage(`No se pudo conectar a la API (FastAPI en http://127.0.0.1:8000): ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Acción del botón principal "Simular Rotaciones"
  const handleSimulate = () => {
    if (!config.region) return;
    runSimulation(config);
  };

  return (
    <div className="app-container">
      {/* BLOQUE 1: Panel Lateral de Configuración (Dev 1) */}
      <Sidebar
        config={config}
        onConfigChange={setConfig}
        onSimulate={handleSimulate}
        isLoading={isLoading}
      />

      {/* BLOQUES 2 y 3: Área Principal / Tablero de Decisión (Dev 2) */}
      <main className="main-dashboard">
        <header className="dashboard-header">
          <div className="dashboard-title">
            <h2>Tablero de Decisión Agronómica</h2>
            <p>
              Campo evaluado: <strong>{config.lotName || "Lote seleccionado"}</strong> &bull;{" "}
              Zona: <strong>{REGION_LABELS[config.region] || "Sin seleccionar (---)"}</strong> &bull;{" "}
              Cultivo actual: <strong>{config.currentCrop}</strong>
            </p>
          </div>
          <div className="nasa-tag">
            <span>🛰️</span> Modelos NASA SMAP &bull; ECOSTRESS &bull; GPM
          </div>
        </header>

        {errorMessage && (
          <div
            style={{
              background: "#fee2e2",
              border: "1px solid #ef4444",
              color: "#991b1b",
              padding: "10px 16px",
              borderRadius: "8px",
              margin: "12px 24px",
              fontSize: "0.85rem",
            }}
          >
            ⚠️ <strong>Aviso:</strong> {errorMessage}
          </div>
        )}

        {/* Bloques 2 y 3: tablero de decisión + evidencia NASA + timeline */}
        <DecisionBoard
          simulacion={simulationData}
          params={config.region ? config : null}
          isLoading={isLoading}
        />
      </main>
    </div>
  );
}
