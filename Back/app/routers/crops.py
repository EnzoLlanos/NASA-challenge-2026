from typing import List, Optional, Annotated
from fastapi import APIRouter, Query
from app.schemas import CropInfo, ZonaSanLuis
from app.scoring.engine import ScoringEngine

router = APIRouter(prefix="/api/crops", tags=["Cultivos"])


@router.get("", response_model=List[CropInfo], summary="Obtener lista de cultivos adaptables por zona")
def get_crops(
    zona: Annotated[
        Optional[ZonaSanLuis],
        Query(description="Zona de San Luis a consultar: 'norte', 'centro' o 'sur'")
    ] = ZonaSanLuis.CENTRO,
    season: Annotated[
        Optional[str],
        Query(description="Filtrar opcionalmente por ciclo de cultivo (ej: verano, invierno, cubierta)")
    ] = None,
):
    """
    Retorna la lista de cultivos leídos desde `data/crops.yaml` adaptados a la zona seleccionada
    de San Luis (`norte`, `centro`, `sur`), con sus requerimientos de agua y suelo.
    """
    crops_dict = ScoringEngine.load_crops_for_zone(zona=zona or ZonaSanLuis.CENTRO)
    crops_list = list(crops_dict.values())
    if season and isinstance(season, str) and season.strip():
        s_clean = season.strip().lower()
        crops_list = [c for c in crops_list if c.season.lower() == s_clean]
    return crops_list
