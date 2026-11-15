import { useState, useEffect } from "react";
import {
  REGION_OPTIONS,
  ZONE_OPTIONS,
  CROP_OPTIONS,
  PRIORITY_OPTIONS,
  REGION_FORM_CONFIG_FALLBACK,
} from "../../data/mockData";
import { fetchRegionsFormConfig } from "../../services/simulationService";
import MapSelector, { SAN_LUIS_REGIONS } from "./MapSelector";

export default function ConfigForm({ config, onChange, onSubmit, isLoading }) {
  const [regionError, setRegionError] = useState(false);
  const [isMapOpen, setIsMapOpen] = useState(false);
  const [regionsFormMeta, setRegionsFormMeta] = useState(REGION_FORM_CONFIG_FALLBACK);

  // Carga las configuraciones regionales desde el Backend (Controller -> Service -> Repository)
  useEffect(() => {
    let active = true;
    fetchRegionsFormConfig()
      .then((data) => {
        if (active && data && typeof data === "object") {
          setRegionsFormMeta((prev) => ({ ...prev, ...data }));
        }
      })
      .catch(() => {
        // Fallback silencioso a REGION_FORM_CONFIG_FALLBACK
      });
    return () => {
      active = false;
    };
  }, []);

  const togglePriority = (id) =>
    onChange({
      ...config,
      priorities: { ...config.priorities, [id]: !config.priorities[id] },
    });

  const handleMapSelect = (regionValue) => {
    setRegionError(false);
    const meta = regionsFormMeta[regionValue] || REGION_FORM_CONFIG_FALLBACK[regionValue];
    const suggestedPriorities = meta?.prioridades_sugeridas || config.priorities;
    const defaultCondition =
      meta?.condicion_contextual?.valor_por_defecto !== undefined
        ? meta.condicion_contextual.valor_por_defecto
        : true;

    onChange({
      ...config,
      region: regionValue,
      zona: regionValue,
      priorities: { ...suggestedPriorities },
      fieldCondition: defaultCondition,
    });
    setIsMapOpen(false);
  };

  const handleConditionToggle = () => {
    const nextVal = !(config.fieldCondition ?? true);
    onChange({
      ...config,
      fieldCondition: nextVal,
    });
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
  const activeRegionMeta = config.region ? regionsFormMeta[config.region] : null;
  const condicionPregunta = activeRegionMeta?.condicion_contextual || null;
  const recommendedCrops = activeRegionMeta?.cultivos_recomendados || [];
  const fieldConditionChecked = config.fieldCondition ?? true;

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

        {/* Condición específica del campo según la región seleccionada */}
        {condicionPregunta && (
          <div className="form-group">
            <span className="form-label">
              {condicionPregunta.icono} Condición del lote en {activeRegionMeta.nombre.replace(" de San Luis", "")}
            </span>
            <label
              className={`priority-chip ${fieldConditionChecked ? "selected" : ""}`}
            >
              <div className="priority-info">
                <span className="priority-icon">{condicionPregunta.icono}</span>
                <div className="priority-texts">
                  <span className="priority-title">{condicionPregunta.etiqueta}</span>
                  <span className="priority-desc">{condicionPregunta.descripcion}</span>
                </div>
              </div>
              <input
                type="checkbox"
                className="priority-checkbox"
                checked={fieldConditionChecked}
                onChange={handleConditionToggle}
              />
            </label>
          </div>
        )}

        <div className="form-group">
          <label htmlFor="crop-select" className="form-label">🌾 ¿Qué venís sembrando?</label>
          <select
            id="crop-select"
            className="form-select"
            value={config.currentCrop}
            onChange={(e) => onChange({ ...config, currentCrop: e.target.value })}
          >
            {CROP_OPTIONS.map((c) => {
              const isRec = recommendedCrops.some(
                (rc) => rc.toLowerCase() === c.value.toLowerCase()
              );
              return (
                <option key={c.value} value={c.value}>
                  {c.label} {isRec && config.region ? "★ Adaptado a tu zona" : ""}
                </option>
              );
            })}
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
          <span className="form-label">
            🎯 ¿Qué priorizás este año?{" "}
            {config.region && (
              <small style={{ fontWeight: 500, color: "#2f6b3a", fontSize: "0.75rem" }}>
                (Sugeridas para {config.region.toUpperCase()})
              </small>
            )}
          </span>
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
