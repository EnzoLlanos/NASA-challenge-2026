from fastapi import APIRouter
from app.schemas import RotationRequest, RotationResponse
from app.scoring.engine import ScoringEngine
from app.services.scoring_service import ScoringService

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
            "nombre": "Zona Norte (San Luis)",
            "descripcion": "Veranos calurosos y secos. Requiere cultivos rústicos como sorgo y buena cobertura.",
            "cultivo_principal": "Sorgo granífero / Maíz con riego",
        },
        {
            "id": "centro",
            "nombre": "Zona Centro (San Luis)",
            "descripcion": "Región núcleo de valles y cuencas. Rotación balanceada maíz-soja con cobertura de invierno.",
            "cultivo_principal": "Maíz / Soja / Trigo",
        },
        {
            "id": "sur",
            "nombre": "Zona Sur (San Luis)",
            "descripcion": "Suelos arenosos (médanos) con vientos fuertes. Prioridad proteger el suelo y raíces profundas.",
            "cultivo_principal": "Girasol / Centeno forrajero",
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
    summary="Evaluar rotaciones agronómicas adaptadas por zona de San Luis",
)
def evaluate_rotations(payload: RotationRequest):
    """
    Recibe la zona de San Luis (`norte`, `centro` o `sur`), la tierra y el cultivo actual.
    Devuelve estrategias de rotación evaluadas en lenguaje simple para agricultores,
    con evidencias satelitales NASA y recomendaciones agroecológicas.
    """
    return ScoringEngine.calculate_rotation(payload)
