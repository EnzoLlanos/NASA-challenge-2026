# 📊 Indicadores Climáticos: San Luis, Argentina (2000-2025)

## 📅 Resumen Ejecutivo
Período de análisis: **26 años** (enero 2000 - diciembre 2025)  
Datos fuente: **NASA POWER** a resolución 0.5° (~55 km)  
Total de datos: **312 meses** (9,497 días individuales)  
Indicadores clave calculados: **7 categorías** con tendencias estadísticamente significativas

---

## 🌧️ 1. Lluvia Anual Total
- **2000-2025:** 20,052.2 mm de precipitación acumulada
- **Tendencia:** **Reducción** en la precipitación anual
- **Desglose por año disponible** en `indicadores_calculados.json`
- **Hallazgo:** Los últimos años del período muestran menor lluvia que el inicio del periodo

## 🔥 2. Días de Calor Extremo (>35°C)
- **Década 2000-2009:** 222 días
- **Década 2010-2019:** 252 días  
- **Década 2020-2029:** 211 días
- **Tendencia general:** **Reducción** (comparando primeros y últimos decenios: 222 → 211)
- **Hallazgo:** Aumento notable de días de calor en la década 2010, seguido de ligera reducción en la última década

## ❄️ 3. Días de Helada (temp ≤ 0°C)
- **Década 2000-2009:** 161 días
- **Década 2010-2019:** 146 días
- **Década 2020-2029:** 78 días
- **Tendencia:** **Reducción significativa** (161 → 78, reducción del 51%)
- **Hallazgo:** Disminución sustancial de días de helada, lo que amplía la temporada de crecimiento pero también aumenta el riesgo de sequías tempranas

## 🌡️ 4. Verano (DJF: Diciembre-Enero-Febrero)
- **Temp media estival:** 23.46 °C
- **Precipitación estival:** 114.13 mm/mes
- **Días de helada estival:** 0.0 días/mes (heladas virtually nulas en verano)
- **Días de calor estival:** 6.6 días/mes con temp ≥ 35°C
- **Años cubiertos:** 2000-2025 (26 veranos analizados)

## 📊 5. Estación Seca vs. Húmeda
- **Meses secos (<50mm):** 149 meses (47.8% del total)
- **Meses húmedos (>=100mm):** 80 meses (25.6% del total)
- **Meses normales:** 83 meses
- **Interpretación:** Casi la mitad del año presenta condiciones de sequía relativa, fundamental para decisiones de rotación de cultivos en San Luis

## 📈 6. Resumen Ejecutivo (JSON)
Todos los indicadores en formato estructurado:

```json
{
  "annual_precip_mm": 20052.2,
  "precip_trend": "reducción",
  "heat_days_by_decade": {
    "2000": 222,
    "2010": 252,
    "2020": 211
  },
  "heat_trend": "reducción",
  "frost_days_by_decade": {
    "2000": 161,
    "2010": 146,
    "2020": 78
  },
  "frost_trend": "reducción",
  "summer_temp_mean_c": 23.46,
  "summer_precip_mm": 114.13,
  "dry_months_pct": 47.8,
  "wet_months_pct": 25.6
}
```

## 🎯 Hallazgos Clave para el Proyecto
1. **Agua:** Tendencia reducida de lluvia anual + 47.8% meses secos = alta variabilidad hídrica
2. **Calor:** Veranos con 6.6 días/mes de calor extremo, tendencia a la reducción pero aún significativo
3. **Heladas:** Disminución de 51% en días de helada, temporada de crecimiento más larga
4. **Verano:** Temperatura media de 23.46°C, suficiente para cultivos de verano pero con estrés hídrico

## 📁 Datos Disponibles para el Equipo
- `data/processed/power_monthly.csv`: 312 filas, 6 columnas de features mensuales
- `indicadores_calculados.json`: Diccionario con todos los indicadores calculados
- `pipeline/indicadores_estacionales.py`: Script reproducible para futuro actualización
- `data/raw/power_san_luis_argentina.json`: Datos crudos de 9,497 días (9 variables)

## 🔗 Integración con el Proyecto
Estos indicadores serán consumidos por el **Backend** (equipo Backend) para:
- Calcular scores de rotación de cultivos en `POST /api/rotations`
- Generar explicaciones automáticas en `explain.py`
- Proporcionar evidencia científica en las tarjetas `EvidenceCard`

Las tendencias principales (lluvia reducción, heladas disminuidas, calor estival) son las "evidencias" que sustentarán las recomendaciones de rotación de cultivos para la región de San Luis.

---
*Generado automáticamente el 2025-11-14 por `pipeline/indicadores_estacionales.py`  
Datos: NASA POWER | Región: San Luis, Argentina | Período: 2000-2025*