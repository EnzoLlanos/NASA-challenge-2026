# 📊 División de Trabajo: Equipo Datos (Juan y Martin)

## 👥 Contexto
El equipo de datos se divide en dos personas para acelerar el avance del proyecto NASA Space Apps 2026, con **1 día** disponible y 6 personas en total.

**Yo soy:** Juan  
**Mi compañero es:** Martin

El dataset NASA POWER ya está **100% procesado y listo**:
- `data/raw/power_san_luis_argentina.json` (1.5 MB, 9,497 días, 26 años)
- `data/processed/power_daily.csv` (1.7 KB)
- `data/processed/power_monthly.csv` (8.3 KB, 312 meses)
- 0% datos faltantes (post-interpolación de huecos ≤ 3 días)

---

## 📋 Tareas Pendientes del Equipo Datos

Queda el siguiente trabajo por dividir:

| # | Tarea | Descripción | Complejidad |
|---|-------|-------------|-------------|
| **1** | `indicadores_estacionales.py` | Calcular tendencias climáticas a 26 años (lluvia, calor, heladas, estaciones) | Alta |
| **2** | `data/crops.yaml` | Crear tabla de cultivos con rasgos para San Luis (maíz, soja, trigo) | Media |
| **3** | `pipeline/validate_data.py` | Reporte de consistencia y validación de datos | Media |
| **4** | `contexto/indicadores_climaticos.md` | Reporte resumen para todo el equipo | Media |

---

## 🧑‍💻 División de Trabajo: Juan vs Martin

### ⚜️ PARTE DE JUAN:
**Enfoque:** Análisis estadístico, tendencias a largo plazo y reportes resumen.

**Tareas asignadas:**

1. **📈 Ejecutar `indicadores_estacionales.py` completo**
   - Calcular tendencia de lluvia anual (2000-2025)
   - Calcular días de calor extremo (>35°C) por década
   - Calcular días de helada (temp ≤ 0°C) por década
   - Promedios estivales (DJF: diciembre-enero-febrero)
   - Balanza estación seca vs. húmeda

   **Script a modificar/extender:** `pipeline/indicadores_estacionales.py`

   **Entregable a Martin:**
   - Diccionario con todos los indicadores calculados
   - Gráficos o tablas resumen (puede ser en formato texto/markdown)
   - Comentarios sobre hallazgos principales

2. **📝 Redactar `contexto/indicadores_climaticos.md`**
   - Tomar los resultados del paso 1
   - Formatear como reporte profesional para todo el equipo
   - Incluir: resumen ejecutivo, tendencias principales, datos crudos disponibles, brechas de información

   **Entregable final:**
   - Archivo `contexto/indicadores_climaticos.md` completo y formateado

---

### ✂️ PARTE DE MARTIN:
**Enfoque:** Estructuras de datos, validación y conexión con el resto del proyecto.

**Tareas asignadas:**

1. **🌱 Crear `data/crops.yaml` con rasgos para San Luis**
   - Definir 5-7 cultivos comunes en la región
   - Especificar para cada cultivo:
     - `water_consumption`: mm por ciclo
     - `drought_tolerance`: 0-1 scale
     - `nitrogen_fixation`: boolean
     - `root_depth`: cm
     - `soil_coverage`: fracción (0-1)
     - `organic_matter`: % aporte
     - `market_potential`: alto/medio/bajo
     - `adaptation_notes`: observaciones específicas San Luis

   **Referencia:** Estructura vista en `guia_equipo_datos.md` y `engine.py` mock

   **Entregable a Juan:**
   - Archivo `data/crops.yaml` completo y formateado
   - Documento corto explicando las decisiones de valores (por qué esos números para San Luis)

2. **✅ Ejecutar `pipeline/validate_data.py` y reportar**
   - Validar consistencia de `power_monthly.csv` y `power_daily.csv`
   - Reportar: total de filas, columnas, rangos de fechas, % faltantes, consistencia temporal
   - Verificar que el formato sea compatible con el backend FastAPI

   **Script a ejecutar:** `pipeline/validate_data.py` (ya existe, solo ejecutar)

   **Entregable a Juan:**
   - Reporte de validación (puede ser texto, markdown o los resultados del script)
   - Observaciones sobre compatibilidad con los schemas del backend

---

## 🔄 Flujo de Trabajo y Handoff

### 📅 Día sugerido (distribución de horas):

**Horas 1-3 (Juan):**
- Ejecutar y completar `indicadores_estacionales.py`
- Generar diccionario de indicadores

**Horas 1-3 (Martin):**
- Crear `data/crops.yaml` con 5 cultivos para San Luis
- Ejecutar `validate_data.py` y recolectar resultados

**Horas 3-4 (Integración):**
- Compartir resultados entre sí
- Juan entrega `indicadores_climaticos.md` (borrador)
- Martin entrega `crops.yaml` + validación reporte

**Horas 4-6 (Finalización):**
- Juan termina el reporte `indicadores_climaticos.md` con los datos de Martin
- Martin revisa si necesita ajustes en `crops.yaml` basándose en los indicadores de Juan
- Ambos firman completado el trabajo de datos

### 📤 Formato de intercambio:

**Juan entrega a Martin:**
```json
{
  "indicadores": {
    "lluvia_promedio_anual": 85.5,
    "tendencia_lluvia": "reducción",
    "dias_calor_por_decada": {2000: 2, 2010: 5, 2020: 8},
    "heladas_por_decada": {...},
    "temp_estival_promedio": 22.5,
    "precip_estival_promedio": 139.3
  },
  "reporte_markdown": "contenido del indicadores_climaticos.md"
}
```

**Martin entrega a Juan:**
```yaml
# data/crops.yaml contenido
maíz:
  water_consumption: 500
  drought_tolerance: 0.3
  ...
```

### 🎯 Objetivo Común

Que al finalizar el trabajo de datos:

1. ✅ Tenemos **indicadores climáticos claros** que el backend usará para calcular scores de rotación
2. ✅ Tenemos **crops.yaml** con rasgos consistentes con el clima de San Luis
3. ✅ Todo el equipo (backend, frontend, coordinación) tiene **datos estructurados** para continuar
4. ✅ El `contexto/` tiene **reportes documentados** para el pitch y documentación

### 🛠️ Herramientas y Comandos

**Para Juan:**
```bash
# Ejecutar análisis de tendencias
python3 pipeline/indicadores_estacionales.py

# Revisar output y generar reporte
# Editar contexto/indicadores_climaticos.md
```

**Para Martin:**
```bash
# Crear crops.yaml (usando el template de guia_equipo_datos.md)
# Ejecutar validación
python3 pipeline/validate_data.py

# Revisar output y formatear resultados
# Entregar crops.yaml + reporte validación
```

### 📞 Preguntas Clave para la Coordinación

1. **Valores de crops.yaml**: ¿Están basados en datos reales o son estimaciones? Martín debe documentar la fuente/razonamiento.

2. **Formato de indicadores**: Juan, ¿en qué formato quiere recibir los datos de Martín para integrarlos al reporte? (JSON, markdown, CSV?)

3. **Compatibilidad**: ¿Los valores de `crops.yaml` son compatibles con los schemas Pydantic del backend? Martín debe asegurar que los nombres y tipos coincidan.

4. **Tiempo de entrega**: ¿A qué hora (del día) cada uno debe tener listo su parte para la integración?

---

## ✅ Checklist de Finalización

### Para Juan (marcar al completar):
- [ ] `pipeline/indicadores_estacionales.py` ejecutado sin errores
- [ ] Diccionario de indicadores calculados (lluvia, calor, heladas, estacional)
- [ ] `contexto/indicadores_climaticos.md` completo y formateado
- [ ] Archivo entregado a Martin con resultados

### Para Martin (marcar al completar):
- [ ] `data/crops.yaml` creado con 5 cultivos mínimos (maíz, soja, trigo + 2 más)
- [ ] Valores con unidades explícitas y rationale documentado
- [ ] `pipeline/validate_data.py` ejecutado y reporte recolectado
- [ ] Entregable a Juan: crops.yaml + validación reporte

### Compartido (ambos):
- [ ] Resulta integrados y revisados mutuamente
- [ ] `contexto/indicadores_climaticos.md` es el reporte oficial
- [ ] El equipo completo puede continuar (backend usa indicadores, frontend sabe qué datos hay)

---

## 💡 Recomendaciones Finales

1. **Commitear individual**: Cada uno haga commit de sus cambios en ramas separadas:
   - `git checkout -b trabajo/datos/juan/indicadores`
   - `git checkout -b trabajo/datos/martin/crops`

2. **Merge antes de integrar**: Antes de entregar el otro parte, hacer merge a `main` o a una rama compartida `datos/paralelo`

3. **Unidades explícitas**: Este es el error número uno (Sección 9 del contexto). Martín, asegúrese que todos los números en `crops.yaml` tengan unidades en la descripción. Juan, lo mismo para los indicadores.

4. **Honestidad en brechas**: Ambos deben estar de acuerdo en qué datos faltan y cuáles no. El contexto exige marcar incertidumbre claramente.

5. **Soporte mutuo**: Si alguno traba en su parte, el otro ayuda en lo básico (por ejemplo, Juan ayuda con la estructura YAML de Martín, Martín ayuda con la interpretación de gráficos de Juan).

---

## 📋 Estado Inicial

| Componente | Responsable | Estado |
|---|---|---|
| `pipeline/indicadores_estacionales.py` | Juan | Pendiente (Step 1) |
| `data/crops.yaml` | Martin | Pendiente (Step 1) |
| `pipeline/validate_data.py` | Martin | Pendiente (ejecutar) |
| `contexto/indicadores_climaticos.md` | Juan | Pendiente (generar a partir de indicadores) |
| Integración mutua | Ambos | Por definir (después de partes individuales) |

---
*Documento creado para coordinar trabajo paralelo en NASA Space Apps Challenge 2026*
*Juan y Martin, equipo de datos | 1 día disponible | 6 personas en proyecto total*