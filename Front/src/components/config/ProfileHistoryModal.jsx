import { useState } from "react";
import { CROP_OPTIONS } from "../../data/mockData";

const CAMPANA_YEARS = ["2025/26", "2024/25", "2023/24", "2022/23", "2021/22"];

const RESULTADO_LABELS = {
  bueno: { label: "Bueno", badge: "verde" },
  regular: { label: "Regular", badge: "ambar" },
  malo: { label: "Malo / Pérdida", badge: "rojo" },
};

const PROBLEMA_LABELS = {
  ninguno: "Sin problemas graves",
  sequia: "💧 Falta de agua / Sequía",
  erosion: "💨 Erosión / Voladura o huellones",
  baja_fertilidad: "🌱 Suelo cansado / Baja fertilidad",
  malezas_plagas: "🐛 Malezas o plagas resistentes",
};

export default function ProfileHistoryModal({
  isOpen,
  profile,
  onClose,
  onSaveProfile,
}) {
  const [nombre, setNombre] = useState(profile?.nombre || "Productor San Luis");
  const [establecimiento, setEstablecimiento] = useState(
    profile?.establecimiento || "Establecimiento Don Pedro"
  );
  const [campanas, setCampanas] = useState(profile?.historial_campanas || []);

  // Formulario para agregar una campaña anterior
  const [nuevaCampana, setNuevaCampana] = useState("2025/26");
  const [nuevoCultivo, setNuevoCultivo] = useState("Soja");
  const [nuevaCobertura, setNuevaCobertura] = useState(false);
  const [nuevoResultado, setNuevoResultado] = useState("regular");
  const [nuevoProblema, setNuevoProblema] = useState("sequia");
  const [nuevaNota, setNuevaNota] = useState("");
  const [openDecisiones, setOpenDecisiones] = useState(false);

  // Estado para la ventanita de advertencia / confirmación y aviso de éxito
  const [confirmModal, setConfirmModal] = useState(null);
  const [feedbackBanner, setFeedbackBanner] = useState(null);

  if (!isOpen) return null;

  const handleAddCampana = (e) => {
    e.preventDefault();
    setConfirmModal({
      titulo: "⚠️ Confirmar carga de campaña",
      mensaje: `¿Querés guardar la campaña ${nuevaCampana} (${nuevoCultivo}) en tu historial del perfil?`,
      textoConfirmar: "Sí, guardar campaña",
      tipo: "confirmar",
      onConfirm: () => {
        const item = {
          id: `camp-${Date.now()}`,
          campana: nuevaCampana,
          cultivo: nuevoCultivo,
          cobertura_invernal: Boolean(nuevaCobertura),
          resultado: nuevoResultado,
          problema_principal: nuevoProblema,
          notas: nuevaNota.trim() || undefined,
        };
        setCampanas((prev) => [...prev, item]);
        setNuevaNota("");
        setConfirmModal(null);
        setFeedbackBanner(`✓ La campaña ${nuevaCampana} (${nuevoCultivo}) quedó guardada en tu historial.`);
      },
    });
  };

  const handleDeleteCampana = (campanaObj) => {
    setConfirmModal({
      titulo: "⚠️ Confirmar eliminación",
      mensaje: `¿Estás seguro de quitar la campaña ${campanaObj.campana} (${campanaObj.cultivo}) de tu historial?`,
      textoConfirmar: "Sí, eliminar",
      tipo: "peligro",
      onConfirm: () => {
        setCampanas((prev) => prev.filter((c) => c.id !== campanaObj.id));
        setConfirmModal(null);
        setFeedbackBanner(`🗑️ Se eliminó la campaña ${campanaObj.campana} del historial.`);
      },
    });
  };

  const handleSave = () => {
    setConfirmModal({
      titulo: "⚠️ Confirmar guardado de perfil",
      mensaje:
        "¿Confirmás guardar los cambios de tu perfil e historial para aplicarlos a las próximas decisiones?",
      textoConfirmar: "Confirmar y aplicar",
      tipo: "confirmar",
      onConfirm: () => {
        const updatedProfile = {
          ...profile,
          nombre: nombre.trim() || "Productor San Luis",
          establecimiento: establecimiento.trim() || "Establecimiento Don Pedro",
          historial_campanas: campanas,
        };
        setConfirmModal(null);
        onSaveProfile(updatedProfile);
        onClose();
      },
    });
  };

  const decisiones = profile?.decisiones_futuras || [];

  return (
    <div className="profile-modal-overlay" onClick={onClose}>
      <div className="profile-modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="profile-modal-header">
          <div>
            <h3>👤 Perfil del Productor e Historial de Campañas</h3>
            <p>
              Cargá qué sembraste y qué problemas tuviste en campañas anteriores para que las decisiones futuras se adapten a la historia real de tu lote.
            </p>
          </div>
          <button
            type="button"
            className="rules-modal-close"
            onClick={onClose}
            aria-label="Cerrar perfil"
          >
            ✕
          </button>
        </div>

        <div className="profile-modal-body">
          {feedbackBanner && (
            <div className="profile-feedback-banner" role="status">
              <span>{feedbackBanner}</span>
              <button
                type="button"
                className="profile-feedback-close"
                onClick={() => setFeedbackBanner(null)}
                aria-label="Cerrar aviso"
              >
                ✕
              </button>
            </div>
          )}

          {/* 1. Datos básicos del perfil */}
          <div className="profile-section">
            <h4>1. Datos de tu perfil y campo</h4>
            <div className="profile-grid-2">
              <div className="profile-field">
                <label>Tu nombre / Productor</label>
                <input
                  type="text"
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                  placeholder="Ej: Juan Pérez"
                />
              </div>
              <div className="profile-field">
                <label>Nombre del campo o lote</label>
                <input
                  type="text"
                  value={establecimiento}
                  onChange={(e) => setEstablecimiento(e.target.value)}
                  placeholder="Ej: Establecimiento Don Pedro"
                />
              </div>
            </div>
          </div>

          {/* 2. Preguntas sobre campañas anteriores */}
          <div className="profile-section">
            <h4>2. Agregar campaña anterior al historial</h4>
            <form className="profile-add-form" onSubmit={handleAddCampana}>
              <div className="profile-grid-3">
                <div className="profile-field">
                  <label>Campaña / Ciclo</label>
                  <select
                    value={nuevaCampana}
                    onChange={(e) => setNuevaCampana(e.target.value)}
                  >
                    {CAMPANA_YEARS.map((y) => (
                      <option key={y} value={y}>
                        Campaña {y}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="profile-field">
                  <label>¿Qué cultivo sembraste?</label>
                  <select
                    value={nuevoCultivo}
                    onChange={(e) => setNuevoCultivo(e.target.value)}
                  >
                    {CROP_OPTIONS.map((c) => (
                      <option key={c.value} value={c.value}>
                        {c.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="profile-field">
                  <label>¿Cómo fue el rinde / resultado?</label>
                  <select
                    value={nuevoResultado}
                    onChange={(e) => setNuevoResultado(e.target.value)}
                  >
                    <option value="bueno">🟢 Bueno</option>
                    <option value="regular">🟡 Regular</option>
                    <option value="malo">🔴 Malo / Pérdida</option>
                  </select>
                </div>
              </div>

              <div className="profile-grid-2" style={{ marginTop: "8px" }}>
                <div className="profile-field">
                  <label>¿Hiciste cobertura o verdeo en invierno?</label>
                  <select
                    value={nuevaCobertura ? "si" : "no"}
                    onChange={(e) => setNuevaCobertura(e.target.value === "si")}
                  >
                    <option value="no">No (quedó en barbecho / suelo desnudo)</option>
                    <option value="si">Sí (con cultivo de cobertura o verdeo)</option>
                  </select>
                </div>

                <div className="profile-field">
                  <label>¿Qué problema principal observaste en el lote?</label>
                  <select
                    value={nuevoProblema}
                    onChange={(e) => setNuevoProblema(e.target.value)}
                  >
                    <option value="sequia">💧 Falta de agua / Sequía</option>
                    <option value="erosion">💨 Erosión / Voladura o huellones</option>
                    <option value="baja_fertilidad">🌱 Suelo cansado / Baja fertilidad</option>
                    <option value="malezas_plagas">🐛 Malezas o plagas resistentes</option>
                    <option value="ninguno">✅ Ninguno relevante</option>
                  </select>
                </div>
              </div>

              <div className="profile-add-bottom">
                <input
                  type="text"
                  value={nuevaNota}
                  onChange={(e) => setNuevaNota(e.target.value)}
                  placeholder="Nota opcional (ej: Helada temprana en marzo, barbecho muy seco...)"
                  className="profile-note-input"
                />
                <button type="submit" className="btn-add-campaign">
                  + Guardar campaña
                </button>
              </div>
            </form>
          </div>

          {/* 3. Historial guardado de campañas anteriores */}
          <div className="profile-section">
            <h4>3. Historial de campañas anteriores ({campanas.length})</h4>
            {campanas.length === 0 ? (
              <p className="profile-empty">
                No hay campañas cargadas todavía. Agregá al menos una arriba para personalizar las decisiones futuras.
              </p>
            ) : (
              <div className="profile-history-list">
                {campanas.map((c) => {
                  const resMeta = RESULTADO_LABELS[c.resultado] || RESULTADO_LABELS.regular;
                  return (
                    <div key={c.id || c.campana} className="profile-history-item">
                      <div className="profile-history-main">
                        <div className="profile-history-top">
                          <span className="profile-year-badge">{c.campana}</span>
                          <strong>{c.cultivo}</strong>
                          <span className={`estado-chip ${resMeta.badge}`}>
                            Resultado: {resMeta.label}
                          </span>
                          <span className="profile-tag">
                            {c.cobertura_invernal
                              ? "🛡️ Con cobertura invernal"
                              : "⚠️ Invierno sin cobertura"}
                          </span>
                        </div>
                        <div className="profile-history-sub">
                          <span>
                            <strong>Observado:</strong>{" "}
                            {PROBLEMA_LABELS[c.problema_principal] || c.problema_principal}
                          </span>
                          {c.notas && <span> · “{c.notas}”</span>}
                        </div>
                      </div>
                      <button
                        type="button"
                        className="btn-delete-campaign"
                        onClick={() => handleDeleteCampana(c)}
                        title="Quitar campaña del historial"
                      >
                        🗑️
                      </button>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* 4. Historial de decisiones futuras guardadas (Desplegable) */}
          {decisiones.length > 0 && (
            <div className={`profile-section ac-profile ${openDecisiones ? "abierto" : ""}`}>
              <button
                type="button"
                className="acordeon-summary"
                style={{ padding: 0 }}
                onClick={() => setOpenDecisiones(!openDecisiones)}
                aria-expanded={openDecisiones}
              >
                <h4 style={{ margin: 0 }}>
                  4. Decisiones futuras guardadas ({decisiones.length})
                </h4>
                <span className={`acordeon-flecha ${openDecisiones ? "girada" : ""}`}>▼</span>
              </button>
              <div className="acordeon-desplegable">
                <div className="acordeon-inner">
                  <div className="profile-history-list" style={{ marginTop: "10px" }}>
                    {decisiones.map((d) => (
                      <div key={d.id} className="profile-history-item decision-saved">
                        <div className="profile-history-main">
                          <div className="profile-history-top">
                            <span className="profile-year-badge">{d.fecha}</span>
                            <strong>{d.estrategia_nombre}</strong>
                            <span className="profile-tag">
                              Región {String(d.region).toUpperCase()}
                            </span>
                          </div>
                          <div className="profile-history-sub">
                            Rotación planificada: <strong>{d.secuencia_resumen}</strong> (basada en{" "}
                            {d.basado_en_campanas} campañas previas)
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="profile-modal-footer">
          <button type="button" className="btn-profile-cancel" onClick={onClose}>
            Cancelar
          </button>
          <button type="button" className="btn-profile-save" onClick={handleSave}>
            ✓ Guardar perfil y usar historial en decisiones futuras
          </button>
        </div>

        {/* Ventanita emergente de advertencia / confirmación */}
        {confirmModal && (
          <div className="confirm-popup-overlay" onClick={() => setConfirmModal(null)}>
            <div className="confirm-popup-card" onClick={(e) => e.stopPropagation()}>
              <h4>{confirmModal.titulo}</h4>
              <p>{confirmModal.mensaje}</p>
              <div className="confirm-popup-actions">
                <button
                  type="button"
                  className="btn-profile-cancel"
                  onClick={() => setConfirmModal(null)}
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  className={`btn-profile-save ${
                    confirmModal.tipo === "peligro" ? "danger" : ""
                  }`}
                  onClick={confirmModal.onConfirm}
                >
                  {confirmModal.textoConfirmar}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
