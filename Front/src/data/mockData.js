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

export const ZONE_OPTIONS = [
  {
    value: "centro",
    label: "🟡 Centro (Capital / Villa Mercedes)",
    desc: "Valle central y transición. Humedad intermedia y lluvias estivales.",
    coords: { lat: -33.30, lng: -65.30 }
  },
  {
    value: "norte",
    label: "🟢 Norte (Valle del Conlara / Sierras)",
    desc: "Clima serrano: suelo húmedo (0.60) pero 35 días de heladas al año.",
    coords: { lat: -32.35, lng: -65.00 }
  },
  {
    value: "sur",
    label: "🟠 Sur (Buena Esperanza / Dupuy)",
    desc: "Llanura medanosa: suelo arenoso y 34 días de calor extremo (≥35°C).",
    coords: { lat: -34.70, lng: -65.30 }
  }
];

export const CROP_OPTIONS = [
  { value: "Soja", label: "🌱 Soja" },
  { value: "Maíz", label: "🌽 Maíz" },
  { value: "Trigo", label: "🌾 Trigo" },
  { value: "Sorgo", label: "🌾 Sorgo granífero" },
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
      metrics: {
        water: "Baja (pérdida por evaporación en barbecho)",
        nutrients: "Deficitaria en N y materia orgánica",
        erosion: "Alto riesgo en meses ventosos"
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
      metrics: {
        water: "Mejor infiltración de humedad profunda",
        nutrients: "Aporta nitrógeno al suelo de forma natural",
        erosion: "Mínimo (el suelo queda cubierto casi todo el año)"
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
      metrics: {
        water: "Guarda mejor el agua que la soja plantada siempre",
        nutrients: "Moderada (buen reciclaje de fósforo)",
        erosion: "Bajo riesgo con pastoreo controlado"
      },
      nasaEvidence: "NASA POWER registra baja frecuencia de heladas tempranas, ideal para maíz tardío.",
      localRisk: "Retirar la hacienda a tiempo para no compactar suelo húmedo."
    }
  ]
};

