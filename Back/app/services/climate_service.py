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
    Servicio de negocio para la simulación agronómica y evaluación de reglas regionales.
    Cruza los datasets climáticos ('power_monthly.csv' y 'power_daily.csv')
    con el dataset de cultivos ('crops.yaml'), las reglas de la Región ('norte', 'centro', 'sur')
    y las condiciones del lote del agricultor para generar las 3 estrategias y la evidencia NASA.
    """

    def __init__(self, repository: ClimateRepository | None = None):
        self.repository = repository or ClimateRepository()

    def simulate(self, request: SimulationRequest) -> SimulationResponse:
        # 1. Cargar los datasets desde el Repository y la info + reglas de la Región seleccionada
        monthly_df = self.repository.get_monthly_dataframe()
        daily_df = self.repository.get_daily_dataframe()
        crops_catalog = self.repository.get_crops_catalog()
        region_info = RegionRepository.get_region_by_id(request.region)

        # 2. Extraer indicadores reales de los datasets climáticos ajustados por la región (Norte, Centro o Sur)
        climate_stats = self._compute_climate_indicators(monthly_df, daily_df, request.region, region_info)

        # 3. Identificar el cultivo actual en el catálogo (crops.yaml)
        current_key = CROP_KEY_ALIAS.get(request.currentCrop.strip().lower(), "soja")
        current_crop_info = crops_catalog.get(current_key, crops_catalog["soja"])

        # 4. Construir las 3 estrategias cruzando crops.yaml + reglas regionales + prioridades del usuario
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
                region=request.region.value,
                amenaza_regional=region_info.amenaza_principal if region_info else None,
            ),
            estrategias=[
                estrategia_actual,
                estrategia_regenerativa,
                estrategia_forraje,
            ],
            evidencia_nasa=evidencia_nasa,
            reglas_regionales=region_info.reglas_activas if (region_info and region_info.reglas_activas) else [],
        )

    # =========================================================================
    # Motor de Reglas por Región (Norte, Centro y Sur)
    # =========================================================================

    def _is_zonal_condition_active(self, request: SimulationRequest) -> bool:
        """Determina si la condición crítica del campo en esa zona está activa."""
        if request.zonalConditions:
            if request.region == RegionSanLuis.NORTE and request.zonalConditions.altasTemperaturasSecano is not None:
                return request.zonalConditions.altasTemperaturasSecano
            if request.region == RegionSanLuis.CENTRO and request.zonalConditions.riesgoNapasOErosionHidrica is not None:
                return request.zonalConditions.riesgoNapasOErosionHidrica
            if request.region == RegionSanLuis.SUR and request.zonalConditions.sueloArenosoVoladura is not None:
                return request.zonalConditions.sueloArenosoVoladura
        return True if request.fieldCondition is None else bool(request.fieldCondition)

    def _apply_regional_rules(
        self,
        region: RegionSanLuis,
        agua: int,
        nutrientes: int,
        erosion: int,
        margen: int,
        avg_water_mm: float,
        avg_drought_tol: float,
        has_cover_crop: bool,
        has_n_fixer: bool,
        is_monoculture: bool,
        strategy_type: str,
        request: SimulationRequest,
        climate_stats: Dict[str, Any],
    ) -> Tuple[int, int, int, int, List[str], List[str]]:
        """
        Aplica las reglas agronómicas específicas de cada región (N1-N3, C1-C3, S1-S3)
        y devuelve (agua, nutrientes, erosion, margen, riesgos_especificos, reglas_aplicadas).
        """
        riesgos: List[str] = []
        reglas_aplicadas: List[str] = []
        condicion_activa = self._is_zonal_condition_active(request)

        # ---------------------------------------------------------------------
        # REGLAS REGIÓN NORTE (520 mm/año · 34 días >35 °C · Alta evaporación)
        # ---------------------------------------------------------------------
        if region == RegionSanLuis.NORTE:
            # Regla N1: Déficit hídrico crítico estival
            if request.irrigation == "lluvia" and avg_water_mm >= 440:
                penal_n1 = 18 if is_monoculture else 8
                if condicion_activa:
                    penal_n1 += 5
                agua = max(15, agua - penal_n1)
                reglas_aplicadas.append("Regla N1 (Déficit hídrico estival)")
                if is_monoculture:
                    riesgos.append(
                        f"Regla N1: Déficit hídrico severo en floración ({int(avg_water_mm)} mm demandados vs 520 mm/año en secano)"
                    )

            # Regla N2: Golpe de calor reproductivo (34 días >35 °C)
            if avg_drought_tol >= 0.75:
                agua = min(96, agua + 12)
                margen = min(94, margen + 10)
                reglas_aplicadas.append("Regla N2 (Resiliencia térmica >35 °C)")
            elif is_monoculture:
                margen = max(25, margen - (12 if condicion_activa else 6))
                reglas_aplicadas.append("Regla N2 (Vulnerabilidad a golpe de calor)")
                riesgos.append(
                    f"Regla N2: {int(climate_stats['annual_heat_days'])} días/año >35 °C provocan aborto floral sin rotación rústica"
                )

            # Regla N3: Escudo contra evaporación directa
            if has_cover_crop:
                agua = min(96, agua + (15 if condicion_activa else 10))
                erosion = min(96, erosion + 12)
                reglas_aplicadas.append("Regla N3 (Escudo anti-evaporación con cobertura)")
                riesgos.append(
                    "Regla N3: Secar la cobertura temprano en septiembre para reservar agua útil al cultivo estival"
                )
            else:
                erosion = max(18, erosion - 12)
                riesgos.append(
                    f"Regla N3: Alta pérdida por evaporación directa ({climate_stats['annual_evap_mm']} mm/año) en barbecho descubierto"
                )

        # ---------------------------------------------------------------------
        # REGLAS REGIÓN CENTRO (680 mm/año · Tormentas estivales · Napas/Cuenca)
        # ---------------------------------------------------------------------
        elif region == RegionSanLuis.CENTRO:
            # Regla C1: Control hidrológico y de napas con raíces vivas
            if is_monoculture:
                penal_c1 = 24 if condicion_activa else 15
                erosion = max(18, erosion - penal_c1)
                reglas_aplicadas.append("Regla C1 (Alerta de escurrimiento y ascenso de napa)")
                riesgos.append(
                    "Regla C1: Suelo sin raíces activas en invierno agrava el escurrimiento y el ascenso de napa freática (Cuenca del Morro)"
                )
            elif has_cover_crop:
                erosion = min(96, erosion + (18 if condicion_activa else 12))
                agua = min(95, agua + 10)
                reglas_aplicadas.append("Regla C1 (Consumo de excedentes hídricos con raíces vivas)")
                riesgos.append(
                    "Regla C1: Monitorear humedad en primavera para regular el consumo de la cobertura viva"
                )

            # Regla C2: Sinergia Gramínea + Leguminosa
            if not is_monoculture and has_n_fixer:
                nutrientes = min(96, nutrientes + 16)
                reglas_aplicadas.append("Regla C2 (Sinergia Gramínea + Leguminosa)")

            # Regla C3: Degradación estructural por monocultivo continuo
            if is_monoculture:
                nutrientes = max(20, nutrientes - 18)
                agua = max(22, agua - 12)
                reglas_aplicadas.append("Regla C3 (Degradación estructural y planchado)")
                riesgos.append(
                    "Regla C3: Pérdida de materia orgánica y compactación superficial ante lluvias intensas de verano"
                )

        # ---------------------------------------------------------------------
        # REGLAS REGIÓN SUR (610 mm/año · Suelos medanosos · 24 heladas · Viento)
        # ---------------------------------------------------------------------
        elif region == RegionSanLuis.SUR:
            # Regla S1: Alerta crítica de voladura de médanos (Erosión eólica)
            if is_monoculture:
                penal_s1 = 36 if condicion_activa else 25
                erosion = max(12, erosion - penal_s1)
                reglas_aplicadas.append("Regla S1 (Peligro crítico de voladura de médanos)")
                riesgos.append(
                    "Regla S1: Riesgo crítico de voladura de suelos arenosos por vientos fuertes de agosto a octubre"
                )
            elif has_cover_crop:
                erosion = min(96, erosion + (20 if condicion_activa else 14))
                reglas_aplicadas.append("Regla S1 (Anclaje de médanos con raíces invernales)")

            # Regla S2: Ventana de heladas tardías y tempranas (24 días/año)
            reglas_aplicadas.append("Regla S2 (Ventana de 24 heladas/año)")
            if is_monoculture:
                riesgos.append(
                    f"Regla S2: Alta exposición a {int(climate_stats['annual_frost_days'])} días de heladas/año y baja retención de humedad en arena"
                )
            elif strategy_type == "regenerativa":
                riesgos.append(
                    f"Regla S2: Ajustar fecha de siembra estival para escapar a las {int(climate_stats['annual_frost_days'])} heladas anuales del Sur"
                )

            # Regla S3: Fijación de perfil arenoso y aptitud mixta/forrajera
            if strategy_type == "forraje":
                agua = min(95, agua + 12)
                margen = min(94, margen + (14 if condicion_activa else 8))
                reglas_aplicadas.append("Regla S3 (Aptitud mixta forrajera en suelo arenoso)")
                riesgos.append(
                    "Regla S3: Retirar hacienda a tiempo para dejar remanente vegetal que proteja el suelo arenoso del viento"
                )

        # Riesgos complementarios si la lista quedó con menos de 2 ítems
        if strategy_type == "regenerativa" and len(riesgos) < 2:
            riesgos.append("Inversión inicial en semilla de cobertura compensada por menor gasto en fertilización nitrogenada")
        elif strategy_type == "forraje" and len(riesgos) < 2:
            riesgos.append("Controlar carga animal en pastoreo directo para evitar compactación superficial")

        return agua, nutrientes, erosion, margen, riesgos[:3], reglas_aplicadas

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
        strategy_type: str,
        climate_stats: Dict[str, Any],
        request: SimulationRequest,
    ) -> Tuple[int, MetricasEstrategia, List[str], List[str]]:
        """
        Calcula las 4 barras (agua, nutrientes, erosion, margen), salud_suelo y riesgos regionales
        a partir de los rasgos en crops.yaml y el motor de reglas por región (Norte, Centro, Sur).
        """
        n = max(len(crops_in_rotation), 1)

        # Rasgos promediados desde crops.yaml
        avg_drought_tol = sum(float(c.get("drought_tolerance", 0.5)) for c in crops_in_rotation) / n
        avg_water_mm = sum(float(c.get("water_consumption", 400)) for c in crops_in_rotation) / n
        avg_coverage = sum(float(c.get("soil_coverage", 0.7)) for c in crops_in_rotation) / n
        avg_om = sum(float(c.get("organic_matter", 0.04)) for c in crops_in_rotation) / n
        avg_root_cm = sum(float(c.get("root_depth", 120)) for c in crops_in_rotation) / n
        has_n_fixer = any(bool(c.get("nitrogen_fixation", False)) for c in crops_in_rotation)

        # 1. Base AGUA (0-100)
        water_ratio = min(
            1.0, max(0.15, 1.0 - (avg_water_mm - 180.0) / max(climate_stats["annual_rain_mm"], 420.0))
        )
        agua = int(round((0.50 * avg_drought_tol + 0.50 * water_ratio) * 100))
        if request.irrigation == "riego":
            agua = min(95, agua + 15)
        if is_monoculture:
            agua = max(20, agua - 16)
        elif has_cover_crop:
            agua = min(95, agua + 10)

        # 2. Base NUTRIENTES (0-100)
        om_norm = min(1.0, avg_om / 0.07)
        root_norm = min(1.0, avg_root_cm / 200.0)
        nutrientes = int(round((0.45 * om_norm + 0.30 * root_norm + (0.25 if has_n_fixer else 0.0)) * 100))
        if is_monoculture:
            nutrientes = max(22, nutrientes - 18)
        elif has_cover_crop and has_n_fixer:
            nutrientes = min(95, nutrientes + 12)

        # 3. Base EROSIÓN (0-100)
        erosion = int(round(avg_coverage * 75 + (20 if has_cover_crop else 0)))
        if is_monoculture:
            erosion = max(20, erosion - 18)

        # 4. Base MARGEN (0-100)
        market_scores = [
            MARKET_SCORE_MAP.get(str(c.get("market_potential", "medio")).lower(), 65)
            for c in crops_in_rotation
        ]
        margen = int(round(sum(market_scores) / n))
        if has_cover_crop and len(crops_in_rotation) >= 2:
            margen = max(58, min(84, margen))

        # 5. Ejecutar Motor de Reglas Regionales (Norte, Centro, Sur)
        agua, nutrientes, erosion, margen, riesgos_reg, reglas_aplicadas = self._apply_regional_rules(
            region=request.region,
            agua=agua,
            nutrientes=nutrientes,
            erosion=erosion,
            margen=margen,
            avg_water_mm=avg_water_mm,
            avg_drought_tol=avg_drought_tol,
            has_cover_crop=has_cover_crop,
            has_n_fixer=has_n_fixer,
            is_monoculture=is_monoculture,
            strategy_type=strategy_type,
            request=request,
            climate_stats=climate_stats,
        )

        # 6. Ajuste por prioridades seleccionadas y cálculo de Salud Global del Suelo
        p = request.priorities
        if not is_monoculture:
            if p.water:
                agua = min(96, agua + 5)
            if p.nutrients:
                nutrientes = min(96, nutrientes + 5)
            if p.erosion:
                erosion = min(96, erosion + 5)
            if p.forageProfit:
                margen = min(95, margen + 6)
        else:
            if p.water:
                agua = max(14, agua - 4)
            if p.nutrients:
                nutrientes = max(16, nutrientes - 4)
            if p.erosion:
                erosion = max(12, erosion - 4)

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
            riesgos_reg,
            reglas_aplicadas,
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

        salud, metricas, riesgos, reglas = self._compute_strategy_metrics(
            crops_in_rotation=[crop_info],
            has_cover_crop=False,
            is_monoculture=True,
            strategy_type="actual",
            climate_stats=climate_stats,
            request=request,
        )

        return EstrategiaItem(
            id="actual",
            nombre=f"Actual ({crop_name} en monocultivo)",
            is_current=True,
            salud_suelo=salud,
            resumen=(
                f"{crop_name} continuo ({crop_info['water_consumption']} mm/ciclo) "
                f"en {climate_stats['region_name']} ({climate_stats['annual_rain_mm']} mm/año): "
                "deja el suelo desnudo durante el otoño e invierno."
            ),
            secuencia=[
                SecuenciaItem(cultivo=crop_name, tipo="cultivo", desde=desde, hasta=hasta)
            ],
            metricas=metricas,
            riesgos=riesgos,
            reglas_aplicadas=reglas,
        )

    def _build_regenerative_strategy(
        self,
        current_key: str,
        crops_catalog: Dict[str, Dict[str, Any]],
        climate_stats: Dict[str, Any],
        request: SimulationRequest,
    ) -> EstrategiaItem:
        # Selección inteligente según región y cultivo actual
        if request.region == RegionSanLuis.NORTE:
            regen_map = {
                "soja": ("sorgo", "arveja"),
                "maíz": ("soja", "arveja"),
                "trigo": ("sorgo", "arveja"),
                "girasol": ("soja", "arveja"),
                "sorgo": ("soja", "arveja"),
                "cebada": ("sorgo", "arveja"),
                "arveja": ("sorgo", "soja"),
            }
        elif request.region == RegionSanLuis.SUR:
            regen_map = {
                "soja": ("girasol", "cebada"),
                "maíz": ("soja", "cebada"),
                "trigo": ("girasol", "arveja"),
                "girasol": ("soja", "cebada"),
                "sorgo": ("soja", "cebada"),
                "cebada": ("girasol", "arveja"),
                "arveja": ("girasol", "cebada"),
            }
        else:  # CENTRO
            regen_map = {
                "soja": ("maíz", "arveja"),
                "maíz": ("soja", "trigo"),
                "trigo": ("soja", "arveja"),
                "girasol": ("maíz", "arveja"),
                "sorgo": ("soja", "arveja"),
                "cebada": ("soja", "arveja"),
                "arveja": ("maíz", "trigo"),
            }

        main_crop_key, cover_crop_key = regen_map.get(current_key, ("maíz", "arveja"))
        main_crop = crops_catalog[main_crop_key]
        cover_crop = crops_catalog[cover_crop_key]
        current_crop = crops_catalog.get(current_key, crops_catalog["soja"])

        salud, metricas, riesgos, reglas = self._compute_strategy_metrics(
            crops_in_rotation=[main_crop, cover_crop, current_crop],
            has_cover_crop=True,
            is_monoculture=False,
            strategy_type="regenerativa",
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
                f"Rotación calibrada para {climate_stats['region_name']} con {main_crop['name']} + "
                f"{cover_crop['name']} (cobertura): protege el suelo todo el año y mejora el balance hídrico."
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
            riesgos=riesgos,
            reglas_aplicadas=reglas,
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
            "sorgo": ("girasol", "cebada"),
            "cebada": ("sorgo", "arveja"),
            "arveja": ("sorgo", "cebada"),
        }
        summer_key, winter_key = forage_map.get(current_key, ("sorgo", "cebada"))
        summer_crop = crops_catalog[summer_key]
        winter_crop = crops_catalog[winter_key]
        current_crop = crops_catalog.get(current_key, crops_catalog["soja"])

        salud, metricas, riesgos, reglas = self._compute_strategy_metrics(
            crops_in_rotation=[summer_crop, winter_crop, current_crop],
            has_cover_crop=True,
            is_monoculture=False,
            strategy_type="forraje",
            climate_stats=climate_stats,
            request=request,
        )

        if request.priorities.forageProfit:
            metricas.margen = min(94, metricas.margen + 10)
            salud = min(95, salud + 5)

        s_desde, s_hasta = CROP_CALENDAR.get(summer_key, (11, 3))
        w_desde, w_hasta = CROP_CALENDAR.get(winter_key, (5, 10))

        return EstrategiaItem(
            id="forraje",
            nombre="Forraje / Renta Resiliente",
            is_current=False,
            salud_suelo=salud,
            resumen=(
                f"{summer_crop['name']} ({summer_crop['water_consumption']} mm, alta rusticidad) + "
                f"{winter_crop['name']} invernal: ancla el suelo con raíces de {summer_crop['root_depth']} cm y suma forraje."
            ),
            secuencia=[
                SecuenciaItem(cultivo=f"{summer_crop['name']} (doble propósito)", tipo="cultivo", desde=s_desde, hasta=s_hasta),
                SecuenciaItem(cultivo=f"{winter_crop['name']} (verdeo)", tipo="cultivo", desde=w_desde, hasta=w_hasta),
            ],
            metricas=metricas,
            riesgos=riesgos,
            reglas_aplicadas=reglas,
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
