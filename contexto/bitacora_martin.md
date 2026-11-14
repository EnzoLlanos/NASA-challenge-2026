# 📔 Bitácora personal — Martin (Equipo Datos)

> **Archivo solo mío.** Acá registro todo lo que voy haciendo, lo que encuentro,
> decisiones y pendientes. No es documentación oficial del proyecto (esa está en
> `contexto/entrega_datos_martin.md`).

---

## 🧑 Quién soy en el proyecto

- **Nombre:** Martin
- **Equipo:** Datos (2 personas: yo + Juan)
- **Mi enfoque:** estructuras de datos, validación, conexión con backend/frontend
- **Enfoque de Juan:** análisis estadístico, tendencias a largo plazo, `indicadores_climaticos.md`
- **Rama de trabajo:** `trabajo/datos/martin` (un commit por punto)
- **Región piloto:** San Luis, Argentina (-33.30, -65.30), período 2000-2025

---

## ✅ Lo que ya hice (con commits)

### Punto 1 — `data/crops.yaml` (`d199077`)
- 7 cultivos: maíz, soja, trigo, sorgo, girasol, cebada, arveja
- Unidades explícitas en cada campo (mm, cm, fracción 0-1, %)
- Racional documentado en comentarios (por qué cada valor para San Luis)
- Campos exactos del schema `CropInfo` del backend + extras `season` y `cycle_months`
  (útiles para que el motor no arme rotaciones con dos cultivos de verano seguidos)
- ⚠️ Valores = estimaciones FAO/INTA, NO mediciones de lote → debe aparecer en `data_gaps`

### Fix del pipeline — `build_features.py` (`8fa9212`)
- **Bug encontrado:** `save_daily_csv` buscaba las variables con los nombres originales
  (`T2M`, `PRECTOTCORR`…) pero el dict ya estaba renombrado (`temp_mean_c`…) →
  todo salía en `None`, y solo guardaba 30 fechas
- Resultado: `power_daily.csv` ahora tiene **9,497 filas reales, 0 None, 0 -999**

### Punto 4 — `power_monthly.csv` (`781ace7`)
- De 6 a **12 columnas**: +`year`, `month`, `temp_max_c`, `temp_min_c`,
  `soil_wet_root_mean`, `evap_land_mm_sum`
- Esto **desbloqueaba a Juan**: su `indicadores_estacionales.py` usa `df['year']` y
  `df['month']` que no existían → habría fallado

### Punto 2 — `pipeline/validate_data.py` (`8ce560e`)
- **29/29 checks OK**: daily (11), monthly (9), crops.yaml (6), compat backend (3)
- El de la guía tenía errores de sintaxis (`from datetime import Path`, f-strings rotas)
  → lo escribí limpio
- Fix adicional: `sys.stdout.reconfigure(encoding="utf-8")` para que la consola
  Windows (cp1252) pueda imprimir emoji/acentos

### Entrega documental — `contexto/entrega_datos_martin.md` (`bd2a364`)
- Resumen para Juan (columnas nuevas del CSV)
- Resumen para backend (estructura crops.yaml + cómo leerlo)
- Resumen para frontend (tabla de columnas con unidades + `data_gaps` a mostrar)

### `requirements.txt` (`4720147`)
- pandas, pyyaml, requests

---

## 🖥️ Entorno (importante — no se olvida)

- **Python NO estaba instalado** en la máquina → lo instalé con winget
- **Ruta exacta** (no está en PATH de la shell actual):
  ```
  C:\Users\Urtizberea\AppData\Local\Programs\Python\Python312\python.exe
  ```
- Instalados: pandas 3.1.1, pyyaml
- Para correr el pipeline (desde la raíz del repo):
  ```bash
  # alias temporal para esta sesión:
  PY="C:/Users/Urtizberea/AppData/Local/Programs/Python/Python312/python.exe"
  $PY pipeline/build_features.py    # regenera los CSV
  $PY pipeline/validate_data.py     # re-valida todo (29 checks)
  ```
- Si Juan no puede correr Python: avisarle que abra terminal nueva
  (PATH se actualiza al abrir una nueva sesión) o use la ruta completa

---

## 🔍 Hallazgos que encontré (para no redescubrir)

1. **`power_daily.csv` decía "1.7 KB / 9,497 filas" en la doc pero tenía 30 filas en `None`**
   → ya corregido, pero ojo: `pipeline_log.md` (de Juan/equipo) todavía dice
   "1.7 KB" — actualizar si hace falta.
2. **La guía de Juan (`guia_equipo_datos.md`) tiene el script `validate_data.py`
   con errores de sintaxis** → el real es `pipeline/validate_data.py`.
3. **Umbral de "meses secos" en la guía (`precip < 50mm`)**: en San Luis el
   promedio mensual ronda 40-140 mm; ese corte es arbitrario, Juan debería revisarlo.
4. **El backend es Express/Node (`Back/`)**, no FastAPI como asumen las guías.
   Solo tiene `/api/health`. El contrato de datos lo siguen definiendo ellos.
5. **Resolución POWER = 0.5° (~55 km)**: sirve para clima regional, NO para lote.
   Siempre en `data_gaps`.
6. `data/raw/` NO está en `.gitignore` (el contexto decía que debía) →
   el JSON de 1.5 MB se está commiteando. ¿Avisar a coordinación?

---

## ⏳ Pendientes míos

- [ ] Merge a `main` cuando Juan/others revisen (¿pedir review?)
- [ ] Verificar que `indicadores_estacionales.py` de Juan corra contra los CSV
      nuevos (columnas `year`/`month` ya agregadas)
- [ ] Opcional: subir `requirements.txt` a conocimiento del equipo
- [ ] Opcional: avisar a Juan sobre el fix de `power_daily.csv` y las columnas nuevas
- [ ] Pendiente de ellos (no mío, pero bloquea integración):
      Juan → `indicadores_climaticos.md` · Backend → `schemas.py` + endpoints

---

## 📌 Cómo trabajo (reglas que me impongo)

1. Un commit por punto en `trabajo/datos/martin` (no mezclar)
2. Unidades explícitas en todo (error #1 al unir datasets)
3. Antes de crear algo, revisar si la guía ya lo trae (y corregir sus bugs)
4. Validar con `validate_data.py` antes de cada commit que toque datos
5. Honestidad en `data_gaps`: nada de prometer precisión de lote

---

*Última actualización: 2026-01-14 — 6 commits en la rama*
