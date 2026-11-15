import api from './api.js';

/**
 * Servicio de simulación agronómica, reglas regionales y configuración adaptativa de formulario.
 * Conecta los componentes de React con los endpoints de FastAPI (/api/simulation y /api/regions/form-config).
 */

/**
 * Ejecuta la simulación de rotaciones enviando la configuración del lote, región y condición zonal a la API.
 *
 * @param {Object} params - Datos de entrada del agricultor
 * @param {"norte" | "centro" | "sur"} params.region - Región seleccionada de San Luis
 * @param {string} params.currentCrop - Cultivo actual (ej: "Soja", "Maíz")
 * @param {"lluvia" | "riego"} params.irrigation - Régimen de agua
 * @param {{ water: boolean, nutrients: boolean, erosion: boolean, forageProfit: boolean }} params.priorities - Prioridades
 * @param {boolean} [params.fieldCondition] - Condición crítica activa de la zona seleccionada
 * @param {Object} [params.zonalConditions] - Detalle opcional de condiciones específicas por región
 * @param {string} [params.lotName] - Nombre del establecimiento o lote
 * @returns {Promise<{ lote: Object, estrategias: Array, evidencia_nasa: Array, reglas_regionales: Array }>}
 */
export async function simulateRotations(params) {
  const region = params.region || params.zona || 'centro';
  const fieldCondition =
    params.fieldCondition !== undefined ? Boolean(params.fieldCondition) : true;

  const payload = {
    region,
    currentCrop: params.currentCrop || 'Soja',
    irrigation: params.irrigation || 'lluvia',
    priorities: {
      water: Boolean(params.priorities?.water),
      nutrients: Boolean(params.priorities?.nutrients),
      erosion: Boolean(params.priorities?.erosion),
      forageProfit: Boolean(params.priorities?.forageProfit),
    },
    fieldCondition,
    zonalConditions: params.zonalConditions || {
      altasTemperaturasSecano: region === 'norte' ? fieldCondition : undefined,
      riesgoNapasOErosionHidrica: region === 'centro' ? fieldCondition : undefined,
      sueloArenosoVoladura: region === 'sur' ? fieldCondition : undefined,
    },
    lotName: params.lotName || 'Establecimiento Don Pedro - San Luis',
  };

  return await api.post('/api/simulation', payload);
}

/**
 * Obtiene la configuración adaptativa del formulario y reglas para las 3 regiones de San Luis.
 * @returns {Promise<Record<string, Object>>}
 */
export async function fetchRegionsFormConfig() {
  return await api.get('/api/regions/form-config');
}

/**
 * Verifica el estado del servidor backend.
 * @returns {Promise<{ status: string, message: string }>}
 */
export async function checkBackendHealth() {
  return await api.get('/api/health');
}

export default {
  simulateRotations,
  fetchRegionsFormConfig,
  checkBackendHealth,
};
