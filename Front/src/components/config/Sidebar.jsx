import { useState } from "react";
import ConfigForm from "./ConfigForm";
import ProfileHistoryModal from "./ProfileHistoryModal";

export default function Sidebar({
  config,
  onChange,
  onConfigChange,
  onSubmit,
  onSimulate,
  isLoading,
  profile,
  onSaveProfile,
}) {
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const handleChange = onChange || onConfigChange;
  const handleSubmit = onSubmit || onSimulate;

  const campanasCount = profile?.historial_campanas?.length || 0;
  const lastCampana =
    campanasCount > 0 ? profile.historial_campanas[campanasCount - 1] : null;

  return (
    <aside className="sidebar-panel">
      <header className="sidebar-header">
        <div className="logo-badge">🌱</div>
        <div className="sidebar-title">
          <h1>AgroNASA Resiliente</h1>
          <p>Tablero de decisión de rotaciones</p>
        </div>
      </header>

      {/* Tarjeta de Perfil e Historial de Campañas Anteriores */}
      <button
        type="button"
        className="profile-sidebar-btn"
        onClick={() => setIsProfileOpen(true)}
      >
        <div className="profile-sidebar-left">
          <span className="profile-sidebar-avatar">👤</span>
          <div className="profile-sidebar-texts">
            <span className="profile-sidebar-name">
              {profile?.nombre || "Productor San Luis"} · {profile?.establecimiento || "Mi Lote"}
            </span>
            <span className="profile-sidebar-sub">
              {campanasCount > 0
                ? `📋 ${campanasCount} campaña(s) en historial (Última: ${lastCampana.campana} - ${lastCampana.cultivo})`
                : "📋 Cargar campañas anteriores para guiar decisiones"}
            </span>
          </div>
        </div>
        <span className="profile-sidebar-badge">Historial</span>
      </button>

      <ConfigForm
        config={config}
        onChange={handleChange}
        onSubmit={handleSubmit}
        isLoading={isLoading}
      />

      <footer style={{ marginTop: "auto", paddingTop: 12, borderTop: "1.5px solid #c8deef" }}>
        <p style={{ margin: 0, fontSize: "0.74rem", color: "#3b628a", textAlign: "center", fontWeight: "600" }}>
          🛰️ Datos: NASA SMAP, ECOSTRESS, GPM y MODIS. Herramienta de apoyo: no reemplaza el criterio del productor.
        </p>
      </footer>

      <ProfileHistoryModal
        key={JSON.stringify(profile)}
        isOpen={isProfileOpen}
        profile={profile}
        onClose={() => setIsProfileOpen(false)}
        onSaveProfile={onSaveProfile}
      />
    </aside>
  );
}
