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

export const REGION_OPTIONS = [
  { value: "norte", label: "🌵 Norte (Quines, Candelaria, Ayacucho)" },
  { value: "centro", label: "🌱 Centro (Villa Mercedes, San Luis, Fraga)" },
  { value: "sur", label: "🌾 Sur (Buena Esperanza, Unión, Dupuy)" }
];

// Configuración adaptativa por región (sincronizada con /api/regions/form-config del Backend)
export const REGION_FORM_CONFIG_FALLBACK = {
  norte: {
    region: "norte",
    nombre: "Región Norte de San Luis",
    subtitulo_clima: "520 mm/año · 34 días >35 °C · 9 heladas/año",
    amenaza_principal: "Déficit hídrico estival severo (520 mm/año) y 34 días de calor extremo (>35 °C).",
    icono_alerta: "☀️",
    precipitacion_anual_mm: 520,
    dias_calor_extremo: 34,
    dias_heladas: 9,
    cultivos_recomendados: ["Sorgo", "Soja", "Maíz", "Trigo"],
    prioridades_sugeridas: { water: true, nutrients: TrueBoolean(true), erosion: true, forageProfit: false },
    condicion_contextual: {
      id: "altasTemperaturasSecano",
      etiqueta: "¿Lote expuesto a olas de calor sin cortina forestal?",
      descripcion: "En el Norte (34 días >35 °C) el suelo desnudo evapora la humedad en 48 hs y estresa floración.",
      icono: "☀️",
      valor_por_defecto: true
    },
    reglas_activas: [
      {
        codigo: "N1",
        nombre: "Déficit hídrico crítico estival",
        factor_climatico: "520 mm/año de lluvia vs demanda >450 mm",
        impacto_metricas: "Penaliza Agua (-20 pts) si se siembra Maíz/Soja en secano sin cobertura"
      },
      {
        codigo: "N2",
        nombre: "Golpe de calor reproductivo (>35 °C)",
        factor_climatico: "34 días/año con temperaturas mayores a 35 °C",
        impacto_metricas: "Bonifica Agua y Margen (+15 pts) al incluir Sorgo o cultivos tolerantes al calor"
      },
      {
        codigo: "N3",
        nombre: "Escudo contra evaporación directa",
        factor_climatico: "Alta radiación solar estival e inviernos secos",
        impacto_metricas: "Bonifica Agua (+15 pts) y Erosión (+12 pts) con cultivo de cobertura invernal"
      }
    ]
  },
  centro: {
    region: "centro",
    nombre: "Región Centro de San Luis",
    subtitulo_clima: "680 mm/año · 26 días >35 °C · 15 heladas/año",
    amenaza_principal: "Erosión hídrica por lluvias torrenciales de verano y ascenso de napas freáticas (Cuenca del Morro).",
    icono_alerta: "🌊",
    precipitacion_anual_mm: 680,
    dias_calor_extremo: 26,
    dias_heladas: 15,
    cultivos_recomendados: ["Maíz", "Soja", "Trigo", "Sorgo"],
    prioridades_sugeridas: { water: true, nutrients: true, erosion: true, forageProfit: false },
    condicion_contextual: {
      id: "riesgoNapasOErosionHidrica",
      etiqueta: "¿Lote con pendiente o riesgo de napa alta / escurrimiento?",
      descripcion: "En la zona Centro y Cuenca del Morro las raíces vivas en invierno consumen excedentes y frenan cárcavas.",
      icono: "🌊",
      valor_por_defecto: true
    },
    reglas_activas: [
      {
        codigo: "C1",
        nombre: "Control hidrológico y de napas con raíces vivas",
        factor_climatico: "680 mm/año concentrados en tormentas estivales",
        impacto_metricas: "Penaliza Erosión (-25 pts) en barbecho desnudo; premia cobertura viva (+18 pts)"
      },
      {
        codigo: "C2",
        nombre: "Sinergia Gramínea + Leguminosa",
        factor_climatico: "Balance de carbono y nitrógeno en zona núcleo",
        impacto_metricas: "Bonifica Nutrientes (+16 pts) al rotar Maíz/Trigo con Soja/Arveja"
      },
      {
        codigo: "C3",
        nombre: "Degradación por monocultivo continuo",
        factor_climatico: "Pérdida de estructura y planchado de suelo",
        impacto_metricas: "Penaliza Nutrientes (-22 pts) y Agua (-18 pts) en monocultivo sin rotación"
      }
    ]
  },
  sur: {
    region: "sur",
    nombre: "Región Sur de San Luis",
    subtitulo_clima: "610 mm/año · 22 días >35 °C · 24 heladas/año",
    amenaza_principal: "Voladura eólica en suelos medanosos/arenosos y alta frecuencia de heladas (24 días/año).",
    icono_alerta: "💨",
    precipitacion_anual_mm: 610,
    dias_calor_extremo: 22,
    dias_heladas: 24,
    cultivos_recomendados: ["Girasol", "Sorgo", "Maíz", "Soja"],
    prioridades_sugeridas: { water: true, nutrients: false, erosion: true, forageProfit: true },
    condicion_contextual: {
      id: "sueloArenosoVoladura",
      etiqueta: "¿Suelo arenoso / medanoso expuesto al viento o con aptitud mixta?",
      descripcion: "En Dupuy los vientos de agosto-octubre vuelan la arena si no hay cobertura o verdeo invernal anclando el suelo.",
      icono: "💨",
      valor_por_defecto: true
    },
    reglas_activas: [
      {
        codigo: "S1",
        nombre: "Alerta crítica de voladura de médanos (Erosión eólica)",
        factor_climatico: "Suelos arenosos + vientos intensos de agosto a octubre",
        impacto_metricas: "Penalización drástica en Erosión (-35 pts) si el lote queda desnudo en invierno"
      },
      {
        codigo: "S2",
        nombre: "Ventana de heladas tardías y tempranas",
        factor_climatico: "24 días de heladas anuales (≤ 0 °C)",
        impacto_metricas: "Bonifica rotaciones con verdeos invernales rústicos (Cebada/Centeno) y raíz profunda"
      },
      {
        codigo: "S3",
        nombre: "Fijación de perfil arenoso y doble propósito",
        factor_climatico: "Baja retención hídrica superficial en médanos (610 mm/año)",
        impacto_metricas: "Bonifica Agua (+14 pts) y Margen Forrajero (+15 pts) con Sorgo/Girasol + Verdeo"
      }
    ]
  }
};

function TrueBoolean(v) {
  return Boolean(v);
}

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
