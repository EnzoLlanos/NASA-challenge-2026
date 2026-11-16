/**
 * Cliente HTTP reutilizable para la comunicación con el backend (FastAPI).
 * Maneja la URL base, cabeceras por defecto (JSON), proxy de Vite y parsing de respuestas/errores.
 */

const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

/**
 * Función central para ejecutar peticiones HTTP reutilizables.
 *
 * @param {string} endpoint - Ruta relativa del endpoint (ej: '/api/simulation')
 * @param {RequestInit} [options={}] - Opciones de fetch (method, headers, body, etc.)
 * @returns {Promise<any>} Datos parseados de la respuesta
 */
export async function apiRequest(endpoint, options = {}) {
  const normalizedEndpoint = endpoint.replace(/^\/+/, '');
  const directUrl = `${BASE_URL.replace(/\/+$/, '')}/${normalizedEndpoint}`;
  const proxyUrl = `/${normalizedEndpoint}`;

  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...(options.headers || {}),
    },
  };

  // Serializar cuerpo si es un objeto JavaScript y no un string o FormData
  if (config.body && typeof config.body === 'object' && !(config.body instanceof FormData)) {
    config.body = JSON.stringify(config.body);
  }

  // Si VITE_API_URL fue configurado explícitamente (ej: en Render), usamos directamente la URL del backend.
  // En desarrollo local (cuando VITE_API_URL no está definido), intentamos primero el proxy de Vite (/api/...)
  // y luego fallback a http://127.0.0.1:8000.
  const isCustomBaseUrl = Boolean(import.meta.env.VITE_API_URL);
  const urlsToTry = isCustomBaseUrl ? [directUrl] : [proxyUrl, directUrl];
  let lastError = null;

  for (const url of urlsToTry) {
    try {
      const response = await fetch(url, config);

      const isJson = response.headers.get('content-type')?.includes('application/json');
      const data = isJson ? await response.json() : await response.text();

      if (!response.ok) {
        const errorMsg =
          (data && typeof data === 'object' && (data.detail || data.message)) ||
          response.statusText ||
          `Error HTTP ${response.status}`;
        throw new Error(typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg));
      }

      return data;
    } catch (error) {
      lastError = error;
    }
  }

  console.error(`[API] Fallo al consultar ${config.method || 'GET'} ${directUrl}:`, lastError?.message);
  throw lastError;
}

/**
 * Métodos auxiliares HTTP reutilizables
 */
export const api = {
  get: (endpoint, options = {}) => apiRequest(endpoint, { ...options, method: 'GET' }),
  post: (endpoint, body, options = {}) => apiRequest(endpoint, { ...options, method: 'POST', body }),
  put: (endpoint, body, options = {}) => apiRequest(endpoint, { ...options, method: 'PUT', body }),
  patch: (endpoint, body, options = {}) => apiRequest(endpoint, { ...options, method: 'PATCH', body }),
  delete: (endpoint, options = {}) => apiRequest(endpoint, { ...options, method: 'DELETE' }),
};

export default api;
