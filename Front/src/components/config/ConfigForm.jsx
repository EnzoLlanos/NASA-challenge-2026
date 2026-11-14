import { CROP_OPTIONS, PRIORITY_OPTIONS } from "../../data/mockData";

export default function ConfigForm({ config, onChange, onSubmit, isLoading }) {
  const togglePriority = (id) =>
    onChange({ ...config, priorities: { ...config.priorities, [id]: !config.priorities[id] } });

  return (
    <form
      className="config-form"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit();
      }}
    >
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
  );
}

