import "./WelcomeState.css";

export default function WelcomeState({ selectedRegion, regionName }) {
  return (
    <div className="welcome-container">
      {/* Cabecera corta y directa */}
      <div className="welcome-hero">
        <div className="welcome-badge">
          <span>🛰️</span>
          <span>NASA POWER &bull; San Luis</span>
        </div>
        <h1 className="welcome-title">Simulador de Rotaciones Agrícolas</h1>
        <p className="welcome-subtitle">
          Diagnóstico satelital para optimizar agua, salud del suelo y cobertura.
        </p>
      </div>

      {/* 3 Pasos rápidos en tarjetas concisas */}
      <div className="welcome-steps-card">
        <div className="steps-grid">
          <div className="step-card">
            <div className="step-badge">Paso 1</div>
            <h3>Elegir Zona</h3>
            <span className="step-keyword">Norte &bull; Centro &bull; Sur</span>
          </div>

          <div className="step-card">
            <div className="step-badge">Paso 2</div>
            <h3>Prioridades</h3>
            <span className="step-keyword">Agua &bull; Suelo &bull; Forraje</span>
          </div>

          <div className="step-card highlight">
            <div className="step-badge">Paso 3</div>
            <h3>Simular</h3>
            <span className="step-keyword">3 Estrategias comparadas</span>
          </div>
        </div>
      </div>

      {/* 3 Focos clave con solo palabras clave */}
      <div className="welcome-features-grid">
        <div className="feature-box">
          <span className="feature-icon">💧</span>
          <div>
            <h4>Humedad Útil</h4>
            <span className="feature-tag">Menos evaporación</span>
          </div>
        </div>

        <div className="feature-box">
          <span className="feature-icon">🛡️</span>
          <div>
            <h4>Freno a la Erosión</h4>
            <span className="feature-tag">Suelo cubierto en invierno</span>
          </div>
        </div>

        <div className="feature-box">
          <span className="feature-icon">🌱</span>
          <div>
            <h4>Nutrientes Naturales</h4>
            <span className="feature-tag">Fijación de nitrógeno</span>
          </div>
        </div>
      </div>

      {/* Mensaje de acción directo */}
      <div className="welcome-cta">
        <span className="cta-icon">👈</span>
        <div className="cta-texts">
          <strong>
            {selectedRegion
              ? `Zona seleccionada: ${regionName || selectedRegion.toUpperCase()}`
              : "Seleccioná la zona en el panel izquierdo"}
          </strong>
          <span>Completá las opciones y presioná <strong>Simular Rotaciones</strong></span>
        </div>
      </div>
    </div>
  );
}
