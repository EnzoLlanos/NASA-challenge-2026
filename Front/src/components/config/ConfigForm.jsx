import { useState } from "react";
import { REGION_OPTIONS, CROP_OPTIONS, PRIORITY_OPTIONS } from "../../data/mockData";
import MapSelector, { SAN_LUIS_REGIONS } from "./MapSelector";

export default function ConfigForm({ config, onChange, onSubmit, isLoading }) {
  const [regionError, setRegionError] = useState(false);
  const [isMapOpen, setIsMapOpen] = useState(false);

  const togglePriority = (id) =>
    onChange({ ...config, priorities: { ...config.priorities, [id]: !config.priorities[id] } });

  const handleMapSelect = (regionValue) => {
    setRegionError(false);
    onChange({ ...config, region: regionValue });
    setIsMapOpen(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!config.region) {
      setRegionError(true);
      return;
    }
    setRegionError(false);
    onSubmit();
  };

  const currentRegionObj = SAN_LUIS_REGIONS.find((r) => r.id === config.region);
  const currentRegionLabel =
    REGION_OPTIONS.find((r) => r.value === config.region)?.label || null;

  return (
    <>
      <form className="config-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">📍 ¿En qué zona de San Luis está tu campo?</label>

          <button
            type="button"
            className={`btn-open-region-map ${config.region ? "selected" : ""} ${
              regionError ? "error" : ""
            }`}
            onClick={() => setIsMapOpen(true)}
          >
            <div className="btn-region-content">
              <span className="btn-region-icon">🛰️</span>
              <div className="btn-region-texts">
                <span className="btn-region-title">
                  {currentRegionLabel || "Seleccionar región en el mapa"}
                </span>
                <span className="btn-region-subtitle">
                  {currentRegionObj
                    ? `${currentRegionObj.stats} · Clic para cambiar`
                    : "Norte, Centro o Sur de San Luis"}
                </span>
              </div>
            </div>
            <span className="btn-region-badge">
              {config.region ? "Cambiar" : "Ver mapa"}
            </span>
          </button>

          {regionError && (
            <span style={{ color: "#dc2626", fontSize: "0.8rem", fontWeight: 600 }}>
              ⚠️ Por favor seleccioná una región (Norte, Centro o Sur) para simular.
            </span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="crop-select" className="form-label">🌾 ¿Qué venís sembrando?</label>
          <select
            id="crop-select"
            className="form-select"
            value={config.currentCrop}
            onChange={(e) => onChange({ ...config, currentCrop: e.target.value })}
          >
            {CROP_OPTIONS.map((c) => (
              <option key={c.value} value={c.value}>{c.label}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <span className="form-label">💧 Régimen de agua</span>
          <div className="pill-group">
            <button
              type="button"
              className={`pill-btn ${config.irrigation === "lluvia" ? "active" : ""}`}
              onClick={() => onChange({ ...config, irrigation: "lluvia" })}
            >
              🌧️ Solo lluvia
            </button>
            <button
              type="button"
              className={`pill-btn ${config.irrigation === "riego" ? "active" : ""}`}
              onClick={() => onChange({ ...config, irrigation: "riego" })}
            >
              🚿 Con riego
            </button>
          </div>
        </div>

        <div className="form-group">
          <span className="form-label">🎯 ¿Qué priorizás este año?</span>
          <div className="priorities-list">
            {PRIORITY_OPTIONS.map((p) => {
              const selected = Boolean(config.priorities[p.id]);
              return (
                <label key={p.id} className={`priority-chip ${selected ? "selected" : ""}`}>
                  <div className="priority-info">
                    <span className="priority-icon">{p.icon}</span>
                    <div className="priority-texts">
                      <span className="priority-title">{p.label}</span>
                      <span className="priority-desc">{p.desc}</span>
                    </div>
                  </div>
                  <input
                    type="checkbox"
                    className="priority-checkbox"
                    checked={selected}
                    onChange={() => togglePriority(p.id)}
                  />
                </label>
              );
            })}
          </div>
        </div>

        <button type="submit" className={`btn-simulate ${isLoading ? "loading" : ""}`} disabled={isLoading}>
          {isLoading ? "⏳ Consultando datos NASA..." : "🚀 Simular Rotaciones"}
        </button>
      </form>

      <MapSelector
        isOpen={isMapOpen}
        selectedRegion={config.region}
        onSelectRegion={handleMapSelect}
        onClose={() => setIsMapOpen(false)}
      />
    </>
  );
}
