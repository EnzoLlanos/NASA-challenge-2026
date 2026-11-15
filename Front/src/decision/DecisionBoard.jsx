import { useState } from 'react';
import { useSimulation } from './api.js';
import './decision.css';

const MESES = ['E', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];
const MESES_LARGO = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];

const METRICAS = [
  { key: 'agua', label: 'Agua', icon: '💧', hint: 'Uso eficiente del agua' },
  { key: 'nutrientes', label: 'Nutrientes', icon: '🌱', hint: 'Fertilidad del suelo' },
  { key: 'erosion', label: 'Protección contra erosión', icon: '🛡️', hint: 'Menos suelo perdido' },
  { key: 'margen', label: 'Margen', icon: '💰', hint: 'Ganancia esperada' },
];

// Semáforo: verde >= 70, amarillo/rojo según valor
function semaforo(v) {
  if (v >= 70) return { clase: 'verde', texto: 'Saludable' };
  if (v >= 45) return { clase: 'ambar', texto: 'Regular' };
  return { clase: 'rojo', texto: 'En riesgo' };
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

function Medidor({ valor }) {
  const s = semaforo(valor);
  const r = 52;
  const circ = Math.PI * r; // semicírculo
  return (
    <div className={`medidor ${s.clase}`} role="img" aria-label={`Salud del suelo ${valor}%, ${s.texto}`}>
      <svg viewBox="0 0 120 70">
        <path d="M8 62 A52 52 0 0 1 112 62" className="medidor-fondo" />
        <path
          d="M8 62 A52 52 0 0 1 112 62"
          className="medidor-valor"
          strokeDasharray={`${(circ * valor) / 100} ${circ}`}
        />
      </svg>
      <div className="medidor-num">{valor}%</div>
      <span className={`insignia ${s.clase}`}>{s.texto}</span>
    </div>
  );
}

function Barrita({ icon, label, valor, hint }) {
  const s = semaforo(valor);
  return (
    <div className="barrita" title={hint}>
      <div className="barrita-top">
        <span>
          {icon} {label}
        </span>
        <strong>{valor}</strong>
      </div>
      <div className="barrita-pista">
        <div className={`barrita-relleno ${s.clase}`} style={{ width: `${valor}%` }} />
      </div>
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

function TarjetaEstrategia({ e, activa, onElegir }) {
  return (
    <article className={`tarjeta ${activa ? 'activa' : ''}`}>
      <header>
        <h3>{e.nombre}</h3>
        {e.is_current ? <span className="insignia azul">Tu situación actual</span> : <span className="insignia azul-suave">Alternativa</span>}
      </header>
      <Medidor valor={e.salud_suelo} />
      <p className="resumen">{e.resumen}</p>
      <h4>Secuencia de cultivos</h4>
      <Secuencia secuencia={e.secuencia} />
      <h4>Comparación</h4>
      {METRICAS.map((m) => (
        <Barrita key={m.key} {...m} valor={e.metricas[m.key]} />
      ))}
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

// Bloques 2 y 3. Props opcionales: `simulacion` (objeto ya cargado) o `params` para el fetch.
export default function DecisionBoard({ simulacion, params }) {
  const { data: fetched, loading, mock } = useSimulation(params);
  const sim = simulacion ?? fetched;
  const [sel, setSel] = useState(null);
  const [vista, setVista] = useState('lado'); // 'lado' | 'selector'

  const seleccionada = sim.estrategias.find((e) => e.id === sel) ?? sim.estrategias[0];
  const visibles = vista === 'lado' ? sim.estrategias : [seleccionada];

  return (
    <div className="decision">
      {mock && <div className="mock-tag">Datos de ejemplo (simulación mock)</div>}
      {loading && <p className="sub">Calculando estrategias…</p>}
      <AvisoAgronomo />

      <section aria-labelledby="c-titulo">
        <div className="barra-titulo">
          <h2 id="c-titulo">Comparador de 3 estrategias — {sim.lote.nombre}</h2>
          <div className="selector" role="group" aria-label="Modo de vista">
            <button className={vista === 'lado' ? 'on' : ''} onClick={() => setVista('lado')}>Lado a lado</button>
            <button className={vista === 'selector' ? 'on' : ''} onClick={() => setVista('selector')}>Una por una</button>
          </div>
        </div>
        {vista === 'selector' && (
          <div className="pestanas" role="tablist">
            {sim.estrategias.map((e) => (
              <button
                key={e.id}
                role="tab"
                aria-selected={e.id === seleccionada.id}
                className={e.id === seleccionada.id ? 'on' : ''}
                onClick={() => setSel(e.id)}
              >
                {e.nombre}
              </button>
            ))}
          </div>
        )}
        <div className={`tarjetas ${vista}`}>
          {visibles.map((e) => (
            <TarjetaEstrategia key={e.id} e={e} activa={e.id === seleccionada.id} onElegir={setSel} />
          ))}
        </div>
      </section>

      <Timeline estrategia={seleccionada} />
      <EvidenciaNasa items={sim.evidencia_nasa} />
    </div>
  );
}
