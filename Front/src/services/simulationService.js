import api from './api.js';

/**
 * Servicio de simulación agronómica y climática.
 * Conecta los componentes de React con el endpoint POST /api/simulation de FastAPI.
 */

/**
 * Ejecuta la simulación de rotaciones enviando la configuración del lote a la API.
 *
 * @param {Object} params - Datos de entrada del agricultor
 * @param {{ lat: number, lng: number }} params.coords - Coordenadas del lote
 * @param {string} params.currentCrop - Cultivo actual (ej: "Soja", "Maíz")
 * @param {"lluvia" | "riego"} params.irrigation - Régimen de agua
 * @param {{ water: boolean, nutrients: boolean, erosion: boolean, forageProfit: boolean }} params.priorities - Prioridades
 * @param {string} [params.lotName] - Nombre del establecimiento o lote
 * @returns {Promise<{ lote: Object, estrategias: Array, evidencia_nasa: Array }>}
 */
export async function simulateRotations(params) {
  const payload = {
    coords: {
      lat: Number(params.coords?.lat ?? -33.675),
      lng: Number(params.coords?.lng ?? -65.457),
    },
    currentCrop: params.currentCrop || 'Soja',
    irrigation: params.irrigation || 'lluvia',
    priorities: {
      water: Boolean(params.priorities?.water),
      nutrients: Boolean(params.priorities?.nutrients),
      erosion: Boolean(params.priorities?.erosion),
      forageProfit: Boolean(params.priorities?.forageProfit),
    },
    lotName: params.lotName || 'Establecimiento Don Pedro - San Luis',
  };

  return await api.post('/api/simulation', payload);
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
  checkBackendHealth,
};
