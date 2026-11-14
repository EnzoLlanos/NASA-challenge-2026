from typing import List, Optional, Annotated
from fastapi import APIRouter, Query
from app.schemas.crop import CropResponse
from app.repositories.crop_repository import CropRepository

router = APIRouter(prefix="/api/crops", tags=["Crops"])


@router.get("", response_model=List[CropResponse], summary="Obtener lista de cultivos regionales")
def get_crops(
    season: Annotated[
        Optional[str],
        Query(description="Filtrar opcionalmente por ciclo de cultivo (ej: estival, invernal, cobertura)")
    ] = None
):
    """
    Retorna la lista de cultivos disponibles con sus rasgos agronómicos e hídricos
    (consumo de agua, tolerancia a sequía, fijación de nitrógeno, profundidad de raíz y potencial de mercado).
    """
    return CropRepository.get_all(season=season)


