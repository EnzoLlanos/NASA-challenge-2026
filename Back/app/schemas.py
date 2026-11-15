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


# Alias por compatibilidad
RegionSanLuis = ZonaSanLuis


# =====================================================================
# 2. DELIMITADOR Y OBJETOS DE TIERRAS Y USUARIOS
# =====================================================================
class Tierra(BaseModel):
    """
    Representa una parcela o lote perteneciente a un agricultor.
    Ubicada en una de las 3 zonas clave de San Luis (sin porcentajes confusos).
    """
    nombre: str = Field(..., min_length=1, description="Nombre o identificación del lote (ej. 'Lote El Ombú')")
    zona: ZonaSanLuis = Field(..., description="Zona de San Luis: 'norte', 'centro' o 'sur'")
    dentro_de_san_luis: bool = Field(
        default=True,
        description="Delimitador: confirma que la tierra pertenece a la provincia de San Luis"
    )
    descripcion: Optional[str] = Field(None, description="Observaciones o tipo de suelo")

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
        """Alias para mantener compatibilidad con endpoints previos."""
        return self.zona


class Usuario(BaseModel):
    """
    Representa al agricultor o productor con su lista de tierras registradas en San Luis.
    """
    id: Optional[str] = Field(None, description="Identificador único del usuario")
    nombre: str = Field(..., min_length=1, description="Nombre del agricultor o establecimiento")
    tierras: List[Tierra] = Field(
        default_factory=list,
        description="Lista de tierras del agricultor en San Luis"
    )


# =====================================================================
# 3. RASGOS DE CULTIVO (Crops) POR ZONA
# =====================================================================
class CropInfo(BaseModel):
    id: str = Field(..., description="Identificador del cultivo (ej. 'maiz', 'soja')")
    name: str = Field(..., description="Nombre común del cultivo")
    zona: ZonaSanLuis = Field(default=ZonaSanLuis.CENTRO, description="Zona de San Luis adaptada")
    water_consumption: float = Field(..., description="Consumo hídrico en mm por ciclo")
    drought_tolerance: float = Field(..., description="Tolerancia a sequía (0 a 1)")
    nitrogen_fixation: bool = Field(..., description="Indica si fija nitrógeno en el suelo")
    root_depth: int = Field(..., description="Profundidad de raíz en cm")
    soil_coverage: float = Field(default=0.7, description="Cobertura de suelo en pico (0 a 1)")
    season: str = Field(default="verano", description="Ventana de siembra: verano, invierno o cubierta")
    cycle_months: int = Field(default=5, description="Meses de duración del ciclo")
    market_potential: str = Field(default="medio", description="Salida comercial local (alto, medio, bajo)")
    adaptation_notes: Optional[str] = Field(None, description="Notas de adaptación agronómica para San Luis")


# Alias retrocompatibles
CropBase = CropInfo
CropResponse = CropInfo


class CropsList(BaseModel):
    zona: ZonaSanLuis
    crops: List[CropInfo]
    source: str = "crops.yaml"


# =====================================================================
# 4. PRIORIDADES SIMPLIFICADAS (Sin porcentajes ni fórmulas complejas)
# =====================================================================
class PrioridadesSimple(BaseModel):
    """
    Opciones claras para el agricultor mediante menús simples.
    Sin sliders de porcentajes matemáticos.
    """
    agua: bool = Field(default=True, description="Priorizar conservar agua en el suelo y evitar evaporación")
    suelo: bool = Field(default=True, description="Priorizar recuperar materia orgánica y nitrógeno")
    erosion: bool = Field(default=True, description="Priorizar proteger el suelo contra viento y lluvias intensas")
    forraje: bool = Field(default=False, description="Priorizar sumar pastoreo o forraje para animales")


# Soporte flexible para recibir prioridades flotantes o booleanas sin romperse
class Priorities(BaseModel):
    agua: float = Field(default=0.4, ge=0.0, le=1.0)
    ingresos: float = Field(default=0.3, ge=0.0, le=1.0)
    suelo: float = Field(default=0.2, ge=0.0, le=1.0)
    erosion: float = Field(default=0.1, ge=0.0, le=1.0)


# =====================================================================
# 5. SOLICITUD DE ROTACIÓN (Entrada)
# =====================================================================
class RotationRequest(BaseModel):
    zona: Optional[ZonaSanLuis] = Field(
        default=ZonaSanLuis.CENTRO,
        description="Zona seleccionada de San Luis: 'norte', 'centro' o 'sur'"
    )
    tierra: Optional[Tierra] = Field(
        default=None,
        description="Objeto Tierra opcional del productor"
    )
    current_crop: Optional[str] = Field(
        default="Soja",
        description="Cultivo actual sembrado (menú desplegable simple)"
    )
    current_rotation: Optional[List[str]] = Field(
        default=["Soja"],
        description="Secuencia de cultivos actual (ej. ['Soja', 'Maíz'])"
    )
    irrigation: Optional[str] = Field(
        default="lluvia",
        description="Régimen hídrico: 'lluvia' o 'riego'"
    )
    priorities: Optional[Any] = Field(
        default=None,
        description="Prioridades seleccionadas por el agricultor (simple o detallada)"
    )


# =====================================================================
# 6. ESTRATEGIAS Y RESULTADOS (Salida limpia: sin porcentajes, con zonas)
# =====================================================================
class SecuenciaItem(BaseModel):
    cultivo: str
    tipo: str = "cultivo"  # 'cultivo' o 'cobertura'
    desde: int = 1         # Mes 1 (enero) a 12 (diciembre)
    hasta: int = 12
    meses_texto: Optional[str] = None


class MetricasCualitativas(BaseModel):
    """
    Descripciones en lenguaje simple y directo para el agricultor.
    Se eliminaron totalmente los porcentajes (+35%, 70%) y los cálculos de margen/ganancia.
    """
    agua: str = Field(..., description="Evaluación del cuidado del agua en lenguaje llano")
    nutrientes: str = Field(..., description="Aporte nutricional y materia orgánica")
    erosion: str = Field(..., description="Protección del suelo frente a viento y lluvias")
    salida_comercial: Optional[str] = Field(
        None,
        description="Salida del producto en mercado local/forraje (sin hablar de ganancias o rentas monetarias)"
    )


class StrategyOption(BaseModel):
    id: str
    nombre: str
    is_current: bool = False
    etiqueta: str = Field("Alternativa", description="Etiqueta visual: 'Tu situación actual', 'Recomendada', 'Doble propósito'")
    salud_suelo: str = Field(..., description="Nivel cualitativo: 'Saludable', 'Moderada', 'En riesgo'")
    salud_suelo_nivel: int = Field(..., ge=0, le=100, description="Nivel relativo para visualización (0 a 100)")
    resumen: str = Field(..., description="Explicación clara en lenguaje de campo")
    secuencia: List[SecuenciaItem] = Field(default_factory=list)
    metricas: MetricasCualitativas
    beneficios: List[str] = Field(default_factory=list)
    riesgos_locales: List[str] = Field(default_factory=list)
    evidencia_nasa: str = Field(..., description="Hallazgo de satélites NASA para la zona")

    # Campos retrocompatibles para Swagger y clientes existentes
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
    zona: ZonaSanLuis = Field(..., description="Zona evaluada de San Luis: norte, centro o sur")
    tierra_nombre: Optional[str] = None
    recomendacion: str = Field(..., description="Nombre de la estrategia más recomendada")
    estrategias: List[StrategyOption] = Field(..., description="Lista de estrategias comparadas")
    data_gaps: List[str] = Field(
        default_factory=lambda: [
            "Estimaciones basadas en satélites NASA POWER y modelos regionales (resolución ~50 km).",
            "No mide humedad a nivel de surco individual; validar con asesor agronómico local antes de sembrar."
        ],
        description="Limitaciones honestas del dato satelital explicadas de forma simple"
    )

    # Campos retrocompatibles
    @property
    def recommendation(self) -> str:
        return self.recomendacion

    @property
    def strategies(self) -> List[StrategyOption]:
        return self.estrategias
