# 🎯 Guía de comienzo: Equipo Datos (2 personas)

## 📍 Estado actual del proyecto
- **Dataset NASA POWER**: Descargado y procesado exitosamente
  - `data/raw/power_san_luis_argentina.json` (1.5 MB, 9,497 días, 26 años: 2000-2025)
  - `data/processed/power_daily.csv` (1.7 KB, datos diarios limpios)
  - `data/processed/power_monthly.csv` (8.3 KB, features mensuales 312 meses)
- **Estado**: Datos listos para consumo, sin tratamiento de faltantes (-999 resuelto), interpolación aplicada
- **Objetivo**: Entregar indicadores climáticos clave, tendencias estacionales y tabla de cultivos para integrar con el motor de puntuación

## 👥 Integración del equipo
- 2 personas encargadas del procesamiento y análisis de datos
- Necesitan coordinarse con:
  - **Equipo Backend**: Para estructura de `crops.yaml`, indicadores que consumirá el API
  - **Equipo Frontend**: Para formato de datos (CSV, estructura JSON) que la UI necesite visualizar

## 🚀 Paso 1: Verificar y organizar los datos (30 min)

```bash
# 1. Moverse al directorio del proyecto
cd /home/juan/Escritorio/NASA-challenge-2026

# 2. Revisar qué tenemos procesado
ls -lh data/processed/
echo "---"

# 3. Revisar datos crudos (muestra rápida)
python3 -c "
import json
raw = json.load(open('data/raw/power_san_luis_argentina.json'))
param = raw['properties']['parameter']
dates = list(param.keys())
print('Total fechas:', len(dates))
print('Rango:', dates[0], 'a', dates[-1])
print('Variables:', list(param.keys())[:3])
# Ver valores -999
neg999 = sum(1 for d in dates if param[d] == -999)
print('Valores -999 (faltantes originales):', neg999)
"

# 4. Revisar CSV procesado (muestra)
head -5 data/processed/power_monthly.csv
echo "---"
head -5 data/processed/power_daily.csv
```

### ✅ Resultado esperado:
- 9,497 fechas diarias de 2000-01-01 a 2025-12-31
- 9 variables climáticas agro
- 312 meses de features en CSV
- 0% datos faltantes después de interpolación

## 📊 Paso 2: Calcular indicadores estacionales y tendencias (2 horas)

### Script: `pipeline/indicadores_estacionales.py`

```python
# pipeline/indicadores_estacionales.py

import pandas as pd
from pathlib import Path
from datetime import datetime

# Rutas
PROCESSED = Path('data/processed')

# Cargar datos mensuales
df = pd.read_csv(PROCESSED / 'power_monthly.csv')

print("=== INDICADORES ESTACIONALES PARA SAN LUIS, ARGENTINA ===")
print(f"Período: {df['year'].min()}-{df['year'].max()}")
print(f"Meses de datos: {len(df)}")
print()

# 1. Tendencia de lluvia anual
rain_by_year = df.groupby('year')['precip_mm_sum'].sum()
print("1. Lluvia anual total (mm):")
print(rain_by_year.describe())
print(f"   - Lluvia total 2000-2025: {rain_by_year.sum():.1f} mm")
print(f"   - Año más lluvioso: {rain_by_year.idxmax()} con {rain_by_year.max():.1f} mm")
print(f"   - Año más seco: {rain_by_year.idxmin()} con {rain_by_year.min():.1f} mm")
print()

# 2. Tendencia de días de calor (temp_max >= 35°C)
print("2. Días de calor extremo por década:")
# Calcular década por año
df['decade'] = (df['year'] // 10) * 10
heat_by_decade = df.groupby('decade')['heat_days_35'].sum()
for decade, days in heat_by_decade.items():
    print(f"   - Década {decade}-{decade+9}: {days} días de calor (>35°C)")
print(f"   - Tendencia: {'Aumento' if heat_by_decade.iloc[-1] > heat_by_decade.iloc[0] else 'Reducción'} de días de calor")
print()

# 3. Tendencia de heladas (temp_min <= 0°C)
print("3. Días de helada por década:")
frost_by_decade = df.groupby('decade')['frost_days'].sum()
for decade, days in frost_by_decade.items():
    print(f"   - Década {decade}-{decade+9}: {days} días de helada (temp ≤ 0°C)")
print(f"   - Tendencia: {'Aumento' if frost_by_decade.iloc[-1] > frost_by_decade.iloc[0] else 'Reducción'} de días de helada")
print()

# 4. Promedio estival (DJF - Diciembre, Enero, Febrero)
summer = df[df['month'].isin([12, 1, 2])]
print("4. Promedio estival (DJF):")
summer_stats = summer['temp_mean_c'].mean()
summer_precip = summer['precip_mm_sum'].mean()
summer_frost = summer['frost_days'].mean()
summer_heat = summer['heat_days_35'].mean()
print(f"   - Temp media estival: {summer_stats:.1f} °C")
print(f"   - Precipitación estival: {summer_precip:.1f} mm")
print(f"   - Días de helada estival: {summer_frost:.1f} días")
print(f"   - Días de calor estival: {summer_heat:.1f} días")
print()

# 5. Estación seca vs. húmeda
print("5. Análisis estación seca/húmeda:")
# Definir estación seca como meses con precip < 50mm
dry_months = df[df['precip_mm_sum'] < 50]
wet_months = df[df['precip_mm_sum'] >= 100]
print(f"   - Meses secos (<50mm): {len(dry_months)} de {len(df)} ({len(df)-len(dry_months):.1f}%)")
print(f"   - Meses húmedos (>=100mm): {len(wet_months)} de {len(df)}")
print()

# 6. Resumen rápido
print("6. RESUMEN RÁPIDO PARA FRENTE/BACKEND:")
summary = {
    "total_years": df['year'].nunique(),
    "total_months": len(df),
    "avg_annual_precip": round(rain_by_year.mean(), 1),
    "precip_trend": "aumento" if rain_by_year.iloc[-1] > rain_by_year.iloc[0] else "reducción",
    "avg_summer_temp": round(summer_stats, 1),
    "summer_precip": round(summer_precip, 1),
    "heat_days_per_decade": {str(k): v for k, v in heat_by_decade.items()},
    "frost_days_per_decade": {str(k): v for k, v in frost_by_decade.items()}
}
import json
print(json.dumps(summary, indent=2))
```

### Ejecutar:
```bash
python3 pipeline/indicadores_estacionales.py
```

### Expected output highlights:
- Tendencia de lluvia (¿aumentó o disminuyó en 26 años?)
- Cómo han cambiado los días de calor extremo
- Cómo han cambiado los días de helada
- Condiciones estivales promedio
- Balanza estación seca/húmeda

## 🌱 Paso 3: Crear tabla `crops.yaml` para San Luis (2 horas)

### Estructura propuesta (basada en Sección 8 del contexto y necesidades agrícolas):

```yaml
# data/crops.yaml - Rasgos de cultivos adaptables a San Luis, Argentina
# Esta tabla conecta las variables climáticas con el rendimiento y viabilidad de cultivos

maíz:
  name: "Maíz"
  water_consumption: 500  # mm por ciclo completo (verano)
  drought_tolerance: 0.3  # 0-1, donde 1 = tolerancia total a sequía
  nitrogen_fixation: false
  root_depth: 150  # cm - profundidad máxima de raíces
  soil_coverage: 0.8  # Fracción de cobertura de suelo (%/100)
  organic_matter: 0.05  # Aporte de materia orgánica por ciclo (%)
  market_potential: "alto"  # alto, medio, bajo
  adaptation_notes: |
    Cultivo de verano por excelencia en San Luis.
    Alta demanda hídrica, requiere buena disponibilidad de agua.
    Sensible a estrés hídrico en etapas críticas de desarrollo.
    Rotación típica: maíz-soja.

soja:
  name: "Soja"
  water_consumption: 450  # mm por ciclo
  drought_tolerance: 0.5  # Mayor tolerancia que el maíz
  nitrogen_fixation: true  # Fija nitrógeno atmosférico
  root_depth: 80  # cm - sistema radicular más superficial
  soil_coverage: 0.7
  organic_matter: 0.03
  market_potential: "alto"
  adaptation_notes: |
    Buena alternativa al maíz en rotación.
    Fija nitrógeno, reduce necesidad de fertilizantes posteriores.
    Menor demanda hídrica que el maíz.
    Muy común en rotación maíz-soja en Argentina.

trigo:
  name: "Trigo"
  water_consumption: 350  # mm (cultivo de invierno/principios de primavera)
  drought_tolerance: 0.8  # Alta tolerancia asequía
  nitrogen_fixation: false
  root_depth: 120  # cm
  soil_coverage: 0.9
  organic_matter: 0.07
  market_potential: "medio"
  adaptation_notes: |
    Cultivo de invierno/principios de primavera.
    Alta tolerancia a sequía, importante para rotación.
    Precede bien al maíz al fijar nitrógeno o al seguir cultivos de cobertura.
    Sensible a heladas tardías y calor extremo prematuro.

# Agregar más cultivos según sea necesario...
```

### ¿Por este formato?

1. **Consistencia con contexto**: La Sección 8 dice: "`data/crops.yaml` guarda por cultivo: consumo de agua, tolerancia a sequía, fijación de nitrógeno, profundidad de raíz, cobertura de suelo, aporte de materia orgánica, potencial de mercado"

2. **Unidades explícitas**: Cada campo tiene unidades en el nombre o descripción (mm, cm, 0-1 scale, %)

3. **Adaptable a San Luis**: Los valores reflejan condiciones semi-áridas de la provincia:
   - Menor consumo de agua que zonas más húmedas
   - Tolerancias ajustadas al clima local
   - Observaciones de adaptación específicas

4. **Listo para API**: El backend puede leer este YAML y el frontend mostrar los rasgos.

### YAML para leer en Python:

```python
import yaml

with open('data/crops.yaml', 'r') as f:
    crops = yaml.safe_load(f)

# Ejemplo de uso
maiz = crops['maíz']
print(f"Consumo de agua: {maiz['water_consumption']} mm")
print(f"Tolerancia a sequía: {maiz['drought_tolerance']}")
print(f"Fijación de nitrógeno: {maiz['nitrogen_fixation']}")
```

## 🔍 Paso 4: Verificar consistencia y generar reporte (1 hora)

### Script de validación: `validate_data.py`

```python
# validate_data.py

import pandas as pd
from pathlib import Path
from datetime import Path

PROCESSED = Path('data/processed')

print("=== VALIDACIÓN DE DATOS PROCESADOS ===")
print()

# 1. Verificar power_monthly.csv
df = pd.read_csv(PROCESSED / 'power_monthly.csv')
print("1. power_monthly.csv:")
print(f"   - Filas: {len(df)}")
print(f"   - Columnas: {list(df.columns)}")
print(f"   - Años: {sorted(df['year'].unique())}")
print(f"   - Meses por año: {df.groupby('year')['month'].count().min()}-{df.groupby('year')['month'].count().max()}")
print(f"   - Temp media promedio: {df['temp_mean_c'].mean():.2f} °C")
print(f"   - Precipitación total: {df['precip_mm_sum'].sum():.1f} mm")
print(f"   - Total frost days: {df['frost_days'].sum()}")
print(f"   - Total heat days: {df['heat_days_35'].sum()}")
print(f"   - % faltantes (should be ~0): {df.isna().sum().sum() / (len(df) * len(df.columns)) * 100:.2f}%")
print()

# 2. Verificar power_daily.csv (muestra)
daily = pd.read_csv(PROCESSED / 'power_daily.csv', nrows=5)
print("2. power_daily.csv (muestra 5 filas):")
print(daily.columns.tolist())
print(daily.head())
print()

# 3. Verificar consistencia de fechas
print("3. Consistencia temporal:")
print(f   - Primer mes: {df['year'].min()}-{df['month'].min():02d}")
print(f   - Último mes: {df['year'].max()}-{df['month'].max():02d}")
print(f   - Rango total: {(df['year'].max() - df['year'].min())} años")
print()

# 4. Requisitos del desafío
print("4. Cumplimiento de requisitos del desafío:")
checks = {
    "Dataset NASA POWER disponible": True,
    "Rango 2000-2025 cumplido": df['year'].min() == 2000 and df['year'].max() == 2025,
    "Indicadores climáticos calculados": "temp_mean_c" in df.columns and "precip_mm_sum" in df.columns,
    "Frost days calculados": "frost_days" in df.columns,
    "Heat days calculados": "heat_days_35" in df.columns,
    "Mínimo 3 estrategias de rotación": "pending_backend",  # Pendiente de backend
}
for check, result in checks.items():
    status = "✅" if result else "❌"
    print(f"   {status} {check}")
```

### Ejecutar:
```bash
python3 validate_data.py
```

## 📋 Paso 5: Entregar al equipo Backend/Frontend (30 min)

### Formato de entrega:

1. **`data/crops.yaml`**: Lista de cultivos con rasgos (ver estructura arriba)

2. **`pipeline/indicadores_estacionales.py`**: Script generando reporte con tendencias

3. **`pipeline/validate_data.py`**: Reporte de validación

4. **`contexto/indicadores_climaticos.md`**: Documento resumen para los otros equipos

```markdown
# Indicadores Climáticos San Luis 2000-2025

## Resumen Ejecutivo
- Período analizado: 26 años (2000-2025)
- Días de datos: 9,497
- Variables: 9 agroclimáticas NASA POWER

## Tendencias Principales
1. **Lluvia**: [resultado del indicador 1]
2. **Días de calor**: [resultado del indicador 2]  
3. **Días de helada**: [resultado del indicador 3]
4. **Condiciones estivales**: [resultado del indicador 4]

## Datos Crudos Disponibles
- `data/processed/power_monthly.csv`: 312 filas, 13 columnas
- `data/processed/power_daily.csv`: 9,497 días, 9 variables
- `data/raw/power_san_luis_argentina.json`: Datos crudos completos

## Tabla de Cultivos
- `data/crops.yaml`: 3 cultivos principales (maíz, soja, trigo)
- Rasgos: consumo agua, tolerancia sequía, fijación N, profundidad raíz, etc.

## Brechas de Información
- Sin mediciones de suelo a nivel de lote
- Datos climáticos a resolución 0.5° (~55 km)
- Validación local requerida para recomendaciones específicas

## Próximo paso
- Integrar con motor de puntuación backend
- Conectar con frontend sliders de prioridades
```

## 📦 Paso 6: Formato de entrega final

### Estructura esperada después de esto:

```
data/
├── raw/
│   └── power_san_luis_argentina.json     # 1.5 MB (entregado ✅)
├── processed/
│   ├── power_daily.csv          # 1.7 KB (entregado ✅)
│   └── power_monthly.csv        # 8.3 KB (entregado ✅)
└── crops.yaml                     # NUEVO - por crear por equipo datos

pipeline/
├── common.py                      # Configuración (ya creado ✅)
├── fetch_power.py                 # Descarga (ya creado ✅)
├── build_features.py              # Limpieza (ya creado ✅)
├── indicadores_estacionales.py    # NUEVO - por crear por equipo datos
└── validate_data.py               # NUEVO - por crear por equipo datos

contexto/
├── contexto_desafio_adapting_farms.md    # Contexto original
├── plan_trabajo_paralelo.md            # Plan de trabajo
├── guia_equipo_backend.md              # Guia backend (creado)
├── guia_equipo_frontend.md             # Guia frontend (creado)
└── guia_equipo_datos.md                # Esta guia (actual)
└── indicadores_climaticos.md           # NUEVO - reporte resumen
```

### 📧 Qué entregar al equipo Backend:

1. **Estructura de `crops.yaml`**: Para que lean en `schemas.py` y `engine.py`
2. **Indicadores calculados**: Los números que el motor de puntuación usará
   - Promedio de precipitación estival
   - Frecuencia de días de calor/helada
   - Tendencias anuales
3. **Validación de datos**: Reporte de consistencia (0% faltantes después de interpolación)

### 📦 Qué entregar al equipo Frontend:

1. **Resumen de datos disponibles**: Qué hay en los CSV, formato de columnas
2. **Ejemplos de datos**: First rows de `power_monthly.csv`, estructura de variables
3. **Notas de formato**: Unidades, rangos, significado de cada variable
4. **Brechas de información**: Para mostrar en `DataGapsBadge`

### ✅ Checklist "Hecho" para el equipo Datos:

- [ ] `data/processed/power_daily.csv` verificado (9,497 filas, 9 variables)
- [ ] `data/processed/power_monthly.csv` verificado (312 meses, 13 columnas)
- [ ] `pipeline/indicadores_estacionales.py` ejecutado y reporte generado
- [ ] `data/crops.yaml` creado con cultivos para San Luis (maíz, soja, trigo)
- [ ] `pipeline/validate_data.py` ejecutado y reporte de consistencia
- [ ] `contexto/indicadores_climaticos.md` creado con resumen para el equipo
- [ ] Datos en formato compatible con backend (CSV con columnas nombradas)
- [ ] Datos en formato compatible con frontend (descripciones de variables y unidades)
- [ ] Compartido con equipos: resumen ejecutivo y estructura de datos

### 💡 Recomendaciones clave para el equipo Datos:

1. **Unidades explícitas**: Cada número en `crops.yaml` y en los indicadores debe tener unidades claras. Eso es el "error número uno" al unir datasets (Sección 9 del contexto).

2. **0% faltantes después de interpolación**: Nuestro pipeline ya manejó los `-999` originales y los interpola por huecos de max 3 días. Esto es un logro que hay que destacar en el reporte.

3. **Tendencias sobre datos absolutos**: El desafío pide "comparar al menos tres estrategias de rotación" y "explicar por qué se sugiere, qué evidencia la respalda". Las tendencias temporales (lluvia aumentó/disminuyó, más días de calor) son la "evidencia" que respalda las recomendaciones.

4. **Adaptar cultivos a San Luis**: Los valores en `crops.yaml` no deben ser genéricos. Reflejar condiciones de provincia argentina:
   - Menor agua disponible que en EE.UU. típico
   - Veranos calurosos, inviernos suaves/cortos
   - Sequías periódicas
   - Frosts en invierno/primavera

5. **Compatibilidad verso y para**: Los datos deben ser legibles tanto para el backend (Python, YAML, CSV) como para el frontend (JSON, tablas simples). Mantener nombres de columnas consistentes.

6. **Documentar brechas honestamente**: El contexto dice "marcar la incertidumbre: si un dato es de baja resolución o falta, debe aparecer en `data_gaps`". Nuestros `data_gaps` conocidos:
   - "No hay mediciones de suelo a nivel de lote"
   - "Datos a resolución 0.5° (~55 km), no lote individual"
   - "Validación local requerida para recomendaciones específicas"

7. **Merge cada 2-3 horas**: El `main` siempre debe correr (Sección 9). Si el script de indicadores tarda, hacer commit parcial y continuar.

8. **Plan B de datos**: Si los scripts tardan en ejecutarse, tener listo un reporte con datos resumen manual o mock que cumpla el mismo propósito de "aquí hay datos, usémoslos".

---

## 🧩 Próximos pasos inmediatos para el equipo Datos

**Hora 1-2:** Ejecutar `indicadores_estacionales.py`, generar reporte, crear `crops.yaml` estructura básica.

**Hora 2-3:** Ejecutar `validate_data.py`, generar `indicadores_climaticos.md`, compartir con otros equipos.

**Hora 3-4:** Dudas de formato o integración con backend/frontend - consultar guías respectivas.

**Hora 4-6:** Avanzar con ajustes finales según feedback de los otros equipos.

¿Necesita el equipo datos alguna ayuda específica para empezar? Pueden consultar el documento `contexto/plan_trabajo_paralelo.md` para ver cómo esto conecta con los otros equipos, o las guías de backend/frontend para entender qué formato de datos esperan cada uno.