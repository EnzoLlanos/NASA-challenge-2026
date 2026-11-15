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
    producerName: params.producerName || 'Productor San Luis',
    campaignHistory: Array.isArray(params.campaignHistory) ? params.campaignHistory : [],
  };

  return await api.post('/api/simulation', payload);
}

const PROFILE_STORAGE_KEY = 'agronasa_profile_v1';

export const DEFAULT_USER_PROFILE = {
  id: 'usr-1',
  nombre: 'Productor San Luis',
  establecimiento: 'Establecimiento Don Pedro',
  region_principal: 'centro',
  historial_campanas: [
    {
      id: 'camp-1',
      campana: '2023/24',
      cultivo: 'Soja',
      cobertura_invernal: false,
      resultado: 'regular',
      problema_principal: 'sequia',
      notas: 'Verano seco y barbecho largo sin cobertura.',
    },
    {
      id: 'camp-2',
      campana: '2024/25',
      cultivo: 'Soja',
      cobertura_invernal: false,
      resultado: 'malo',
      problema_principal: 'erosion',
      notas: 'Se repitió soja sobre rastrojo escaso; hubo escurrimiento y pérdida de suelo.',
    },
  ],
  decisiones_futuras: [],
};

export function getLocalProfile() {
  try {
    const raw = localStorage.getItem(PROFILE_STORAGE_KEY);
    if (raw) {
      return { ...DEFAULT_USER_PROFILE, ...JSON.parse(raw) };
    }
  } catch {
    // ignore storage errors
  }
  return DEFAULT_USER_PROFILE;
}

export function saveLocalProfile(profile) {
  try {
    localStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(profile));
  } catch {
    // ignore storage errors
  }
  return profile;
}

export async function fetchUserProfile(userId = 'usr-1') {
  try {
    const remote = await api.get(`/api/users/${userId}`);
    if (remote && typeof remote === 'object') {
      saveLocalProfile(remote);
      return remote;
    }
  } catch {
    // fallback a localStorage
  }
  return getLocalProfile();
}

export async function updateUserProfile(profile) {
  const userId = profile.id || 'usr-1';
  saveLocalProfile(profile);
  try {
    const updated = await api.put(`/api/users/${userId}/perfil`, profile);
    saveLocalProfile(updated);
    return updated;
  } catch {
    return profile;
  }
}

export async function saveFutureDecision(decision, currentProfile) {
  const base = currentProfile || getLocalProfile();
  const newDecision = {
    id: `dec-${Date.now()}`,
    fecha: new Date().toLocaleDateString('es-AR'),
    ...decision,
  };
  const updatedLocal = {
    ...base,
    decisiones_futuras: [newDecision, ...(base.decisiones_futuras || [])],
  };
  saveLocalProfile(updatedLocal);
  try {
    const remote = await api.post(`/api/users/${base.id || 'usr-1'}/decisiones`, newDecision);
    saveLocalProfile(remote);
    return remote;
  } catch {
    return updatedLocal;
  }
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
  getLocalProfile,
  saveLocalProfile,
  fetchUserProfile,
  updateUserProfile,
  saveFutureDecision,
};
