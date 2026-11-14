import { useEffect, useState } from 'react';
import { mockSimulation } from './mockSimulation.js';

// Cuando el backend exponga el objeto de simulación, definir VITE_SIM_URL
// (ej: http://localhost:3000/api/simulation). Si falla, usa el mock.
export function useSimulation(params) {
  const [state, setState] = useState({ data: mockSimulation, loading: false, mock: true });
  const key = JSON.stringify(params ?? {});

  useEffect(() => {
    const url = import.meta.env.VITE_SIM_URL;
    if (!url) return;
    let cancel = false;
    setState((s) => ({ ...s, loading: true }));
    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: key,
    })
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .then((data) => !cancel && setState({ data, loading: false, mock: false }))
      .catch(() => !cancel && setState({ data: mockSimulation, loading: false, mock: true }));
    return () => {
      cancel = true;
    };
  }, [key]);

  return state;
}
