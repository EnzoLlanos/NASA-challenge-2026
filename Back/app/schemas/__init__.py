from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


# =====================================================================
# 1. ZONAS DE SAN LUIS (Norte, Centro, Sur)
# =====================================================================
class ZonaSanLuis(str, Enum):
    NORTE = "norte"
    CENTRO = "centro"
    SUR = "sur"


RegionSanLuis = ZonaSanLuis


# =====================================================================
# 2. DELIMITADOR Y OBJETOS DE TIERRAS Y USUARIOS
# =====================================================================
class Tierra(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre o identificación del lote")
    zona: ZonaSanLuis = Field(..., description="Zona de San Luis: 'norte', 'centro' o 'sur'")
    dentro_de_san_luis: bool = Field(default=True, description="Delimitador: dentro de San Luis")
    descripcion: Optional[str] = None

    @field_validator("zona", mode="before")
    @classmethod
    def normalizar_zona(cls, v):
        if isinstance(v, str):
            v_clean = v.strip().lower()
            if v_clean in ["norte", "centro", "sur"]:
                return v_clean
        return v

    @property
    def region(self) -> ZonaSanLuis:
        return self.zona


class Usuario(BaseModel):
    id: Optional[str] = None
    nombre: str
    tierras: List[Tierra] = Field(default_factory=list)


# =====================================================================
# 3. RASGOS DE CULTIVO (Crops) POR ZONA
# =====================================================================
class CropInfo(BaseModel):
    id: str
    name: str
    zona: ZonaSanLuis = ZonaSanLuis.CENTRO
    water_consumption: float
    drought_tolerance: float
    nitrogen_fixation: bool
    root_depth: int
    soil_coverage: float = 0.7
    season: str = "verano"
    cycle_months: int = 5
    market_potential: str = "medio"
    adaptation_notes: Optional[str] = None


CropBase = CropInfo
CropResponse = CropInfo


class CropsList(BaseModel):
    zona: ZonaSanLuis
    crops: List[CropInfo]
    source: str = "crops.yaml"


# =====================================================================
# 4. PRIORIDADES SIMPLIFICADAS (Sin porcentajes)
# =====================================================================
class PrioridadesSimple(BaseModel):
    agua: bool = True
    suelo: bool = True
    erosion: bool = True
    forraje: bool = False


class Priorities(BaseModel):
    agua: float = 0.4
    ingresos: float = 0.3
    suelo: float = 0.2
    erosion: float = 0.1


# =====================================================================
# 5. SOLICITUD DE ROTACIÓN (Entrada)
# =====================================================================
class RotationRequest(BaseModel):
    zona: Optional[ZonaSanLuis] = Field(default=ZonaSanLuis.CENTRO)
    tierra: Optional[Tierra] = None
    current_crop: Optional[str] = "Soja"
    current_rotation: Optional[List[str]] = Field(default=["Soja"])
    irrigation: Optional[str] = "lluvia"
    priorities: Optional[Any] = None


# =====================================================================
# 6. ESTRATEGIAS Y RESULTADOS (Salida: sin porcentajes, con zonas)
# =====================================================================
class SecuenciaItem(BaseModel):
    cultivo: str
    tipo: str = "cultivo"
    desde: int = 1
    hasta: int = 12
    meses_texto: Optional[str] = None


class MetricasCualitativas(BaseModel):
    agua: str
    nutrientes: str
    erosion: str
    salida_comercial: Optional[str] = None


class StrategyOption(BaseModel):
    id: str
    nombre: str
    is_current: bool = False
    etiqueta: str = "Alternativa"
    salud_suelo: str
    salud_suelo_nivel: int = 70
    resumen: str
    secuencia: List[SecuenciaItem] = Field(default_factory=list)
    metricas: MetricasCualitativas
    beneficios: List[str] = Field(default_factory=list)
    riesgos_locales: List[str] = Field(default_factory=list)
    evidencia_nasa: str

    @property
    def name(self) -> str:
        return self.nombre

    @property
    def why(self) -> str:
        return self.resumen

    @property
    def evidence(self) -> str:
        return self.evidencia_nasa

    @property
    def risks_to_validate(self) -> str:
        return "; ".join(self.riesgos_locales)


class RotationResponse(BaseModel):
    zona: ZonaSanLuis = ZonaSanLuis.CENTRO
    tierra_nombre: Optional[str] = None
    recomendacion: str
    estrategias: List[StrategyOption] = Field(default_factory=list)
    data_gaps: List[str] = Field(default_factory=list)

    @property
    def recommendation(self) -> str:
        return self.recomendacion

    @property
    def strategies(self) -> List[StrategyOption]:
        return self.estrategias


__all__ = [
    "ZonaSanLuis",
    "RegionSanLuis",
    "Tierra",
    "Usuario",
    "CropInfo",
    "CropBase",
    "CropResponse",
    "CropsList",
    "PrioridadesSimple",
    "Priorities",
    "RotationRequest",
    "SecuenciaItem",
    "MetricasCualitativas",
    "StrategyOption",
    "RotationResponse",
]
