import MapSelector from "./MapSelector";
import ConfigForm from "./ConfigForm";
import { SAMPLE_LOT_SAN_LUIS } from "../../data/mockData";

export default function Sidebar({ config, onConfigChange, onSimulate, isLoading }) {
  const handleLoadDemo = () => {
    onConfigChange({
      ...config,
      coords: SAMPLE_LOT_SAN_LUIS.coords,
      currentCrop: SAMPLE_LOT_SAN_LUIS.currentCrop,
      irrigation: SAMPLE_LOT_SAN_LUIS.irrigation,
      priorities: { ...SAMPLE_LOT_SAN_LUIS.priorities },
      lotName: SAMPLE_LOT_SAN_LUIS.name
    });
  };

  return (
    <aside className="sidebar-panel">
      <header className="sidebar-header">
        <div className="logo-badge">🌱</div>
        <div className="sidebar-title">
          <h1>AgroNASA Resiliente</h1>
          <p>Tablero de decisión de rotaciones</p>
        </div>
      </header>

      <MapSelector
        selectedLocation={config.coords}
        onLocationChange={(coords) => onConfigChange({ ...config, coords })}
        onLoadDemo={handleLoadDemo}
      />

      <ConfigForm config={config} onChange={onConfigChange} onSubmit={onSimulate} isLoading={isLoading} />

      <footer style={{ marginTop: "auto", paddingTop: 12, borderTop: "1.5px solid #c8deef" }}>
        <p style={{ margin: 0, fontSize: "0.74rem", color: "#3b628a", textAlign: "center", fontWeight: "600" }}>
          🛰️ Datos: NASA SMAP, ECOSTRESS, GPM y MODIS. Herramienta de apoyo: no reemplaza el criterio del productor.
        </p>
      </footer>
    </aside>
  );
}
