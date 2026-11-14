from typing import List, Optional
from pydantic import BaseModel, Field


# =============================================================================
# 1. Clases de filas crudas de los Datasets (power_monthly.csv y power_daily.csv)
# =============================================================================
class PowerMonthlyRow(BaseModel):
    """Representa una fila individual del archivo 'power_monthly.csv' (312 meses)."""
    year_month: str = Field(..., description="Año y mes en formato YYYY-MM (ej. '2000-01')")
    year: Optional[int] = None
    month: Optional[int] = None
    temp_mean_c: float = Field(..., description="Temperatura media del mes (°C)")
    temp_max_c: Optional[float] = None
    temp_min_c: Optional[float] = None
    precip_mm_sum: float = Field(..., description="Precipitación acumulada del mes (mm)")
    frost_days: int = Field(..., description="Cantidad de días con helada (temp <= 0 °C)")
    heat_days_35: int = Field(..., description="Cantidad de días de calor extremo (temp >= 35 °C)")
    soil_wet_root_mean: Optional[float] = None
    evap_land_mm_sum: Optional[float] = None
    total_days: int = Field(..., description="Días medidos en el mes")


class PowerDailyRow(BaseModel):
    """Representa una fila individual del archivo 'power_daily.csv' (9497 días)."""
    date: int | str
    temp_mean_c: float
    temp_max_c: float
    temp_min_c: float
    precip_mm: float
    rh_pct: float
    solar_kwh_m2: float
    soil_wet_surface: float
    soil_wet_root: float
    evap_land_mm: float


# =============================================================================
# 2. Clases de Entrada (Lo que envía el formulario del Frontend en el POST)
# =============================================================================
class Coordinates(BaseModel):
    """Coordenadas seleccionadas en el mapa."""
    lat: float = Field(..., example=-33.675)
    lng: float = Field(..., example=-65.457)


class SimulationPriorities(BaseModel):
    """Checkboxes de prioridades seleccionados por el agricultor."""
    water: bool = Field(default=True, description="Prioridad: Cuidar agua")
    nutrients: bool = Field(default=True, description="Prioridad: Recuperar nutrientes")
    erosion: bool = Field(default=True, description="Prioridad: Frenar erosión")
    forageProfit: bool = Field(default=False, description="Prioridad: Sumar forraje / renta")


class SimulationRequest(BaseModel):
    """Payload JSON que envía el formulario ConfigForm.jsx al simular."""
    coords: Coordinates
    currentCrop: str = Field(..., example="Soja", description="Cultivo que viene sembrando el productor")
    irrigation: str = Field(default="lluvia", example="lluvia", description="Régimen de agua: 'lluvia' o 'riego'")
    priorities: SimulationPriorities
    lotName: Optional[str] = Field(default="Establecimiento Don Pedro - San Luis", description="Nombre del lote")


# =============================================================================
# 3. Clases de Salida (Lo que espera recibir DecisionBoard.jsx en el Frontend)
# =============================================================================
class LoteInfo(BaseModel):
    """Datos del lote evaluado."""
    nombre: str
    lat: float
    lon: float
    hectareas: int = Field(default=120)


class SecuenciaItem(BaseModel):
    """Tramo del calendario anual (mes de inicio a fin) para un cultivo o cobertura."""
    cultivo: str
    tipo: str = Field(..., description="'cultivo' o 'cobertura'")
    desde: int = Field(..., ge=1, le=12, description="Mes de inicio (1=Ene, 12=Dic)")
    hasta: int = Field(..., ge=1, le=12, description="Mes de fin (1=Ene, 12=Dic)")


class MetricasEstrategia(BaseModel):
    """Barras de comparación (escala 0 a 100) para cada estrategia."""
    agua: int = Field(..., ge=0, le=100)
    nutrientes: int = Field(..., ge=0, le=100)
    erosion: int = Field(..., ge=0, le=100)
    margen: int = Field(..., ge=0, le=100)


class EstrategiaItem(BaseModel):
    """Representa una tarjeta de estrategia de rotación en el comparador."""
    id: str = Field(..., example="actual")
    nombre: str = Field(..., example="Actual (Monocultivo)")
    is_current: bool = Field(..., description="True si es la situación actual del agricultor")
    salud_suelo: int = Field(..., ge=0, le=100, description="Valor de 0 a 100 para el medidor semicircular")
    resumen: str
    secuencia: List[SecuenciaItem]
    metricas: MetricasEstrategia
    riesgos: List[str]


class EvidenciaNasaItem(BaseModel):
    """Representa una tarjeta de evidencia satelital NASA."""
    satelite: str = Field(..., example="NASA POWER")
    titulo: str
    nivel: str = Field(..., example="azul", description="'azul' o 'rojo'")
    texto: str
    dato: str


class SimulationResponse(BaseModel):
    """Respuesta completa del endpoint POST /api/simulation."""
    lote: LoteInfo
    estrategias: List[EstrategiaItem]
    evidencia_nasa: List[EvidenciaNasaItem]
