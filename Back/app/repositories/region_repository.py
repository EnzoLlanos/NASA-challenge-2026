from typing import Dict, List, Optional
from app.schemas.region import (
    RegionSanLuis,
    RegionDetailResponse,
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
        "cultivos_recomendados": ["Sorgo granífero", "Cultivo de cobertura (Vicia / Centeno)", "Soja", "Maíz (tardío o bajo riego)"],
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
        "cultivos_recomendados": ["Maíz", "Soja", "Cultivo de cobertura (Vicia / Centeno)", "Trigo"],
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
        "cultivos_recomendados": ["Girasol", "Sorgo granífero", "Cultivo de cobertura (Vicia / Centeno)", "Maíz", "Soja"],
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
    Capa Repository para Regiones de San Luis (Norte, Centro, Sur) y Usuarios con sus Tierras.
    """

    @staticmethod
    def get_all_regions() -> List[RegionDetailResponse]:
        """Devuelve las 3 regiones de San Luis (norte, centro, sur) con sus datos agroclimáticos."""
        return [RegionDetailResponse(**data) for data in REGIONS_DATABASE.values()]

    @staticmethod
    def get_region_by_id(region: RegionSanLuis) -> Optional[RegionDetailResponse]:
        """Obtiene el detalle de una región específica."""
        data = REGIONS_DATABASE.get(region)
        if data:
            return RegionDetailResponse(**data)
        return None

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
