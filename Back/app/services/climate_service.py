from typing import Dict, Any, List, Tuple
import pandas as pd
from app.repositories.climate_repository import ClimateRepository
from app.repositories.region_repository import RegionRepository
from app.schemas.region import RegionSanLuis
from app.schemas.simulation import (
    SimulationRequest,
    SimulationResponse,
    LoteInfo,
    EstrategiaItem,
    SecuenciaItem,
    MetricasEstrategia,
    EvidenciaNasaItem,
)

# Ventanas de calendario (mes inicio, mes fin) según ciclo de cultivo en San Luis
CROP_CALENDAR = {
    "soja": (11, 4),      # Noviembre a Abril
    "maíz": (10, 3),      # Octubre a Marzo
    "girasol": (11, 3),   # Noviembre a Marzo
    "sorgo": (11, 3),     # Noviembre a Marzo
    "trigo": (5, 11),     # Mayo a Noviembre
    "cebada": (5, 10),    # Mayo a Octubre
    "arveja": (4, 9),     # Abril a Septiembre (cobertura invernal)
}

MARKET_SCORE_MAP = {
    "alto": 82,
    "medio": 65,
    "bajo": 42,
}

CROP_KEY_ALIAS = {
    "maiz": "maíz",
    "maíz": "maíz",
    "soja": "soja",
    "trigo": "trigo",
    "girasol": "girasol",
    "sorgo": "sorgo",
    "cebada": "cebada",
    "arveja": "arveja",
}

REGION_COORDS = {
    RegionSanLuis.NORTE: (-32.50, -65.80),
    RegionSanLuis.CENTRO: (-33.67, -65.45),
    RegionSanLuis.SUR: (-34.85, -65.50),
}


class ClimateService:
    """
    Servicio de negocio para la simulación agronómica.
    Cruza los datasets climáticos ('power_monthly.csv' y 'power_daily.csv')
    con el dataset de cultivos ('crops.yaml'), los datos de la Región ('norte', 'centro', 'sur')
    y las prioridades del agricultor para generar las 3 estrategias de rotación y la evidencia NASA.
    """

    def __init__(self, repository: ClimateRepository | None = None):
        self.repository = repository or ClimateRepository()

    def simulate(self, request: SimulationRequest) -> SimulationResponse:
        # 1. Cargar los datasets desde el Repository y la info de la Región seleccionada
        monthly_df = self.repository.get_monthly_dataframe()
        daily_df = self.repository.get_daily_dataframe()
        crops_catalog = self.repository.get_crops_catalog()
        region_info = RegionRepository.get_region_by_id(request.region)

        # 2. Extraer indicadores reales de los datasets climáticos ajustados por la región (Norte, Centro o Sur)
        climate_stats = self._compute_climate_indicators(monthly_df, daily_df, request.region, region_info)

        # 3. Identificar el cultivo actual en el catálogo (crops.yaml)
        current_key = CROP_KEY_ALIAS.get(request.currentCrop.strip().lower(), "soja")
        current_crop_info = crops_catalog.get(current_key, crops_catalog["soja"])

        # 4. Construir las 3 estrategias cruzando crops.yaml + clima regional + prioridades del usuario
        estrategia_actual = self._build_current_strategy(
            current_key, current_crop_info, climate_stats, request
        )
        estrategia_regenerativa = self._build_regenerative_strategy(
            current_key, crops_catalog, climate_stats, request
        )
        estrategia_forraje = self._build_forage_strategy(
            current_key, crops_catalog, climate_stats, request
        )

        # 5. Construir tarjetas de Evidencia NASA a partir de los datasets mensual, diario y región
        evidencia_nasa = self._build_nasa_evidence(climate_stats, current_crop_info["name"])

        default_lat, default_lon = REGION_COORDS.get(request.region, (-33.67, -65.45))
        lat = request.coords.lat if request.coords else default_lat
        lon = request.coords.lng if request.coords else default_lon
        region_label = region_info.nombre if region_info else f"Región {request.region.value.capitalize()}"
        lote_nombre = (
            f"{request.lotName} ({region_label})"
            if request.lotName
            else f"Establecimiento Don Pedro – {region_label}"
        )

        return SimulationResponse(
            lote=LoteInfo(
                nombre=lote_nombre,
                lat=lat,
                lon=lon,
                hectareas=120,
            ),
            estrategias=[
                estrategia_actual,
                estrategia_regenerativa,
                estrategia_forraje,
            ],
            evidencia_nasa=evidencia_nasa,
        )

    # =========================================================================
    # Métodos privados: Procesamiento de Datasets Climáticos y de Cultivos
    # =========================================================================

    def _compute_climate_indicators(
        self,
        monthly_df: pd.DataFrame,
        daily_df: pd.DataFrame,
        region: RegionSanLuis,
        region_info: Any,
    ) -> Dict[str, Any]:
        """Calcula indicadores combinando power_monthly.csv, power_daily.csv y los datos de la Región."""
        if "month" not in monthly_df.columns:
            monthly_df["month"] = monthly_df["year_month"].apply(lambda ym: int(ym.split("-")[1]))

        total_years = max(len(monthly_df) / 12.0, 1.0)
        base_rain_mm = float(monthly_df["precip_mm_sum"].sum() / total_years)
        base_evap_mm = (
            float(monthly_df["evap_land_mm_sum"].sum() / total_years)
            if "evap_land_mm_sum" in monthly_df.columns
            else 680.0
        )
        base_heat_days = float(monthly_df["heat_days_35"].sum() / total_years)
        base_frost_days = float(monthly_df["frost_days"].sum() / total_years)

        # Ajustar con los parámetros regionales de San Luis (Norte, Centro, Sur)
        if region_info:
            annual_rain_mm = round(float(region_info.precipitacion_media_anual_mm), 1)
            annual_heat_days = float(region_info.dias_calor_extremo_anual)
            annual_frost_days = float(region_info.dias_heladas_anual)
        else:
            annual_rain_mm = round(base_rain_mm, 1)
            annual_heat_days = round(base_heat_days, 1)
            annual_frost_days = round(base_frost_days, 1)

        # Evaporación y meses secos según aridez regional
        evap_multiplier = 1.12 if region == RegionSanLuis.NORTE else (0.95 if region == RegionSanLuis.SUR else 1.0)
        annual_evap_mm = round(base_evap_mm * evap_multiplier, 1)

        # Porcentaje de lluvia concentrada entre noviembre y marzo
        summer_rain = monthly_df[monthly_df["month"].isin([11, 12, 1, 2, 3])]["precip_mm_sum"].sum()
        total_rain = monthly_df["precip_mm_sum"].sum()
        pct_summer_rain = int(round((summer_rain / max(total_rain, 1.0)) * 100))

        # Meses secos en invierno (< 25 mm promedio)
        monthly_avg_rain = monthly_df.groupby("month")["precip_mm_sum"].mean()
        base_dry_months = int((monthly_avg_rain < 25.0).sum())
        dry_months_count = base_dry_months + (1 if region == RegionSanLuis.NORTE else 0)

        # --- De power_daily.csv (9,497 días) ---
        daily_months = (daily_df["date"].astype(int) // 100) % 100
        winter_spring_mask = daily_months.isin([7, 8, 9, 10])
        summer_mask = daily_months.isin([12, 1, 2, 3])

        soil_surface_mean = float(daily_df["soil_wet_surface"].mean())
        soil_surface_dry_season = float(daily_df.loc[winter_spring_mask, "soil_wet_surface"].mean())

        moisture_factor = 0.85 if region == RegionSanLuis.NORTE else (0.92 if region == RegionSanLuis.SUR else 1.0)
        regional_soil_mean = round(soil_surface_mean * moisture_factor, 2)

        base_drop_pct = int(
            round(((soil_surface_mean - soil_surface_dry_season) / max(soil_surface_mean, 0.01)) * 100)
        )
        base_drop_pct = max(base_drop_pct, 12)
        soil_moisture_drop_pct = (
            base_drop_pct + 6
            if region == RegionSanLuis.NORTE
            else (base_drop_pct + 3 if region == RegionSanLuis.SUR else base_drop_pct)
        )

        avg_solar_summer = round(float(daily_df.loc[summer_mask, "solar_kwh_m2"].mean()) * evap_multiplier, 1)

        return {
            "region": region.value,
            "region_name": region_info.nombre if region_info else f"Región {region.value.capitalize()}",
            "annual_rain_mm": annual_rain_mm,
            "annual_evap_mm": annual_evap_mm,
            "annual_heat_days": annual_heat_days,
            "annual_frost_days": annual_frost_days,
            "pct_summer_rain": pct_summer_rain,
            "dry_months_count": dry_months_count,
            "soil_surface_mean": regional_soil_mean,
            "soil_moisture_drop_pct": soil_moisture_drop_pct,
            "avg_solar_summer": avg_solar_summer,
        }

    def _compute_strategy_metrics(
        self,
        crops_in_rotation: List[Dict[str, Any]],
        has_cover_crop: bool,
        is_monoculture: bool,
        climate_stats: Dict[str, Any],
        request: SimulationRequest,
    ) -> Tuple[int, MetricasEstrategia]:
        """
        Calcula las 4 barras (agua, nutrientes, erosion, margen) y el indicador salud_suelo
        en escala 0-100 a partir de los rasgos reales en crops.yaml y el régimen hídrico regional.
        """
        n = max(len(crops_in_rotation), 1)

        # Rasgos promediados desde crops.yaml
        avg_drought_tol = sum(float(c.get("drought_tolerance", 0.5)) for c in crops_in_rotation) / n
        avg_water_mm = sum(float(c.get("water_consumption", 400)) for c in crops_in_rotation) / n
        avg_coverage = sum(float(c.get("soil_coverage", 0.7)) for c in crops_in_rotation) / n
        avg_om = sum(float(c.get("organic_matter", 0.04)) for c in crops_in_rotation) / n
        avg_root_cm = sum(float(c.get("root_depth", 120)) for c in crops_in_rotation) / n
        has_n_fixer = any(bool(c.get("nitrogen_fixation", False)) for c in crops_in_rotation)

        # 1. Métrica AGUA (0-100) sensible a la lluvia regional (520mm Norte, 680mm Centro, 610mm Sur)
        water_ratio = min(
            1.0, max(0.15, 1.0 - (avg_water_mm - 180.0) / max(climate_stats["annual_rain_mm"], 420.0))
        )
        agua = int(round((0.50 * avg_drought_tol + 0.50 * water_ratio) * 100))
        if request.region == RegionSanLuis.NORTE and avg_water_mm >= 450 and request.irrigation == "lluvia":
            agua = max(18, agua - 8)
        if request.irrigation == "riego":
            agua = min(95, agua + 14)
        if is_monoculture:
            agua = max(20, agua - 22)
        elif has_cover_crop:
            agua = min(95, agua + 14)

        # 2. Métrica NUTRIENTES (0-100)
        om_norm = min(1.0, avg_om / 0.07)
        root_norm = min(1.0, avg_root_cm / 200.0)
        nutrientes = int(round((0.45 * om_norm + 0.30 * root_norm + (0.25 if has_n_fixer else 0.0)) * 100))
        if is_monoculture:
            nutrientes = max(22, nutrientes - 25)
        elif has_cover_crop and has_n_fixer:
            nutrientes = min(95, nutrientes + 15)

        # 3. Métrica EROSIÓN (0-100, más = mayor protección contra erosión)
        erosion = int(round(avg_coverage * 75 + (22 if has_cover_crop else 0)))
        if request.region == RegionSanLuis.SUR and is_monoculture:
            # Suelos medanosos del Sur sufren mayor erosión eólica en barbecho desnudo
            erosion = max(14, erosion - 40)
        elif is_monoculture:
            erosion = max(20, erosion - 35)

        # 4. Métrica MARGEN (0-100)
        market_scores = [
            MARKET_SCORE_MAP.get(str(c.get("market_potential", "medio")).lower(), 65)
            for c in crops_in_rotation
        ]
        margen = int(round(sum(market_scores) / n))
        if has_cover_crop and len(crops_in_rotation) >= 2:
            margen = max(55, min(80, margen))

        # 5. Ajuste por prioridades seleccionadas y cálculo de Salud Global del Suelo
        p = request.priorities
        if not is_monoculture:
            if p.water:
                agua = min(96, agua + 6)
            if p.nutrients:
                nutrientes = min(96, nutrientes + 6)
            if p.erosion:
                erosion = min(96, erosion + 6)
            if p.forageProfit:
                margen = min(95, margen + 7)
        else:
            if p.water:
                agua = max(16, agua - 4)
            if p.nutrients:
                nutrientes = max(18, nutrientes - 4)
            if p.erosion:
                erosion = max(14, erosion - 4)

        w_agua = 1.6 if p.water else 0.7
        w_nut = 1.6 if p.nutrients else 0.7
        w_ero = 1.6 if p.erosion else 0.7
        w_mar = 1.5 if p.forageProfit else 0.7
        total_w = w_agua + w_nut + w_ero + w_mar

        salud_suelo = int(
            round((agua * w_agua + nutrientes * w_nut + erosion * w_ero + margen * w_mar) / total_w)
        )
        salud_suelo = max(15, min(98, salud_suelo))

        return (
            salud_suelo,
            MetricasEstrategia(agua=agua, nutrientes=nutrientes, erosion=erosion, margen=margen),
        )

    def _build_current_strategy(
        self,
        current_key: str,
        crop_info: Dict[str, Any],
        climate_stats: Dict[str, Any],
        request: SimulationRequest,
    ) -> EstrategiaItem:
        crop_name = crop_info["name"]
        desde, hasta = CROP_CALENDAR.get(current_key, (11, 4))

        salud, metricas = self._compute_strategy_metrics(
            crops_in_rotation=[crop_info],
            has_cover_crop=False,
            is_monoculture=True,
            climate_stats=climate_stats,
            request=request,
        )

        return EstrategiaItem(
            id="actual",
            nombre=f"Actual ({crop_name} en monocultivo)",
            is_current=True,
            salud_suelo=salud,
            resumen=(
                f"{crop_name} sobre {crop_name.lower()} ({crop_info['water_consumption']} mm/ciclo) "
                f"en {climate_stats['region_name']} ({climate_stats['annual_rain_mm']} mm/año): "
                "el suelo queda desnudo gran parte del año."
            ),
            secuencia=[
                SecuenciaItem(cultivo=crop_name, tipo="cultivo", desde=desde, hasta=hasta)
            ],
            metricas=metricas,
            riesgos=[
                "Pérdida de materia orgánica y estructura superficial",
                f"Erosión por viento en los {climate_stats['dry_months_count']} meses secos de invierno",
            ],
        )

    def _build_regenerative_strategy(
        self,
        current_key: str,
        crops_catalog: Dict[str, Dict[str, Any]],
        climate_stats: Dict[str, Any],
        request: SimulationRequest,
    ) -> EstrategiaItem:
        regen_map = {
            "soja": ("maíz", "arveja"),
            "maíz": ("soja", "trigo"),
            "trigo": ("soja", "arveja"),
            "girasol": ("trigo", "arveja"),
            "sorgo": ("soja", "arveja"),
            "cebada": ("soja", "arveja"),
            "arveja": ("maíz", "trigo"),
        }
        main_crop_key, cover_crop_key = regen_map.get(current_key, ("maíz", "arveja"))
        main_crop = crops_catalog[main_crop_key]
        cover_crop = crops_catalog[cover_crop_key]
        current_crop = crops_catalog.get(current_key, crops_catalog["soja"])

        salud, metricas = self._compute_strategy_metrics(
            crops_in_rotation=[main_crop, cover_crop, current_crop],
            has_cover_crop=True,
            is_monoculture=False,
            climate_stats=climate_stats,
            request=request,
        )

        main_desde, main_hasta = CROP_CALENDAR.get(main_crop_key, (10, 3))
        cov_desde, cov_hasta = CROP_CALENDAR.get(cover_crop_key, (4, 9))

        return EstrategiaItem(
            id="regenerativa",
            nombre="Regenerativa (Suelo y Agua)",
            is_current=False,
            salud_suelo=salud,
            resumen=(
                f"Rotación desde {current_crop['name']} hacia {main_crop['name']} + {cover_crop['name']} (cobertura): "
                "el suelo permanece cubierto casi todo el año y recupera fertilidad."
            ),
            secuencia=[
                SecuenciaItem(cultivo=main_crop["name"], tipo="cultivo", desde=main_desde, hasta=main_hasta),
                SecuenciaItem(
                    cultivo=f"{cover_crop['name']} (cobertura)",
                    tipo="cobertura",
                    desde=cov_desde,
                    hasta=cov_hasta,
                ),
            ],
            metricas=metricas,
            riesgos=[
                "Margen algo menor el primer año por costo de semilla de cobertura",
                "Requiere ajustar la fecha de secado de la cobertura con técnico local",
            ],
        )

    def _build_forage_strategy(
        self,
        current_key: str,
        crops_catalog: Dict[str, Dict[str, Any]],
        climate_stats: Dict[str, Any],
        request: SimulationRequest,
    ) -> EstrategiaItem:
        forage_map = {
            "soja": ("sorgo", "cebada"),
            "maíz": ("sorgo", "trigo"),
            "trigo": ("girasol", "cebada"),
            "girasol": ("sorgo", "cebada"),
            "sorgo": ("maíz", "cebada"),
            "cebada": ("sorgo", "arveja"),
            "arveja": ("sorgo", "cebada"),
        }
        summer_key, winter_key = forage_map.get(current_key, ("sorgo", "cebada"))
        summer_crop = crops_catalog[summer_key]
        winter_crop = crops_catalog[winter_key]
        current_crop = crops_catalog.get(current_key, crops_catalog["soja"])

        salud, metricas = self._compute_strategy_metrics(
            crops_in_rotation=[summer_crop, winter_crop, current_crop],
            has_cover_crop=True,
            is_monoculture=False,
            climate_stats=climate_stats,
            request=request,
        )

        if request.priorities.forageProfit:
            metricas.margen = min(92, metricas.margen + 12)
            salud = min(94, salud + 6)

        s_desde, s_hasta = CROP_CALENDAR.get(summer_key, (11, 3))
        w_desde, w_hasta = CROP_CALENDAR.get(winter_key, (5, 10))

        return EstrategiaItem(
            id="forraje",
            nombre="Forraje / Renta Resiliente",
            is_current=False,
            salud_suelo=salud,
            resumen=(
                f"{summer_crop['name']} ({summer_crop['water_consumption']} mm, alta tolerancia) + "
                f"{winter_crop['name']} de invierno: diversifica desde {current_crop['name']} con raíces de {summer_crop['root_depth']} cm."
            ),
            secuencia=[
                SecuenciaItem(cultivo=f"{summer_crop['name']} (doble propósito)", tipo="cultivo", desde=s_desde, hasta=s_hasta),
                SecuenciaItem(cultivo=f"{winter_crop['name']} (verdeo)", tipo="cultivo", desde=w_desde, hasta=w_hasta),
            ],
            metricas=metricas,
            riesgos=[
                "Depende de contar con hacienda o mercado zonal de forraje/grano",
                "Controlar carga animal para evitar compactación superficial",
            ],
        )

    def _build_nasa_evidence(
        self, climate_stats: Dict[str, Any], crop_name: str
    ) -> List[EvidenciaNasaItem]:
        """Construye las 3 tarjetas de evidencia NASA a partir de power_daily.csv, power_monthly.csv y la Región."""
        return [
            EvidenciaNasaItem(
                satelite="SMAP",
                titulo="Humedad del suelo",
                nivel="rojo",
                texto=(
                    f"En {climate_stats['region_name']}, la humedad superficial del suelo "
                    f"(promedio {climate_stats['soil_surface_mean']}) cae un {climate_stats['soil_moisture_drop_pct']}% "
                    "entre julio y octubre cuando el lote queda descubierto."
                ),
                dato=f"Humedad superficial {climate_stats['soil_moisture_drop_pct']}% más baja en invierno-primavera",
            ),
            EvidenciaNasaItem(
                satelite="ECOSTRESS",
                titulo="Estrés de las plantas y evaporación",
                nivel="rojo",
                texto=(
                    f"Se registran {int(climate_stats['annual_heat_days'])} días/año con más de 35 °C y "
                    f"{int(climate_stats['annual_frost_days'])} días de heladas. En monocultivo de {crop_name}, "
                    f"la evaporación anual ({climate_stats['annual_evap_mm']} mm) eleva la pérdida de agua."
                ),
                dato=f"{int(climate_stats['annual_heat_days'])} días/año >35 °C • {int(climate_stats['annual_frost_days'])} heladas/año",
            ),
            EvidenciaNasaItem(
                satelite="GPM",
                titulo="Lluvia",
                nivel="azul",
                texto=(
                    f"El {climate_stats['pct_summer_rain']}% de la lluvia regional ({climate_stats['annual_rain_mm']} mm/año) "
                    f"cae entre noviembre y marzo, mientras que {climate_stats['dry_months_count']} meses invernales "
                    "promedian menos de 25 mm: conviene cubrir el suelo para retener esa agua."
                ),
                dato=f"{climate_stats['pct_summer_rain']}% de la lluvia en 5 meses ({climate_stats['annual_rain_mm']} mm/año)",
            ),
        ]
