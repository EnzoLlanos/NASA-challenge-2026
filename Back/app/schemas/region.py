from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, field_validator, model_validator

# =====================================================================
# DELIMITADORES DE SAN LUIS (Configurables por si las dudas)
# =====================================================================
MIN_PORCENTAJE_TIERRA_EN_SAN_LUIS: float = 50.0

SAN_LUIS_BOUNDS = {
    "lat_min": -36.00,  # Límite Sur (Gobernador Dupuy / La Pampa)
    "lat_max": -31.85,  # Límite Norte (Ayacucho / La Rioja - Córdoba)
    "lon_min": -67.35,  # Límite Oeste (Desaguadero / Mendoza - San Juan)
    "lon_max": -64.95,  # Límite Este (Chacabuco - Pedernera / Córdoba)
}


class RegionSanLuis(str, Enum):
    NORTE = "norte"
    CENTRO = "centro"
    SUR = "sur"


class ReglaRegionalItem(BaseModel):
    """Representa una regla agronómica y de riesgo específica de una región de San Luis."""
    codigo: str = Field(..., example="N1", description="Código identificador de la regla (ej. N1, C1, S1)")
    nombre: str = Field(..., example="Déficit hídrico crítico estival")
    factor_climatico: str = Field(..., example="520 mm/año y alta evaporación")
    impacto_metricas: str = Field(..., example="Penaliza Agua (-25 pts) en cultivos >450 mm sin riego")
    alerta_riesgo: str = Field(..., description="Texto de alerta que recibe el productor cuando se activa la regla")


class CondicionCampoPregunta(BaseModel):
    """Pregunta/condición contextual específica de la zona para adaptar el formulario."""
    id: str = Field(..., example="sueloArenosoVoladura")
    etiqueta: str = Field(..., example="¿Lote con médanos o suelo muy suelto propenso a voladura?")
    descripcion: str = Field(..., example="En el Sur los vientos de agosto-octubre vuelan la capa fértil si queda desnudo")
    icono: str = Field(default="💨")
    valor_por_defecto: bool = Field(default=True)


class RegionFormConfigResponse(BaseModel):
    """Configuración adaptativa del formulario y reglas para una región seleccionada."""
    region: RegionSanLuis
    nombre: str
    subtitulo_clima: str
    amenaza_principal: str
    icono_alerta: str = "🛰️"
    precipitacion_anual_mm: float
    dias_calor_extremo: int
    dias_heladas: int
    cultivos_recomendados: List[str]
    prioridades_sugeridas: Dict[str, bool]
    condicion_contextual: CondicionCampoPregunta
    reglas_activas: List[ReglaRegionalItem]


class Tierra(BaseModel):
    """
    Objeto Tierra perteneciente a un usuario.
    Representa un campo o lote ubicado en una de las 3 regiones de San Luis (norte, centro, sur).
    """
    nombre: str = Field(..., min_length=1, description="Nombre identificador de la tierra o lote (ej: 'Lote La Esperanza')")
    region: RegionSanLuis = Field(..., description="Región de San Luis donde se ubica: 'norte', 'centro' o 'sur'")
    porcentaje_en_san_luis: float = Field(
        default=100.0,
        ge=0.0,
        le=100.0,
        description="Porcentaje de la superficie de la tierra dentro de San Luis (delimitador mínimo: 50%)"
    )
    hectareas: Optional[float] = Field(default=None, gt=0, description="Superficie opcional del lote en hectáreas")
    lat: Optional[float] = Field(default=None, description="Latitud opcional (validada dentro de San Luis)")
    lon: Optional[float] = Field(default=None, description="Longitud opcional (validada dentro de San Luis)")

    @field_validator("region", mode="before")
    @classmethod
    def normalize_region(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @model_validator(mode="after")
    def validar_delimitador_san_luis(self):
        if self.porcentaje_en_san_luis < MIN_PORCENTAJE_TIERRA_EN_SAN_LUIS:
            raise ValueError(
                f"Delimitador San Luis: La tierra '{self.nombre}' tiene solo {self.porcentaje_en_san_luis}% en San Luis. "
                f"Debe tener como mínimo el {MIN_PORCENTAJE_TIERRA_EN_SAN_LUIS}% de su superficie dentro de la provincia."
            )

        if self.lat is not None:
            if not (SAN_LUIS_BOUNDS["lat_min"] <= self.lat <= SAN_LUIS_BOUNDS["lat_max"]):
                raise ValueError(
                    f"Delimitador Geográfico: La latitud {self.lat} está fuera de la provincia de San Luis "
                    f"({SAN_LUIS_BOUNDS['lat_min']} a {SAN_LUIS_BOUNDS['lat_max']})."
                )
        if self.lon is not None:
            if not (SAN_LUIS_BOUNDS["lon_min"] <= self.lon <= SAN_LUIS_BOUNDS["lon_max"]):
                raise ValueError(
                    f"Delimitador Geográfico: La longitud {self.lon} está fuera de la provincia de San Luis "
                    f"({SAN_LUIS_BOUNDS['lon_min']} a {SAN_LUIS_BOUNDS['lon_max']})."
                )
        return self


class Usuario(BaseModel):
    """Clase Usuario con su array de tierras ubicadas en San Luis."""
    id: Optional[str] = Field(default=None, description="Identificador único del usuario")
    nombre: str = Field(..., min_length=1, description="Nombre del productor o usuario")
    tierras: List[Tierra] = Field(
        default_factory=list,
        description="Array de objetos Tierra (cada una con su región y nombre)"
    )


class RegionDetailResponse(BaseModel):
    """Información agroclimática resumida de cada región de San Luis (Norte, Centro, Sur)."""
    id: RegionSanLuis = Field(..., description="Identificador de la región: norte, centro o sur")
    nombre: str = Field(..., description="Nombre completo de la región")
    departamentos_referencia: List[str] = Field(..., description="Departamentos o localidades de referencia")
    latitud_rango: str = Field(..., description="Franja de latitud que abarca la región en San Luis")
    precipitacion_media_anual_mm: float = Field(..., description="Lluvia promedio anual en mm (NASA POWER)")
    dias_calor_extremo_anual: int = Field(..., description="Días promedio al año con T > 35°C")
    dias_heladas_anual: int = Field(..., description="Días promedio al año con T <= 0°C")
    aptitud_y_suelo: str = Field(..., description="Características del suelo y régimen hídrico")
    cultivos_recomendados: List[str] = Field(..., description="Cultivos que mejor se adaptan a la región")
    amenaza_principal: Optional[str] = Field(default=None, description="Principal amenaza agroclimática regional")
    prioridades_sugeridas: Optional[Dict[str, bool]] = Field(default=None, description="Prioridades recomendadas para la zona")
    condicion_contextual: Optional[CondicionCampoPregunta] = Field(default=None, description="Condición específica del formulario para la zona")
    reglas_activas: Optional[List[ReglaRegionalItem]] = Field(default=None, description="Reglas de negocio y riesgo que aplican en esta región")


class DelimiterInfoResponse(BaseModel):
    """Respuesta con la configuración activa del delimitador de San Luis."""
    provincia: str = "San Luis, Argentina"
    min_porcentaje_tierra_en_san_luis: float = MIN_PORCENTAJE_TIERRA_EN_SAN_LUIS
    max_porcentaje_fuera_san_luis: float = 100.0 - MIN_PORCENTAJE_TIERRA_EN_SAN_LUIS
    limites_geograficos: dict = SAN_LUIS_BOUNDS
    regiones_habilitadas: List[str] = [r.value for r in RegionSanLuis]
