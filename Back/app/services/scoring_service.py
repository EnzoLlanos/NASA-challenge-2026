from typing import List, Optional, Any
from app.schemas import (
    ZonaSanLuis,
    Tierra,
    RotationRequest,
    RotationResponse,
    PrioridadesSimple,
)
from app.scoring.engine import ScoringEngine


class ScoringService:
    """
    Capa de servicio que conecta las peticiones de los routers con el motor de puntuación agronómico.
    Alineado con el flujo simplificado para agricultores: sin porcentajes y segmentado por zonas de San Luis.
    """

    @classmethod
    def generate_rotation_recommendations(
        cls,
        current_rotation: Optional[List[str]] = None,
        priorities: Optional[Any] = None,
        region: Optional[Any] = None,
        zona: Optional[Any] = None,
        tierra: Optional[Tierra] = None,
        current_crop: Optional[str] = None,
    ) -> RotationResponse:
        # Resolver zona activa (soporta tanto 'zona' como 'region')
        zona_efectiva = zona or region or (tierra.zona if tierra else ZonaSanLuis.CENTRO)
        if hasattr(zona_efectiva, "value"):
            z_val = str(zona_efectiva.value).lower()
            try:
                zona_efectiva = ZonaSanLuis(z_val)
            except ValueError:
                zona_efectiva = ZonaSanLuis.CENTRO

        req = RotationRequest(
            zona=zona_efectiva,
            tierra=tierra,
            current_crop=current_crop or (current_rotation[0] if current_rotation else "Soja"),
            current_rotation=current_rotation or ["Soja"],
            priorities=priorities,
        )

        return ScoringEngine.calculate_rotation(req)
