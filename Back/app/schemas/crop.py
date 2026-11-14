from pydantic import BaseModel, Field
from typing import Literal


class CropBase(BaseModel):
    id: str = Field(..., description="Identificador único del cultivo en minúsculas (ej: maiz, soja)")
    name: str = Field(..., description="Nombre común del cultivo")
    water_consumption_mm: float = Field(..., description="Consumo hídrico estimado en mm durante el ciclo")
    drought_tolerance: float = Field(..., ge=0.0, le=1.0, description="Tolerancia a sequía entre 0.0 y 1.0")
    nitrogen_fixation: bool = Field(..., description="Indica si fija nitrógeno en el suelo")
    root_depth_cm: int = Field(..., description="Profundidad radicular en centímetros")
    market_potential: Literal["alto", "medio", "bajo"] = Field(..., description="Potencial de renta o liquidez en el mercado")
    cycle_season: str = Field("estival", description="Estación principal de crecimiento (estival, invernal, cobertura)")


class CropResponse(CropBase):
    pass
