# 📦 Entrega Equipo Datos (Martin) — NASA Space Apps 2026

**Fecha:** 2026-01-14 · **Rama:** `trabajo/datos/martin` · **Validación:** 29/29 checks OK

---

## 1. Qué se entregó

| Archivo | Estado | Descripción |
|---|---|---|
| `data/crops.yaml` | ✅ nuevo | 7 cultivos para San Luis con rasgos y unidades explícitas |
| `pipeline/validate_data.py` | ✅ nuevo | 29 checks de consistencia, ejecutable con `python pipeline/validate_data.py` |
| `pipeline/build_features.py` | ✅ corregido | Bug de `save_daily_csv` + 12 columnas en monthly |
| `data/processed/power_daily.csv` | ✅ regenerado | 9,497 filas × 10 columnas, 0 None, 0 -999 |
| `data/processed/power_monthly.csv` | ✅ regenerado | 312 filas × 12 columnas, 0 NaN |

---

## 2. Para Juan (indicadores + `indicadores_climaticos.md`)

**`power_monthly.csv` ahora tiene las columnas que tu script necesita:**

```
year_month, year, month, temp_mean_c, temp_max_c, temp_min_c,
precip_mm_sum, frost_days, heat_days_35, soil_wet_root_mean,
evap_land_mm_sum, total_days
```

- `year` y `month` están como columnas separadas → `df.groupby('year')` funciona directo.
- Nuevas: `temp_max_c`, `temp_min_c` (útiles para extremos), `soil_wet_root_mean` (humedad de suelo), `evap_land_mm_sum` (evapotranspiración) → puedes sumar indicadores de estrés hídrico.
- **Ojo con un bug en la guía:** el umbral de "meses secos" del ejemplo (`precip < 50 mm`) es para un umbral mensual genérico; en San Luis el promedio mensual ronda 40-140 mm, revisá el corte.

**Entregable tuyo pendiente:** `contexto/indicadores_climaticos.md` con tendencias (lluvia, calor por década, heladas por década, estacionalidad).

---

## 3. Para Backend (`schemas.py`, `engine.py`, `data_loader`)

### `crops.yaml` — estructura por cultivo (7 cultivos: maíz, soja, trigo, sorgo, girasol, cebada, arveja)

```yaml
maíz:
  name: "Maíz"
  water_consumption: 500        # mm por ciclo completo
  drought_tolerance: 0.3        # 0-1
  nitrogen_fixation: false
  root_depth: 150               # cm
  soil_coverage: 0.8            # fracción 0-1
  organic_matter: 0.05          # % por ciclo
  market_potential: "alto"      # alto | medio | bajo
  season: "verano"              # verano | invierno | cubierta  (extra, Pydantic lo ignora)
  cycle_months: 6               # (extra)
  adaptation_notes: "..."
```

Los campos coinciden con el schema `CropInfo` de la guía. Los extras `season` y `cycle_months` sirven para armar rotaciones verano↔invierno en `engine.py` (rotación con dos cultivos de verano seguidos no tiene sentido agronómico —validar en el motor).

**Cómo leerlo:**
```python
import yaml
crops = yaml.safe_load(open("data/crops.yaml", encoding="utf-8"))
```

### `power_monthly.csv` — para `climate_summary` / `field-profile`

Promedios calculados ya verificados (2000-2025, San Luis):

| Indicador | Valor (aprox.) |
|---|---|
| Temp media anual | 17.4 °C |
| Temp máx media mensual | 32.8 °C |
| Temp mín media mensual | 3.7 °C |
| Precipitación anual | ~ 650 mm (verificar con indicadores de Juan) |
| frost_days (totales 26 años) | ver `validate_data.py` output |
| heat_days_35 (totales 26 años) | ver `validate_data.py` output |

> ⚠️ El backend debe leer estos CSV en tiempo de arranque (`data_loader`), no hardcodear. La resolución POWER es 0.5° (~55 km): sirve para clima regional, NO para lote individual.

---

## 4. Para Frontend

### Datos disponibles para visualizar

**`power_monthly.csv`** (312 puntos, ideal para gráficos de línea/tendencia):

| Columna | Unidad | Uso sugerido |
|---|---|---|
| `year_month` | AAAA-MM | eje X de series |
| `temp_mean_c`, `temp_max_c`, `temp_min_c` | °C | temperatura, bandas de extremos |
| `precip_mm_sum` | mm/mes | lluvia mensual, estacionalidad |
| `frost_days` | días/mes | riesgo de helada (badge naranja) |
| `heat_days_35` | días/mes | olas de calor (badge rojo) |
| `soil_wet_root_mean` | fracción 0-1 | humedad del suelo (mostrar como %) |
| `evap_land_mm_sum` | mm/mes | evapotranspiración |
| `total_days` | días | días con datos en el mes |

**`power_daily.csv`** (9,497 filas): mismo esquema a nivel día, para zoom de temporada.

**`crops.yaml`** → `GET /api/crops`: mostrar `water_consumption` como "L/m²" o mm, `drought_tolerance` y `soil_coverage` como barras 0-100%, `market_potential` como chip de color (alto=verde, medio=amarillo, bajo=gris).

### `data_gaps` a mostrar en `DataGapsBadge` (honestidad técnica)

1. Sin mediciones de suelo a nivel de lote (solo modelo a 0.5°).
2. Datos climáticos a resolución 0.5° (~55 km) — no representan el microclima del campo.
3. Sin datos NDVI/satelitales aún (pendiente / mock).
4. Rasgos de cultivos son estimaciones FAO/INTA, requieren validación con técnico local.
5. Recomendaciones válidas como apoyo a la decisión, no reemplazan la experiencia agronómica local.

---

## 5. Estado de validación (resumen)

```
1. power_daily.csv     → 11/11 OK (9,497 filas continuas, sin None/-999)
2. power_monthly.csv   →  9/9  OK (312 meses, 12 columnas, 0 NaN)
3. data/crops.yaml     →  6/6  OK (7 cultivos, campos CropInfo completos)
4. Compat backend      →  3/3  OK (year/month, climate_summary, nombres engine.py)
                        → 29/29 OK en total
```

**Regenerar datos tras cambios:**
```bash
python pipeline/build_features.py   # regenera los CSV (requiere data/raw/)
python pipeline/validate_data.py    # re-valida todo
```

---

## 6. Pendientes / siguientes pasos del equipo datos

- [ ] ~~`data/crops.yaml`~~ ✅ hecho (7 cultivos)
- [ ] ~~`pipeline/validate_data.py`~~ ✅ hecho (29/29)
- [ ] ~~Fix `power_daily.csv`~~ ✅ hecho (9,497 filas reales)
- [ ] ~~Columnas `year`/`month` en monthly~~ ✅ hecho (bloqueaba a Juan)
- [ ] **Juan:** ejecutar `indicadores_estacionales.py` → `contexto/indicadores_climaticos.md`
- [ ] **Martin (opcional):** `requirements.txt` del pipeline (pandas, pyyaml)
- [ ] **Coordinación:** avisar a backend cuando Juan publique indicadores para cerrar `field-profile`

---

*Entregado por Martin — rama `trabajo/datos/martin`*
