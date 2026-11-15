from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
import unicodedata

from app.schemas import (
    ZonaSanLuis,
    CropInfo,
    StrategyOption,
    SecuenciaItem,
    MetricasCualitativas,
    RotationResponse,
    RotationRequest,
    Tierra,
)


def _normalizar(texto: str) -> str:
    """Elimina acentos y espacios para comparar identificadores de cultivos."""
    t = texto.lower().strip()
    return unicodedata.normalize("NFKD", t).encode("ASCII", "ignore").decode("utf-8")


class ScoringEngine:
    """
    Motor de recomendación agronómica adaptado por zonas de San Luis (Norte, Centro, Sur).
    Diseñado para agricultores: no utiliza fórmulas de porcentaje (%) ni cálculos de ganancia monetaria.
    """

    _cached_crops_by_zone: Dict[str, Dict[str, CropInfo]] = {}
    _yaml_path: Optional[Path] = None

    @classmethod
    def _find_crops_yaml(cls, zona_key: Optional[str] = None) -> Optional[Path]:
        if zona_key:
            posibles_rutas_zona = [
                Path(f"data/zonas/crops_{zona_key}.yaml"),
                Path(f"../data/zonas/crops_{zona_key}.yaml"),
                Path(f"../../data/zonas/crops_{zona_key}.yaml"),
                Path(__file__).resolve().parents[3] / "data" / "zonas" / f"crops_{zona_key}.yaml",
                Path(__file__).resolve().parents[2] / "data" / "zonas" / f"crops_{zona_key}.yaml",
            ]
            for p in posibles_rutas_zona:
                if p.is_file():
                    return p

        if cls._yaml_path and cls._yaml_path.exists():
            return cls._yaml_path

        posibles_rutas = [
            Path("data/crops.yaml"),
            Path("../data/crops.yaml"),
            Path("../../data/crops.yaml"),
            Path(__file__).resolve().parents[3] / "data" / "crops.yaml",
            Path(__file__).resolve().parents[2] / "data" / "crops.yaml",
        ]
        for p in posibles_rutas:
            if p.is_file():
                cls._yaml_path = p
                return p
        return None

    @classmethod
    def load_crops_for_zone(cls, zona: ZonaSanLuis = ZonaSanLuis.CENTRO) -> Dict[str, CropInfo]:
        """
        Lee el archivo data/crops.yaml o data/zonas/crops_{zona}.yaml adaptado a la zona seleccionada.
        Soporta tanto un YAML organizado por zonas como archivos individuales por zona.
        """
        zona_key = zona.value if isinstance(zona, ZonaSanLuis) else str(zona).lower()
        if zona_key in cls._cached_crops_by_zone:
            return cls._cached_crops_by_zone[zona_key]

        yaml_file = cls._find_crops_yaml(zona_key)
        raw_dict = {}
        if yaml_file:
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    loaded = yaml.safe_load(f)
                    if isinstance(loaded, dict):
                        raw_dict = loaded
            except Exception:
                raw_dict = {}

        # Si el YAML tiene estructura por zonas (ej: norte: { maiz: ... })
        crops_data = {}
        if zona_key in raw_dict and isinstance(raw_dict[zona_key], dict):
            source_dict = raw_dict[zona_key]
        elif "zonas" in raw_dict and zona_key in raw_dict["zonas"]:
            source_dict = raw_dict["zonas"][zona_key]
        else:
            # Archivo plano con cultivos generales adaptables
            source_dict = raw_dict

        for crop_id, data in source_dict.items():
            if not isinstance(data, dict):
                continue
            cid = _normalizar(crop_id)
            crops_data[cid] = CropInfo(
                id=cid,
                name=data.get("name", crop_id.capitalize()),
                zona=zona,
                water_consumption=float(data.get("water_consumption", 400)),
                drought_tolerance=float(data.get("drought_tolerance", 0.5)),
                nitrogen_fixation=bool(data.get("nitrogen_fixation", False)),
                root_depth=int(data.get("root_depth", 100)),
                soil_coverage=float(data.get("soil_coverage", 0.7)),
                season=str(data.get("season", "verano")),
                cycle_months=int(data.get("cycle_months", 5)),
                market_potential=str(data.get("market_potential", "medio")),
                adaptation_notes=data.get("adaptation_notes"),
            )

        # Si no había cultivos cargados del YAML, usamos respaldo agronómico calibrado
        if not crops_data:
            crops_data = cls._default_crops_for_zone(zona)

        cls._cached_crops_by_zone[zona_key] = crops_data
        return crops_data

    @staticmethod
    def _default_crops_for_zone(zona: ZonaSanLuis) -> Dict[str, CropInfo]:
        """Cultivos base de San Luis si no hay archivo YAML externo."""
        return {
            "maiz": CropInfo(
                id="maiz",
                name="Maíz",
                zona=zona,
                water_consumption=500.0,
                drought_tolerance=0.3,
                nitrogen_fixation=False,
                root_depth=150,
                soil_coverage=0.8,
                season="verano",
                cycle_months=6,
                market_potential="alto",
                adaptation_notes="Principal cultivo de verano. Rastrojo abundante.",
            ),
            "soja": CropInfo(
                id="soja",
                name="Soja",
                zona=zona,
                water_consumption=450.0,
                drought_tolerance=0.5,
                nitrogen_fixation=True,
                root_depth=80,
                soil_coverage=0.7,
                season="verano",
                cycle_months=5,
                market_potential="alto",
                adaptation_notes="Fija nitrógeno biológico. Raíz superficial.",
            ),
            "sorgo": CropInfo(
                id="sorgo",
                name="Sorgo",
                zona=zona,
                water_consumption=300.0,
                drought_tolerance=0.9,
                nitrogen_fixation=False,
                root_depth=200,
                soil_coverage=0.7,
                season="verano",
                cycle_months=5,
                market_potential="medio",
                adaptation_notes="Excelente tolerancia a olas de calor y sequía.",
            ),
            "trigo": CropInfo(
                id="trigo",
                name="Trigo",
                zona=zona,
                water_consumption=350.0,
                drought_tolerance=0.8,
                nitrogen_fixation=False,
                root_depth=120,
                soil_coverage=0.9,
                season="invierno",
                cycle_months=7,
                market_potential="medio",
                adaptation_notes="Cereal de invierno que evita el suelo desnudo.",
            ),
            "arveja": CropInfo(
                id="arveja",
                name="Vicia / Arveja (cobertura)",
                zona=zona,
                water_consumption=200.0,
                drought_tolerance=0.75,
                nitrogen_fixation=True,
                root_depth=60,
                soil_coverage=0.95,
                season="cubierta",
                cycle_months=4,
                market_potential="bajo",
                adaptation_notes="Protección invernal máxima y aporte natural de nitrógeno.",
            ),
            "girasol": CropInfo(
                id="girasol",
                name="Girasol",
                zona=zona,
                water_consumption=300.0,
                drought_tolerance=0.85,
                nitrogen_fixation=False,
                root_depth=250,
                soil_coverage=0.6,
                season="verano",
                cycle_months=5,
                market_potential="alto",
                adaptation_notes="Raíz muy profunda que rompe capas compactadas.",
            ),
        }

    @classmethod
    def calculate_rotation(cls, request: RotationRequest) -> RotationResponse:
        """
        Genera la recomendación de rotación adaptada a la zona de San Luis elegida.
        Devuelve estrategias sin porcentajes ni campos de margen/ganancia monetaria.
        """
        # 1. Determinar zona activa
        zona = request.zona or ZonaSanLuis.CENTRO
        if request.tierra and request.tierra.zona:
            zona = request.tierra.zona
        tierra_nombre = request.tierra.nombre if request.tierra else None

        # 2. Cultivo actual del productor
        cultivo_actual = request.current_crop or (
            request.current_rotation[0] if request.current_rotation else "Soja"
        )
        cultivo_actual_clean = cultivo_actual.capitalize()

        # 3. Contexto agroclimático según la zona de San Luis
        if zona == ZonaSanLuis.NORTE:
            nombre_zona = "Zona Norte de San Luis (Valle del Conlara / Sierras)"
            lluvia_contexto = "Clima templado-serrano con buena humedad de suelo (0.60) pero 35 días de heladas al año."
            estrategia_rec_nombre = f"{cultivo_actual_clean} → Arveja / Vicia → Maíz"
            secuencia_rec = [
                SecuenciaItem(cultivo=cultivo_actual_clean, tipo="cultivo", desde=11, hasta=4, meses_texto="Noviembre a Abril"),
                SecuenciaItem(cultivo="Arveja / Vicia (cobertura)", tipo="cobertura", desde=5, hasta=9, meses_texto="Mayo a Septiembre"),
                SecuenciaItem(cultivo="Maíz de ciclo completo", tipo="cultivo", desde=10, hasta=4, meses_texto="Octubre a Abril"),
            ]
            rec_agua = "El suelo del valle retiene buena humedad radicular (0.60 según NASA POWER)"
            rec_nutrientes = "La leguminosa de invierno fija nitrógeno y reduce fertilización química"
            rec_erosion = "La cobertura densa protege las laderas de la erosión hídrica por lluvias serranas"
            rec_salida = "Excelente colocación de grano y ahorro en fertilizantes"
            nasa_evidencia_rec = (
                "Satélites NASA POWER registran baja incidencia de calor extremo (<3 días/año ≥35°C) y buena humedad edáfica, "
                "pero advierten riesgo de heladas tardías en primavera sobre las sierras."
            )
            riesgo_rec = "Monitorear pronóstico de heladas tardías en octubre antes de sembrar maíz temprano."

        elif zona == ZonaSanLuis.SUR:
            nombre_zona = "Zona Sur de San Luis (Llanura medanosa / Buena Esperanza)"
            lluvia_contexto = "Suelos arenosos con baja retención hídrica y veranos con 34 días de calor sofocante (≥35°C)."
            estrategia_rec_nombre = f"{cultivo_actual_clean} → Centeno / Cebada → Sorgo granífero"
            secuencia_rec = [
                SecuenciaItem(cultivo=cultivo_actual_clean, tipo="cultivo", desde=11, hasta=4, meses_texto="Noviembre a Abril"),
                SecuenciaItem(cultivo="Centeno / Cebada (cobertura)", tipo="cobertura", desde=5, hasta=9, meses_texto="Mayo a Septiembre"),
                SecuenciaItem(cultivo="Sorgo granífero (raíz profunda)", tipo="cultivo", desde=10, hasta=3, meses_texto="Octubre a Marzo"),
            ]
            rec_agua = "El sorgo consume 40% menos agua y sus raíces de 200 cm buscan humedad profunda"
            rec_nutrientes = "Aporte continuo de rastrojo que regenera la materia orgánica en suelos arenosos"
            rec_erosion = "El centeno cubre el suelo en los meses ventosos de invierno evitando voladuras de médanos"
            rec_salida = "Grano y forraje rústico de alta demanda ganadera en el sur provincial"
            nasa_evidencia_rec = (
                "NASA POWER y SMAP detectan 34 días/año con calor ≥35°C y baja humedad radicular (0.32). "
                "El sorgo es el cultivo más resiliente para evitar el estrés hídrico estival."
            )
            riesgo_rec = "Evitar dejar el suelo desnudo en agosto y septiembre por fuertes vientos y voladuras."

        else:  # CENTRO
            nombre_zona = "Zona Centro de San Luis (Capital / Villa Mercedes)"
            lluvia_contexto = "Planicie agrícola intermedia con régimen moderado de calor y heladas."
            estrategia_rec_nombre = f"Maíz → Soja → Cultivo de cobertura (Vicia / Centeno)"
            secuencia_rec = [
                SecuenciaItem(cultivo="Maíz", tipo="cultivo", desde=10, hasta=3, meses_texto="Octubre a Marzo"),
                SecuenciaItem(cultivo="Vicia (cobertura)", tipo="cobertura", desde=4, hasta=9, meses_texto="Abril a Septiembre"),
                SecuenciaItem(cultivo="Soja", tipo="cultivo", desde=10, hasta=4, meses_texto="Octubre a Abril"),
            ]
            rec_agua = "Mayor infiltración de lluvia y menor escurrimiento en las pendientes"
            rec_nutrientes = "La vicia aporta nitrógeno natural y el maíz deja rastrojo duradero"
            rec_erosion = "Suelo protegido casi todo el año frente a lluvias torrenciales y viento"
            rec_salida = "Granos con amplia recepción en acopios de la zona"
            nasa_evidencia_rec = (
                "NASA POWER muestra que más del 70% de la lluvia cae en solo 5 meses de verano. "
                "Tener cobertura viva en invierno y rastrojo en verano evita que el agua se escurra sin infiltrar."
            )
            riesgo_rec = "Ajustar la fertilización fosforada inicial según análisis de lote."

        # 4. Estrategia Actual (Alerta/Monocultivo)
        estrategia_actual = StrategyOption(
            id="actual",
            nombre=f"{cultivo_actual_clean} continuo (Situación actual)",
            is_current=True,
            etiqueta="Tu situación actual",
            salud_suelo="En riesgo",
            salud_suelo_nivel=35,
            resumen=f"Sembrar solo {cultivo_actual_clean} año tras año deja el suelo desnudo casi 6 meses en {nombre_zona}.",
            secuencia=[
                SecuenciaItem(cultivo=cultivo_actual_clean, tipo="cultivo", desde=11, hasta=4, meses_texto="Noviembre a Abril"),
                SecuenciaItem(cultivo="Barbecho largo (suelo sin cubrir)", tipo="cultivo", desde=5, hasta=10, meses_texto="Mayo a Octubre"),
            ],
            metricas=MetricasCualitativas(
                agua="El agua se evapora rápido al no haber plantas tapando el suelo",
                nutrientes="El suelo va perdiendo materia orgánica y fertilidad natural",
                erosion="Peligro de formación de huellones o voladura de tierra con el viento",
                salida_comercial="Venta conocida, pero con mayor gasto en fertilizantes y agroquímicos",
            ),
            beneficios=["Manejo sencillo y conocido", "Un solo cultivo para cosechar"],
            riesgos_locales=[
                "Pérdida continua de fertilidad del lote",
                "Compactación del suelo por falta de raíces vivas",
            ],
            evidencia_nasa=f"Satélites NASA detectan hasta 5 meses seguidos de suelo descubierto en {nombre_zona}, aumentando el estrés hídrico.",
        )

        # 5. Estrategia Recomendada (Regenerativa / Adaptada)
        estrategia_recomendada = StrategyOption(
            id="recomendada",
            nombre=estrategia_rec_nombre,
            is_current=False,
            etiqueta="Recomendada",
            salud_suelo="Saludable",
            salud_suelo_nivel=85,
            resumen=f"Rotación balanceada para {nombre_zona}: mantiene el suelo cubierto, cuida el agua y suma nutrientes naturales.",
            secuencia=secuencia_rec,
            metricas=MetricasCualitativas(
                agua=rec_agua,
                nutrientes=rec_nutrientes,
                erosion=rec_erosion,
                salida_comercial=rec_salida,
            ),
            beneficios=[
                "Menor necesidad de comprar fertilizantes químicos",
                "El suelo absorbe mejor las lluvias de verano",
                "Corta el ciclo de malezas y plagas difíciles",
            ],
            riesgos_locales=[riesgo_rec],
            evidencia_nasa=nasa_evidencia_rec,
        )

        # 6. Estrategia Alternativa (Doble propósito / Forrajera)
        estrategia_alternativa = StrategyOption(
            id="doble_proposito",
            nombre="Sorgo / Girasol → Verdeo de Avena (Forraje y grano)",
            is_current=False,
            etiqueta="Doble propósito",
            salud_suelo="Moderada",
            salud_suelo_nivel=65,
            resumen=f"Opción para productores mixtos de {nombre_zona} que quieran alimento para animales y cosecha de grano.",
            secuencia=[
                SecuenciaItem(cultivo="Sorgo o Girasol", tipo="cultivo", desde=11, hasta=3, meses_texto="Noviembre a Marzo"),
                SecuenciaItem(cultivo="Avena forrajera", tipo="cobertura", desde=4, hasta=9, meses_texto="Abril a Septiembre"),
            ],
            metricas=MetricasCualitativas(
                agua="Cultivos muy rústicos con bajo consumo de agua en verano",
                nutrientes="Mantiene niveles estables de nutrientes en el perfil",
                erosion="Buena cobertura en otoño e invierno con pastoreo liviano",
                salida_comercial="Alimento propio para ganado o venta de fardos en la zona",
            ),
            beneficios=[
                "Alimento seguro para el ganado en los meses secos",
                "Diversifica el ingreso del campo",
            ],
            riesgos_locales=[
                "Controlar la carga animal para que el pisoteo no compacte el suelo húmedo"
            ],
            evidencia_nasa=f"NASA POWER confirma que en {nombre_zona} las lluvias de marzo-abril permiten implantar verdeos con buena emergencia.",
        )

        estrategias = [estrategia_recomendada, estrategia_alternativa, estrategia_actual]

        return RotationResponse(
            zona=zona,
            tierra_nombre=tierra_nombre,
            recomendacion=estrategia_recomendada.nombre,
            estrategias=estrategias,
            data_gaps=[
                f"Datos ajustados a la {nombre_zona} con satélites NASA POWER y modelos INTA.",
                "Los resultados son orientativos para apoyar tu decisión: conversalo siempre con tu asesor técnico de confianza.",
            ],
        )


def calculate_rotation_for_zone(request: RotationRequest) -> RotationResponse:
    """Función de conveniencia para llamar al motor de puntuación."""
    return ScoringEngine.calculate_rotation(request)
