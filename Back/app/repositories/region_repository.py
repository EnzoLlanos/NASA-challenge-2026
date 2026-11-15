from typing import Dict, List, Optional
from app.schemas.region import (
    RegionSanLuis,
    RegionDetailResponse,
    RegionFormConfigResponse,
    ReglaRegionalItem,
    CondicionCampoPregunta,
    Usuario,
    Tierra,
)


REGIONS_DATABASE: Dict[RegionSanLuis, dict] = {
    RegionSanLuis.NORTE: {
        "id": RegionSanLuis.NORTE,
        "nombre": "Región Norte de San Luis",
        "departamentos_referencia": ["Ayacucho", "Junín", "San Martín", "Belgrano (Norte)", "Quines", "Candelaria"],
        "latitud_rango": "-31.85° a -33.00°",
        "precipitacion_media_anual_mm": 520.0,
        "dias_calor_extremo_anual": 34,
        "dias_heladas_anual": 9,
        "aptitud_y_suelo": "Clima árido a semiárido cálido con alta demanda evaporativa estival. Suelos francos a franco-arenosos; excelente respuesta con manejo de rastrojo o riego complementario.",
        "cultivos_recomendados": ["Sorgo", "Soja", "Maíz", "Trigo"],
        "amenaza_principal": "Déficit hídrico estival severo (520 mm/año) y 34 días de calor extremo (>35 °C).",
        "prioridades_sugeridas": {
            "water": True,
            "nutrients": True,
            "erosion": True,
            "forageProfit": False,
        },
        "condicion_contextual": {
            "id": "altasTemperaturasSecano",
            "etiqueta": "¿Lote expuesto a olas de calor sin cortina forestal?",
            "descripcion": "En el Norte (34 días >35 °C) el suelo desnudo evapora la humedad en 48 hs y estresa floración.",
            "icono": "☀️",
            "valor_por_defecto": True,
        },
        "reglas_activas": [
            {
                "codigo": "N1",
                "nombre": "Déficit hídrico crítico estival",
                "factor_climatico": "520 mm/año de lluvia vs demanda >450 mm",
                "impacto_metricas": "Penaliza Agua (-20 pts) si se siembra Maíz/Soja en secano sin cobertura",
                "alerta_riesgo": "Riesgo severo de déficit hídrico en floración con precipitaciones de solo 520 mm/año.",
            },
            {
                "codigo": "N2",
                "nombre": "Golpe de calor reproductivo (>35 °C)",
                "factor_climatico": "34 días/año con temperaturas mayores a 35 °C",
                "impacto_metricas": "Bonifica Agua y Margen (+15 pts) al incluir Sorgo o cultivos tolerantes al calor",
                "alerta_riesgo": "34 días anuales >35 °C inducen aborto floral en cultivos sensibles sin rastrojo protector.",
            },
            {
                "codigo": "N3",
                "nombre": "Escudo contra evaporación directa",
                "factor_climatico": "Alta radiación solar estival e inviernos secos",
                "impacto_metricas": "Bonifica Agua (+15 pts) y Erosión (+12 pts) con cultivo de cobertura invernal",
                "alerta_riesgo": "La evaporación potencial supera la lluvia anual; dejar rastrojo en superficie es crítico.",
            },
        ],
    },
    RegionSanLuis.CENTRO: {
        "id": RegionSanLuis.CENTRO,
        "nombre": "Región Centro de San Luis",
        "departamentos_referencia": ["Juan Martín de Pueyrredón", "Coronel Pringles", "General Pedernera", "Chacabuco", "Villa Mercedes", "Cuenca del Morro"],
        "latitud_rango": "-33.00° a -34.20°",
        "precipitacion_media_anual_mm": 680.0,
        "dias_calor_extremo_anual": 26,
        "dias_heladas_anual": 15,
        "aptitud_y_suelo": "Zona agrícola núcleo semiárida de transición. Suelos susceptibles a erosión hídrica y eólica (especialmente en Cuenca del Morro), donde mantener raíces vivas es prioritario.",
        "cultivos_recomendados": ["Maíz", "Soja", "Trigo", "Sorgo"],
        "amenaza_principal": "Erosión hídrica por lluvias torrenciales de verano y ascenso de napas freáticas (Cuenca del Morro).",
        "prioridades_sugeridas": {
            "water": True,
            "nutrients": True,
            "erosion": True,
            "forageProfit": False,
        },
        "condicion_contextual": {
            "id": "riesgoNapasOErosionHidrica",
            "etiqueta": "¿Lote con pendiente o riesgo de napa alta / escurrimiento?",
            "descripcion": "En la zona Centro y Cuenca del Morro las raíces vivas en invierno consumen excedentes y frenan cárcavas.",
            "icono": "🌊",
            "valor_por_defecto": True,
        },
        "reglas_activas": [
            {
                "codigo": "C1",
                "nombre": "Control hidrológico y de napas con raíces vivas",
                "factor_climatico": "680 mm/año concentrados en tormentas estivales",
                "impacto_metricas": "Penaliza Erosión (-25 pts) en barbecho desnudo; premia cobertura viva (+18 pts)",
                "alerta_riesgo": "Suelo sin raíces activas en invierno agrava ascensos de napa freática y escurrimiento superficial.",
            },
            {
                "codigo": "C2",
                "nombre": "Sinergia Gramínea + Leguminosa",
                "factor_climatico": "Balance de carbono y nitrógeno en zona núcleo",
                "impacto_metricas": "Bonifica Nutrientes (+16 pts) al rotar Maíz/Trigo con Soja/Arveja",
                "alerta_riesgo": "Alternar raíces fasciculadas (gramíneas) y pivotantes (leguminosas) evita piso de arado.",
            },
            {
                "codigo": "C3",
                "nombre": "Degradación por monocultivo continuo",
                "factor_climatico": "Pérdida de estructura y planchado de suelo",
                "impacto_metricas": "Penaliza Nutrientes (-22 pts) y Agua (-18 pts) en monocultivo sin rotación",
                "alerta_riesgo": "El monocultivo reduce la infiltración de lluvias intensas de verano y acelera la pérdida de MO.",
            },
        ],
    },
    RegionSanLuis.SUR: {
        "id": RegionSanLuis.SUR,
        "nombre": "Región Sur de San Luis",
        "departamentos_referencia": ["Gobernador Dupuy", "Unión", "Buena Esperanza", "Nueva Galia", "Fortuna"],
        "latitud_rango": "-34.20° a -36.00°",
        "precipitacion_media_anual_mm": 610.0,
        "dias_calor_extremo_anual": 22,
        "dias_heladas_anual": 24,
        "aptitud_y_suelo": "Llanura medanosa pampeana con suelos arenosos profundos, menor retención hídrica superficial, mayor frecuencia de heladas y vientos intensos en primavera.",
        "cultivos_recomendados": ["Girasol", "Sorgo", "Maíz", "Soja"],
        "amenaza_principal": "Voladura eólica en suelos medanosos/arenosos y alta frecuencia de heladas (24 días/año).",
        "prioridades_sugeridas": {
            "water": True,
            "nutrients": False,
            "erosion": True,
            "forageProfit": True,
        },
        "condicion_contextual": {
            "id": "sueloArenosoVoladura",
            "etiqueta": "¿Suelo arenoso / medanoso expuesto al viento o con aptitud mixta?",
            "descripcion": "En Dupuy los vientos de agosto-octubre vuelan la arena si no hay cobertura o verdeo invernal anclando el suelo.",
            "icono": "💨",
            "valor_por_defecto": True,
        },
        "reglas_activas": [
            {
                "codigo": "S1",
                "nombre": "Alerta crítica de voladura de médanos (Erosión eólica)",
                "factor_climatico": "Suelos arenosos + vientos intensos de agosto a octubre",
                "impacto_metricas": "Penalización drástica en Erosión (-35 pts) si el lote queda desnudo en invierno",
                "alerta_riesgo": "Riesgo crítico de voladura de suelos arenosos por vientos de primavera si queda sin cobertura viva.",
            },
            {
                "codigo": "S2",
                "nombre": "Ventana de heladas tardías y tempranas",
                "factor_climatico": "24 días de heladas anuales (≤ 0 °C)",
                "impacto_metricas": "Bonifica rotaciones con verdeos invernales rústicos (Cebada/Centeno) y cultivos de raíz profunda",
                "alerta_riesgo": "Alta frecuencia de heladas (24 días/año); requiere ajustar fecha de siembra y usar híbridos rústicos.",
            },
            {
                "codigo": "S3",
                "nombre": "Fijación de perfil arenoso y doble propósito",
                "factor_climatico": "Baja retención hídrica superficial en médanos (610 mm/año)",
                "impacto_metricas": "Bonifica Agua (+14 pts) y Margen Forrajero (+15 pts) con Sorgo/Girasol + Verdeo",
                "alerta_riesgo": "En suelos arenosos el rastrojo superficial es indispensable para retener el agua de lluvia.",
            },
        ],
    },
}

# Base en memoria de Usuarios con su array de Tierras para pruebas e integración
USERS_DATABASE: Dict[str, Usuario] = {
    "usr-1": Usuario(
        id="usr-1",
        nombre="Productor Demo San Luis",
        tierras=[
            Tierra(
                nombre="Establecimiento Don Pedro",
                region=RegionSanLuis.CENTRO,
                porcentaje_en_san_luis=100.0,
                hectareas=250.0,
                lat=-33.67,
                lon=-65.45,
            ),
            Tierra(
                nombre="Lote El Algarrobo (Limítrofe Norte)",
                region=RegionSanLuis.NORTE,
                porcentaje_en_san_luis=65.0,
                hectareas=180.0,
                lat=-32.15,
                lon=-65.80,
            ),
            Tierra(
                nombre="Campo Médano Sur",
                region=RegionSanLuis.SUR,
                porcentaje_en_san_luis=100.0,
                hectareas=400.0,
                lat=-34.85,
                lon=-65.50,
            ),
        ],
    )
}


class RegionRepository:
    """
    Capa Repository para Regiones de San Luis (Norte, Centro, Sur),
    sus Reglas Agronómicas y Usuarios con sus Tierras.
    """

    @staticmethod
    def get_all_regions() -> List[RegionDetailResponse]:
        """Devuelve las 3 regiones de San Luis (norte, centro, sur) con sus datos agroclimáticos y reglas."""
        return [RegionDetailResponse(**data) for data in REGIONS_DATABASE.values()]

    @staticmethod
    def get_region_by_id(region: RegionSanLuis) -> Optional[RegionDetailResponse]:
        """Obtiene el detalle de una región específica junto con sus reglas activas."""
        data = REGIONS_DATABASE.get(region)
        if data:
            return RegionDetailResponse(**data)
        return None

    @staticmethod
    def get_form_config_by_region(region: RegionSanLuis) -> Optional[RegionFormConfigResponse]:
        """Devuelve la configuración adaptativa del formulario y reglas para la región indicada."""
        data = REGIONS_DATABASE.get(region)
        if not data:
            return None
        icono_map = {
            RegionSanLuis.NORTE: "☀️",
            RegionSanLuis.CENTRO: "🌊",
            RegionSanLuis.SUR: "💨",
        }
        return RegionFormConfigResponse(
            region=data["id"],
            nombre=data["nombre"],
            subtitulo_clima=(
                f"{int(data['precipitacion_media_anual_mm'])} mm/año · "
                f"{data['dias_calor_extremo_anual']} días >35 °C · "
                f"{data['dias_heladas_anual']} heladas/año"
            ),
            amenaza_principal=data["amenaza_principal"],
            icono_alerta=icono_map.get(region, "🛰️"),
            precipitacion_anual_mm=data["precipitacion_media_anual_mm"],
            dias_calor_extremo=data["dias_calor_extremo_anual"],
            dias_heladas=data["dias_heladas_anual"],
            cultivos_recomendados=data["cultivos_recomendados"],
            prioridades_sugeridas=data["prioridades_sugeridas"],
            condicion_contextual=CondicionCampoPregunta(**data["condicion_contextual"]),
            reglas_activas=[ReglaRegionalItem(**r) for r in data["reglas_activas"]],
        )

    @staticmethod
    def get_all_form_configs() -> Dict[str, RegionFormConfigResponse]:
        """Devuelve las configuraciones de formulario y reglas de las 3 regiones indexadas por ID."""
        result: Dict[str, RegionFormConfigResponse] = {}
        for reg in RegionSanLuis:
            cfg = RegionRepository.get_form_config_by_region(reg)
            if cfg:
                result[reg.value] = cfg
        return result

    @staticmethod
    def get_all_users() -> List[Usuario]:
        """Devuelve todos los usuarios registrados con su array de tierras."""
        return list(USERS_DATABASE.values())

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Usuario]:
        """Busca un usuario por su ID."""
        return USERS_DATABASE.get(user_id)

    @staticmethod
    def save_user(usuario: Usuario) -> Usuario:
        """Guarda o actualiza un usuario y su lista de tierras."""
        if not usuario.id:
            usuario.id = f"usr-{len(USERS_DATABASE) + 1}"
        USERS_DATABASE[usuario.id] = usuario
        return usuario

    @staticmethod
    def add_land_to_user(user_id: str, tierra: Tierra) -> Optional[Usuario]:
        """Agrega un objeto Tierra al array de tierras de un usuario existente."""
        usuario = USERS_DATABASE.get(user_id)
        if not usuario:
            return None
        usuario.tierras.append(tierra)
        return usuario
