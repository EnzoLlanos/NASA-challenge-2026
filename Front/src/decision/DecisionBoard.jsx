import { useState } from 'react';
import { useSimulation } from './api.js';
import { REGION_FORM_CONFIG_FALLBACK } from '../data/mockData.js';
import './decision.css';

const MESES = ['E', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];
const MESES_LARGO = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];

const METRICAS = [
  { key: 'agua', label: 'Agua', icon: '💧', hint: 'Uso eficiente del agua' },
  { key: 'nutrientes', label: 'Nutrientes', icon: '🌱', hint: 'Fertilidad del suelo' },
  { key: 'erosion', label: 'Protección contra erosión', icon: '🛡️', hint: 'Menos suelo perdido' },
];

// Semáforo por estado cualitativo (sin números ni porcentajes)
function semaforo(valor) {
  if (typeof valor === 'number' || (!Number.isNaN(Number(valor)) && String(valor).trim() !== '')) {
    const num = Number(valor);
    if (num >= 70) return { clase: 'verde', texto: 'Estable', pct: 85 };
    if (num >= 45) return { clase: 'ambar', texto: 'Regular', pct: 55 };
    return { clase: 'rojo', texto: 'En riesgo', pct: 30 };
  }
  const e = String(valor || '').toLowerCase();
  if (e.includes('saludable') || e.includes('estable') || e.includes('muy buena') || e.includes('alta') || e.includes('mejor') || e.includes('excelente')) {
    return { clase: 'verde', texto: 'Estable', pct: 85 };
  }
  if (e.includes('riesgo') || e.includes('baja') || e.includes('deficitaria') || e.includes('crítica') || e.includes('peligro')) {
    return { clase: 'rojo', texto: 'En riesgo', pct: 30 };
  }
  return { clase: 'ambar', texto: 'Regular', pct: 55 };
}

function enRango(mes, desde, hasta) {
  return desde <= hasta ? mes >= desde && mes <= hasta : mes >= desde || mes <= hasta;
}

// Devuelve, por mes, 'cubierto' | 'vulnerable' | 'desnudo' y el cultivo activo.
export function calcularCobertura(secuencia) {
  const base = Array.from({ length: 12 }, (_, i) => {
    const mes = i + 1;
    const item = secuencia.find((s) => enRango(mes, s.desde, s.hasta));
    return { mes, item };
  });
  return base.map(({ mes, item }, i) => {
    if (item) {
      const emergencia = mes === item.desde && item.tipo === 'cultivo';
      return { item, estado: emergencia ? 'vulnerable' : 'cubierto' };
    }
    const previo = base[(i + 11) % 12].item;
    return { item: null, estado: previo ? 'vulnerable' : 'desnudo' };
  });
}

function mesesDesnudos(secuencia) {
  const c = calcularCobertura(secuencia);
  return {
    desnudo: c.filter((x) => x.estado === 'desnudo').length,
    vulnerable: c.filter((x) => x.estado === 'vulnerable').length,
  };
}

function Medidor({ estado }) {
  const s = semaforo(estado);

  return (
    <div className={`medidor ${s.clase}`} role="img" aria-label={`Salud del suelo: ${s.texto}`}>
      <div className="medidor-cab">
        <span className="medidor-titulo">Salud del suelo</span>
        <span className={`estado-chip ${s.clase}`}>{s.texto}</span>
      </div>
      <div className="medidor-pista">
        <div className="medidor-valor" style={{ width: `${s.pct}%` }} />
      </div>
    </div>
  );
}

function Barrita({ icon, label, valor, hint }) {
  if (valor === undefined || valor === null) return null;
  const esNumero = typeof valor === 'number' || (!Number.isNaN(Number(valor)) && String(valor).trim() !== '');
  const s = semaforo(valor);

  if (esNumero) {
    return (
      <div className="barrita" title={hint}>
        <div className="barrita-top">
          <span className="barrita-label">
            <span aria-hidden="true">{icon}</span> {label}
          </span>
          <strong className={`estado-chip ${s.clase}`}>
            {s.texto}
          </strong>
        </div>
      </div>
    );
  }

  const texto = String(valor);
  const i = texto.indexOf(':');
  const detalle = i > -1 ? texto.slice(i + 1).trim() : '';
  return (
    <div className="barrita" title={hint}>
      <div className="barrita-top">
        <span className="barrita-label">
          <span aria-hidden="true">{icon}</span> {label}
        </span>
        <strong className={`estado-chip ${s.clase}`}>{s.texto}</strong>
      </div>
      {detalle && <p className="barrita-detalle">{detalle}</p>}
    </div>
  );
}

function Secuencia({ secuencia }) {
  return (
    <ol className="secuencia">
      {secuencia.map((s, i) => (
        <li key={i} className={`paso ${s.tipo}`}>
          <span className="paso-nombre">{s.cultivo}</span>
          <span className="paso-meses">
            {MESES_LARGO[s.desde - 1]} → {MESES_LARGO[s.hasta - 1]}
          </span>
        </li>
      ))}
    </ol>
  );
}

function ReglasModal({ isOpen, onClose, regionKey, reglasBackend, amenazaBackend }) {
  if (!isOpen) return null;

  const fallbackMeta = REGION_FORM_CONFIG_FALLBACK[regionKey] || REGION_FORM_CONFIG_FALLBACK.centro;
  const reglas =
    Array.isArray(reglasBackend) && reglasBackend.length > 0
      ? reglasBackend
      : fallbackMeta.reglas_activas;
  const amenaza = amenazaBackend || fallbackMeta.amenaza_principal;

  return (
    <div className="rules-modal-overlay" onClick={onClose}>
      <div className="rules-modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="rules-modal-header">
          <div>
            <h3>
              {fallbackMeta.icono_alerta} Diagnóstico NASA · {fallbackMeta.nombre}
            </h3>
            <p>{fallbackMeta.subtitulo_clima}</p>
          </div>
          <button
            type="button"
            className="rules-modal-close"
            onClick={onClose}
            aria-label="Cerrar reglas"
          >
            ✕
          </button>
        </div>

        <div className="rules-modal-threat">
          <strong>Amenaza principal de la zona:</strong> {amenaza}
        </div>

        <div className="rules-modal-list">
          {reglas.map((r) => (
            <div key={r.codigo} className="rules-modal-item">
              <div className="rules-modal-item-top">
                <span className="rules-code-badge">{r.codigo}</span>
                <strong>{r.nombre}</strong>
              </div>
              <p className="rules-modal-impact">{r.impacto_metricas}</p>
              {r.factor_climatico && (
                <small className="rules-modal-factor">📡 Dato NASA: {r.factor_climatico}</small>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function TarjetaEstrategia({ e, activa, onElegir, onOpenRules }) {
  const [openComparacion, setOpenComparacion] = useState(false);
  const [openRiesgos, setOpenRiesgos] = useState(false);

  return (
    <article className={`tarjeta ${activa ? 'activa' : ''}`}>
      <header>
        <h3>{e.nombre}</h3>
        {e.is_current ? <span className="insignia azul">Tu situación actual</span> : <span className="insignia azul-suave">Alternativa</span>}
      </header>
      <Medidor estado={e.salud_suelo} />
      <p className="resumen">{e.resumen}</p>
      <h4>Secuencia de cultivos</h4>
      <Secuencia secuencia={e.secuencia} />

      <div className={`acordeon-box comparacion ${openComparacion ? 'abierto' : ''}`}>
        <button
          type="button"
          className="acordeon-summary"
          onClick={() => setOpenComparacion(!openComparacion)}
          aria-expanded={openComparacion}
        >
          <span>Comparación de indicadores</span>
          <span className={`acordeon-flecha ${openComparacion ? 'girada' : ''}`}>▼</span>
        </button>
        <div className="acordeon-desplegable">
          <div className="acordeon-inner">
            {METRICAS.map((m) => (
              <Barrita key={m.key} {...m} valor={e.metricas?.[m.key]} />
            ))}
          </div>
        </div>
      </div>

      {Array.isArray(e.riesgos) && e.riesgos.length > 0 && (
        <div className={`acordeon-box riesgos-box ${openRiesgos ? 'abierto' : ''}`}>
          <div className="riesgos-header-row">
            <button
              type="button"
              className="acordeon-summary riesgos-summary"
              onClick={() => setOpenRiesgos(!openRiesgos)}
              aria-expanded={openRiesgos}
            >
              <span>⚠️ Riesgos en tu región</span>
              <span className={`acordeon-flecha ${openRiesgos ? 'girada' : ''}`}>▼</span>
            </button>
            <button
              type="button"
              className="btn-info-rules"
              onClick={(ev) => {
                ev.preventDefault();
                ev.stopPropagation();
                onOpenRules();
              }}
              title="Ver diagnóstico NASA y reglas activas de tu región"
              aria-label="Ver reglas de la región"
            >
              ℹ️
            </button>
          </div>
          <div className="acordeon-desplegable">
            <div className="acordeon-inner">
              <ul className="riesgos-lista">
                {e.riesgos.map((r, idx) => (
                  <li key={idx}>{r}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      <button className="boton" onClick={() => onElegir(e.id)} aria-pressed={activa}>
        {activa ? 'Estrategia seleccionada ✓' : 'Ver en el calendario'}
      </button>
    </article>
  );
}

function Timeline({ estrategia }) {
  const cob = calcularCobertura(estrategia.secuencia);
  const cnt = mesesDesnudos(estrategia.secuencia);
  return (
    <section className="panel" aria-labelledby="t-titulo">
      <h2 id="t-titulo">📅 Calendario: {estrategia.nombre}</h2>
      <p className="sub">
        {cnt.desnudo > 0
          ? `El suelo queda desnudo ${cnt.desnudo} ${cnt.desnudo === 1 ? 'mes' : 'meses'} y vulnerable ${cnt.vulnerable}.`
          : `El suelo no queda desnudo ningún mes (${cnt.vulnerable} meses de transición).`}
      </p>
      <div className="timeline">
        <div className="tl-fila tl-cab">
          <span className="tl-label" />
          {MESES.map((m, i) => (
            <span key={i} className="tl-mes" title={MESES_LARGO[i]}>
              {m}
            </span>
          ))}
        </div>
        {estrategia.secuencia.map((s, k) => (
          <div className="tl-fila" key={k}>
            <span className="tl-label">{s.cultivo}</span>
            {Array.from({ length: 12 }, (_, i) => {
              const activo = enRango(i + 1, s.desde, s.hasta);
              const siembra = activo && i + 1 === s.desde;
              return (
                <span key={i} className={`tl-celda ${activo ? `on ${s.tipo}` : ''}`}>
                  {siembra ? '🌱' : ''}
                </span>
              );
            })}
          </div>
        ))}
        <div className="tl-fila">
          <span className="tl-label">Estado del suelo</span>
          {cob.map((c, i) => (
            <span key={i} className={`tl-celda estado ${c.estado}`} title={`${MESES_LARGO[i]}: ${c.estado}`} />
          ))}
        </div>
      </div>
      <ul className="leyenda">
        <li><i className="dot verde" /> Cubierto</li>
        <li><i className="dot ambar" /> Vulnerable (recién sembrado / rastrojo)</li>
        <li><i className="dot rojo" /> Desnudo</li>
        <li>🌱 Siembra</li>
      </ul>
    </section>
  );
}

function EvidenciaNasa({ items }) {
  const [abierto, setAbierto] = useState(false);

  return (
    <section className="panel nasa" aria-labelledby="n-titulo">
      <button
        type="button"
        className="nasa-toggle"
        onClick={() => setAbierto(!abierto)}
        aria-expanded={abierto}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <h2 id="n-titulo" style={{ margin: 0 }}>🛰️ ¿Qué detectó la NASA en tu lote?</h2>
          <span className="insignia azul-suave" style={{ fontSize: '11px' }}>
            {items.length} satélites
          </span>
        </div>
        <span className="nasa-toggle-icono">
          {abierto ? '▲ Ocultar detalles' : '▼ Desplegar datos satelitales'}
        </span>
      </button>

      {abierto && (
        <div className="nasa-grid">
          {items.map((it) => (
            <article key={it.satelite} className={`nasa-card ${it.nivel}`}>
              <div className="nasa-cab">
                <span className={`insignia ${it.nivel}`}>{it.satelite}</span>
                <strong>{it.titulo}</strong>
              </div>
              <p>{it.texto}</p>
              <small>{it.dato}</small>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

function AvisoAgronomo() {
  return (
    <aside className="aviso" role="note">
      <span aria-hidden="true">⚠️</span>
      <div>
        <strong>Herramienta de apoyo, no reemplaza a tu agrónomo.</strong>
        <p>Los resultados son estimaciones. Validá cualquier cambio de rotación con tu ingeniero agrónomo de confianza antes de decidir.</p>
      </div>
    </aside>
  );
}

function PanelHistorialDecision({ diag, profile, seleccionada, onSaveDecision }) {
  const [abierto, setAbierto] = useState(false);
  const [savedId, setSavedId] = useState(null);
  const campanas = profile?.historial_campanas || [];

  const resumen =
    diag?.resumen_historial ||
    (campanas.length > 0
      ? `${campanas.length} campaña(s) en tu historial (${campanas
          .map((c) => `${c.campana}: ${c.cultivo}`)
          .join(', ')})`
      : null);

  if (!resumen) return null;

  const impactos =
    Array.isArray(diag?.impacto_decisiones) && diag.impacto_decisiones.length > 0
      ? diag.impacto_decisiones
      : [
          'Se analizaron tus campañas previas para penalizar la repetición de monocultivo y priorizar cultivos que recuperen cobertura y fertilidad.',
        ];

  const handleGuardar = () => {
    if (!seleccionada || !onSaveDecision) return;
    onSaveDecision(seleccionada);
    setSavedId(seleccionada.id);
  };

  return (
    <section
      className={`panel historial-decision-panel ${abierto ? 'abierto' : ''}`}
      aria-label="Diagnóstico por historial de campañas"
    >
      <button
        type="button"
        className="historial-toggle"
        onClick={() => setAbierto(!abierto)}
        aria-expanded={abierto}
      >
        <div className="historial-toggle-left">
          <h3>📋 Decisiones futuras guiadas por tu Historial de Campañas</h3>
          <span className="insignia verde" style={{ fontSize: '11px' }}>
            {campanas.length || diag?.campanas_analizadas || 1} campaña(s)
          </span>
        </div>
        <span className="historial-toggle-icono">
          {abierto ? '▲ Ocultar detalles' : '▼ Ver diagnóstico e impacto'}
        </span>
      </button>

      <div className={`acordeon-desplegable ${abierto ? 'abierto' : ''}`}>
        <div className="acordeon-inner">
          <div className="historial-decision-body">
            <div className="historial-decision-top">
              <p className="sub" style={{ margin: 0 }}>
                <strong>Antecedentes del lote:</strong> {resumen}
              </p>
              {seleccionada && onSaveDecision && (
                <button
                  type="button"
                  className={`btn-save-decision ${savedId === seleccionada.id ? 'saved' : ''}`}
                  onClick={handleGuardar}
                >
                  {savedId === seleccionada.id
                    ? '✓ Decisión futura guardada en tu perfil'
                    : `💾 Guardar "${seleccionada.nombre}" para próxima campaña`}
                </button>
              )}
            </div>
            <ul className="historial-impacto-lista">
              {impactos.map((imp, i) => (
                <li key={i}>{imp}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}

// Bloques 2 y 3. Props opcionales: `simulacion` (objeto ya cargado) o `params` para el fetch.
export default function DecisionBoard({
  simulacion,
  params,
  isLoading: propLoading,
  profile,
  onSaveDecision,
}) {
  const { data: fetched, loading: hookLoading, mock } = useSimulation(simulacion ? null : params);
  const sim = simulacion ?? fetched;
  const isMock = !simulacion && mock;
  const estaCargando = propLoading || hookLoading;

  const [sel, setSel] = useState(null);
  const [vista, setVista] = useState('lado'); // 'lado' | 'selector'
  const [isRulesModalOpen, setIsRulesModalOpen] = useState(false);

  const estrategias = sim?.estrategias || [];
  const seleccionada = estrategias.find((e) => e.id === sel) ?? estrategias[0];
  const visibles = vista === 'lado' ? estrategias : [seleccionada].filter(Boolean);
  const nombreLote = sim?.lote?.nombre || sim?.tierra_nombre || 'Campo en San Luis';
  const activeRegionKey = sim?.lote?.region || params?.region || params?.zona || 'centro';
  const amenazaRegional = sim?.lote?.amenaza_regional;

  return (
    <div className="decision">
      {isMock && <div className="mock-tag">Datos de ejemplo (seleccioná tu región y tocá Simular Rotaciones)</div>}
      {estaCargando && <p className="sub">Calculando estrategias y aplicando reglas regionales con datos NASA…</p>}
      <AvisoAgronomo />
      <PanelHistorialDecision
        diag={sim?.diagnostico_historial}
        profile={profile}
        seleccionada={seleccionada}
        onSaveDecision={onSaveDecision}
      />

      <section aria-labelledby="c-titulo">
        <div className="barra-titulo">
          <div>
            <h2 id="c-titulo">Comparador de 3 estrategias — {nombreLote}</h2>
            {amenazaRegional && (
              <p className="sub" style={{ marginTop: 4, marginBottom: 0, fontSize: '13px' }}>
                🎯 <strong>Amenaza regional evaluada:</strong> {amenazaRegional}
              </p>
            )}
          </div>
          <div className="selector" role="group" aria-label="Modo de vista">
            <button className={vista === 'lado' ? 'on' : ''} onClick={() => setVista('lado')}>Lado a lado</button>
            <button className={vista === 'selector' ? 'on' : ''} onClick={() => setVista('selector')}>Una por una</button>
          </div>
        </div>
        {vista === 'selector' && (
          <div className="pestanas" role="tablist">
            {estrategias.map((e) => (
              <button
                key={e.id}
                role="tab"
                aria-selected={seleccionada && e.id === seleccionada.id}
                className={seleccionada && e.id === seleccionada.id ? 'on' : ''}
                onClick={() => setSel(e.id)}
              >
                {e.nombre}
              </button>
            ))}
          </div>
        )}
        <div className={`tarjetas ${vista}`}>
          {visibles.map((e) => (
            <TarjetaEstrategia
              key={e.id}
              e={e}
              activa={seleccionada && e.id === seleccionada.id}
              onElegir={setSel}
              onOpenRules={() => setIsRulesModalOpen(true)}
            />
          ))}
        </div>
      </section>

      {seleccionada && <Timeline estrategia={seleccionada} />}
      <EvidenciaNasa items={sim?.evidencia_nasa || []} />

      <ReglasModal
        isOpen={isRulesModalOpen}
        onClose={() => setIsRulesModalOpen(false)}
        regionKey={activeRegionKey}
        reglasBackend={sim?.reglas_regionales}
        amenazaBackend={amenazaRegional}
      />
    </div>
  );
}
