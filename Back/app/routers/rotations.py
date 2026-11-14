from fastapi import APIRouter
from app.schemas.rotation import RotationRequest, RotationResponse
from app.services.scoring_service import ScoringService

router = APIRouter(prefix="/api/rotations", tags=["Rotations"])


@router.post("", response_model=RotationResponse, summary="Evaluar y comparar estrategias de rotación de cultivos")
def evaluate_rotations(payload: RotationRequest):
    """
    Recibe la rotación actual del productor y sus prioridades (ponderaciones para agua, ingresos, suelo y erosión).
    Devuelve un ranking de estrategias comparadas con puntaje 0 a 1, justificación, beneficios y evidencias climáticas.
    """
    return ScoringService.generate_rotation_recommendations(
        current_rotation=payload.current_rotation,
        priorities=payload.priorities,
    )
