from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from app.schemas.region import RegionSanLuis, Tierra


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
    region: Optional[RegionSanLuis] = Field(
        default=RegionSanLuis.CENTRO,
        description="Región de San Luis seleccionada (norte, centro o sur) en lugar del mapa abierto"
    )
    tierra: Optional[Tierra] = Field(
        default=None,
        description="Objeto Tierra opcional (nombre, región y validación de delimitador en San Luis)"
    )
    location: Optional[Location] = Field(
        default=None,
        description="Ubicación geográfica opcional por retrocompatibilidad"
    )
    current_rotation: List[str] = Field(
        default=["maíz", "soja"],
        description="Lista de cultivos que componen la rotación actual del productor"
    )
    priorities: Priorities

    @field_validator("region", mode="before")
    @classmethod
    def normalize_region(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v


class StrategyOption(BaseModel):
    name: str = Field(..., description="Nombre de la secuencia de rotación de cultivos")
    is_current: bool = Field(False, description="Indica si corresponde a la rotación actual del productor")
    score: float = Field(..., ge=0.0, le=1.0, description="Puntuación ponderada calculada (0 a 1)")
    why: str = Field(..., description="Justificación agronómica y balance general")
    benefits: List[str] = Field(..., description="Lista de beneficios principales")
    evidence: str = Field(..., description="Evidencia de respaldo con datos climáticos o satelitales (NASA POWER)")
    evidence_details: Optional[dict] = Field(
        None,
        description="Evidencia estructurada con trazabilidad científica (dataset, finding, resolution, period)"
    )
    risks_to_validate: str = Field(..., description="Factores de riesgo o advertencias a validar con asesor local")


class RotationResponse(BaseModel):
    region_evaluada: RegionSanLuis = Field(
        default=RegionSanLuis.CENTRO,
        description="Región de San Luis para la cual se calibraron las estrategias (norte, centro, sur)"
    )
    tierra_nombre: Optional[str] = Field(
        default=None,
        description="Nombre de la tierra evaluada si fue provista"
    )
    recommendation: str = Field(..., description="Nombre de la estrategia óptima recomendada")
    strategies: List[StrategyOption] = Field(..., description="Listado de estrategias comparadas ordenadas por puntaje")
    data_gaps: List[str] = Field(
        default_factory=lambda: [
            "Resolución espacial NASA POWER ~0.5° (~50 km), no captura microclimas a nivel de lote individual.",
            "Ausencia de sensores de humedad de suelo in situ: validar humedad útil antes de siembras críticas.",
            "Recomendación agronómica orientativa: contrastar siempre con el asesor técnico local."
        ],
        description="Brechas de información y limitaciones honestas del modelo satelital"
    )
