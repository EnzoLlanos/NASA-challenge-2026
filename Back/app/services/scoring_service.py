from typing import List, Dict, Tuple, Optional
from app.repositories.crop_repository import CropRepository
from app.repositories.region_repository import RegionRepository
from app.schemas.region import RegionSanLuis, Tierra
from app.schemas.rotation import Priorities, StrategyOption, RotationResponse


class ScoringService:
    """Motor de cálculo y puntuación inteligente de estrategias de rotación agrícola por región de San Luis."""

    @staticmethod
    def _normalize_priorities(priorities: Priorities) -> Dict[str, float]:
        total = priorities.agua + priorities.ingresos + priorities.suelo + priorities.erosion
        if total <= 0:
            return {"agua": 0.25, "ingresos": 0.25, "suelo": 0.25, "erosion": 0.25}
        return {
            "agua": priorities.agua / total,
            "ingresos": priorities.ingresos / total,
            "suelo": priorities.suelo / total,
            "erosion": priorities.erosion / total,
        }

    @staticmethod
    def evaluate_rotation_scores(
        crop_ids: List[str],
        region: RegionSanLuis = RegionSanLuis.CENTRO,
    ) -> Tuple[float, float, float, float]:
        """
        Calcula las 4 notas parciales (0 a 1) para una secuencia de cultivos según la región de San Luis:
        (nota_agua, nota_ingresos, nota_suelo, nota_erosion)
        """
        if not crop_ids:
            return 0.5, 0.5, 0.5, 0.5

        crops_data = []
        for cid in crop_ids:
            c = CropRepository.find_by_name_or_id(cid)
            if c:
                crops_data.append(c)

        if not crops_data:
            return 0.5, 0.5, 0.5, 0.5

        n = len(crops_data)

        # 1. Nota Agua: Promedio de tolerancia a sequía ajustado por consumo hídrico y aridez regional
        avg_drought_tol = sum(c["drought_tolerance"] for c in crops_data) / n
        avg_water_mm = sum(c["water_consumption_mm"] for c in crops_data) / n
        # En el Norte (520mm) la exigencia de bajo consumo hídrico es más estricta que en Centro (680mm)
        ref_water_mm = 220.0 if region == RegionSanLuis.NORTE else 250.0
        water_demand_score = max(0.0, min(1.0, 1.0 - (avg_water_mm - ref_water_mm) / 350.0))
        nota_agua = round(0.6 * avg_drought_tol + 0.4 * water_demand_score, 2)

        # 2. Nota Ingresos: Según potencial de mercado de los cultivos
        market_weights = {"alto": 1.0, "medio": 0.65, "bajo": 0.25}
        nota_ingresos = round(sum(market_weights.get(c["market_potential"], 0.5) for c in crops_data) / n, 2)

        # 3. Nota Suelo: Aporte de nitrógeno + profundidad y heterogeneidad radicular
        has_n_fixer = any(c["nitrogen_fixation"] for c in crops_data)
        avg_root_depth = sum(c["root_depth_cm"] for c in crops_data) / n
        root_score = min(1.0, avg_root_depth / 160.0)
        n_bonus = 0.35 if has_n_fixer else 0.0
        nota_suelo = round(min(1.0, 0.65 * root_score + n_bonus), 2)

        # 4. Nota Erosión: Presencia de cultivo invernal o cobertura para no dejar suelo desnudo
        has_winter_or_cover = any(
            c["cycle_season"] in ["invernal", "cobertura"] or c["id"] in ["cobertura", "trigo"]
            for c in crops_data
        )
        diversity_factor = min(1.0, n / 3.0)
        # En el Sur (suelos arenosos y ventosos) dejar el campo desnudo penaliza más fuerte
        unprotected_base = 0.25 if region == RegionSanLuis.SUR else 0.35
        base_erosion = 0.88 if has_winter_or_cover else unprotected_base
        nota_erosion = round(min(1.0, base_erosion * 0.8 + diversity_factor * 0.2), 2)

        return nota_agua, nota_ingresos, nota_suelo, nota_erosion

    @classmethod
    def compute_weighted_score(
        cls,
        crop_ids: List[str],
        normalized_weights: Dict[str, float],
        region: RegionSanLuis = RegionSanLuis.CENTRO,
    ) -> Tuple[float, Dict[str, float]]:
        nota_agua, nota_ingresos, nota_suelo, nota_erosion = cls.evaluate_rotation_scores(crop_ids, region=region)
        score = (
            normalized_weights["agua"] * nota_agua
            + normalized_weights["ingresos"] * nota_ingresos
            + normalized_weights["suelo"] * nota_suelo
            + normalized_weights["erosion"] * nota_erosion
        )
        clamped_score = round(max(0.0, min(1.0, score)), 2)
        breakdown = {
            "agua": nota_agua,
            "ingresos": nota_ingresos,
            "suelo": nota_suelo,
            "erosion": nota_erosion,
        }
        return clamped_score, breakdown

    @classmethod
    def generate_rotation_recommendations(
        cls,
        current_rotation: List[str],
        priorities: Priorities,
        region: Optional[RegionSanLuis] = RegionSanLuis.CENTRO,
        tierra: Optional[Tierra] = None,
    ) -> RotationResponse:
        # Si viene un objeto Tierra, su región tiene prioridad y ya pasó por el delimitador de San Luis
        effective_region = tierra.region if tierra else (region or RegionSanLuis.CENTRO)
        tierra_nombre = tierra.nombre if tierra else None
        region_meta = RegionRepository.get_region_by_id(effective_region)

        norm_weights = cls._normalize_priorities(priorities)

        # Limpiar y reconocer rotación actual
        cleaned_current = [c.strip() for c in current_rotation if c.strip()]
        if not cleaned_current:
            cleaned_current = ["Maíz", "Soja"]

        current_display_name = " → ".join(cleaned_current)

        rain_mm = region_meta.precipitacion_media_anual_mm if region_meta else 650.0
        heat_days = region_meta.dias_calor_extremo_anual if region_meta else 26
        region_label = region_meta.nombre if region_meta else f"Región {effective_region.value.capitalize()}"

        # Predefinir estrategias comparativas calibradas para la región seleccionada
        candidate_definitions = [
            {
                "id": "current",
                "name": current_display_name,
                "crops": cleaned_current,
                "is_current": True,
                "why": f"Rotación tradicional en {region_label} orientada a liquidez comercial a corto plazo, pero deja ventanas sin cobertura activa.",
                "benefits": ["Alta liquidez comercial inmediata", "Familiaridad de manejo agronómico"],
                "evidence": f"En {region_label} ({rain_mm:.0f} mm/año), NASA POWER muestra hasta 5 meses de invierno con campo descubierto y riesgo de evaporación y erosión eólica.",
                "evidence_details": {
                    "dataset": "NASA POWER Soil Wetness & Wind Speed (MERRA-2)",
                    "finding": f"En {region_label}, 5 meses de suelo descubierto en invierno inducen pérdidas de humedad y riesgo erosivo eólico.",
                    "resolution": "0.5° x 0.5°",
                    "period": "2000-2025",
                    "region": effective_region.value,
                },
                "risks_to_validate": "Monitorear compactación, pérdida de humedad por evaporación y declive paulatino de materia orgánica.",
            },
            {
                "id": "cover_enhanced",
                "name": "Maíz → Soja → Cultivo de cobertura",
                "crops": ["maiz", "soja", "cobertura"],
                "is_current": False,
                "why": f"Excelente equilibrio hídrico y edáfico para {region_label}. El cultivo de cobertura (Vicia/Centeno) frena la erosión invernal y fija nitrógeno biológico.",
                "benefits": [
                    "Reduce demanda hídrica en meses críticos al mejorar infiltración",
                    "Añade materia orgánica al perfil superior",
                    "Interrumpe ciclos biológicos de malezas y plagas",
                ],
                "evidence": f"NASA POWER registra inviernos secos (<20 mm/mes) en {region_label}. La cobertura viva protege el suelo y minimiza evaporación directa.",
                "evidence_details": {
                    "dataset": "NASA POWER Monthly Precipitation (PRECTOTCORR)",
                    "finding": f"Inviernos secos en {region_label} hacen crítica la retención de agua mediante cobertura vegetal viva.",
                    "resolution": "0.5° x 0.5°",
                    "period": "2000-2025",
                    "region": effective_region.value,
                },
                "risks_to_validate": "Definir fecha óptima de secado o terminación de la cobertura con asesor técnico para no restar agua a la siembra estival.",
            },
            {
                "id": "drought_sorghum",
                "name": "Sorgo → Soja",
                "crops": ["sorgo", "soja"],
                "is_current": False,
                "why": f"Estrategia de alta resiliencia climática en {region_label}: el sorgo tolera mejor las olas de calor (>35°C) y el estrés hídrico estival.",
                "benefits": [
                    "Alta resistencia a sequías y olas de calor estivales",
                    "Gran volumen de rastrojo que conserva la humedad superficial",
                    "Diversificación del sistema radicular",
                ],
                "evidence": f"{region_label} promedia {heat_days} días de calor extremo estival (>35°C) donde el sorgo mantiene rendimiento fotosintético estable.",
                "evidence_details": {
                    "dataset": "NASA POWER Daily Max Temperature (T2M_MAX)",
                    "finding": f"{heat_days} días anuales de calor extremo (T > 35°C) en {region_label}; el sorgo consume 30% menos agua que el maíz.",
                    "resolution": "0.5° x 0.5°",
                    "period": "2000-2025",
                    "region": effective_region.value,
                },
                "risks_to_validate": "Verificar canales comerciales y logística de entrega de sorgo en acopios zonales.",
            },
            {
                "id": "full_rotation",
                "name": "Trigo / Soja 2da → Maíz → Cobertura",
                "crops": ["trigo", "soja", "maiz", "cobertura"],
                "is_current": False,
                "why": f"Intensificación sustentable para {region_label} que maximiza captura de carbono y cobertura continua del suelo.",
                "benefits": [
                    "Cero meses de suelo descubierto frente al viento",
                    "Doble flujo de ingresos en el año agrícola",
                    "Mayor fijación biológica y reciclaje profundo de nutrientes",
                ],
                "evidence": f"Aprovecha pulsos de precipitación primaverales de {region_label} ({rain_mm:.0f} mm anuales) maximizando la eficiencia de uso del agua.",
                "evidence_details": {
                    "dataset": "NASA POWER Seasonal Precipitation Trends",
                    "finding": "Pulsos de lluvia primaveral permiten implantar cobertura continua manteniendo el balance de materia orgánica.",
                    "resolution": "0.5° x 0.5°",
                    "period": "2000-2025",
                    "region": effective_region.value,
                },
                "risks_to_validate": "Requiere mayor disponibilidad de agua útil inicial en el perfil previo a la siembra de trigo.",
            },
        ]

        # Calcular scores
        evaluated_strategies: List[StrategyOption] = []
        for candidate in candidate_definitions:
            score, breakdown = cls.compute_weighted_score(
                candidate["crops"],
                norm_weights,
                region=effective_region,
            )

            # Ajuste fino de la justificación si el usuario prioriza fuertemente un eje
            why_text = candidate["why"]
            if norm_weights["agua"] >= 0.4:
                why_text += f" (Aporte hídrico evaluado: {int(breakdown['agua'] * 100)}/100)."
            elif norm_weights["erosion"] >= 0.35:
                why_text += f" (Protección contra erosión calculada: {int(breakdown['erosion'] * 100)}/100)."

            is_curr = candidate["is_current"]

            strategy_opt = StrategyOption(
                name=candidate["name"],
                is_current=is_curr,
                score=score,
                why=why_text,
                benefits=candidate["benefits"],
                evidence=candidate["evidence"],
                evidence_details=candidate["evidence_details"],
                risks_to_validate=candidate["risks_to_validate"],
            )
            evaluated_strategies.append(strategy_opt)

        # Ordenar estrategias de mayor a menor puntuación
        evaluated_strategies.sort(key=lambda s: s.score, reverse=True)

        best_recommendation = evaluated_strategies[0].name

        return RotationResponse(
            region_evaluada=effective_region,
            tierra_nombre=tierra_nombre,
            recommendation=best_recommendation,
            strategies=evaluated_strategies,
        )
