import { useEffect, useState } from 'react';
import { mockSimulation } from './mockSimulation.js';
import { simulateRotations } from '../services/simulationService.js';

/**
 * Hook que consume el servicio de simulación real.
 * Si la API falla o no está disponible, hace fallback suave al mock para no romper la UI.
 *
 * @param {Object} params - Parámetros de simulación
 * @returns {{ data: Object, loading: boolean, mock: boolean, error: string | null }}
 */
export function useSimulation(params) {
  const [state, setState] = useState({
    data: mockSimulation,
    loading: false,
    mock: true,
    error: null,
  });

  const key = JSON.stringify(params ?? {});

  useEffect(() => {
    // Si no hay parámetros definidos, no ejecutamos
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
            data: mockSimulation,
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
