import ConfigForm from "./ConfigForm";

export default function Sidebar({ config, onConfigChange, onSimulate, isLoading }) {
  return (
    <aside className="sidebar-panel">
      <header className="sidebar-header">
        <div className="logo-badge">🌱</div>
        <div className="sidebar-title">
          <h1>AgroNASA Resiliente</h1>
          <p>Tablero de decisión de rotaciones</p>
        </div>
      </header>

      <ConfigForm config={config} onChange={onConfigChange} onSubmit={onSimulate} isLoading={isLoading} />

      <footer style={{ marginTop: "auto", paddingTop: 12, borderTop: "1.5px solid #c8deef" }}>
        <p style={{ margin: 0, fontSize: "0.74rem", color: "#3b628a", textAlign: "center", fontWeight: "600" }}>
          🛰️ Datos: NASA SMAP, ECOSTRESS, GPM y MODIS. Herramienta de apoyo: no reemplaza el criterio del productor.
        </p>
      </footer>
    </aside>
  );
}
