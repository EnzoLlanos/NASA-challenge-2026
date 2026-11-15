import { ZONE_OPTIONS, CROP_OPTIONS, PRIORITY_OPTIONS } from "../../data/mockData";

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
        <label htmlFor="zone-select" className="form-label">📍 Zona de San Luis</label>
        <select
          id="zone-select"
          className="form-select"
          value={config.zona || "centro"}
          onChange={(e) => {
            const z = ZONE_OPTIONS.find((opt) => opt.value === e.target.value);
            onChange({
              ...config,
              zona: e.target.value,
              coords: z ? z.coords : config.coords,
              lotName: z ? `Campo en ${z.label}` : config.lotName
            });
          }}
        >
          {ZONE_OPTIONS.map((z) => (
            <option key={z.value} value={z.value}>{z.label}</option>
          ))}
        </select>
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
        <label htmlFor="irrigation-select" className="form-label">💧 ¿Cómo recibe agua el lote?</label>
        <select
          id="irrigation-select"
          className="form-select"
          value={config.irrigation || "lluvia"}
          onChange={(e) => onChange({ ...config, irrigation: e.target.value })}
        >
          <option value="lluvia">🌧️ Solo lluvia (secano)</option>
          <option value="riego">🚿 Con equipo de riego</option>
        </select>
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

