# Contexto del proyecto: Adapting Farms with NASA Data (NASA Space Apps 2026)

Resumen de la conversación: introducción al desafío, recursos, plan de trabajo, estructura del repositorio y primeros pasos con los datos.

- Equipo: 6 personas
- Tiempo disponible: 1 día
- Objetivo: desarrollar una app (herramienta de apoyo a la decisión)
- Estado actual: repositorio creado; se empieza por el pipeline de datos con NASA POWER

---

## 1. Introducción al desafío

**El problema.** Los agricultores de todo el mundo enfrentan temperaturas cambiantes, lluvias cada vez menos predecibles, escasez de agua, clima extremo y pérdida de salud del suelo. Esto vuelve muy difícil una decisión clave: qué cultivos incluir en la rotación. Un cultivo que mejora el suelo en un lugar puede consumir demasiada agua, traer enfermedades, no tener mercado local o no encajar en la temporada de crecimiento de otra zona.

**La oportunidad.** Los datos de observación de la Tierra de la NASA, acumulados durante décadas, permiten entender las condiciones locales de cultivo. Las técnicas de IA pueden convertir esos datos en información práctica y fácil de usar para los agricultores.

**El desafío.** Crear una herramienta de apoyo a la decisión (app, modelo, mapa interactivo u otra) que combine datos de la NASA con información local sobre suelo, características de los cultivos y prioridades del agricultor. Debe ayudarlo a explorar estrategias de rotación que fortalezcan la salud del suelo y adapten la finca a condiciones cambiantes.

**Qué se espera.**

- Comparar al menos tres estrategias de rotación, incluida la rotación actual del agricultor.
- Para cada una, explicar por qué se sugiere, qué evidencia la respalda, qué beneficios ofrece, qué brechas de información hay y qué riesgos requieren revisión de expertos locales.
- Identificar momentos de campo desnudo, épocas de mayor vulnerabilidad de los cultivos actuales y oportunidades para interrumpir ciclos de plagas, reducir la demanda de agua, mejorar la infiltración o sumar ingresos.
- Dejar claro que es una herramienta de apoyo: no reemplaza el juicio del agricultor ni la experiencia agronómica local.

**Consideraciones opcionales del enunciado.**

- Entender condiciones y datos: explicar términos como evapotranspiración, anomalías de humedad del suelo, NDVI, riesgo de heladas; aclarar diferencias entre observación satelital y medición terrestre.
- IA, modelado y fusión de datos: comparar enfoques, explicar cómo el modelo trata la incertidumbre, armonizar datasets de distinta resolución a una grilla común.
- Exploración de rotaciones: ciclo de nutrientes, erosión, materia orgánica, ciclos de plagas, uso de agua, forraje, mercado; explicar el rol de fijadores de nitrógeno, cultivos de cobertura, raíces profundas y tolerantes a sequía.
- Mapeo y visualización: mapas interactivos, zonas de riesgo de erosión, puntos calientes de estrés hídrico, líneas de tiempo, superposiciones, sliders de escenario.
- Diseño centrado en el agricultor: interfaz simple, que el agricultor ingrese sus propias prioridades y restricciones, recordatorios de que la herramienta apoya y no reemplaza.

---

## 2. Datos y recursos del desafío

### Núcleo NASA

| Dataset | Qué aporta |
|---|---|
| SMAP | Humedad del suelo superficial y estado de congelación, cada 2 a 3 días |
| GPM / IMERG | Precipitación global (confiabilidad de lluvias, tormentas extremas, erosión) |
| Landsat y MODIS/VIIRS | Reflectancia, NDVI, estrés de vegetación, suelo desnudo, cambio estacional (Landsat 30 m, MODIS/VIIRS 250 a 1000 m) |
| NASA POWER | Clima y agroclimatología: temperatura, humedad, radiación, heladas |
| SRTM | Elevación y terreno: pendiente, escorrentía, erosión |
| ECOSTRESS | Temperatura de superficie y evapotranspiración a alta resolución |
| GRACE / GRACE-FO | Tendencias de agua a largo plazo |
| GEDI | Biomasa y estructura de vegetación |

### Reanálisis y clima

NLDAS/GLDAS, ERA5 (ECMWF), PRISM (EE. UU.).

### Suelo y cultivos

SSURGO/STATSGO2, Web Soil Survey, Cropland Data Layer (CropScape), USDA NASS QuickStats, USDA Ag Data Commons.

### Agua y evapotranspiración

OpenET (oeste de EE. UU.), USGS NWIS, CoCoRaHS (validación en tierra).

### Imágenes y cobertura

Sentinel-2 (ESA), NAIP, NLCD, LANDFIRE.

### Mercado y agronomía global

USDA AMS Market News, FAO GAEZ.

**Nota importante:** la mayoría de las fuentes de suelo, cultivos y mercado son de EE. UU. Si el equipo trabaja en otra región, conviene apoyarse en los datasets globales (SMAP, IMERG, MODIS, POWER, ERA5, GAEZ, Sentinel-2) y buscar equivalentes locales para suelo y cultivos.

---

## 3. Cómo empezar (plan de 1 día con 6 personas)

### Primera hora: decisiones de todo el equipo

- Región piloto única (un condado de EE. UU. si usan datos del USDA, o su zona usando solo datasets globales).
- Un usuario concreto (por ejemplo, productor de 200 ha con riego limitado que rota maíz-soja).
- Alcance del MVP: el agricultor marca su campo y sus prioridades, la app muestra el diagnóstico de condiciones y compara 3 rotaciones.
- Solo 3 o 4 datasets: NASA POWER, SMAP o GLDAS, NDVI (MODIS/Landsat) y opcionalmente SRTM.
- Crear la cuenta gratuita de Earthdata cuanto antes.

### Roles sugeridos

| Rol | Tarea |
|---|---|
| Datos 1 | Clima y humedad del suelo (POWER, SMAP/GLDAS), dejar datos pre-procesados en archivos |
| Datos 2 | NDVI, campo desnudo, estrés, terreno si da el tiempo |
| Lógica de rotación | Tabla de cultivos y motor de puntuación |
| Frontend | Mapa interactivo, sliders de prioridades, comparación de rotaciones |
| Diseño y UX | Pantallas, lenguaje simple, glosario |
| Coordinación y pitch | Integración, cumplimiento de requisitos, storytelling, video y presentación |

### Cronograma de referencia

- Horas 0 a 1: alcance, región, roles, cuentas, repositorio compartido.
- Horas 1 a 6: datos listos y limpios; en paralelo, esqueleto del frontend con datos de ejemplo y definición de pantallas.
- Horas 6 a 12: motor de rotaciones conectado, mapa con capas reales, sliders.
- Horas 12 a 18: integración, explicaciones y evidencia por rotación, aviso de herramienta de apoyo.
- Horas 18 a 21: pruebas, arreglos, extras opcionales.
- Últimas horas: documentación, video o pitch y envío con margen.

### Riesgos a evitar

- Integrar todos los datasets (con 3 o 4 bien usados alcanza).
- Depender de descargas en vivo durante la demo.
- Dejar el pitch para el final.
- Prometer precisión agronómica que no pueden validar; marcar las brechas con honestidad.

---

## 4. Estructura del repositorio

La idea central es separar el pipeline de datos (offline) de la app (online): los scripts generan archivos chicos y la API solo los lee.

```
proyecto/
├─ README.md                 # qué es, cómo correrlo, fuentes, limitaciones
├─ .env.example              # credenciales (nunca commitear .env)
├─ .gitignore                # data/raw/, .env, node_modules, __pycache__
├─ data/
│  ├─ raw/                   # descargas pesadas (ignorado por git)
│  ├─ processed/             # features finales chicos (CSV/JSON/GeoJSON, <20 MB)
│  └─ crops.yaml             # tabla de cultivos y sus rasgos
├─ pipeline/                 # equipo de datos
│  ├─ common.py              # región piloto, rutas, helpers
│  ├─ fetch_power.py         # clima + humedad de suelo (NASA POWER)
│  ├─ fetch_ndvi.py          # vegetación (MODIS/Landsat/Sentinel-2)
│  ├─ fetch_soil.py          # suelo (SSURGO u otro)
│  ├─ fetch_terrain.py       # pendiente/erosión (SRTM/NASADEM)
│  └─ build_features.py      # une todo en data/processed/
├─ backend/
│  ├─ requirements.txt
│  └─ app/
│     ├─ main.py             # FastAPI, CORS, rutas
│     ├─ schemas.py          # modelos Pydantic (el contrato de la API)
│     ├─ data_loader.py      # carga data/processed/ en memoria
│     ├─ scoring/
│     │  ├─ engine.py        # puntaje de rotaciones
│     │  └─ explain.py       # genera "por qué", evidencia, riesgos, brechas
│     └─ tests/
├─ frontend/
│  ├─ package.json
│  └─ src/
│     ├─ api/                # cliente de la API
│     ├─ components/         # Map, PriorityPanel, RotationCompare,
│     │                      # EvidenceCard, Glossary, DataGapsBadge
│     └─ pages/
├─ docs/                     # pitch, diagrama, fuentes, limitaciones
└─ notebooks/                # exploración (no es parte de la app)
```

---

## 5. Stack recomendado

| Capa | Herramienta | Por qué |
|---|---|---|
| Backend | FastAPI + Pydantic | Rápido de escribir, documenta solo la API en `/docs` |
| Datos | pandas, xarray, rioxarray, geopandas, rasterio | Estándar para series y rásters |
| Frontend | React + Vite, Leaflet o MapLibre, Recharts | Mapa y gráficos sin configuración pesada |
| Estilos | Tailwind | Evita perder tiempo en CSS |

Alternativa si el equipo domina Python y casi nadie sabe React: Streamlit con `folium` o `pydeck`. Elegir una de las dos y no cambiar.

---

## 6. Herramientas para acceder a los datasets

| Dato | Cómo acceder | Notas |
|---|---|---|
| NASA POWER (temperatura, lluvia, radiación, humedad de suelo, evapotranspiración, heladas) | API REST `power.larc.nasa.gov/api/temporal/daily/point` con `requests` | Sin login. Es el primer script a escribir. Usar `community=AG` y revisar en la documentación los nombres exactos de variables |
| SMAP, MODIS, GPM/IMERG, Landsat | Librería Python `earthaccess` | Requiere cuenta gratuita de Earthdata; guardar credenciales en `.env` |
| Series de NDVI por punto | AppEEARS (API de NASA) o `earthaccess` con MOD13 | AppEEARS devuelve CSV por punto, más simple que bajar rásters |
| Sentinel-2, Landsat, elevación | Microsoft Planetary Computer con `pystac-client`, `odc-stac`, `planetary-computer` | Sin login para leer; buena opción para NDVI y campo desnudo a escala fina |
| Capas visuales en el mapa | NASA GIBS / Worldview (teselas WMTS) | Se agregan como capa, sin descargar nada |
| Suelo (SSURGO) | USDA Soil Data Access (API REST con SQL) | Solo EE. UU. |
| Cultivos (CDL) | CropScape o colección `usda-cdl` de Planetary Computer | Solo EE. UU. |
| Clima de respaldo | Open-Meteo (histórico, sin clave) | Plan B si POWER falla |

Recomendación: evitar ERA5 vía Copernicus CDS para esta entrega (las colas pueden ser lentas) y evitar OpenET si no se tiene clave. Cada fuente extra no imprescindible es riesgo.

---

## 7. Contrato de la API (acordar en la hora 1)

```
GET  /api/crops                      -> lista de cultivos y rasgos
GET  /api/field-profile?lat=&lon=    -> resumen climático, series de NDVI,
                                        períodos de campo desnudo, riesgos
POST /api/rotations                  -> recibe ubicación, prioridades y
                                        rotación actual; devuelve 3+ estrategias
```

Forma de cada estrategia (coincide con lo que pide el desafío):

```json
{
  "name": "Maíz → Soja → Cultivo de cobertura",
  "is_current": false,
  "score": 0.74,
  "why": "Texto corto en lenguaje simple",
  "benefits": ["Menor demanda de agua en verano", "..."],
  "evidence": [
    {"dataset": "NASA POWER", "finding": "Lluvia en verano -18% vs. 2000-2010",
     "resolution": "0.5° / diario", "period": "2000-2025"}
  ],
  "data_gaps": ["No hay mediciones de suelo a nivel de lote"],
  "risks_to_validate": ["Revisar con un técnico local la fecha de siembra"]
}
```

---

## 8. Motor de puntuación

Debe ser transparente y explicable, no una caja negra.

1. `data/crops.yaml` guarda por cultivo: consumo de agua, tolerancia a sequía, fijación de nitrógeno, profundidad de raíz, cobertura de suelo, aporte de materia orgánica, potencial de mercado.
2. Del pipeline salen indicadores del lugar: estrés hídrico, olas de calor, riesgo de helada, meses de campo desnudo, pendiente.
3. El puntaje de una rotación es la suma ponderada de qué tan bien sus cultivos responden a esos indicadores, con pesos que vienen de los sliders del agricultor (agua, ingresos, suelo, erosión).
4. `explain.py` convierte cada término del puntaje en una frase y una evidencia citable, así el "por qué" sale directo del cálculo.

La IA puede aportar en un lugar secundario: detectar anomalías en las series o redactar el resumen en lenguaje claro a partir de la evidencia ya calculada.

---

## 9. Recomendaciones al programar

- Mock primero: a la hora 2 el backend debe devolver respuestas falsas con el formato real, y luego se reemplazan por reales.
- Una región piloto y un `common.py` con coordenadas y fechas definidas en un solo lugar.
- Guardar la procedencia (dataset, resolución, período) en cada dato; alimenta las tarjetas de evidencia.
- Marcar la incertidumbre: si un dato es de baja resolución o falta, debe aparecer en `data_gaps`.
- Cachear todo: si un script ya bajó un archivo, que no lo vuelva a bajar.
- Ramas cortas por rol y merge a `main` cada 2 o 3 horas; `main` siempre tiene que correr.
- Credenciales solo en `.env`, con `.env.example` en el repo.
- Plan B de demo: grabar un video de la app funcionando antes del final.
- Unidades y fechas explícitas en cada columna (fuente número uno de errores al unir datasets).

---

## 10. Primeros pasos con los datos (empezar por lo básico)

Se arranca con un solo dataset (NASA POWER, sin login), un solo punto y una sola tabla limpia. Primero se bajan y se inspeccionan los datos crudos, y después se limpian.

### Paso 0: preparar el entorno

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install pandas requests pyarrow
pip freeze > requirements.txt
```

En `.gitignore`: `data/raw/`, `.env`, `.venv/`.

### Paso 1: fijar la región piloto

`pipeline/common.py`:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

# CAMBIAR: coordenadas del campo piloto
PILOT = {"name": "piloto", "lat": -33.30, "lon": -66.34}

START = "20000101"   # POWER usa YYYYMMDD
END = "20251231"
```

### Paso 2: descargar datos crudos

`pipeline/fetch_power.py`:

```python
import json
import requests
from common import RAW, PILOT, START, END

URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

PARAMS = {
    "parameters": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN,GWETTOP,GWETROOT,EVLAND",
    "community": "AG",
    "latitude": PILOT["lat"],
    "longitude": PILOT["lon"],
    "start": START,
    "end": END,
    "format": "JSON",
}

def main():
    out = RAW / f"power_{PILOT['name']}.json"
    if out.exists():                      # caché: no volver a bajar
        print("ya existe", out)
        return
    r = requests.get(URL, params=PARAMS, timeout=120)
    r.raise_for_status()
    out.write_text(json.dumps(r.json()))
    print("guardado", out)

if __name__ == "__main__":
    main()
```

Ejecutar con `python pipeline/fetch_power.py`. Si algún nombre de variable da error, revisar la documentación de la API de POWER (`power.larc.nasa.gov/docs`); es lo primero que suele fallar.

### Paso 3: inspeccionar antes de limpiar

Preguntas a responder en un notebook:

- ¿Cuántas filas hay? Deberían ser unos 9.500 días.
- ¿Hay valores `-999`? POWER usa -999 para datos faltantes.
- ¿Hay fechas duplicadas o saltos en la serie?
- ¿Los rangos tienen sentido? (temperatura entre -30 y 50 °C, lluvia mayor o igual a 0, humedad de suelo entre 0 y 1)
- ¿Qué variables tienen más faltantes?

```python
import json, pandas as pd
raw = json.load(open("../data/raw/power_piloto.json"))
df = pd.DataFrame(raw["properties"]["parameter"])
print(df.shape); print(df.describe()); print((df == -999).sum())
```

### Paso 4: limpiar y generar la tabla procesada

`pipeline/build_features.py`:

```python
import json
import numpy as np
import pandas as pd
from common import RAW, PROCESSED, PILOT

def load_power():
    raw = json.loads((RAW / f"power_{PILOT['name']}.json").read_text())
    df = pd.DataFrame(raw["properties"]["parameter"])
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    df.index.name = "date"
    return df

def clean(df):
    df = df.replace(-999, np.nan)
    df = df[~df.index.duplicated()].sort_index()
    df = df.asfreq("D")                                   # índice diario completo
    df = df.rename(columns={
        "T2M": "temp_mean_c", "T2M_MAX": "temp_max_c", "T2M_MIN": "temp_min_c",
        "PRECTOTCORR": "precip_mm", "RH2M": "rh_pct",
        "ALLSKY_SFC_SW_DWN": "solar_kwh_m2", "GWETTOP": "soil_wet_surface",
        "GWETROOT": "soil_wet_root", "EVLAND": "evap_land_mm",
    })
    df = df.interpolate(limit=3)                          # solo huecos cortos
    df["precip_mm"] = df["precip_mm"].clip(lower=0)
    return df

def monthly_features(df):
    m = df.resample("MS").agg({
        "temp_mean_c": "mean", "temp_max_c": "max", "temp_min_c": "min",
        "precip_mm": "sum", "soil_wet_root": "mean", "evap_land_mm": "sum",
    })
    m["frost_days"] = (df["temp_min_c"] <= 0).resample("MS").sum()
    m["heat_days_35"] = (df["temp_max_c"] >= 35).resample("MS").sum()
    return m

if __name__ == "__main__":
    daily = clean(load_power())
    daily.to_parquet(PROCESSED / "power_daily.parquet")
    monthly_features(daily).to_csv(PROCESSED / "power_monthly.csv")
    print(daily.isna().mean().round(3))                   # % de faltantes por columna
```

Decisiones a dejar escritas en el README: qué se hizo con los faltantes (solo se interpolan huecos de hasta 3 días), qué umbral se usa para helada y ola de calor, y las unidades de cada columna.

### Paso 5: verificar y compartir

- [ ] `data/processed/power_monthly.csv` existe y pesa pocos KB
- [ ] Sin `-999` ni fechas duplicadas
- [ ] Un gráfico rápido de lluvia mensual y temperatura mínima se ve razonable (se nota la estacionalidad)
- [ ] Commit del script y de `processed/` (el raw queda ignorado)
- [ ] Avisar al equipo del backend qué columnas hay, para armar `schemas.py`

---

## 11. Qué sigue

1. Calcular indicadores climáticos por temporada y por década: tendencia de lluvia, aumento de días de calor, frecuencia de heladas.
2. Sumar NDVI (campo desnudo y estrés de vegetación).
3. Sumar suelo y pendiente.
4. Conectar todo al motor de puntuación.

En paralelo, el resto del equipo puede avanzar con la tabla `crops.yaml`, el esqueleto de FastAPI con respuestas falsas y el diseño de las pantallas.

### Pendientes y notas

- Definir la región piloto (con eso se ajustan las coordenadas y el `crops.yaml` con cultivos adecuados a la zona).
- El código no fue ejecutado; hay que probarlo y ajustar nombres de variables de POWER si la API se queja.
- La página oficial del desafío no pudo leerse automáticamente (bloquea el acceso automatizado); el texto de Details y Resources fue provisto por el usuario.
- Fuente secundaria consultada sobre el desafío: https://problem.procreator.design/problems/cmqdt5sja00bbduzls20sursx
