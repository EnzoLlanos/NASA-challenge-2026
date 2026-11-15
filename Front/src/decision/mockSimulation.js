// Objeto de simulación adaptado a las 3 Zonas de San Luis (Norte, Centro, Sur)
// Sustentado con datos de NASA POWER (2000-2025), SMAP y SRTM.

export const ZONAS_SIMULACION = {
  norte: {
    lote: { nombre: 'Lote Norte – Valle del Conlara (Merlo)', lat: -32.35, lon: -65.0, hectareas: 120 },
    estrategias: [
      {
        id: 'actual',
        nombre: 'Actual (Monocultivo sin cobertura)',
        is_current: true,
        salud_suelo: 'En riesgo',
        resumen: 'Monocultivo continuo en zona serrana: suelo desnudo y expuesto a heladas tardías.',
        secuencia: [{ cultivo: 'Soja', tipo: 'cultivo', desde: 11, hasta: 4 }],
        metricas: {
          agua: 'Baja: el barbecho invernal desaprovecha la buena humedad del valle',
          nutrientes: 'Deficitaria: pérdida progresiva de fertilidad natural',
          erosion: 'Alto riesgo de erosión hídrica en pendientes serranas',
        },
        riesgos: ['Heladas tardías primaverales', 'Erosión por escorrentía en laderas'],
      },
      {
        id: 'regenerativa',
        nombre: 'Regenerativa Serrana (Maíz + Arveja/Vicia)',
        is_current: false,
        salud_suelo: 'Saludable',
        resumen: 'Aprovecha la buena humedad del suelo (0.60) con leguminosa fijadora de nitrógeno.',
        secuencia: [
          { cultivo: 'Maíz de ciclo completo', tipo: 'cultivo', desde: 10, hasta: 4 },
          { cultivo: 'Arveja / Vicia (cobertura)', tipo: 'cobertura', desde: 5, hasta: 9 },
        ],
        metricas: {
          agua: 'Muy buena: el suelo del valle retiene humedad y reduce evaporación',
          nutrientes: 'Alta: la leguminosa aporta nitrógeno biológico al suelo',
          erosion: 'Excelente protección de pendientes contra lluvias torrenciales',
        },
        riesgos: ['Monitorear fecha de heladas tardías antes de implantar maíz'],
      },
      {
        id: 'balanceada',
        nombre: 'Rotación Cereal / Forrajera',
        is_current: false,
        salud_suelo: 'Moderada',
        resumen: 'Trigo de invierno seguido de soja de segunda o maíz tardío.',
        secuencia: [
          { cultivo: 'Trigo de invierno', tipo: 'cultivo', desde: 5, hasta: 11 },
          { cultivo: 'Soja 2da o Maíz tardío', tipo: 'cultivo', desde: 12, hasta: 4 },
        ],
        metricas: {
          agua: 'Moderada: dos cosechas que aprovechan el agua del perfil',
          nutrientes: 'Equilibrada con rastrojo abundante de trigo',
          erosion: 'Buena cobertura invernal frente a vientos de sierra',
        },
        riesgos: ['Vigilar humedad al momento de la siembra de segunda'],
      },
    ],
    evidencia_nasa: [
      {
        satelite: 'NASA POWER',
        titulo: 'Régimen de Heladas',
        nivel: 'rojo',
        texto: 'La estación serrana registra 35 días de heladas al año. Se aconseja sembrar cultivos estivales tras el riesgo primaveral.',
        dato: '35 días con temp ≤ 0°C anuales',
      },
      {
        satelite: 'SMAP',
        titulo: 'Humedad de Raíz',
        nivel: 'verde',
        texto: 'Humedad en zona radicular alta (0.60): retiene significativamente más agua que el sur provincial.',
        dato: 'Humedad edáfica favorable',
      },
      {
        satelite: 'SRTM / GPM',
        titulo: 'Relieve y Escorrentía',
        nivel: 'azul',
        texto: 'Pendientes de 800-1200 msnm: tener cobertura viva frena el lavado de suelo por lluvias serranas.',
        dato: 'Protección contra erosión hídrica',
      },
    ],
  },

  sur: {
    lote: { nombre: 'Lote Sur – Buena Esperanza / Dupuy (Médanos)', lat: -34.70, lon: -65.30, hectareas: 180 },
    estrategias: [
      {
        id: 'actual',
        nombre: 'Actual (Soja en suelo arenoso)',
        is_current: true,
        salud_suelo: 'En riesgo',
        resumen: 'Soja continua en suelo arenoso: sufre los 34 días de calor extremo y genera voladura de tierra.',
        secuencia: [{ cultivo: 'Soja', tipo: 'cultivo', desde: 11, hasta: 4 }],
        metricas: {
          agua: 'Crítica: el suelo arenoso no retiene agua y las olas de calor la evaporan',
          nutrientes: 'Muy baja: pérdida de la escasa materia orgánica superficial',
          erosion: 'Peligro extremo de voladura de médanos en invierno y primavera',
        },
        riesgos: ['Estrés hídrico severo en floración', 'Voladura de tierra por viento'],
      },
      {
        id: 'regenerativa',
        nombre: 'Resiliente a Sequía (Sorgo + Centeno)',
        is_current: false,
        salud_suelo: 'Saludable',
        resumen: 'Sorgo con raíces de 200 cm que superan el calor, protegido por centeno en invierno.',
        secuencia: [
          { cultivo: 'Sorgo granífero (raíz profunda)', tipo: 'cultivo', desde: 10, hasta: 3 },
          { cultivo: 'Centeno (cobertura/forraje)', tipo: 'cobertura', desde: 5, hasta: 9 },
        ],
        metricas: {
          agua: 'Excelente: el sorgo consume 40% menos agua que el maíz',
          nutrientes: 'Aporte de rastrojo abundante que forma suelo en la arena',
          erosion: 'Máxima protección contra viento en los meses secos (agosto-octubre)',
        },
        riesgos: ['Secar el centeno a tiempo para sembrar sorgo con humedad'],
      },
      {
        id: 'balanceada',
        nombre: 'Rotación Girasol Oleaginoso',
        is_current: false,
        salud_suelo: 'Moderada',
        resumen: 'Girasol pivotante para explorar humedad profunda y verdeo invernal de avena.',
        secuencia: [
          { cultivo: 'Girasol', tipo: 'cultivo', desde: 10, hasta: 3 },
          { cultivo: 'Avena forrajera', tipo: 'cobertura', desde: 4, hasta: 9 },
        ],
        metricas: {
          agua: 'Muy buena: la raíz pivotante baja hasta 250 cm de profundidad',
          nutrientes: 'Reciclaje de nutrientes en capas profundas del perfil',
          erosion: 'Media: requiere sembrar el verdeo inmediatamente tras la cosecha',
        },
        riesgos: ['Monitorear orugas y palomas en la floración del girasol'],
      },
    ],
    evidencia_nasa: [
      {
        satelite: 'NASA POWER',
        titulo: 'Calor Extremo Estival',
        nivel: 'rojo',
        texto: 'El sur registra 34 días/año con calor sofocante (≥35°C), 12 veces más que el norte. Priorizar cultivos C4 rústicos.',
        dato: '34 días/año ≥ 35°C',
      },
      {
        satelite: 'SMAP',
        titulo: 'Humedad de Suelo Arenoso',
        nivel: 'rojo',
        texto: 'Humedad radicular muy baja (0.32): el suelo arenoso drena rápido y exige cultivos de raíz profunda.',
        dato: 'Retención de agua limitada',
      },
      {
        satelite: 'MODIS / Landsat',
        titulo: 'Erosión Eólica',
        nivel: 'azul',
        texto: 'Imágenes satelitales confirman suelo descubierto en agosto y septiembre, período de máximos vientos.',
        dato: 'Crítico evitar suelo desnudo',
      },
    ],
  },

  centro: {
    lote: { nombre: 'Lote Centro – San Luis / Villa Mercedes', lat: -33.30, lon: -65.30, hectareas: 100 },
    estrategias: [
      {
        id: 'actual',
        nombre: 'Actual (Monocultivo tradicional)',
        is_current: true,
        salud_suelo: 'En riesgo',
        resumen: 'Soja sobre soja: deja el campo sin cobertura durante 5 meses secos.',
        secuencia: [{ cultivo: 'Soja', tipo: 'cultivo', desde: 11, hasta: 4 }],
        metricas: {
          agua: 'Baja: el agua de lluvia invernal se evapora en el barbecho',
          nutrientes: 'Deficitaria: el suelo pierde fertilidad año tras año',
          erosion: 'Riesgo moderado de encostramiento y huellones',
        },
        riesgos: ['Pérdida de materia orgánica', 'Compactación por falta de raíces vivas'],
      },
      {
        id: 'regenerativa',
        nombre: 'Rotación Maíz + Vicia + Soja',
        is_current: false,
        salud_suelo: 'Saludable',
        resumen: 'Rotación equilibrada: rastrojo duradero de maíz y nitrógeno natural de la vicia.',
        secuencia: [
          { cultivo: 'Maíz', tipo: 'cultivo', desde: 10, hasta: 3 },
          { cultivo: 'Vicia (cobertura)', tipo: 'cobertura', desde: 4, hasta: 9 },
          { cultivo: 'Soja', tipo: 'cultivo', desde: 10, hasta: 4 },
        ],
        metricas: {
          agua: 'Mejor: el suelo absorbe más agua de lluvia y evita escurrimientos',
          nutrientes: 'Alta: la vicia aporta nitrógeno natural y ahorra fertilizantes',
          erosion: 'Muy buena: el campo permanece cubierto prácticamente todo el año',
        },
        riesgos: ['Ajustar la fertilización fosforada inicial según lote'],
      },
      {
        id: 'balanceada',
        nombre: 'Doble Propósito (Sorgo / Forraje)',
        is_current: false,
        salud_suelo: 'Moderada',
        resumen: 'Sorgo para grano o forraje combinado con verdeo de avena para pastoreo.',
        secuencia: [
          { cultivo: 'Sorgo granífero', tipo: 'cultivo', desde: 11, hasta: 3 },
          { cultivo: 'Avena (verdeo)', tipo: 'cobertura', desde: 4, hasta: 9 },
        ],
        metricas: {
          agua: 'Moderada: tolera veranos con lluvias irregulares',
          nutrientes: 'Mantiene niveles estables de materia orgánica',
          erosion: 'Buena protección con pastoreo controlado',
        },
        riesgos: ['Controlar carga animal para no pisar el suelo húmedo'],
      },
    ],
    evidencia_nasa: [
      {
        satelite: 'NASA POWER',
        titulo: 'Concentración de Lluvias',
        nivel: 'azul',
        texto: 'Más del 70% de la precipitación anual cae en solo 5 meses de verano. El suelo debe estar listo para infiltrarla.',
        dato: 'Lluvia concentrada en verano',
      },
      {
        satelite: 'SMAP',
        titulo: 'Humedad Radicular Media',
        nivel: 'verde',
        texto: 'Humedad en raíz (0.41): responde de forma inmediata a la siembra de coberturas vegetales.',
        dato: 'Respuesta favorable a cobertura',
      },
      {
        satelite: 'ECOSTRESS',
        titulo: 'Estrés Térmico Estival',
        nivel: 'rojo',
        texto: 'Detecta picos de calor en enero-febrero durante la floración: rotar fechas de siembra amortigua el impacto.',
        dato: '26 días/año ≥ 35°C',
      },
    ],
  },
};

export function getSimulationForParams(params) {
  const zona = params?.zona || 'centro';
  const data = ZONAS_SIMULACION[zona] || ZONAS_SIMULACION.centro;

  if (params?.currentCrop) {
    // Si el usuario especificó otro cultivo actual, reflejarlo
    return {
      ...data,
      estrategias: data.estrategias.map((est) => {
        if (est.is_current) {
          return {
            ...est,
            nombre: `${params.currentCrop} continuo (Situación actual)`,
            secuencia: [{ cultivo: params.currentCrop, tipo: 'cultivo', desde: 11, hasta: 4 }],
          };
        }
        return est;
      }),
    };
  }

  return data;
}

export const mockSimulation = ZONAS_SIMULACION.centro;
