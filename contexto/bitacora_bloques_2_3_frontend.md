# Bitácora Frontend — Bloques 2 y 3 (Tablero de Decisión y Visualización de Estrategias)

Reto NASA Space Apps 2026: *Adapting Farms with NASA Data*.
Fecha: 2026-11-14.

## Qué se hizo

### 1. Tablero de Decisión (`Front/src/decision/`)
| Archivo | Rol |
|---|---|
| `DecisionBoard.jsx` | Componente principal de los Bloques 2 y 3. Props opcionales: `simulacion` (objeto ya cargado) y `params` (para pedir la simulación). |
| `api.js` | Hook `useSimulation(params)`. Si existe `VITE_SIM_URL` hace `POST` con los params; si falla o no está definida, usa el mock. |
| `mockSimulation.js` | Objeto de simulación de ejemplo (lote de San Luis, 3 estrategias, evidencia NASA). |
| `decision.css` | Estilos del dashboard (insignias verde/rojo/azul, medidores, timeline). |

### 2. Contenido del tablero
- **Aviso al agrónomo:** card de advertencia, herramienta de apoyo que requiere validación profesional.
- **Bloque 2 — Comparador de 3 estrategias** (Actual/Monocultivo, Regenerativa, Forraje/Renta):
  - Vista "Lado a lado" o "Una por una" con pestañas.
  - Medidor/semáforo de Salud del Suelo (0-100%).
  - Secuencia de cultivos.
  - Barras comparativas de Agua, Nutrientes, Erosión y Margen.
- **Bloque 3 — Evidencia NASA:** sección "¿Qué detectó la NASA en tu lote?" con SMAP / ECOSTRESS / GPM traducidos a lenguaje de campo.
- **Timeline:** secuencia de siembra y períodos de suelo cubierto o vulnerable, según la estrategia seleccionada.
- Etiqueta "Datos de ejemplo" mientras se use el mock.

### 3. Integración con el Bloque 1 (`Front/src/App.jsx`)
- Se resolvió el conflicto de `App.jsx` tras traer los cambios del equipo.
- Se mantiene el layout del Bloque 1 (Sidebar de configuración).
- Se quitaron las tarjetas de vista previa y el placeholder "Dev 2", que duplicaban el tablero.
- `handleSimulate` guarda la configuración usada en el estado `simParams`, que se pasa a `<DecisionBoard params={simParams} />`.

### 4. Git
- Rama: `bloques-2-3-tablero-decision` (commit `feat: bloques 2 y 3 ...`).
- Merge con `--no-ff` a `main` local, después de actualizar con los commits del equipo de datos (sin conflictos).
- **Pendiente:** `git push origin main` y `git push -u origin bloques-2-3-tablero-decision`. Requieren credenciales de GitHub (Personal Access Token, `gh auth login` o SSH).

## Verificación
- `npm run build` (Vite) compila sin errores.
- `oxlint`: 0 errores, 2 warnings en `api.js` (`setState` dentro de un effect), sin impacto funcional.
- No se hizo prueba visual en navegador ni con backend real.

## Cómo probarlo
```bash
cd Front
npm install
npm run dev     # http://localhost:5173
```

## Pendientes / acuerdos con el equipo
- **Contrato de datos:** el tablero espera el formato de `mockSimulation.js` (`lote`, `estrategias`, `evidencia_nasa`), distinto del de `data/mockData.js` del Bloque 1. Acordar con backend el JSON del endpoint de simulación.
- Definir `VITE_SIM_URL` en `Front/.env` cuando el backend (FastAPI, `Back/`) exponga la simulación.
- Corregir los 2 warnings de lint en `api.js` si se desea.
- Revisión visual y responsive.
