# 🗺️ Zonificación Agrícola y Validación Científica de Cultivos: San Luis

**Autor / Responsable:** Mati (Experto en Datos Agrícolas y Zonificación)  
**Proyecto:** Adapting Farms with NASA Data (NASA Space Apps Challenge 2026)  
**Fecha:** 2026-11-15  
**Estado:** Fase 1 completada (listo para integración con Backend y UI)

---

## 🎯 Objetivo de la Zonificación
Los agricultores de San Luis no enfrentan las mismas condiciones en el norte serrano que en las planicies arenosas del sur. Para ofrecer recomendaciones de rotación realistas y comprensibles a productores de cualquier nivel técnico, dividimos la provincia en **3 zonas agroclimáticas homogéneas** sustentadas en observaciones satelitales y agroecológicas globales oficiales de la NASA y la FAO.

---

## 🛰️ Datasets Globales Oficiales Utilizados
Siguiendo las fuentes recomendadas del desafío NASA Space Apps 2026:

1. **NASA POWER (Agroclimatology & Meteorology, 2000–2025):**
   * Cobertura histórica de 26 años a resolución diaria/mensual (0.5°).
   * Variables clave analizadas:
     * `T2M` / `T2M_MAX` / `T2M_MIN`: Temperaturas medias y térmicas extremas.
     * `frost_days`: Frecuencia anual de días con $T_{min} \le 0^\circ\text{C}$.
     * `heat_days_35`: Días con estrés térmico severo ($T_{max} \ge 35^\circ\text{C}$).
     * `GWETROOT` (0–1): Humedad de suelo en la zona radicular modelada por Goddard Earth Observing System.
     * `PRECTOTCORR`: Precipitación acumulada.

2. **SRTM (Shuttle Radar Topography Mission - Modelos de Elevación 30 m):**
   * Gradiente altimétrico y morfológico de la provincia:
     * *Norte:* Sierras centrales y Valle del Conlara (800 a 1.200 msnm), pendientes pronunciadas y microclimas de valle.
     * *Centro:* Planicie aluvial y cuenca del río Quinto (500 a 750 msnm).
     * *Sur:* Llanura medanosa y deprimida (< 450 msnm).

3. **FAO GAEZ v4 (Global Agro-Ecological Zones):**
   * Metodología de referencia para el cálculo de **Aptitud Agroclimática (`aptitud_zona`)**:
     * **Muy Apta / Alta ($0.80 - 1.00$):** Condiciones de temperatura, radiación y disponibilidad de agua óptimas para el ciclo fenológico.
     * **Moderada ($0.55 - 0.79$):** Condiciones viables con riesgo de estrés térmico o hídrico en ventanas puntuales.
     * **Marginal / Baja ($0.25 - 0.54$):** Alto riesgo de pérdida de rendimiento en secano sin suplemento hídrico o variedades ultra-resistentes.

4. **Copernicus Sentinel-2 / Landsat (NDVI & Suelo Desnudo):**
   * Sustento para la inclusión de cultivos de invierno/cobertura (*arveja*, *cebada*, *trigo*): protegen el perfil edáfico de la erosión hídrica en laderas (norte) y de la erosión eólica sobre suelos sueltos (sur) entre mayo y agosto.

---

## 📊 Comparativa Agroclimática por Zona (Datos Reales NASA POWER 2000–2025)

| Indicador Clave | Zona Norte (Valle Conlara / Merlo) | Zona Centro (San Luis / V. Mercedes) | Zona Sur (Buena Esperanza / Dupuy) |
| :--- | :---: | :---: | :---: |
| **Punto Referencia** | Lat -32.35, Lon -65.00 | Lat -33.30, Lon -65.30 | Lat -34.70, Lon -65.30 |
| **Altitud (SRTM)** | 800 – 1.200 msnm (Serrano) | 500 – 750 msnm (Planicie) | 350 – 500 msnm (Llanura medanosa) |
| **Lluvia Media Anual** | **748 mm/año** | **771 mm/año** | **773 mm/año** |
| **Días de Helada ($T \le 0^\circ\text{C}$)** | **34.7 días/año** | **14.8 días/año** | **15.7 días/año** |
| **Días Calor Extremo ($\ge 35^\circ\text{C}$)** | **2.8 días/año** | **26.3 días/año** | **34.0 días/año** |
| **Humedad Raíz (`GWETROOT`)** | **0.597** (Alta retención) | **0.413** (Media) | **0.326** (Baja retención / suelo arenoso) |
| **Temperatura Media Anual** | **14.5 °C** | **17.0 °C** | **16.8 °C** |
| **Estrés Hídrico Estival** | Bajo | Moderado | **Severo (calor + suelo seco)** |
| **Riesgo Agronómico Crítico** | Heladas tardías / Erosión hídrica | Olas de calor estivales | Sequía agronómica y erosión eólica |

> 💡 **Hallazgo Clave del Análisis de Datos:**  
> La precipitación promedio anual acumulada en los 26 años es prácticamente idéntica en toda la provincia (~750 a 770 mm/año). Sin embargo, el **Sur experimenta 12 veces más días de calor sofocante ($\ge 35^\circ\text{C}$)** que el Norte y su suelo retiene casi la **mitad de agua en la zona de raíces (`GWETROOT` 0.32 vs 0.60)**. Por ende, la aridez del Sur es de naturaleza **edáfica y evaporativa**, justificando plenamente cultivos rústicos y de raíz profunda.

---

## 🌾 Matriz de Aptitud por Cultivo y Zona (FAO GAEZ + NASA POWER)

| Cultivo | Norte | Centro | Sur | Justificación Agronómica |
| :--- | :---: | :---: | :---: | :--- |
| 🌽 **Maíz** | **0.85** *(Alto)* | **0.60** *(Medio)* | **0.30** *(Marginal)* | Demanda 500 mm concentrados en floración. En el Sur, las olas de calor (>34 d) abortan espigas sin riego. En el Norte, la humedad del suelo (0.60) amortigua la demanda. |
| 🌱 **Soja** | **0.85** *(Alto)* | **0.65** *(Medio)* | **0.40** *(Marginal)* | Fija nitrógeno; excelente en rotación en Norte/Centro. En el Sur es riesgosa en años secos. |
| 🌾 **Trigo** | **0.70** *(Medio)* | **0.80** *(Alto)* | **0.65** *(Medio)* | Tolera frío y sequía invernal. En el Norte serrano requiere monitorear heladas tardías primaverales. |
| 🌾 **Sorgo** | **0.60** *(Medio)* | **0.80** *(Alto)* | **0.95** *(Óptimo)* | Cultivo rey para el Sur semiárido: raíz de hasta 200 cm, metabolismo C4 eficiente frente a olas de calor y 40% menos consumo de agua que el maíz. |
| 🌻 **Girasol** | **0.65** *(Medio)* | **0.80** *(Alto)* | **0.90** *(Óptimo)* | Raíz pivotante profunda (hasta 250 cm) que extrae agua en suelos arenosos del Sur donde el maíz no llega. |
| 🍺 **Cebada** | **0.65** *(Medio)* | **0.75** *(Alto)* | **0.85** *(Óptimo)* | Ciclo invernal más corto y menor demanda de agua que el trigo; ideal para antecesor de verano en el Sur. |
| 🟢 **Arveja** | **0.80** *(Alto)* | **0.85** *(Óptimo)* | **0.80** *(Alto)* | Cobertura total (95%) y fijación biológica de N2. Fundamental para evitar que los suelos del Sur queden desnudos y sufran voladuras de tierra en invierno. |

---

## 📁 Archivos Generados para el Equipo

1. `data/zonas.yaml`: Especificación formal de cada zona con coordenadas, límites, riesgo y datos climáticos medidos.
2. `data/zonas/crops_norte.yaml`: Rasgos y aptitudes calibradas para la zona Norte.
3. `data/zonas/crops_centro.yaml`: Rasgos y aptitudes calibradas para la zona Centro.
4. `data/zonas/crops_sur.yaml`: Rasgos y aptitudes calibradas para la zona Sur.
5. `data/processed/power_monthly_norte.csv` & `power_monthly_sur.csv`: Series temporales mensuales (2000–2025) derivadas de NASA POWER.
6. `pipeline/build_zonas.py`: Script reproductor de la calibración agroecológica.
