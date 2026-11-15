# Documentación de Frontend — Bloque 1: Panel de Configuración y Geo

**Reto:** NASA Space Apps Challenge 2026 — *Adapting Farms with NASA Data*  
**Módulo:** Frontend (`/Front`)  
**Responsable:** Dev 1 (Panel de Configuración y Entrada de Datos)  
**Estado:** ✅ Terminado e integrado en `main`

---

## 1. Objetivo del Bloque 1

Siguiendo las pautas del desafío de la NASA y el diseño centrado en el agricultor, el objetivo de este bloque es ofrecer una interfaz simple, clara y táctil para que el productor agropecuario pueda ingresar los datos de su campo **sin necesidad de conocimientos técnicos ni manejo de datos satelitales crudos**.

El panel lateral se ubica a la izquierda de la pantalla y concentra toda la captura de información necesaria para alimentar el motor de simulación de rotaciones de cultivos.

---

## 2. Componentes y Estructura Desarrollada

Se crearon y organizaron los siguientes archivos dentro de `Front/src/`:

```
Front/
├── index.html                               # Inclusión de Leaflet CDN (CSS y JS)
├── src/
│   ├── App.jsx                              # Integración del layout principal y estado global
│   ├── index.css                            # Resets CSS limpios para el viewport completo
│   ├── styles/
│   │   └── config.css                       # Estilos agro-tech (verdes, tierra, botones pill y cards)
│   ├── data/
│   │   └── mockData.js                      # Contrato de datos compartido entre Dev 1 y Dev 2
│   └── components/
│       └── config/
│           ├── Sidebar.jsx                  # Contenedor lateral del Bloque 1
│           ├── MapSelector.jsx              # Mini mapa interactivo satelital con Leaflet
│           └── ConfigForm.jsx               # Formulario amigable del agricultor
```

---

## 3. Detalle de Funcionalidades Implementadas

### A. Mini Mapa Interactivo (`MapSelector.jsx`)
* **Librería utilizada:** Leaflet nativo sobre React 19 (vía CDN para máxima estabilidad y cero conflictos de dependencias).
* **Capa satelital:** Vista satelital real de alta resolución (Esri World Imagery) para que el productor reconozca su campo visualmente.
* **Interacción ágil:** 
  * Clic en cualquier punto del mapa para mover el marcador.
  * Marcador arrastrable (*draggable*) con actualización en tiempo real de coordenadas (Latitud y Longitud).
* **Botón de impacto para la demo ("🎯 Cargar lote de ejemplo - San Luis"):**
  * Con un solo clic, ejecuta una animación suave (*flyTo*) hacia **Villa Mercedes / Cuenca del Morro, San Luis** (`lat: -33.675`, `lng: -65.457`).
  * Dibuja automáticamente un **polígono verde delimitando el lote de 150 hectáreas**, con etiqueta identificatoria.
  * Precarga todos los campos del formulario con los datos representativos de la región.

### B. Formulario Centrado en el Agricultor (`ConfigForm.jsx`)
* **¿Qué venís sembrando? (Select):** Opciones directas con cultivos comunes de la región pampeana/semiárida:
  * 🌱 Soja de primera
  * 🌽 Maíz tardío / temprano
  * 🌾 Trigo
  * 🌻 Girasol
* **Régimen de Agua (Botones tipo Pill):**
  * Botones grandes y táctiles para seleccionar entre **🌧️ Solo lluvia (Secano)** y **🚿 Con riego**.
  * Estado activo destacado en verde bosque oscuro de alto contraste.
* **Prioridades del Productor (Chips interactivos con Checkbox):**
  * Permite marcar una o varias metas estratégicas para la campaña:
    1. **💧 Cuidar agua:** Maximizar infiltración y reducir evaporación del suelo.
    2. **🧪 Recuperar nutrientes:** Aportar nitrógeno biológico y materia orgánica.
    3. **🛡️ Frenar erosión:** Mantener cobertura vegetal frente a vientos y lluvias torrenciales.
    4. **🐄 Sumar forraje / renta:** Pastoreo liviano o esquemas de doble propósito.
  * Feedback visual con borde iluminado y fondo verde suave al seleccionarse.
* **Botón Principal ("🚀 Simular Rotaciones"):**
  * Dispara el cálculo y pasa el payload de configuración.
  * Incluye estado de carga (*"⏳ Consultando datos NASA..."*) para simular la consulta satelital ante el jurado.

### C. Contrato de Datos Compartido (`mockData.js`)
Para no bloquear el desarrollo del **Dev 2 (Bloques 2 y 3)**, se estandarizó la estructura del objeto de simulación:
* Datos del lote de ejemplo de San Luis.
* Opciones de cultivos y prioridades.
* Las **3 estrategias de rotación** requeridas por la consigna oficial:
  1. *Estrategia Actual (Monocultivo / Soja continua).*
  2. *Rotación Regenerativa (Vicia + Maíz + Trigo/Soja 2da).*
  3. *Rotación Doble Propósito / Renta Rápida (Girasol + Centeno forrajero + Maíz tardío).*
* Métricas e indicadores satelitales NASA (SMAP, ECOSTRESS, GPM, MODIS) listos para consumir por el panel de resultados.

### D. Diseño Visual y Estilos (`config.css`)
* Paleta inspirada en agro-tech moderna: verdes orgánicos (`#134e2b`, `#238636`), blancos y grises de alta legibilidad.
* Tipografía del sistema de renderizado nítido.
* Tarjetas limpias con sombras suaves y esquinas redondeadas.
* Diseño responsivo que se adapta en columna en pantallas de menor resolución (tablets/laptops).

---

## 4. Punto de Conexión con el Compañero (Bloques 2 y 3)

El Bloque 1 entrega a la aplicación principal (`App.jsx`) el estado `config`:

```javascript
{
  coords: { lat: -33.675, lng: -65.457 },
  currentCrop: "Soja",
  irrigation: "lluvia", // o "riego"
  priorities: {
    water: true,
    nutrients: true,
    erosion: true,
    forageProfit: false
  },
  lotName: "Establecimiento Don Pedro - San Luis"
}
```

El compañero (Dev 2) sólo debe crear sus componentes en `Front/src/components/dashboard/` consumiendo este `config` y el resultado `simulationData` para renderizar:
* **Bloque 2:** Semáforo de salud de suelo y tarjetas comparativas de las 3 estrategias.
* **Bloque 3:** Línea de tiempo de siembra y justificación con datos de satélites NASA.

---

## 5. Cómo Ejecutar y Probar

Desde la terminal del proyecto:

```bash
cd Front
npm install
npm run dev
```

Abrir en el navegador: `http://localhost:5173`
1. Interactuar con el mapa o hacer clic en **"🎯 Cargar lote de ejemplo - San Luis"**.
2. Elegir cultivo y alternar entre *Solo lluvia* y *Con riego*.
3. Seleccionar las prioridades del campo.
4. Presionar **"Simular Rotaciones"** para observar la actualización inmediata en el tablero.
