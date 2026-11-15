import { useState, useEffect } from "react";
import Sidebar from "./components/config/Sidebar";
import { SAMPLE_LOT_SAN_LUIS } from "./data/mockData";
import "./styles/config.css";
import DecisionBoard from "./decision/DecisionBoard.jsx";
import WelcomeState from "./components/welcome/WelcomeState.jsx";
import {
  simulateRotations,
  getLocalProfile,
  fetchUserProfile,
  updateUserProfile,
  saveFutureDecision,
} from "./services/simulationService.js";

const REGION_LABELS = {
  norte: "Región Norte",
  centro: "Región Centro",
  sur: "Región Sur",
};

export default function App() {
  const initialProfile = getLocalProfile();
  const lastCampaignCrop =
    initialProfile?.historial_campanas?.length > 0
      ? initialProfile.historial_campanas[initialProfile.historial_campanas.length - 1].cultivo
      : "Soja";

  const [profile, setProfile] = useState(initialProfile);

  // Estado de configuración del lote (con región por defecto vacía "---")
  const [config, setConfig] = useState({
    region: "",
    zona: "centro",
    coords: SAMPLE_LOT_SAN_LUIS.coords,
    currentCrop: lastCampaignCrop,
    irrigation: "lluvia",
    priorities: {
      water: true,
      nutrients: true,
      erosion: true,
      forageProfit: false,
    },
    lotName: initialProfile?.establecimiento || SAMPLE_LOT_SAN_LUIS.name,
    producerName: initialProfile?.nombre || "Productor San Luis",
    campaignHistory: initialProfile?.historial_campanas || [],
  });

  const [isLoading, setIsLoading] = useState(false);
  const [hasCalculated, setHasCalculated] = useState(false);
  const [simulationData, setSimulationData] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Sincronizar perfil guardado desde el Backend al iniciar
  useEffect(() => {
    let active = true;
    fetchUserProfile("usr-1").then((loaded) => {
      if (active && loaded) {
        setProfile(loaded);
        const lastCrop =
          loaded.historial_campanas?.length > 0
            ? loaded.historial_campanas[loaded.historial_campanas.length - 1].cultivo
            : undefined;
        setConfig((prev) => ({
          ...prev,
          currentCrop: lastCrop || prev.currentCrop,
          lotName: loaded.establecimiento || prev.lotName,
          producerName: loaded.nombre || prev.producerName,
          campaignHistory: loaded.historial_campanas || [],
        }));
      }
    });
    return () => {
      active = false;
    };
  }, []);

  // Guardar cambios en el perfil e historial de campañas y reflejarlos en el simulador
  const handleSaveProfile = async (newProfile) => {
    const saved = await updateUserProfile(newProfile);
    setProfile(saved);

    const hist = saved.historial_campanas || [];
    const latestCrop = hist.length > 0 ? hist[hist.length - 1].cultivo : config.currentCrop;
    const hadDrought = hist.some((c) => c.problema_principal === "sequia");
    const hadErosion = hist.some((c) => c.problema_principal === "erosion" || !c.cobertura_invernal);
    const hadLowFert = hist.some((c) => c.problema_principal === "baja_fertilidad");

    const updatedConfig = {
      ...config,
      currentCrop: latestCrop,
      lotName: saved.establecimiento || config.lotName,
      producerName: saved.nombre || config.producerName,
      campaignHistory: hist,
      priorities: {
        ...config.priorities,
        water: hadDrought ? true : config.priorities.water,
        erosion: hadErosion ? true : config.priorities.erosion,
        nutrients: hadLowFert ? true : config.priorities.nutrients,
      },
    };
    setConfig(updatedConfig);

    // Si ya había simulado una región, recalcula las decisiones futuras con el nuevo historial
    if (updatedConfig.region && hasCalculated) {
      runSimulation(updatedConfig);
    }
  };

  // Guardar una estrategia elegida como decisión futura en el perfil
  const handleSaveFutureDecision = async (estrategia) => {
    const decisionPayload = {
      campana_objetivo: "Próxima campaña",
      region: config.region || "centro",
      estrategia_id: estrategia.id,
      estrategia_nombre: estrategia.nombre,
      secuencia_resumen: (estrategia.secuencia || []).map((s) => s.cultivo).join(" → "),
      basado_en_campanas: (profile?.historial_campanas || []).length,
    };
    const updatedProfile = await saveFutureDecision(decisionPayload, profile);
    setProfile(updatedProfile);
  };

  // Ejecuta la llamada al servicio de simulación de la API
  const runSimulation = async (paramsToSimulate) => {
    setIsLoading(true);
    setHasCalculated(true);
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
    runSimulation({
      ...config,
      lotName: profile?.establecimiento || config.lotName,
      producerName: profile?.nombre || config.producerName,
      campaignHistory: profile?.historial_campanas || config.campaignHistory || [],
    });
  };

  return (
    <div className="app-container">
      {/* Bloque 1: Configuración del Lote y Perfil con Historial */}
      <Sidebar
        config={config}
        onChange={setConfig}
        onSubmit={handleSimulate}
        isLoading={isLoading}
        profile={profile}
        onSaveProfile={handleSaveProfile}
      />

      {/* Bloque 2 y 3: Tablero de Decisión o Bienvenida Inicial */}
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

        {!hasCalculated ? (
          <WelcomeState
            selectedRegion={config.region}
            regionName={REGION_LABELS[config.region]}
          />
        ) : (
          <DecisionBoard
            simulacion={simulationData}
            params={config}
            isLoading={isLoading}
            profile={profile}
            onSaveDecision={handleSaveFutureDecision}
          />
        )}
      </main>
    </div>
  );
}
