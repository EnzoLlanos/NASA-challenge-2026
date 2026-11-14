# 📋 Plan de Trabajo Paralelo: NASA Challenge 2026

## 🕒 Contexto
Tras completar el **Step 1** del pipeline de datos NASA POWER (descarga y limpieza para San Luis, Argentina), el equipo puede avanzar en múltiples frentes simultáneamente dado el límite de **1 día** y **6 personas**.

El pipeline de datos quedó funcionando y generó:
- `data/raw/power_san_luis_argentina.json` (1.5 MB)
- `data/processed/power_daily.csv` (1.7 KB)
- `data/processed/power_monthly.csv` (8.3 KB)

## 👥 Reparto de Roles (6 personas)

| Rol | Enfoque | Entregable Principal | Tecnologías |
|---|---|---|---|
| **Datos 1** | Pipeline climático avanzado | Indicadores estacionales, tendencias | Python, pandas, xarray |
| **Datos 2** | NDVI y vegetación | Series de tiempo vegetación | Python, earthaccess, AppEEARS |
| **Lógica Rotación** | Motor de puntuación | `scoring/engine.py` + explicaciones | Python, Pydantic |
| **Frontend** | Interfaz usuario | Map, sliders, comparador | React + Vite, Leaflet/MapLibre, Recharts |
| **Diseño/UX** | Experiencia agricultor | Pantallas, glosario, diseño | Tailwind, Figma (o Herramienta similar) |
| **Coordinación/Pitch** | Integración y story | Video pitch, documentación | Markdown, herramientas de video |

---

## 🎯 Frente 1: Datos Avanzados (Datos 1 + Datos 2)

### Datos 1: Indicadores Climáticos Estacionales
**Objetivo:** Calcular tendencias y características estacionales desde el dataset POWER ya procesado.

**Tareas:**
- Tendencia de lluvia anual (2000-2025)
- Aumento de días de calor (>35°C)
- Frecuencia de heladas (temp_min ≤ 0°C)
- Estación seca vs. húmeda identification

**Herramientas:**
- Python 3.12
- pandas, numpy
- xarray para datos geoespaciales
- matplotlib/seaborn para visualizaciones

**Archivos a crear:**
- `pipeline/indicadores_estacionales.py` - Script que lee `power_monthly.csv` y genera reporte
- `docs/indicadores_climaticos.md` - Documento con hallazgos

### Datos 2: Integración NDVI/MODIS
**Objetivo:** Añadir información de vegetación aunque sea con datos globales.

**Tareas:**
- Verificar viabilidad de AppEEARS o earthaccess para NDVI por punto
- Si no da tiempo: usar datos de síntesis o mock con comportamiento realista
- Calcular "días de campo desnudo" basados en NDVI threshold

**Herramientas:**
- `earthaccess` (si hay cuenta Earthdata)
- AppEEARS API de NASA
- Python requests para llamadas a API
- `plotly` para gráficos interactivos

**Nota:** El documento contexto recomienda evitar datasets extras no imprescindibles. Priorizar con **MOCK** que se integra al sistema y luego reemplazar con datos reales.

---

## 🎯 Frente 2: Motor de Puntuación y Lógica (Lógica Rotación)

### Objetivo Implementar el motor descrito en la Sección 8 del contexto.

**Estructura propuesta:**
```
backend/app/scoring/
├── engine.py        # Puntaje de rotaciones
└── explain.py       # Genera "por qué", evidencia, riesgos, brechas
```

**Fórmulas definidas en el contexto:**
1. El puntaje es suma ponderada de qué tan bien los cultivos responden a indicadores
2. Pesos vienen de sliders del agricultor (agua, ingresos, suelo, erosión)
3. `explain.py` convierte términos del puntaje en frases con evidencia citable

**Entrada esperada (según contrato API):**
```json
POST /api/rotations
{
  "location": {"lat": -33.30, "lon": -65.30},
  "current_rotation": ["maíz", "soja"],
  "priorities": {"agua": 0.4, "ingresos": 0.3, "suelo": 0.2, "erosion": 0.1}
}
```

**Salida:**
```json
{
  "name": "Maíz → Soja → Cultivo de cobertura",
  "is_current": false,
  "score": 0.74,
  "why": "Texto corto en lenguaje simple",
  "benefits": ["Menor demanda de agua en verano", "..."],
  "evidence": [
    {"dataset": "NASA POWER", "finding": "Lluvia en verano -18% vs. 2000-2010", "resolution": "0.5° / diario", "period": "2000-2025"}
  ],
  "data_gaps": ["No hay mediciones de suelo a nivel de lote"],
  "risks_to_validate": ["Revisar con un técnico local la fecha de siembra"]
}
```

**Tareas:**
- Crear `data/crops.yaml` con rasgos de cultivos adaptables a San Luis
- Implementar `engine.py` con cálculo ponderado
- Implementar `explain.py` con generación de texto automático
- Probar con datos mock primero (hora 2 del cronograma)

**Herramientas:**
- Python 3.12
- Pydantic para schemas de API
- YAML para configuración de cultivos

---

## 🎯 Frente 3: Frontend Interactivo (React + Vite)

### Estado actual del Front
El proyecto ya tiene estructura React + Vite en `Front/src/` y `Front/package.json`.

### Tareas prioritarias (Horas 1-12 según cronograma)

**Hora 1-2: Esqueletos y mock data**
- Definir schemas en `backend/app/schemas.py` (contrato API)
- Crear mock responses en frontend que imiten la estructura real
- Conectar `api/` client con endpoints falsos

**Hora 2-6: Mapas y capas**
- Implementar mapa base con Leaflet o MapLibre
- Añadir capa de prioridades (slider)
- Superponer indicadores climáticos (temperatura, lluvia)
- Slider de prioridades: agua, ingresos, suelo, erosión

**Hora 6-12: Comparador de rotaciones**
- Componente `RotationCompare` que muestra 3+ estrategias
- `EvidenceCard` por cada estrategia con hallazgos
- `DataGapsBadge` que muestre brechas de información

### Estructura de componentes sugerida (del documento contexto):

```
frontend/src/components/
├─ Map/              # Mapa con capas climáticas
├─ PriorityPanel/    # Sliders de prioridades del agricultor
├─ RotationCompare/  # Comparador de 3+ rotaciones
├─ EvidenceCard/     # Card por cada estrategia con "por qué", beneficios
├─ DataGapsBadge/    # Indicador de brechas de información
├─ Glossary/         # Glosario de términos (evapotranspiración, NDVI, etc.)
└─ DataGapsBadge/    # Recordatorio de que es herramienta de apoyo
```

### Entregables:
- `Frontend/src/api/api.ts` - Cliente API con mock y real
- `Frontend/src/pages/` - Páginas principales (home, dashboard, comparison)
- `Frontend/src/styles/` - Estilos Tailwind consistentes

**Herramientas:**
- React 18 + Vite 5
- Leaflet + MapLibre (recomendado en contexto)
- Recharts o Chart.js para gráficos
- Tailwind CSS para estilos
- TypeScript (recomendado para schemas)

---

## 🎯 Frente 4: Diseño Centrado en el Agricultor (UX)

### Objetivo: Garantizar que la herramienta "apoye y no reemplace" el juicio del agricultor.

**Principios del documento contexto:**
- Interfaz simple, lenguaje claro
- Agricultor ingresa sus propias prioridades y restricciones
- Recordatorios claros de que es herramienta de apoyo
- No reemplaza juicio agronómico local

**Tareas:**
- Definir glosario de términos clave (evapotranspiración, anomalías humedad suelo, NDVI, riesgo heladas)
- Diseñar screens de ingreso de prioridades (slider 0-1)
- Crear tarjetas de explicación que muestren "por qué" una rotación tiene ese score
- Diseñar badges de brechas de información (con honestidad técnica)
- Definir lenguaje para pantallas de "apoyo a la decisión"

**Entregables:**
- `docs/glosario_agronomico.md`
- Diseños de pantallas (Figma o sketch)
- Componente `SupportReminder` que siempre aparezca en pantalla

---

## 🎯 Frente 5: Coordinación y Pitch (Cross-functional)

### Tareas paralelas:
- **Video demo:** Grabar recorriendo la app con datos mock (Plan B recomendado en contexto hora 21)
- **Documentación:** Actualizar `README.md` con nuevos endpoints y features
- **Pitch video:** Guion de 3 minutos mostrando:
  1. Región y usuario definido
  2. Ingreso de prioridades
  3. Comparación de rotaciones
  4. Evidencia científica (datos NASA)
  5. Aviso de herramienta de apoyo
- **Storytelling:** Definir el "usuario tipo" y su historia (productor 200ha, riego limitado, maíz-soja)

### Herramientas:
- Grabador de pantalla (OBS, Camtasia)
- Edición: CapCut o iMovie
- Guion en Markdown
- Presentation: Google Slides o PowerPoint

---

## 📡 Integración y Dependencias

### Flujo de datos entre frentes:

```
┌─────────────┐      ┌─────────────────────┐
│  Backend     │      │  Frontend           │
│ (FastAPI)    ├──→──►│ (React + Vite)      │
│              │      │  - API client       │
│  engine.py   │      │  - Map components   │
│  schemas.py  │      │  - PriorityPanel    │
└─────────────┘      └─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  Data Pipeline      │
│ (Python scripts)   │
│ fetch_power.py     │
│ build_features.py  │
│ indicadores.py     │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  Datos Procesados   │
│ power_daily.csv     │
│ power_monthly.csv   │
│ crops.yaml          │
└─────────────────────┘
```

### Puntos de integración críticos:

1. **`schemas.py`**: Definir modelos Pydantic que coincidan con contrato API (Sección 7 del contexto)
   - `GET /api/crops` → lista de cultivos y rasgos
   - `GET /api/field-profile?lat=&lon=` → resumen climático, NDVI, períodos campo desnudo, riesgos
   - `POST /api/rotations` → recibe ubicación, prioridades y rotación actual; devuelve 3+ estrategias

2. **`crops.yaml`**: Tabla cruzada que conecta datos climáticos con rasgos de cultivos
   - Consumo de agua por cultivo
   - Tolerancia a sequía
   - Fijación de nitrógeno
   - Profundidad de raíz
   - Cobertura de suelo
   - Aporte de materia orgánica
   - Potencial de mercado
   - *Notas: adaptable a región San Luis*

3. **Endpoints reales vs mock:**
   - Hora 2: Backend debe devolver respuestas falsas con formato real
   - Luego reemplazar por reales cuando pipeline esté listo
   - Siempre `main` debe correr (Sección 9 del contexto)

---

## 📅 Cronograma Acelerado (1 día)

| Hora | Deliverable | Responsable |
|------|-------------|-------------|
| **0-1** | Alcance definido, roles, repositorio compartido | Coordinación |
| **1-2** | Mock data backend + schemas.py | Lógica Rotación + Backend |
| **2-3** | Estructura Frontend + Map base | Frontend |
| **3-4** | PriorityPanel component | Frontend |
| **4-5** | engine.py versión mock | Lógica Rotación |
| **5-6** | Explicaciones automáticas (explain.py) | Lógica Rotación |
| **6-7** | Datos climáticos exploratorios | Datos 1 |
| **7-8** | Glosario y diseño UX básico | Diseño/UX |
| **8-9** | Integración Frontend-Backend (mock) | Frontend + Backend |
| **9-10** | Video demo corta (Plan B) | Coordinación |
| **10-12** | Pulir UI, agregar evidencias | Frontend + Lógica Rotación |
| **12-18** | Integración datos reales (si da) | Datos 1 + Datos 2 |
| **18-21** | Arreglos, pruebas, extras | Todo el equipo |
| **21-24** | Documentación, video pitch, envío | Coordinación |

---

## ✅ Checklist de "Hecho" para cada frente

### Backend:
- [ ] `backend/app/schemas.py` con 3 schemas (Crops, FieldProfile, Rotations)
- [ ] `backend/app/scoring/engine.py` calcula score ponderado
- [ ] `backend/app/scoring/explain.py` genera texto automático
- [ ] Endpoints mock funcionando en `/api/rotations`
- [ ] `.env.example` actualizado con credenciales placeholder

### Frontend:
- [ ] Mapa interactivo con capa base
- [ ] Sliders de prioridades (agua, ingresos, suelo, erosión)
- [ ] Componente RotationCompare con 3 tarjetas
- [ ] EvidenciaCard con hallazgos citeables
- [ ] DataGapsBadge visible en interfaz
- [ ] Glosario termshover o sidebar

### Datos:
- [ ] `data/processed/power_monthly.csv` ya existe (hecho!)
- [ ] `pipeline/indicadores_estacionales.py` generado
- [ ] MOCK crops.yaml creado con 5 cultivos comunes
- [ ] Scripts con cacheo implementado (no volver a bajar)

### Documentación:
- [ ] `contexto/plan_trabajo_paralelo.md` actualizado
- [ ] `contexto/pipeline_log.md` completado
- [ ] `docs/` folder con indicadores y glosario
- [ ] Video pitch guionado (aunque no grabado)

---

## 💡 Recomendaciones Clave

1. **Mock primero**: A la hora 2, backend debe responder con formato real aunque datos sean falsos. Esto permite avanzar frontend independiente.

2. **Regla de las 2-3 horas**: Merge a `main` cada 2-3 horas; `main` siempre debe correr (Sección 9 del contexto).

3. **Credenciales en `.env`**: Nunca commitear `.env`; usar `.env.example` en el repo (Sección 9).

4. **Plan B video**: Grabar video de la app funcionando antes del final (Sección 9, recomendación).

5. **Unidades y fechas explícitas**: Número uno de errores al unir datasets. Asegurar que todo especifique unidades y formato fecha.

6. **No sobreintegrar**: Con 3-4 datasets bien usados alcanza (Sección 10 del contexto). Mejor hacer bien poquito que poco de todo.

7. **Herramienta de apoyo, no reemplazo**: Cada pantalla debe tener recordatorio visual de esto (badges, lenguaje, diseño).

---

## 🚀 Próximo paso inmediato

**Recomendación:** Empezar por **Backend schemas.py + Frontend Map base** en paralelo, mientras **Datos 1 ejecuta indicadores_estacionales.py**. Estos tres frentes no dependen uno del otro para empezar y sentarán las bases para la integración posterior.

¿Te parece bien si comienzo implementando estos tres frentes simultáneamente y te voy actualizando el progreso en el documento de plan de trabajo?