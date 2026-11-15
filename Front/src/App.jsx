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
    zona: "centro",
    coords: SAMPLE_LOT_SAN_LUIS.coords,
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
      {/* Bloque 1: Configuración del Lote */}
      <Sidebar
        config={config}
        onChange={setConfig}
        onSubmit={handleSimulate}
        isLoading={isLoading}
      />

      {/* Bloque 2 y 3: Tablero de Decisión y Evidencia NASA */}
      <main className="main-dashboard">
        {errorMessage && (
          <div
            style={{
              background: "#fee2e2",
              color: "#991b1b",
              border: "1px solid #f87171",
              padding: "12px 16px",
              borderRadius: "8px",
              fontSize: "0.9rem",
              fontWeight: 600,
            }}
          >
            ⚠️ {errorMessage}
          </div>
        )}

        {/* Tablero de decisión integrado */}
        <DecisionBoard
          simulacion={simulationData}
          params={config}
          isLoading={isLoading}
        />
      </main>
    </div>
  );
}
