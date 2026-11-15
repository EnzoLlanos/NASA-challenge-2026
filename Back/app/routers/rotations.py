from fastapi import APIRouter
from app.schemas import RotationRequest, RotationResponse
from app.scoring.engine import ScoringEngine

router = APIRouter(tags=["Estrategias de Rotación"])


@router.get(
    "/api/zones",
    summary="Listar las 3 zonas de San Luis (Norte, Centro, Sur) para menús desplegables",
)
@router.get(
    "/api/regions",
    summary="Alias de zonas para compatibilidad",
)
def get_zones():
    """
    Retorna las 3 zonas de San Luis para alimentar los menús desplegables del frontend
    sin mapas complejos ni porcentajes.
    """
    return [
        {
            "id": "norte",
            "nombre": "Zona Norte (Valle del Conlara / Sierras)",
            "descripcion": "Clima serrano templado con buena humedad de suelo (0.60) pero 35 días de heladas al año. Prioridad: maíz, soja y leguminosas de cobertura.",
            "cultivo_principal": "Maíz / Soja / Arveja (cobertura)",
            "coords": {"lat": -32.35, "lng": -65.00},
        },
        {
            "id": "centro",
            "nombre": "Zona Centro (Capital / Villa Mercedes)",
            "descripcion": "Región agrícola central con lluvias concentradas en verano. Rotación balanceada maíz-soja con cobertura invernal.",
            "cultivo_principal": "Maíz / Soja / Trigo / Vicia",
            "coords": {"lat": -33.30, "lng": -65.30},
        },
        {
            "id": "sur",
            "nombre": "Zona Sur (Buena Esperanza / Dupuy)",
            "descripcion": "Suelos arenosos medanosos con 34 días de calor sofocante (≥35°C) y baja retención de agua. Prioridad: sorgo rústico, girasol y centeno contra viento.",
            "cultivo_principal": "Sorgo granífero / Girasol / Centeno",
            "coords": {"lat": -34.70, "lng": -65.30},
        },
    ]


@router.post(
    "/api/rotations",
    response_model=RotationResponse,
    summary="Calcular estrategias de rotación por zona de San Luis",
)
@router.post(
    "/api/estrategias",
    response_model=RotationResponse,
    summary="Evaluar rotaciones agronómicas adaptadas (sin porcentajes)",
)
@router.post(
    "/api/simulation",
    response_model=RotationResponse,
    summary="Endpoint de simulación para el Tablero de Decisión del Frontend",
)
def evaluate_rotations(payload: RotationRequest):
    """
    Recibe la zona de San Luis (`norte`, `centro` o `sur`), la tierra y el cultivo actual.
    Devuelve estrategias de rotación evaluadas en lenguaje simple para agricultores,
    sin porcentajes ni márgenes de ganancia confusos, con evidencias de satélites NASA.
    """
    return ScoringEngine.calculate_rotation(payload)
