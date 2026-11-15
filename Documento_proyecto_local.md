# 📚 Documentación Local del Proyecto: NASA Space Apps Challenge 2026

*Este archivo es solo para uso local y está incluido en .gitignore. No forma parte del repositorio remoto.*

---

## 🌟 Visión General del Proyecto
**Desafío:** NASA Space Apps Challenge 2026  
**Título:** Adapting Farms with NASA Data  
**Equipo:** 6 personas, 1 día disponible  
**Fecha de inicio:** 2025-11-14  
**Estado:** En progreso - Fase de pipeline de datos completada

---

## 📂 Estructura del Repositorio

### Raíz del proyecto `/NASA-challenge-2026/`
```
.git/              # Historial de versionado (Git)
.back/             # Backend Node.js (estructura original)
.front/            # Frontend React + Vite (estructura original)
.contexto/         # Documentación y planificación del proyecto
.data/             # Datos del proyecto (raw y processed)
.pipeline/         # Scripts pipeline de datos
.index.html        # Página principal
```

### Estructura de Datos `/data/`
```
data/raw/          # Datos crudos (1.5 MB)
  └── power_san_luis_argentina.json  # JSON NASA POWER, 26 años, 9 variables

data/processed/    # Datos limpios y features generadas (8.7 KB total)
  ├── power_daily.csv        # 1.7 KB, 9,497 días × 9 variables
  └── power_monthly.csv      # 8.3 KB, 312 meses con features estacionales

data/crops.yaml      # *PENDIENTE* - Martín: rasgos de cultivos para San Luis
```

### Pipeline de Datos `/pipeline/`
```
pipeline/common.py       # Configuración: rutas, coordenadas San Luis, fechas
pipeline/fetch_power.py  # Descarga datos NASA POWER (sin login necesario)
pipeline/build_features.py  # Limpieza y features mensuales (hecho por Juan originalmente)
pipeline/indicadores_estacionales.py  # *Juan*: Análisis tendencial 26 años
indicadores_calculados.json  # *Juan*: Resultados del análisis estacional
```

### Documentación `/contexto/`
```
contexto/              # Documentación del proyecto
  ├── contexto_desafio_adapting_farms.md  # Base del desafío (6 páginas)
  ├── plan_trabajo_paralelo.md            # División en 5 frentes de trabajo
  ├── guia_equipo_backend.md              # Guía para el equipo Backend (2 personas)
  ├── guia_equipo_frontend.md             # Guía para el equipo Frontend (2 personas)
  ├── guia_equipo_datos.md                # Guía para el equipo Datos (2 personas)
  ├── guia_equipo_backend.md              # Guía división Juan vs Martin
  ├── division_trabajo_datos.md           # *Juan*: Indicadores estacionales
  ├── pipeline_log.md                     # Registro paso a paso del pipeline
  └── indicadores_climaticos.md           # *Juan*: Reporte resumen climático
```

### Archivos de Configuración Raíz
- `.gitignore` - Archivos y carpetas ignoradas por Git
- `.env.example` - Variables de entorno (nunca commitear .env real)
- `package.json` y `package-lock.json` - Dependencias Node.js
- `index.html` - Página HTML principal

---

## 👤 Trabajo de Juan (Enfoque Datos)

### Tareas Completadas:
1. **Pipeline NASA POWER** ✅
   - Descarga de 9,497 días (26 años: 2000-2025)
   - Limpieza y eliminación de `-999` (datos faltantes de POWER)
   - Generación de `power_daily.csv` y `power_monthly.csv`

2. **Análisis Estacional** ✅
   - Script `pipeline/indicadores_estacionales.py`
   - 7 indicadores climáticos calculados
   - Reporte `contexto/indicadores_climaticos.md`
   - JSON `indicadores_calculados.json`

3. **Indicadores Clave Calculados:**
   - Lluvia total: 20,052.2 mm, tendencia **reducción**
   - Días calor (>35°C): 222→252→211 por década
   - Días helada (≤0°C): 161→146→78 (**reducción 51%**)
   - Verano (DJF): temp 23.46°C, precip 114.13mm/mes
   - Estación seca: 47.8% meses, húmeda: 25.6% meses

4. **Entregables a Martín:**
   - `indicadores_calculados.json` 
   - `contexto/indicadores_climaticos.md`
   - `pipeline/indicadores_estacionales.py` (reproducible)

### Scripts Desarrollados por Juan:
- `pipeline/build_features.py` (versión inicial con pandas/numpy, después adaptado)
- `pipeline/indicadores_estacionales.py` (versión final sin dependencias externas)

---

## 👤 Trabajo de Martin (Enfoque Datos - Pendiente)

### Tareas Pendientes:
1. **`data/crops.yaml`** - Tabla de 5 cultivos con rasgos para San Luis
   - Maíz, soja, trigo + 2 cultivos adicionales
   - water_consumption, drought_tolerance, nitrogen_fixation, root_depth, soil_coverage, organic_matter, market_potential, adaptation_notes

2. **`pipeline/validate_data.py`** - Reporte de consistencia de datos
   - Validar power_monthly.csv y power_daily.csv
   - Reportar filas, columnas, rangos, % faltantes

3. **Entregable a Juan:**
   - `data/crops.yaml` completado
   - Reporte de validación de datos

---

## 🔄 Flujo de Trabajo Registrado

### Fase 1: Setup y Datos (Horas 0-6)
- ✅ Definir región piloto: San Luis, Argentina (lat -33.30, lon -65.30)
- ✅ Crear pipeline NASA POWER (fetch_power.py)
- ✅ Ejecutar fetch_power.py - datos crudos descargados
- ✅ Ejecutar build_features.py - datos limpios generados
- ✅ Verificar 9,497 días, 9 variables, 0% faltantes post-interpolación

### Fase 2: Documentación y División (Horas 6-8)
- ✅ Crear plan_trabajo_paralelo.md (5 frentes de trabajo)
- ✅ Crear guías por equipo (backend, frontend, datos)
- ✅ **Dividir equipo datos: Juan vs Martin**
- ✅ Juan: indicadores estacionales
- ✅ Martin: crops.yaml + validación

### Fase 3: Análisis e Integración (Horas 8-12)
- ✅ Juan: ejecutar indicadores_estacionales.py
- ✅ Juan: generar indicadores_climaticos.md
- ✅ Juan: guardar indicadores_calculados.json
- ⏳ Martin: crear crops.yaml
- ⏳ Martin: ejecutar validate_data.py
- ⏳ Integración y firma final

---

## 📊 Datos Clave del Proyecto

### Dataset NASA POWER - San Luis, Argentina
| Parámetro | Valor |
|---|---|
| **Coordenadas** | lat: -33.30, lon: -65.30 |
| **Período** | 2000-01-01 a 2025-12-31 |
| **Años** | 26 años completos |
| **Días de datos** | 9,497 días |
| **Variables** | 9 variables agroclimáticas |
| **Resolución** | 0.5° (~55 km) |
| **API** | power.larc.nasa.gov (sin login) |

### Variables Climáticas (9)
1. T2M - Temperatura media (°C)
2. T2M_MAX - Temperatura máxima (°C)
3. T2M_MIN - Temperatura mínima (°C)
4. PRECTOTCORR - Lluvia corregida (mm/día)
5. RH2M - Humedad relativa (%)
6. ALLSKY_SFC_SW_DWN - Radiación solar (MJ/m²/día)
7. GWETTOP - Humedad superficial suelo (0-1)
8. GWETROOT - Humedad zona radicular (0-1)
9. EVLAND - Evapotranspiración (mm/día)

### Indicadores Estacionales Calculados (Juan)
| Indicador | Valor | Tendencia |
|---|---|---|
| Lluvia total 2000-2025 | 20,052.2 mm | Reducción |
| Días calor (>35°C) década 2000 | 222 días | - |
| Días calor década 2010 | 252 días | pico |
| Días calor década 2020 | 211 días | reducción |
| Días helada década 2000 | 161 días | - |
| Días helada década 2020 | 78 días | **reducción 51%** |
| Verano temp media | 23.46 °C | - |
| Verano precip media | 114.13 mm/mes | - |
| Meses secos (<50mm) | 149 (47.8%) | - |
| Meses húmedos (>=100mm) | 80 (25.6%) | - |

---

## 🗂️ Próximos Pasos Para El Equipo

### Para Continuar el Trabajo:

**Para Martin (datos):**
1. Crear `data/crops.yaml` con 5 cultivos para San Luis
2. Ejecutar `pipeline/validate_data.py` y reportar
3. Entregar a Juan: crops.yaml + reporte validación

**Para Backend:**
1. Implementar `schemas.py` con 3 endpoints Pydantic
2. Desarrollar `engine.py` motor de puntuación
3. Probar endpoints mock (`GET /api/crops`, `GET /api/field-profile`, `POST /api/rotations`)

**Para Frontend:**
1. Configurar Vite + mapa base San Luis
2. Implementar PriorityPanel con 4 sliders
3. Crear RotationCompare con 3 estrategias
4. Integrar API client con endpoints mock

**Para Coordinación:**
1. Merge de ramas cuando cada equipo termine su parte
2. Probar flujo completo: frontend -> backend -> datos
3. Grabar video demo (Plan B del desafío)
4. Documentación final y pitch

---

## 🛠️ Estado Actual de los Archivos Importantes

### Archivos Modificados/Creados (Local):
```
✅ pipeline/indicadores_estacionales.py     # Juan: cálculo de indicadores
✅ indicadores_calculados.json              # Juan: resultados JSON
✅ contexto/indicadores_climaticos.md       # Juan: reporte markdown
✅ data/processed/power_daily.csv           # Datos diarios limpios
✅ data/processed/power_monthly.csv         # Datos mensuales features
✅ data/raw/power_san_luis_argentina.json   # Datos crudos NASA POWER
✅ pipeline/build_features.py               # Limpieza de datos
✅ pipeline/fetch_power.py                  # Descarga datos NASA
✅ pipeline/common.py                       # Configuración proyecto
✅ contexto/plan_trabajo_paralelo.md        # División en frentes
✅ contexto/guia_equipo_backend.md          # Guía equipo Backend
✅ contexto/guia_equipo_frontend.md         # Guía equipo Frontend
✅ contexto/guia_equipo_datos.md            # Guía equipo Datos
✅ contexto/division_trabajo_datos.md       # División Juan vs Martin
```

### Archivos en .gitignore (no trackeados localmente):
- `Documento_proyecto_local.md` ← **Este archivo actual**
- `.env`, `.env.*`
- `data/raw/` (ya está en .gitignore original)
- `node_modules/`, `.pnp`, etc.

---

## 💡 Recomendaciones y Mejores Prácticas

### Documentación:
1. **Siempre documentar** los scripts con propósitos y fórmulas
2. **Unidades explícitas** en todos los números (el error #1 al unir datasets)
3. **Tendencias sobre absolutos** - las tendencias temporal son la "evidencia" del desafío
4. **Brechas honestas** - marcar incertidumbre en `data_gaps` de todas las salidas

### Control de Versiones:
1. **Commit cada 2-3 horas** - `main` siempre debe correr (Sección 9 del contexto)
2. **Ramas por rol** - trabajo en branches feature/, merge a main
3. **Sin credenciales en git** - usar .env, nunca commitear .env real
4. **Plan B video** - grabar demo con datos mock si es necesario

### Datos:
1. **Cachear todo** - si un script ya bajó un archivo, que no lo vuelva a bajar
2. **Unidades y fechas explícitas** en cada columna
3. **0% datos faltantes** después de interpolación (logro del pipeline actual)
4. **Adaptar cultivos a región** - crops.yaml debe reflejar condiciones San Luis, no EE.UU.

---

## 🚨 Problemas Conocidos y Limitaciones

### Datos NASA POWER:
- **Resolución 0.5° (~55 km)** - adecuado para nivel provincial, no lote individual
- **Cobertura global** - funciona para Argentina aunque datos sean globales
- **Sin login necesario** - ventaja sobre otros datasets NASA (earthaccess requiere cuenta)
- **Variables agroclimáticas** - ideales para toma de decisiones de rotación

### Proyecto 1 Día:
- **Alcance reducido** a 3-4 datasets máximos (consejo del contexto)
- **MVP mínimo** viable antes de agregar más datos
- **Priorizar sobre cantidad** - 4 datasets bien usados vs 10 parcialmente

### Recursos del Equipo:
- **6 personas, 1 día** - división en 5 frentes de trabajo
- **Backend + Frontend + Datos** = 2+2+2 personas
- **Dependencias críticas** - schemas.py debe coincidir con API frontend

---

## 📅 Cronograma Real (1 Día)

| Hora | Actividad | Responsable |
|------|-----------|-------------|
| 0-1 | Setup, roles, región, repo | Coordinación |
| 1-2 | Backend schemas.py + Frontend mapa | Backend + Frontend |
| 2-3 | Juan: indicadores, Martin: crops.yaml | Datos (Juan + Martin) |
| 3-4 | Intercambio resultados Juan↔Martin | Los dos |
| 4-5 | Integración inicial | Todos |
| 5-6 | Pulir UI, agregar evidencias | Frontend |
| 6-8 | Datos reales vs mock | Datos |
| 8-10 | Arreglos, pruebas | Todos |
| 10-12 | Video demo / pitch prep | Coordinación |
| 12-24 | Documentación, envío final | Todos |

---

*Última actualización: 2025-11-14  
Generado automáticamente para documentación local*  
*Este archivo está exento de versionado Git (ver .gitignore)*