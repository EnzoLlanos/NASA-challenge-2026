🌾 AgroNASA — Rotaciones Resilientes

NASA Space Apps Challenge | Adapting Farms with NASA Data

AgroNASA es una plataforma web interactiva de apoyo a la toma de decisiones agrícolas. Su objetivo es ayudar a productores y técnicos agropecuarios (inicialmente enfocado en la provincia de San Luis, Argentina) a diseñar, comparar y seleccionar estrategias de rotación de cultivos adaptadas a la variabilidad y el riesgo climático real de su región.

📌 Tabla de Contenidos
¿Qué hace el proyecto?
¿Cómo funciona?
Beneficios e Impacto
Metas a Futuro
Tecnologías y Herramientas
Estructura del Proyecto
Guía de Instalación y Uso
🚀 ¿Qué hace el proyecto?

AgroNASA evalúa el riesgo agroclimático de cada lote (estrés hídrico, olas de calor, heladas tardías y ventanas seguras de siembra) utilizando 26 años de datos satelitales y meteorológicos de NASA POWER (2000–2025).

A partir de la selección geográfica y el historial de manejo del productor, el sistema genera recomendaciones agronómicas claras que incluyen:

Estrategias de rotación comparables (conservación/cobertura, diversificación de riesgo o planteo de rendimiento).
Puntuación y diagnóstico de resiliencia con explicación detallada de las reglas aplicadas.
Calendario anual interactivo con las fechas óptimas de siembra, desarrollo y cosecha.
Evidencia satelital NASA que respalda de forma transparente cada recomendación.

Preview unavailable Figura 1: Pantalla principal con selector de zonas de San Luis y configuración de lote.

⚙️ ¿Cómo funciona?

El sistema integra tres módulos principales:

1. Pipeline de Datos Climáticos (NASA POWER)
Descarga series meteorológicas históricas diarias (precipitación, radiación, temperatura máxima/mínima, humedad relativa) a través de la API de NASA POWER para las distintas zonas agroecológicas definidas en data/zonas.yaml.
Limpia datos atípicos (-999) y calcula indicadores mensuales y estacionales de sequía y estrés térmico (pipeline/build_features.py e indicadores_estacionales.py).
2. Motor de Simulación y Scoring (Backend FastAPI)
Modela los requerimientos fenológicos y de agua de cada cultivo (data/crops.yaml).
Cruza los datos del lote y su historial de campañas con el historial climático de la zona.
Evalúa penalizaciones y bonificaciones agronómicas para rankear las mejores combinaciones de rotación (Back/app/scoring/engine.py).

Preview unavailable Figura 2: Formulario de configuración del establecimiento y panel de historial de campañas.

3. Tablero de Decisión Agronómica (Frontend React)
Muestra un mapa interactivo con Leaflet para ubicar el lote.
Despliega tarjetas comparativas de estrategias con puntajes visuales y reglas aplicadas.
Provee una línea de tiempo anual (Timeline) y un bloque de Evidencia NASA con métricas climáticas clave.

Preview unavailable Figura 3: Comparación lado a lado de estrategias de rotación y métricas de resiliencia.

Preview unavailable Figura 4: Calendario agrícola proyectado y bloque de evidencia climática de NASA POWER.

💡 Beneficios e Impacto
Decisiones con respaldo científico: Sustituye suposiciones o medias climáticas estáticas por 26 años de registros climáticos satelitales de alta resolución.
Mitigación del riesgo de sequía y heladas: Alerta sobre ventanas de estrés antes de comprometer la siembra.
Transparencia agronómica: El productor sabe exactamente por qué una rotación es recomendada (sin cajas negras).
Sostenibilidad del suelo: Fomenta cultivos de cobertura y rotaciones que preservan nutrientes y humedad en el perfil.
🎯 Metas a Futuro
Corto Plazo: Validar las matrices de recomendación con técnicos agrícolas y productores locales de la región semiárida central de Argentina.
Mediano Plazo: Incorporar pronósticos estacionales predictivos (ENSO, modelos climáticos estacionales) e integrar datos de humedad del suelo de misiones satelitales como SMAP.
Largo Plazo: Extender la cobertura a nivel nacional e internacional, agregando exportación de reportes agronómicos certificados en PDF para seguros y créditos agrícolas.
🛠️ Tecnologías y Herramientas
Área	Tecnologías / Herramientas
Frontend	React 19, Vite 8, Leaflet, JavaScript (ES Modules), CSS3 moderno
Backend	Python 3.12, FastAPI, Uvicorn, Pydantic
Ciencia de Datos	Pandas, Requests, PyYAML
Datos Satelitales	NASA POWER API (Prediction of Worldwide Energy Resources)
Control de Versiones	Git & GitHub

Preview unavailable Figura 5: Endpoints del motor de recomendación en FastAPI Swagger UI.

📁 Estructura del Repositorio
text
├── Back/                      # Backend en FastAPI
│   ├── app/
│   │   ├── scoring/           # Motor de cálculo y reglas agronómicas
│   │   ├── routers/           # Endpoints de cultivos, zonas y simulación
│   │   ├── repositories/      # Acceso a datos locales y climáticos
│   │   └── main.py            # Entrada principal de la API
│   └── requirements.txt
├── Front/                     # Frontend en React + Vite
│   ├── src/
│   │   ├── components/        # Mapa (Leaflet), Sidebar, Estado de Bienvenida
│   │   ├── decision/          # DecisionBoard, tarjetas de rotación, timeline
│   │   └── services/          # Conexión con la API del Backend
│   └── package.json
├── data/                      # Datos climáticos y catálogos agronómicos
│   ├── crops.yaml             # Requisitos agronómicos por cultivo
│   ├── zonas.yaml             # Coordenadas y límites de zonas de San Luis
│   └── processed/             # Series históricas diarias y mensuales
├── pipeline/                  # Scripts de descarga y procesamiento NASA POWER
└── README.md
💻 Guía de Instalación y Uso
Prerrequisitos
Node.js (v18 o superior)
Python (v3.10 o superior)
1. Clonar el repositorio
bash
git clone https://github.com/TU_USUARIO/NASA-challenge-2026.git
cd NASA-challenge-2026
2. Configurar y levantar el Backend
bash
cd Back
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py

El backend quedará corriendo en http://localhost:8000 (documentación Swagger disponible en /docs).

3. Configurar y levantar el Frontend

En otra terminal:

bash
cd Front
npm install
npm run dev

Abre tu navegador en http://localhost:5173 para usar la aplicación.

Proyecto desarrollado con orgullo para el NASA Space Apps Challenge 2026.

📂 ¿Dónde guardar las fotos para que se vean en GitHub?
Crea una carpeta llamada docs/screenshots/ en la raíz del proyecto.
Guarda allí tus capturas con los nombres que figuran en el texto:
01_bienvenida_mapa.png
02_config_lote.png
03_tarjetas_estrategias.png
04_timeline_evidencia.png
05_api_swagger.png (opcional)
Cuando hagas el commit y push a GitHub, ¡se renderizarán automáticamente con las imágenes!

