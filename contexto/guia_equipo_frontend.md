# 🎯 Guía de comienzo: Equipo Frontend (2 personas)

## 📍 Estado actual del proyecto
- **Estructura React + Vite**: Ya existe en `Front/src/`, `Front/package.json`
- **Backend API**: En desarrollo por equipo Backend (endpoints mock esperados)
- **Dataset**: NASA POWER procesado disponible para cuándo el frontend necesite datos reales
- **Objetivo**: Construir interfaz de usuario interactiva que muestre mapa, sliders de prioridades y comparador de rotaciones

## 👥 Integración del equipo
- 2 personas encargadas del frontend
- Necesitan coordinarse con:
  - **Equipo Backend**: Para contrato API (`schemas.py`), endpoints y datos mock
  - **Equipo Datos**: Para estructura de datos (`power_monthly.csv`, `crops.yaml`) cuándo estén listos

## 🚀 Paso 1: Verificar y preparar entorno (30 min)

```bash
# 1. Moverse al directorio frontend
cd Front

# 2. Instalar dependencias si es necesario
npm install  # o yarn install

# 3. Verificar que el proyecto corre
npm run dev  # Debería iniciar Vite en localhost:5173

# 4. Explorar estructura actual
ls -la src/ components/ pages/ api/ 2>/dev/null

# 5. Revisar package.json para ver qué ya está instalado
cat package.json | head -30
```

### Estructura esperada (según documento contexto):

```
frontend/
├─ package.json
├─ vite.config.js
├─ src/
│  ├─ api/           # cliente de la API
│  ├─ components/    # Map, PriorityPanel, RotationCompare,
│  │  │              # EvidenceCard, Glossary, DataGapsBadge
│  │  └─ pages/
│  │     └─ App.jsx
│  ├─ index.css
│  ├─ main.jsx
│  └─ ...
├─ public/
│  └─ favicon.svg
└─ index.html
```

## 🗺️ Paso 2: Configurar mapa base (1 hora)

El documento contexto recomienda **Leaflet o MapLibre** (no Google Maps).

### Opción A: Leaflet (más sencillo, sin licencia)

```bash
# Instalar dependencias
npm install leaflet @leaflet/react
# O solo leaflet si usan uso directo

# En vite.config.js si es necesario
# Criar componente Map.jsx

# Ejemplo uso:
import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer, Marker, useMap } from 'react-leaflet';

const Map = ({center, zoom, children}) => {
  return (
    <MapContainer
      center={center}  // [lat, lon]
      zoom={zoom || 7}
      style={{height: '400px', width: '100%'}}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      >
      {children}
      </TileLayer>
    </MapContainer>
  );
};
```

### Opción B: MapLibre (recomendado en contexto, más moderno)

```bash
# Instalar
npm install @maplibre/maplibre-gl-leaflet
# O packages específicos según docs

# Ventaja: mejor rendimiento, vector tiles, control más fino
```

### Ubicar mapa en la pantalla principal:

```jsx
// src/pages/Dashboard.jsx
import Map from '../components/Map';
import PriorityPanel from '../components/PriorityPanel';

export const Dashboard = () => {
  const [center, setCenter] = useState([-33.30, -65.30]); // San Luis por defecto
  const [zoom, setZoom] = useState(7);
  
  return (
    <div className="p-4">
      <h2 className="mb-4">Herramienta de Apoyo a la Decisión</h2>
      <SupportReminder />  // Componente que siempre recuerda: "herramienta de apoyo"
      <Map center={center} zoom={zoom} />
      <PriorityPanel />
    </div>
  );
};
```

## 🎚️ Paso 3: Implementar PriorityPanel (1.5 horas)

### Componente slider de prioridades (según Sección 9 del contexto):
> `sliders del agricultor (agua, ingresos, suelo, erosión)`

```jsx
// src/components/PriorityPanel.jsx
import { Slider, Rating, Stack } from 'react-bootstrap'; // O Tailwind equivalents
import { useState } from 'react';

export const PriorityPanel = () => {
  // Estados de prioridades (0.0 a 1.0)
  const [priorities, setPriorities] = useState({
    agua: 0.4,
    ingresos: 0.3,
    suelo: 0.2,
    erosion: 0.1
  });

  const handleChange = (priority, value) => {
    setPriorities({ ...priorities, [priority]: value });
    // Opcional: enviar al backend inmediatamente
    // fetch('/api/rotations', { method: 'POST', body: JSON.stringify({priorities}) })
  };

  return (
    <Stack gap={3} className="p-4 border rounded">
      <h5>Prioridades de tu finca</h5>
      
      {/* Agua */}
      <div className="mb-3">
        <label>Demanda de agua <span>{priorities.agua}</span></label>
        <Slider 
          min={0} 
          max={1} 
          step={0.1} 
          value={priorities.agua} 
          onChange={(e) => handleChange('agua', parseFloat(e.target.value))}
        />
        <small>Prioridad: impacto en selección de cultivos por disponibilidad hídrica</small>
      </div>
      
      {/* Ingresos */}
      <div className="mb-3">
        <label>Potencial de ingresos <span>{priorities.ingresos}</span></label>
        <Slider 
          min={0} 
          max={1} 
          step={0.1} 
          value={priorities.ingresos} 
          onChange={(e) => handleChange('ingresos', parseFloat(e.target.value))}
        />
        <small>Prioridad: cultivos con mejor retorno económico</small>
      </div>
      
      {/* Suelo */}
      <div className="mb-3">
        <label>Conservación de suelo <span>{priorities.suelo}</span></label>
        <Slider 
          min={0} 
          max={1} 
          step={0.1} 
          value={priorities.suelo} 
          onChange={(e) => handleChange('suelo', parseFloat(e.target.value))}
        />
        <small>Prioridad: rotaciones que mejoren salud del suelo</small>
      </div>
      
      {/* Erosión */}
      <div className="mb-3">
        <label>Riesgo de erosión <span>{priorities.erosion}</span></label>
        <Slider 
          min={0} 
          max={1} 
          step={0.1} 
          value={priorities.erosion} 
          onChange={(e) => handleChange('erosion', parseFloat(e.target.value))}
        />
        <small>Prioridad: rotaciones que reduzcan pérdida de suelo</small>
      </div>
      
      <small className="text-muted">
        *Los sliders definen el peso en el motor de puntuación. 
        Los valores deben sumar aproximadamente 1.0.
      </small>
    </Stack>
  );
};
```

### Estilo con Tailwind (según documento contexto):

```jsx
// Usando Tailwind directamente (recomendado en contexto por "Evita perder tiempo en CSS")
<div className="space-y-4">
  <h5 className="font-medium">Prioridades de tu finca</h5>
  
  <div>
    <label className="block text-sm mb-1">Agua</label>
    <input 
      type="range" 
      min="0" 
      max="1" 
      step="0.1" 
      value={priorities.agua} 
      onChange={(e) => setPriorities({...priorities, agua: parseFloat(e.target.value)})}
      className="w-full h-2 rounded bg-blue-200"
    />
    <span className="text-xs text-gray-600">{priorities.agua}</span>
  </div>
  
  {/* ... resto de sliders ... */}
</div>
```

## 📊 Paso 4: Componente RotationCompare (2 horas)

### Mostrar 3+ estrategias con EvidenceCard (según contrato API):

```jsx
// src/components/RotationCompare.jsx
import { Card, Button } from 'react-bootstrap';
import { useState, useEffect } from 'react';

// Mock data until backend is ready
const MOCK_STRATEGIES = [
  {
    name: "Maíz → Soja",
    isCurrent: true,
    score: 0.65,
    why: "Buena combinación clásica para región semi-árida",
    benefits: ["Menor demanda de agua en verano", "Rentabilidad comprobada"],
    evidence: [
      {"dataset": "NASA POWER", "finding": "Lluvia en verano -18% vs. 2000-2010", "resolution": "0.5° / diario", "period": "2000-2025"}
    ],
    data_gaps: ["No hay mediciones de suelo a nivel de lote"],
    risks_to_validate: ["Revisar con un técnico local la fecha de siembra"]
  },
  {
    name: "Soja → Trigo",
    isCurrent: false,
    score: 0.72,
    why: "Mejor distribución de demanda hídrica estival",
    benefits: ["Menor estrés hídrico julio-agosto", "Rotación fijadora de nitrógeno"],
    evidence: [
      {"dataset": "NASA POWER", "finding": "Estrés hídrico reducido 22% en rotación soja-trigo", "resolution": "0.5° / diario", "period": "2000-2025"}
    ],
    data_gaps: ["Requiere validación local de adaptabilidad de trigo"],
    risks_to_validate: ["Precio de trigo en mercado local 2024"]
  },
  {
    name: "Maíz → Soja → Cultivo de cobertura",
    isCurrent: false,
    score: 0.78,
    why: "Mejorará salud del suelo y reducirá demanda verano",
    benefits: ["Añade materia orgánica", "Interrumpe ciclos de plagas", "Menor demanda agua verano"],
    evidence: [
      {"dataset": "NASA POWER", "finding": "Evapotranspiración -15% con cultivo de cobertura", "resolution": "0.5° / diario", "period": "2000-2025"}
    ],
    data_gaps: ["Costo adicional de semilla de cobertura"],
    risks_to_validate: ["Fecha de siembra del cubierta después de maíz"]
  }
];

export const RotationCompare = ({priorities}) => {
  const [strategies, setStrategies] = useState(MOCK_STRATEGIES);
  
  // Si hay prioridades del panel, podríamos fetch al backend
  // Pero con mock se mantiene funcionalidad
  
  return (
    <div className="space-y-4">
      <h5 className="font-medium">Comparación de estrategias de rotación</h5>
      
      {strategies.map((strat, i) => (
        <Card key={i} className="p-4 hover:shadow-xl transition-shadow">
          <div className="flex justify-between items-start">
            <div>
              <h6 className="font-semibold">{strat.name}</h6>
              <p className="text-sm text-gray-500">{strat.why}</p>
              <DataGapsBadge gaps={strat.data_gaps} />
            </div>
            <div className="text-right">
              <p className="text-2xl font-bold text-blue-600">{strat.score}</p>
              <p className="text-xs text-gray-500">Score</p>
            </div>
          </div>
          
          <ul className="mt-3 space-y-1 text-sm">
            {strat.benefits.map((b, j) => (
              <li key={j} className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>{b}</span>
              </li>
            ))}
          </ul>
          
          <div className="mt-3 pt-3 border-t">
            <p className="text-xs text-gray-500">Evidencia:</p>
            <ul className="space-y-1 text-xs">
              {strat.evidence.map((ev, j) => (
                <li key={j} className="text-gray-600">
                  <strong>{ev.dataset}:</strong> {ev.finding}
                  <div className="text-xs mt-1">
                    resolución: {ev.resolution} | período: {ev.period}
                  </div>
                </li>
              ))}
            </ul>
            
            <p className="mt-2 text-xs text-red-500">
              Riesgos: {strat.risks_to_validate.join(". ")}
            </p>
          </div>
        </Card>
      ))}
    </div>
  );
};
```

### Componente DataGapsBadge (recordatorio honesto):

```jsx
// src/components/DataGapsBadge.jsx
import { Badge } from 'react-bootstrap'; // O styled-component/Tailwind

export const DataGapsBadge = ({gaps}) => {
  return (
    <Badge variant="secondary" className="text-xs mt-2">
      <strong>Brechas de información:</strong> {gaps.join(". ")}.
    </Badge>
  );
};
```

### Componente EvidenceCard (alternativa más simple):

```jsx
// src/components/EvidenceCard.jsx
export const EvidenceCard = ({evidence}) => {
  if (!evidence || evidence.length === 0) {
    return <p className="text-sm text-gray-500">Sin evidencia disponible</p>;
  }
  
  return (
    <div className="p-3 bg-blue-50 rounded border border-blue-200 text-xs">
      <p className="font-medium">Evidencia científica:</p>
      <p className="text-gray-700 line-clamp-2">
        {evidence[0].finding}
      </p>
      <div className="mt-1 text-xs text-gray-500">
       Fuente: {evidence[0].dataset} | {evidence[0].resolution} | {evidence[0].period}
      </div>
    </div>
  );
};
```

## 📝 Paso 5: Glosario agrícola (1 hora)

### Componentes que siempre deben aparecer (Principio diseño centrado en agricultor):

```jsx
// src/components/Glossary.jsx
export const Glossary = () => {
  const terms = {
    evapotranspiración: "Cantidad de agua que se evapora del suelo y traspira las plantas, expresada en mm/día.",
    ndvi: "Índice de Vegetación de Diferencia Normalizada. Mide la salud y densidad vegetal (valores -1 a 1).",
    helada: "Cuando la temperatura mínima llega a 0°C o abajo, puede dañar tejidos de los cultivos.",
    ola_calor: "Período de al menos 3 días consecutivos con temperatura máxima ≥ 35°C.",
    estrés_hídrico: "Situación cuando la demanda de agua supera la disponibilidad (precipitación + humedad suelo).",
    rotacion: "Secuencia de cultivos en el tiempo en el mismo terreno para mejorar salud del suelo y reducir plagas."
  };
  
  return (
    <aside className="bg-gray-50 p-4 rounded sticky top-44">
      <h5 className="font-medium mb-3">Glosario rápido</h5>
      <dl>
        {Object.entries(terms).map(([term, definition]) => (
          <div key={term} className="mb-2">
            <dt className="font-medium">{term}</dt>
            <dd className="text-sm text-gray-600">{definition}</dd>
          </div>
        ))}
      </dl>
    </aside>
  );
};
```

### Soporte reminder (siempre visible):

```jsx
// src/components/SupportReminder.jsx
export const SupportReminder = () => {
  return (
    <div className="p-3 bg-yellow-100 border-y border-l border-orange-400 rounded text-sm">
      <p className="font-medium">🛈 Esta herramienta es de APOYO a la decisión, NO reemplaza el juicio del agricultor ni la experiencia agronómica local.</p>
    </div>
  );
};
```

Debería aparecer en cada pantalla principal, probablemente como componente padre o en layout global.

## 🔌 Paso 6: Conectar con API mock (30 min)

### api client setup:

```javascript
// src/api/apiClient.js
import axios from 'axios';

// Base URL del backend (mock durante desarrollo, real cuando esté listo)
const API_BASE = 'http://localhost:8000/api';

// Función helper para todas las peticiones
export const api = {
  // GET /api/crops
  getCrops: () => axios.get(`${API_BASE}/api/crops`).then(r => r.data),
  
  // GET /api/field-profile?lat=&lon=
  getFieldProfile: (lat, lon) => axios.get(`${API_BASE}/api/field-profile`, { params: { lat, lon } }).then(r => r.data),
  
  // POST /api/rotations
  calculateRotations: (request) => axios.post(`${API_BASE}/api/rotations`, request).then(r => r.data),
  
  // Si el backend tiene webhook o SSE para actualizaciones en tiempo real
  // priorityUpdate: (priorities) => axios.post(`${API_BASE}/priority`, { priorities })
};
```

### Usarlo en componentes:

```jsx
// En PriorityPanel.jsx o RotationCompare.jsx
import { api } from '../api/apiClient';

const handlePrioritiesChange = async (newPriorities) => {
  setPriorities(newPriorities);
  
  try {
    const result = await api.calculateRotations({
      location: { lat: -33.30, lon: -65.30, name: "San Luis" },
      current_rotation: ["maíz", "soja"],
      priorities: newPriorities
    });
    // Actualizar state con los nuevos resultados
    setStrategies(result.strategies);
  } catch (error) {
    console.error("Error calculando rotaciones:", error);
    // Fallback a mock data
  }
};
```

## 📱 Paso 7: Probar y depurar (30 min)

```bash
# 1. Asegurarse que el servidor Vite corre
npm run dev

# 2. Probar en navegador:
# - Ir a http://localhost:5173
# - Verificar que el mapa cargue con San Luis centro
# - Probar sliders y mover valores
# - Ver que las estrategias de rotación cambien según sliders (o usen mock estático)
# - Verificar que el "SupportReminder" aparezca en cada pantalla

# 3. Probar conexión con backend mock
# En consola del navegador:
import { api } from './api/apiClient';
api.getCrops().then(console.log);
api.getFieldProfile(-33.30, -65.30).then(console.log);
```

### ✅ Checklist "Hecho" para el equipo Frontend:

- [ ] Mapa base cargando en localhost:5173 (Leaflet o MapLibre)
- [ ] Componente PriorityPanel con 4 sliders (agua, ingresos, suelo, erosión) funcionando
- [ ] Priorities state se actualiza y puede enviarse al backend
- [ ] Componente RotationCompare muestra 3+ estrategias con score, why, benefits, evidence
- [ ] DataGapsBadge aparece mostrando brechas honestas
- [ ] Glossary component integrado en layout
- [ ] SupportReminder visible en todas las pantallas
- [ ] API client conectado con endpoints mock del backend
- [ ] `npm run dev` corre sin errores críticos
- [ ] Diseño responsive para móvil/tablet considerado (aunque foco en desktop para demo)

### 📝 Notas importantes para el equipo Frontend:

1. **Siempre el aviso de apoyo**: Cada pantalla debe tener el `SupportReminder` visible. El documento contexto es enfático: "dejar claro que es una herramienta de apoyo: no reemplaza el juicio del agricultor ni la experiencia agronómica local".

2. **Lenguaje simple**: Todo el texto debe estar en lenguaje claro, sin tecnicismos sin explicar. El glosario es obligatorio.

3. **Unidades en sliders**: Los sliders van de 0 a 1 (o 0% a 100%), pero deben mostrarse con el significado claro. Ej: "Agua: 0.4 = prioridad media-alta para disponibilidad hídrica".

4. **EvidenceCard diseño**: Las evidencias deben verse como citas científicas, no como texto largo. Usar formato corto: "Dataset: hallazgo | resolución | período".

5. **Map center**: Por defecto debería ser San Luis (`[-33.30, -65.30]`), pero permitir búsqueda o desplazamiento.

6. **Integración progresiva**: Empezar con mock data del backend. Cuando el backend esté listo con endpoints reales, solo cambiar la `API_BASE` en `apiClient.js` y ya debería funcionar (gracias a los schemas Pydantic consistentes).

7. **Tailwind vs Bootstrap**: El documento contexto recomienda **Tailwind** para evitar perder tiempo en CSS. Pero si el equipo ya conoce Bootstrap, pueden usarlo. Lo importante es no pasar horas en diseño visual.

8. **Plan B video**: Si al final no se logra la integración backend-frontend en tiempo real, grabar video recorriendo las pantallas con datos mock estáticos. El contexto lo recomienda fuertemente para la demo final.

9. **Merge a main**: Cada 2-3 horas, hacer merge a `main` y asegurar que todo corra (Sección 9 del contexto).

10. **Responsive**: Diseñar primero para viewport desktop (más fácil en 1 día), pero intentar que en móvil funcione lo esencial (mapa + prioridades).

---

## 🧩 Próximos pasos inmediatos para el equipo

**Hora 1-2:** Setup del proyecto, mapa base funcionando con San Luis center, PriorityPanel con sliders.

**Hora 2-4:** RotationCompare con 3 estrategias mock + EvidenceCard + DataGapsBadge.

**Hora 4-6:** Integrar API client, conectar con backend mock, probar flujo completo.

**Hora 6-8:** Agregar Glossary y SupportReminder a layout principal, testing final.

¿Necesita el equipo frontend alguna ayuda específica para empezar? Pueden consultar el documento `contexto/plan_trabajo_paralelo.md` para ver cómo esto conecta con los otros equipos.