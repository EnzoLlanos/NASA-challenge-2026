from typing import List
from pydantic import BaseModel, Field


class PowerMonthlyRow(BaseModel):
    """
    Representa una fila individual del archivo 'power_monthly.csv'.
    Es el reflejo directo de los datos históricos mensuales que procesó el equipo de datos.
    """
    year_month: str = Field(..., description="Año y mes en formato YYYY-MM (ej. '2000-01')")
    temp_mean_c: float = Field(..., description="Temperatura media del mes (°C)")
    precip_mm_sum: float = Field(..., description="Precipitación acumulada del mes (mm)")
    frost_days: int = Field(..., description="Cantidad de días con helada (temp <= 0 °C)")
    heat_days_35: int = Field(..., description="Cantidad de días de calor extremo (temp >= 35 °C)")
    total_days: int = Field(..., description="Días medidos en el mes")


class LocationInfo(BaseModel):
    """
    Representa las coordenadas y el nombre de la ubicación del lote que se muestra en el mapa.
    """
    name: str = Field(..., example="San Luis, Argentina (Campo Piloto)")
    lat: float = Field(..., example=-33.30)
    lon: float = Field(..., example=-65.30)


class ClimateKPIs(BaseModel):
    """
    Representa las tarjetas principales de métricas anuales (KPIs) en la parte superior del Dashboard:
    lluvia promedio anual, días de helada al año, días de calor extremo y temperatura media.
    """
    annual_rain_mm: float = Field(..., example=771.2)
    annual_frost_days: float = Field(..., example=14.8)
    annual_heat_days_35: float = Field(..., example=26.3)
    avg_temp_c: float = Field(..., example=17.0)


class MonthlyClimatologyItem(BaseModel):
    """
    Representa un punto en el gráfico anual (un mes de 1 a 12).
    Contiene los promedios históricos de lluvia, temperatura, heladas y calor para dibujar
    las barras y curvas en Recharts / Chart.js.
    """
    month: int = Field(..., ge=1, le=12, example=1)
    month_name: str = Field(..., example="Enero")
    temp_mean_c: float = Field(..., example=24.3)
    precip_mm: float = Field(..., example=133.7)
    frost_days: float = Field(..., example=0.0)
    heat_days_35: float = Field(..., example=8.1)


class FieldProfileResponse(BaseModel):
    """
    Representa la respuesta completa que devuelve el endpoint GET /api/field-profile.
    Es el contrato final que consume la pantalla principal del Frontend con todos sus componentes.
    """
    location: LocationInfo
    period: str = Field(..., example="2000 - 2025 (26 años)")
    kpis: ClimateKPIs
    monthly_climatology: List[MonthlyClimatologyItem]
    dry_season_months: List[str]
    risk_alerts: List[str]
    data_gaps: List[str]
