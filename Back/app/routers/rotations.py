from fastapi import APIRouter
from app.schemas.rotation import RotationRequest, RotationResponse
from app.services.scoring_service import ScoringService

router = APIRouter(tags=["Estrategias"])


@router.post(
    "/api/rotations",
    response_model=RotationResponse,
    summary="Evaluar y comparar estrategias de rotación por región de San Luis (norte, centro, sur)",
)
@router.post(
    "/api/estrategias",
    response_model=RotationResponse,
    summary="Evaluar estrategias agronómicas para una Tierra o Región de San Luis",
)
def evaluate_rotations(payload: RotationRequest):
    """
    Recibe la región de San Luis (`norte`, `centro` o `sur`) o el objeto `Tierra` (`nombre`, `region`),
    junto con la rotación actual y las prioridades del productor.
    Devuelve las estrategias comparadas con puntaje (0 a 1), beneficios y evidencia climática regional.
    """
    return ScoringService.generate_rotation_recommendations(
        current_rotation=payload.current_rotation,
        priorities=payload.priorities,
        region=payload.region,
        tierra=payload.tierra,
    )
