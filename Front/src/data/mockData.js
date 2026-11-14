// Datos compartidos entre Dev 1 (Configuración) y Dev 2 (Resultados)

export const SAMPLE_LOT_SAN_LUIS = {
  id: "lote-san-luis-demo",
  name: "Establecimiento Don Pedro - San Luis",
  coords: { lat: -33.675, lng: -65.457 },
  currentCrop: "Soja",
  irrigation: "lluvia",
  soilType: "Franco-arenoso, susceptible a erosión eólica",
  priorities: { water: true, nutrients: true, erosion: true, forageProfit: false }
};

export const CROP_OPTIONS = [
  { value: "Soja", label: "🌱 Soja" },
  { value: "Maíz", label: "🌽 Maíz" },
  { value: "Trigo", label: "🌾 Trigo" },
  { value: "Girasol", label: "🌻 Girasol" }
];

export const PRIORITY_OPTIONS = [
  { id: "water", label: "Cuidar agua", desc: "Más infiltración, menos evaporación", icon: "💧" },
  { id: "nutrients", label: "Recuperar nutrientes", desc: "Nitrógeno biológico y materia orgánica", icon: "🧪" },
  { id: "erosion", label: "Frenar erosión", desc: "Cobertura frente a viento y lluvia", icon: "🛡️" },
  { id: "forageProfit", label: "Sumar forraje / renta", desc: "Pastoreo liviano o doble propósito", icon: "🐄" }
];

export const MOCK_SIMULATION_RESULT = {
  lotInfo: SAMPLE_LOT_SAN_LUIS,
  timestamp: new Date().toISOString(),
  strategies: [
    {
      id: "actual",
      name: "Estrategia Actual (Monocultivo)",
      tag: "Riesgo Hídrico y Nutricional",
      badgeType: "danger",
      sequence: ["Soja", "Barbecho largo (suelo desnudo)", "Soja"],
      soilHealthScore: 42,
      metrics: {
        water: "Baja (pérdida por evaporación en barbecho)",
        nutrients: "Deficitaria en N y materia orgánica",
        erosion: "Alto riesgo en meses ventosos",
        margin: "Depende 100% de la lluvia de verano"
      },
      nasaEvidence: "SMAP y MODIS detectan 4 meses con suelo desnudo y estrés térmico recurrente en floración.",
      localRisk: "Degradación del suelo superficial y compactación."
    },
    {
      id: "regenerativa",
      name: "Rotación Regenerativa (Suelo y Agua)",
      tag: "Recomendada",
      badgeType: "success",
      sequence: ["Trigo / Soja 2da", "Vicia villosa (cobertura)", "Maíz"],
      soilHealthScore: 89,
      metrics: {
        water: "+35% infiltración de humedad profunda",
        nutrients: "+75 kg N/ha aportado biológicamente",
        erosion: "Mínimo (cobertura verde 90% del año)",
        margin: "Estable, menor gasto en fertilizantes"
      },
      nasaEvidence: "ECOSTRESS y GPM muestran suelo más fresco y mejor absorción de lluvias intensas.",
      localRisk: "Definir fecha de secado de la vicia para no consumir agua del cultivo siguiente."
    },
    {
      id: "balanceada",
      name: "Rotación Forraje y Renta Rápida",
      tag: "Doble Propósito",
      badgeType: "info",
      sequence: ["Girasol", "Centeno / Avena forrajera", "Maíz tardío"],
      soilHealthScore: 76,
      metrics: {
        water: "+20% retención respecto a soja continua",
        nutrients: "Moderada (buen reciclaje de fósforo)",
        erosion: "Bajo riesgo con pastoreo controlado",
        margin: "Renta intermedia con ganado + grano"
      },
      nasaEvidence: "NASA POWER registra baja frecuencia de heladas tempranas, ideal para maíz tardío.",
      localRisk: "Retirar la hacienda a tiempo para no compactar suelo húmedo."
    }
  ]
};

