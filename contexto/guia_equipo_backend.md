# 🎯 Guía de comienzo: Equipo Backend (2 personas)

## 📍 Estado actual del proyecto
- **Dataset NASA POWER**: Procesado y listo en `data/processed/power_monthly.csv`
- **Estructura del repositorio**: Already tiene backend/ folder con package.json, .env.example
- **Objeto principal**: Implementar API FastAPI + Pydantic que sirva los datos climáticos y el motor de puntuación de rotaciones

## 👥 Integración del equipo
- 2 personas encargadas del backend
- Necesitan coordinarse con:
  - **Equipo Datos**: Para consumo de `power_monthly.csv` y eventual `crops.yaml`
  - **Equipo Frontend**: Para contrato de API (`schemas.py`, endpoints)

## 🚀 Paso 1: Preparar entorno (30 min)

```bash
# 1. Verificar estructura actual
ls -la Back/src/ Back/app/ 2>/dev/null || echo "Estructura a crear"

# 2. Install dependencias si es necesario
# El Back/ package.json sugiere Node, pero el backend es Python
# Verificar si existe entorno Python
python3 --version
which python3

# 3. Moverse al directorio backend
cd Back

# 4. Instalar FastAPI y Pydantic si no existen
python3 -m pip install fastapi uvicorn pydantic 2>/dev/null || \
  apt list --installed 2>/dev/null | grep python3-pip

# 5. Verificar .env.example
cat .env.example 2>/dev/null || echo "No existe, crear uno"
```

## 📋 Paso 2: Definir schemas API (1 hora)

### Endpoints requeridos (Según Sección 9 del contexto):

```python
# backend/app/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# 1. GET /api/crops -> lista de cultivos y rasgos
class CropInfo(BaseModel):
    name: str
    water_consumption: float  # mm por ciclo
    drought_tolerance: float  # 0-1 scale
    nitrogen_fixation: bool
    root_depth: float  # cm
    soil_coverage: float  # % ground cover
    organic_matter: float  # % aportado
    market_potential: str  # "alto", "medio", "bajo"
    # Rasgos adicionales para San Luis
    adaptation_notes: Optional[str] = None

class CropsList(BaseModel):
    crops: List[CropInfo]
    source: str  # "crops.yaml" o "hardcoded mock"

# 2. GET /api/field-profile?lat=&lon= -> resumen climático, series de NDVI, períodos de campo desnudo, riesgos
class FieldProfile(BaseModel):
    location: dict  # {"lat": float, "lon": float, "name": str}
    climate_summary: dict  # Métricas mensuales resumidas
    ndvi_series: Optional[List[dict]] = None  # Mock si no hay datos
    bare_land_periods: List[str]  # Meses sin cultivos
    risk_indicators: List[str]  # Heladas, olas de calor, etc.
    data_gaps: List[str]  # Brechas de información

# 3. POST /api/rotations -> recibe ubicación, prioridades y rotación actual; devuelve 3+ estrategias
class RotationRequest(BaseModel):
    location: dict  # {"lat": float, "lon": float, "name": str}
    current_rotation: List[str]  # ["maíz", "soja", "trigo"]
    priorities: dict  # {"agua": float, "ingresos": float, "suelo": float, "erosion": float}
    # Pesos deben sumar 1.0 o ser normalizados automaticamente

class RotationStrategy(BaseModel):
    name: str
    is_current: bool
    score: float  # 0-1
    why: str  # Texto corto lenguaje simple
    benefits: List[str]
    evidence: List[dict]  # {"dataset": str, "finding": str, "resolution": str, "period": str}
    data_gaps: List[str]
    risks_to_validate: List[str]

class RotationsResponse(BaseModel):
    strategies: List[RotationStrategy]
    recommendation: Optional[str] = None
```

### 🎯 Objetivo del schemas.py
- Crear modelos Pydantic que coincidan exactamente con el contrato del desafío
- Usar tipos que el frontend pueda consumir fácilmente
- Incluir validación de que pesos de priorities sumen 1.0 (opcional pero bueno)
- Dejar placeholders claros para datos que vendrán del equipo de datos

## 🛠️ Paso 3: Implementar motor de puntuación (1.5 horas)

### Estructura:
```
backend/app/scoring/
├── engine.py        # Cálculo del puntaje
└── explain.py       # Generación de explicaciones textuales
```

### engine.py - Lógica mínima viable:

```python
# backend/app/scoring/engine.py

from typing import List, Dict
from datetime import datetime
import yaml
from pathlib import Path

# Cargar rasgos de cultivos (después crear crops.yaml)
# Por ahora, usar datos mock o simples
CROPS_DB = {
    "maíz": {
        "water_consumption": 500,  # mm
        "drought_tolerance": 0.3,
        "root_depth": 150,
        "market_potential": "alto",
    },
    "soja": {
        "water_consumption": 450,
        "drought_tolerance": 0.5,
        "root_depth": 80,
        "market_potential": "alto",
    },
    # Agregar más cultivos según sea necesario
}

def calculate_score(
    rotation: List[str],
    priorities: Dict[str, float],
    climate_indicators: Dict
) -> float:
    """
    Calcula un puntaje 0-1 para una rotación de cultivos.
    
    Fórmula transparente (no caja negra):
    score = suma(peso_indicador * valor_cultivo)
    
    donde:
    - priorities = {"agua": 0.4, "ingresos": 0.3, "suelo": 0.2, "erosion": 0.1}
    - Cada indicador se calcula basándose en los datos climáticos
    - El rasgo de cada cultivo contribuye al indicador
    """
    
    # Normalizar pesos si no suman 1
    total_priority = sum(priorities.values())
    normalized = {k: v/total_priority for k, v in priorities.items()}
    
    # Calcular componentes (simplificado)
    water_score = 0
    soil_score = 0
    income_score = 0
    
    for crop in rotation:
        if crop in CROPS_DB:
            crop_data = CROPS_DB[crop]
            # Componente agua: tolerancia a sequía + consumo vs disponibilidad
            water_score += crop_data["drought_tolerance"] / len(rotation)
            # Componente suelo: profundidad de raíz
            soil_score += min(crop_data["root_depth"] / 300, 1.0) / len(rotation)  # Normalizar a 300cm
    
    # Combinar con pesos
    score = (
        normalized.get("agua", 0.4) * water_score +
        normalized.get("ingresos", 0.3) * income_score +
        normalized.get("suelo", 0.2) * soil_score
    )
    
    return round(min(max(score, 0), 1), 2)  # Asegurar que esté en [0, 1]


def generate_explanation(
    rotation: List[str],
    score: float,
    climate_indicators: Dict,
    priorities: Dict[str, float]
) -> Dict:
    """
    Convierte el puntaje y términos en frases y evidencia citable.
    Esto cumple con la Sección 8 del contexto: 'explain.py convierte cada término del puntaje en una frase'
    """
    
    reasons = []
    risks = []
    benefits = []
    
    # Analizar por qué este score
    if priorities.get("agua", 0) > 0.3:
        # Si el agricultorPrioriza agua, explicar hallazgos climáticos
        avg_rain = climate_indicators.get("avg_precip", 0)
        if avg_rain < 100:  # Lluvia baja
            reasons.append(
                f"Verano con lluvias abajo del promedio ({avg_rain:.0f}mm), "
                "requiere cultivos con alta tolerancia a sequía"
            )
        else:
            reasons.append(
                f"Buena disponibilidad hídrica estival ({avg_rain:.0f}mm), "
                "adecuado para cultivos de mayor demanda hídrica"
            )
    
    # Riesgos basados en indicadores climáticos
    frost_days = climate_indicators.get("frost_days", 0)
    heat_days = climate_indicators.get("heat_days_35", 0)
    
    if frost_days > 0:
        risks.append(
            f"{frost_days} días de helada identificados en temporada - "
            "revisar fechas de siembra con técnico local"
        )
    
    if heat_days > 10:
        risks.append(
            f"{heat_days} días de calor extremo (>35°C) - "
            "verificar sensibilidad térmica de los cultivos seleccionados"
        )
    
    # Benefits basados en rasgos de cultivo
    for crop in rotation:
        if crop in CROPS_DB:
            if CROPS_DB[crop].get("nitrogen_fixation", False):
                benefits.append(
                    f"{crop} fija nitrógeno, reduce necesidad de fertilizantes"
                )
    
    return {
        "why": "; ".join(reasons) if reasons else "Rotación equilibrada para la región",
        "benefits": benefits[:4],  # Máx 4 beneficios
        "evidence": [],  # Se llenará desde el pipeline
        "risks_to_validate": risks[:3]  # Máx 3 riesgos
    }
```

### explain.py - Generación de texto:

```python
# backend/app/scoring/explain.py

from typing import List, Dict
from .engine import calculate_score, generate_explanation

def explain_rotation(
    rotation: List[str],
    current_rotation: List[str],
    priorities: Dict[str, float],
    climate_data: Dict
) -> Dict:
    """
    Función principal que formatea el resultado según el contrato API.
    Coincide con la estructura JSON de la Sección 7/8 del contexto.
    """
    
    score = calculate_score(rotation, priorities, climate_data)
    explanation = generate_explanation(rotation, score, climate_data, priorities)
    
    is_current = rotation == current_rotation
    
    return {
        "name": " → ".join(rotation),
        "is_current": is_current,
        "score": score,
        "why": explanation["why"],
        "benefits": explanation["benefits"],
        "evidence": explanation["evidence"],
        "data_gaps": climate_data.get("gaps", ["Sin datos de suelo a nivel de lote"]),
        "risks_to_validate": explanation["risks_to_validate"]
    }
```

## 🔌 Paso 4: Crear endpoint principal (1 hora)

```python
# backend/app/app.py (o main.py dependiendo estructura actual)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import List

from schemas import CropsList, FieldProfile, RotationRequest, RotationsStrategy, RotationsResponse
from scoring.engine import calculate_score, generate_explanation
from scoring import explain_rotation

app = FastAPI(
    title="Adapting Farms API",
    description="Herramienta de apoyo a la decisión para rotación de cultivos",
    version="0.1.0"
)

# Datos mock temporales mientras tanto el equipo de datos proporciona reales
MOCK_CLIMATE_INDICATORS = {
    "avg_precip": 85.5,  # mm promedio estival
    "frost_days": 2,
    "heat_days_35": 5,
    "gaps": ["No hay mediciones de suelo a nivel de lote"]
}

MOCK_CROPS_DB = [
    {"name": "maíz", "water_consumption": 500, "drought_tolerance": 0.3, "root_depth": 150, "market_potential": "alto"},
    {"name": "soja", "water_consumption": 450, "drought_tolerance": 0.5, "root_depth": 80, "market_potential": "alto"},
    {"name": "trigo", "water_consumption": 350, "drought_tolerance": 0.8, "root_depth": 120, "market_potential": "medio"},
]

@app.get("/api/crops", response_model=CropsList)
async def get_crops():
    """Retorna lista de cultivos y sus rasgos"""
    return {
        "crops": [
            {"name": "maíz", "water_consumption": 500, "drought_tolerance": 0.3, 
             "nitrogen_fixation": False, "root_depth": 150, "soil_coverage": 0.8, 
             "organic_matter": 0.05, "market_potential": "alto"},
            {"name": "soja", "water_consumption": 450, "drought_tolerance": 0.5,
             "nitrogen_fixation": True, "root_depth": 80, "soil_coverage": 0.7,
             "organic_matter": 0.03, "market_potential": "alto"},
            {"name": "trigo", "water_consumption": 350, "drought_tolerance": 0.8,
             "nitrogen_fixation": False, "root_depth": 120, "soil_coverage": 0.9,
             "organic_matter": 0.07, "market_potential": "medio"}
        ],
        "source": "hardcoded mock - reemplazar con crops.yaml del equipo de datos"
    }

@app.get("/api/field-profile", response_model=FieldProfile)
async def get_field_profile(lat: float, lon: float, name: str = "campo"):
    """Resumen climático para una ubicación específica"""
    return {
        "location": {"lat": lat, "lon": lon, "name": name},
        "climate_summary": {
            "temp_mean_c": 22.5,
            "precip_mm": 85.5,
            "frost_days": 2,
            "heat_days_35": 5,
            "evapotranspiration_mm": 450
        },
        "ndvi_series": None,  # Mock - equipo datos 2 podría llenar
        "bare_land_periods": ["Julio", "Agosto"],  # Meses de campo desnudo
        "risk_indicators": [
            f"{MOCK_CLIMATE_INDICATORS['frost_days']} días de helada",
            f"{MOCK_CLIMATE_INDICATORS['heat_days_35']} días de calor extremo"
        ],
        "data_gaps": MOCK_CLIMATE_INDICATORS["gaps"]
    }

@app.post("/api/rotations", response_model=RotationsResponse)
async def calculate_rotations(request: RotationRequest):
    """
    Recibe ubicación, prioridades y rotación actual;
    devuelve 3+ estrategias con score y explicación.
    """
    
    # Rotaciones candidatas a evaluar (incluyendo la actual)
    candidate_rotations = [
        request.current_rotation,  # La que ya usa el agricultor
        ["maíz", "soja"],  # Opción básica
        ["soja", "trigo"],  # Alternativa
        ["maíz", "soja", "trigo"],  # Rotación completa
        ["soja", "maíz"],  # Orden inverso
    ]
    
    strategies = []
    for rotation in candidate_rotations[:4]:  # Máx 4 estrategias para no saturar
        # Calcular score
        score = calculate_score(rotation, request.priorities, MOCK_CLIMATE_INDICATORS)
        
        # Generar explicación
        explanation = generate_explanation(
            rotation, score, MOCK_CLIMATE_INDICATORS, request.priorities
        )
        
        strategy = {
            "name": " → ".join(rotation),
            "is_current": rotation == request.current_rotation,
            "score": score,
            "why": explanation["why"],
            "benefits": explanation["benefits"],
            "evidence": explanation["evidence"],
            "data_gaps": MOCK_CLIMATE_INDICATORS["gaps"],
            "risks_to_validate": explanation["risks_to_validate"]
        }
        strategies.append(strategy)
    
    # Ordenar por score descendente
    strategies.sort(key=lambda x: x["score"], reverse=True)
    
    # Agregar recomendación al mejor
    response = {
        "strategies": strategies,
        "recommendation": strategies[0]["name"] if strategies else None
    }
    
    return response

# Para correr: uvicorn backend.app.app:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 📊 Paso 5: Probar el backend (30 min)

```bash
# 1. Ejecutar el servidor
cd Back
python3 -m uvicorn app.app:app --reload  # Ajustar según estructura real

# 2. Probar endpoints con curl o en navegador
curl http://localhost:8000/api/crops

curl -X POST http://localhost:8000/api/rotations \
  -H "Content-Type: application/json" \
  -d '{
    "location": {"lat": -33.30, "lon": -65.30, "name": "san_luis_argentina"},
    "current_rotation": ["maíz", "soja"],
    "priorities": {"agua": 0.4, "ingresos": 0.3, "suelo": 0.2, "erosion": 0.1}
  }'

# 3. Probar field profile
curl "http://localhost:8000/api/field-profile?lat=-33.30&lon=-65.30"
```

### ✅ Checklist "Hecho" para el equipo Backend:

- [ ] `backend/app/schemas.py` creado con 3 modelos Pydantic (CropsList, FieldProfile, RotationsResponse)
- [ ] `backend/app/scoring/engine.py` implementado con `calculate_score()` funcional
- [ ] `backend/app/scoring/explain.py` implementado con `generate_explanation()` funcional
- [ ] Endpoint `GET /api/crops` retorna datos mock coherentes
- [ ] Endpoint `GET /api/field-profile` retorna resumen climático
- [ ] Endpoint `POST /api/rotations` retorna 3+ estrategias con score y explicación
- [ ] Se puede correr `uvicorn` y probar con curl
- [ ] `.env.example` actualizado con variables placeholder (aunque POWER no necesita clave)
- [ ] Documentado en README.md los endpoints disponibles

### 📝 Notas importantes para el equipo:

1. **Mock primero**: El backend debe devolver respuestas falsas con el formato real desde la hora 2 (Sección 9 del contexto). Esto permite al frontend avanzar independientemente.

2. **Unidades explícitas**: Cada número debe tener unidades explícitas (mm, °C, %, cm). Eso es el "error número uno" al unir datasets (Sección 9).

3. **Pesos de priorities**: El sistema debe normalizar automáticamente si los pesos no suman 1.0, o lanzar warning pero continuar.

4. **Evidencia citable**: Cada estrategia debe tener `evidence` con formato `{"dataset": "NASA POWER", "finding": "...", "resolution": "0.5° / diario", "period": "2000-2025"}`. Esto alimenta las tarjetas de evidencia aunque sean datos mock.

5. **Datos gaps**: Siempre incluir `data_gaps` honestos. El contexto dice "marcar la incertidumbre: si un dato es de baja resolución o falta, debe aparecer en `data_gaps`".

6. **Integration with pipeline**: Cuando el equipo de datos tenga listo `power_monthly.csv`, el backend debe poder leerlo con:
   ```python
   import pandas as pd
   df = pd.read_csv("data/processed/power_monthly.csv")
   # Luego extraer indicadores para el motor de puntuación
   ```

7. **Ramillas cortas**: Crear ramas por feature y merge a `main` cada 2-3 horas (Sección 9). `main` siempre tiene que correr.

8. **Plan B video**: Si los datos tardan en bajarse, grabar video con mock data antes del final (Sección 9).

---

## 🧩 Próximos pasos inmediatos para el equipo

**Hora 1-2:** Crear `schemas.py` completo y probar los 3 endpoints con curl.

**Hora 2-3:** Implementar `engine.py` y `explain.py` con lógica mínima pero funcional.

**Hora 3-4:** Integrar todo en `app.py` y hacer testing completo con las 3 tipos de peticiones.

**Hora 4-6:** Documentar en `README.md` cómo correr el backend y probar el flujo completo.

¿Necesita el equipo backend alguna ayuda específica para empezar? Pueden consultar el documento `contexto/plan_trabajo_paralelo.md` para ver cómo esto conecta con los otros equipos.