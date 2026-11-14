import { useState } from "react";
import Sidebar from "./components/config/Sidebar";
import { SAMPLE_LOT_SAN_LUIS, MOCK_SIMULATION_RESULT } from "./data/mockData";
import "./styles/config.css";

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
  const [simulationData, setSimulationData] = useState(MOCK_SIMULATION_RESULT);

  // Acción del botón principal "Simular Rotaciones"
  const handleSimulate = () => {
    setIsLoading(true);
    // Simular un retardo realista de consulta satelital NASA (700ms)
    setTimeout(() => {
      setSimulationData({
        ...MOCK_SIMULATION_RESULT,
        lotInfo: {
          ...SAMPLE_LOT_SAN_LUIS,
          coords: config.coords,
          currentCrop: config.currentCrop,
          irrigation: config.irrigation === "lluvia" ? "Secano (Solo lluvia)" : "Bajo Riego",
          priorities: config.priorities
        },
        timestamp: new Date().toLocaleTimeString()
      });
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

        {/* Vista previa de las 3 estrategias para validar que la simulación responde */}
        <section className="preview-cards-grid">
          {simulationData?.strategies.map((strategy) => (
            <article
              key={strategy.id}
              className={`strategy-preview-card ${strategy.id === "regenerativa" ? "featured" : ""}`}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span className={`card-tag tag-${strategy.badgeType}`}>{strategy.tag}</span>
                <span className="score-badge">{strategy.soilHealthScore}%</span>
              </div>
              <h3 style={{ margin: "6px 0 0", fontSize: "1.1rem" }}>{strategy.name}</h3>
              <p style={{ margin: "4px 0", fontSize: "0.85rem", color: "#4b5563" }}>
                <strong>Secuencia:</strong> {strategy.sequence.join(" ➔ ")}
              </p>
              <div
                style={{
                  background: "#f8fafc",
                  padding: "8px 10px",
                  borderRadius: "6px",
                  fontSize: "0.8rem",
                  marginTop: "6px"
                }}
              >
                <strong>🛰️ Dato NASA:</strong> {strategy.nasaEvidence}
              </div>
            </article>
          ))}
        </section>

        {/* Placeholder amigable indicando la integración limpia con el Dev 2 */}
        <div className="dev2-placeholder-container">
          <div style={{ fontSize: "2rem" }}>🤝</div>
          <h3 style={{ margin: 0, color: "#1e5e3a" }}>
            ¡Bloque 1 configurado e integrado con éxito!
          </h3>
          <p style={{ margin: 0, maxWidth: "600px", color: "#64748b", fontSize: "0.9rem" }}>
            Cuando tu amigo (Dev 2) termine sus componentes (Semáforo de salud del suelo, comparador
            detallado y calendario NASA), se montan directamente en este espacio reemplazando esta
            tarjeta.
          </p>
        </div>
      </main>
    </div>
  );
}
