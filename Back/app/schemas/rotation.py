from pydantic import BaseModel, Field
from typing import List, Optional


class Location(BaseModel):
    lat: Optional[float] = Field(None, description="Latitud de la parcela (ej: -33.30)")
    lon: Optional[float] = Field(None, description="Longitud de la parcela (ej: -65.30)")
    name: Optional[str] = Field("San Luis", description="Nombre o localidad de referencia")


class Priorities(BaseModel):
    agua: float = Field(..., ge=0.0, le=1.0, description="Ponderación de optimización del recurso hídrico")
    ingresos: float = Field(..., ge=0.0, le=1.0, description="Ponderación de rentabilidad y potencial de mercado")
    suelo: float = Field(..., ge=0.0, le=1.0, description="Ponderación de salud del suelo y fijación de nutrientes")
    erosion: float = Field(..., ge=0.0, le=1.0, description="Ponderación de mitigación del riesgo de erosión y cobertura")


class RotationRequest(BaseModel):
    location: Optional[Location] = Field(
        default=None,
        description="Ubicación geográfica opcional de la parcela"
    )
    current_rotation: List[str] = Field(
        default=["maíz", "soja"],
        description="Lista de cultivos que componen la rotación actual del productor"
    )
    priorities: Priorities



class StrategyOption(BaseModel):
    name: str = Field(..., description="Nombre de la secuencia de rotación de cultivos")
    is_current: bool = Field(False, description="Indica si corresponde a la rotación actual del productor")
    score: float = Field(..., ge=0.0, le=1.0, description="Puntuación ponderada calculada (0 a 1)")
    why: str = Field(..., description="Justificación agronómica y balance general")
    benefits: List[str] = Field(..., description="Lista de beneficios principales")
    evidence: str = Field(..., description="Evidencia de respaldo con datos climáticos o satelitales (NASA POWER)")
    risks_to_validate: str = Field(..., description="Factores de riesgo o advertencias a validar con asesor local")


class RotationResponse(BaseModel):
    recommendation: str = Field(..., description="Nombre de la estrategia óptima recomendada")
    strategies: List[StrategyOption] = Field(..., description="Listado de estrategias comparadas ordenadas por puntaje")
