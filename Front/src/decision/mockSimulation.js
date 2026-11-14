// Objeto de simulación MOCK. Reemplazar por la respuesta real del backend
// (ver `useSimulation` en ./api.js). Escala de métricas: 0-100, MÁS = MEJOR
// (erosión alta = poco riesgo de erosión, es decir "más protección").
// Meses: 1 = enero ... 12 = diciembre.
export const mockSimulation = {
  lote: { nombre: 'Lote Norte – San Luis', lat: -33.3, lon: -65.3, hectareas: 120 },
  estrategias: [
    {
      id: 'actual',
      nombre: 'Actual (Monocultivo)',
      is_current: true,
      salud_suelo: 34,
      resumen: 'Soja sobre soja: buen margen hoy, pero el suelo queda desnudo gran parte del año.',
      secuencia: [{ cultivo: 'Soja', tipo: 'cultivo', desde: 11, hasta: 4 }],
      metricas: { agua: 35, nutrientes: 30, erosion: 25, margen: 70 },
      riesgos: ['Pérdida de materia orgánica', 'Erosión por viento en invierno'],
    },
    {
      id: 'regenerativa',
      nombre: 'Regenerativa',
      is_current: false,
      salud_suelo: 82,
      resumen: 'Maíz + cultivo de cobertura + soja: el suelo casi siempre tapado y con más nitrógeno.',
      secuencia: [
        { cultivo: 'Maíz', tipo: 'cultivo', desde: 10, hasta: 3 },
        { cultivo: 'Vicia (cobertura)', tipo: 'cobertura', desde: 4, hasta: 9 },
      ],
      metricas: { agua: 78, nutrientes: 85, erosion: 88, margen: 58 },
      riesgos: ['Margen algo menor el primer año', 'Requiere ajustar manejo de la cobertura'],
    },
    {
      id: 'forraje',
      nombre: 'Forraje / Renta',
      is_current: false,
      salud_suelo: 61,
      resumen: 'Sorgo forrajero + verdeo de invierno: renta pareja y cobertura media.',
      secuencia: [
        { cultivo: 'Sorgo forrajero', tipo: 'cultivo', desde: 11, hasta: 3 },
        { cultivo: 'Avena (verdeo)', tipo: 'cultivo', desde: 5, hasta: 8 },
      ],
      metricas: { agua: 55, nutrientes: 60, erosion: 66, margen: 74 },
      riesgos: ['Depende de tener hacienda o mercado de forraje'],
    },
  ],
  evidencia_nasa: [
    {
      satelite: 'SMAP',
      titulo: 'Humedad del suelo',
      nivel: 'rojo',
      texto: 'El satélite detectó que el suelo de tu lote se seca más rápido que el promedio de la zona entre julio y octubre.',
      dato: 'Humedad superficial 18% bajo lo normal',
    },
    {
      satelite: 'ECOSTRESS',
      titulo: 'Estrés de las plantas y evaporación',
      nivel: 'rojo',
      texto: 'El satélite detectó 4 meses de suelo desnudo con alto riesgo de evaporación.',
      dato: '4 meses de suelo expuesto',
    },
    {
      satelite: 'GPM',
      titulo: 'Lluvia',
      nivel: 'azul',
      texto: 'Más del 70% de la lluvia cae entre noviembre y marzo: conviene tener cultivo o cobertura en esa época.',
      dato: '70% de la lluvia en 5 meses',
    },
  ],
};
