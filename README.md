# 🌾 AgroNASA — Resilient Crop Rotations
> **NASA Space Apps Challenge** | *Adapting Farms with NASA Data*

AgroNASA is an interactive agricultural decision-support web application. Its purpose is to assist farmers and agronomists (initially focused on the province of **San Luis, Argentina**) in designing, comparing, and selecting **crop rotation strategies** tailored to the actual climate variability and risks of their region.

---

## 📌 Table of Contents
- [What Does It Do?](#-what-does-it-do)
- [How Does It Work?](#-how-does-it-work)
- [Benefits & Impact](#-benefits--impact)
- [What We Hope to Achieve](#-what-we-hope-to-achieve)
- [Tools, Languages & Technologies](#-tools-languages--technologies)
- [Project Architecture](#-project-architecture)
- [Installation & Setup](#-installation--setup)

---

## 🚀 What Does It Do?

AgroNASA evaluates the agroclimatic risk of agricultural plots (water stress, heatwaves, late frosts, and optimal planting windows) using **26 years of historical satellite and meteorological records from NASA POWER (2000–2025)**.

Based on regional geographic selection and the farmer's historical field management, the platform generates actionable agronomic recommendations, including:
- **Comparable crop rotation strategies** (soil conservation/cover crops, risk diversification, or high-yield planning).
- **Resilience scoring and diagnosis** with transparent rule explanations.
- **Interactive annual timeline/calendar** displaying optimal sowing, development, and harvest stages.
- **NASA satellite evidence panel** providing direct climatic justification behind each recommendation.

<!-- SCREENSHOT 1 SUGGESTION -->
![Welcome State and Interactive Map](docs/screenshots/01_bienvenida_mapa.png)
*Figure 1: Main screen featuring the interactive zone selector for San Luis and farm configuration.*

---

## ⚙️ How Does It Work?

The system is built upon three integrated modules:

### 1. Climate Data Pipeline (NASA POWER)
- Ingests daily historical meteorological time-series (precipitation, solar radiation, min/max temperatures, relative humidity) via the NASA POWER API for agroecological zones defined in `data/zonas.yaml`.
- Cleans missing/fill values (`-999`) and calculates monthly and seasonal indicators for drought and thermal stress (`pipeline/build_features.py` and `indicadores_estacionales.py`).

### 2. Simulation & Scoring Engine (FastAPI Backend)
- Models crop-specific phenological and water balance requirements (`data/crops.yaml`).
- Cross-references farm parcel data and previous crop history against regional climate patterns.
- Computes agronomic bonuses and penalties to rank optimal crop rotations (`Back/app/scoring/engine.py`).

<!-- SCREENSHOT 2 SUGGESTION -->
![Parcel Configuration and Crop History](docs/screenshots/02_config_lote.png)
*Figure 2: Plot configuration sidebar and previous campaign history panel.*

### 3. Agronomic Decision Board (React Frontend)
- Visualizes an **interactive Leaflet map** to pinpoint the parcel location.
- Presents **side-by-side strategy comparison cards** with visual resilience metrics and underlying agronomic rules.
- Features an **annual crop timeline** and an integrated **NASA Evidence** dashboard displaying the climatic indicators that justify the advice.

<!-- SCREENSHOT 3 SUGGESTION -->
![Decision Board and Strategy Comparison](docs/screenshots/03_tarjetas_estrategias.png)
*Figure 3: Side-by-side rotation strategy comparison showing resilience scores and trade-offs.*

<!-- SCREENSHOT 4 SUGGESTION -->
![Annual Timeline and NASA Evidence](docs/screenshots/04_timeline_evidencia.png)
*Figure 4: Projected annual crop calendar and NASA POWER satellite evidence summary.*

---

## 💡 Benefits & Impact

- **Data-Driven & Science-Backed:** Replaces guesswork and static climate averages with 26 years of high-resolution satellite climate data.
- **Risk Mitigation:** Alerts farmers to potential water deficits, heatwaves, or frost hazards before planting investments are made.
- **Transparent Agronomy:** "No black boxes"—producers can inspect the exact NASA indicators and agronomic rules driving every suggestion.
- **Soil & Resource Conservation:** Promotes cover crops and crop diversification to improve water use efficiency and soil health.

---

## 🎯 What We Hope to Achieve

- **Short Term:** Validate recommendation models alongside local farmers and agricultural extension specialists in the semi-arid central region of Argentina.
- **Medium Term:** Incorporate predictive seasonal forecasts (ENSO indicators, seasonal forecasting models) and integrate satellite soil moisture datasets such as **SMAP**.
- **Long Term:** Expand regional coverage across Latin America and offer certified agronomic export reports (PDF) for agricultural credit and climate risk insurance.

---

## 🛠️ Tools, Languages & Technologies

| Layer | Tools & Technologies |
|---|---|
| **Frontend** | React 19, Vite 8, Leaflet, Modern JavaScript (ES Modules), CSS3 |
| **Backend** | Python 3.12, FastAPI, Uvicorn, Pydantic |
| **Data Science & Processing** | Pandas, Requests, PyYAML |
| **Satellite Data** | NASA POWER API (Prediction of Worldwide Energy Resources) |
| **Version Control & Quality** | Git, GitHub, Oxlint |

<!-- SCREENSHOT 5 SUGGESTION (OPTIONAL) -->
![Backend API Documentation](docs/screenshots/05_api_swagger.png)
*Figure 5: Interactive REST API endpoints in FastAPI Swagger UI.*

---

## 📁 Project Architecture

```text
├── Back/                      # FastAPI Backend
│   ├── app/
│   │   ├── scoring/           # Agronomic scoring engine and rules
│   │   ├── routers/           # Endpoints for crops, regions, and simulations
│   │   ├── repositories/      # Data access layer
│   │   └── main.py            # API entrypoint
│   └── requirements.txt
├── Front/                     # React + Vite Frontend
│   ├── src/
│   │   ├── components/        # Leaflet Map, Sidebar, Welcome State
│   │   ├── decision/          # Decision Board, rotation cards, timeline
│   │   └── services/          # Backend API client integration
│   └── package.json
├── data/                      # Climate data and agronomic catalogs
│   ├── crops.yaml             # Phenological & environmental crop requirements
│   ├── zonas.yaml             # Coordinates & bounding boxes for target zones
│   └── processed/             # Cleaned daily and monthly climate series
├── pipeline/                  # NASA POWER automated data extraction scripts
└── README.md
```

---

## 💻 Installation & Setup

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.10 or higher)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/NASA-challenge-2026.git
cd NASA-challenge-2026
```

### 2. Configure and run the Backend
```bash
cd Back
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
*The backend API will run on `http://localhost:8000` (Swagger UI available at `/docs`).*

### 3. Configure and run the Frontend
In another terminal window:
```bash
cd Front
npm install
npm run dev
```
*Open `http://localhost:5173` in your browser to start using AgroNASA.*

---

*Developed with pride for the **NASA Space Apps Challenge 2026**.*
