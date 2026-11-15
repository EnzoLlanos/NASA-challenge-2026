import { useEffect, useState } from 'react';
import { getSimulationForParams, mockSimulation } from './mockSimulation.js';
import { simulateRotations } from '../services/simulationService.js';

/**
 * Hook que consume el servicio de simulación real.
 * Si la API falla o no está disponible, hace fallback suave al mock para no romper la UI.
 *
 * @param {Object} params - Parámetros de simulación
 * @returns {{ data: Object, loading: boolean, mock: boolean, error: string | null }}
 */
export function useSimulation(params) {
  const fallback = getSimulationForParams ? getSimulationForParams(params) : mockSimulation;
  const [state, setState] = useState({
    data: fallback || mockSimulation,
    loading: false,
    mock: true,
    error: null,
  });

  const key = JSON.stringify(params ?? {});

  useEffect(() => {
    if (!params) return;

    let cancel = false;
    setState((s) => ({ ...s, loading: true, error: null }));

    simulateRotations(params)
      .then((data) => {
        if (!cancel) {
          setState({ data, loading: false, mock: false, error: null });
        }
      })
      .catch((err) => {
        if (!cancel) {
          console.warn('[useSimulation] Usando datos mock por error en la API:', err.message);
          setState({
            data: fallback || mockSimulation,
            loading: false,
            mock: true,
            error: err.message,
          });
        }
      });

    return () => {
      cancel = true;
    };
  }, [key]);

  return state;
}
