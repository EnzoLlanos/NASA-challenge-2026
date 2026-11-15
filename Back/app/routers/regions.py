from typing import List, Dict
from fastapi import APIRouter, status
from app.schemas.region import (
    RegionSanLuis,
    RegionDetailResponse,
    RegionFormConfigResponse,
    DelimiterInfoResponse,
    Usuario,
    Tierra,
)
from app.services.region_service import RegionService

router = APIRouter(tags=["Regiones"])


@router.get(
    "/api/regions",
    response_model=List[RegionDetailResponse],
    summary="Listar las 3 regiones de San Luis (Norte, Centro y Sur) con sus reglas",
)
def get_regions():
    """
    Devuelve las 3 regiones productivas de la provincia de San Luis (`norte`, `centro`, `sur`)
    con sus datos agroclimáticos e hídricos de NASA POWER y sus reglas agronómicas.
    """
    return RegionService.list_regions()


@router.get(
    "/api/regions/form-config",
    response_model=Dict[str, RegionFormConfigResponse],
    summary="Obtener la configuración adaptativa del formulario y reglas para las 3 zonas",
)
def get_all_regions_form_config():
    """
    Devuelve un diccionario indexado por región (`norte`, `centro`, `sur`) con las reglas activas,
    prioridades sugeridas, cultivos recomendados y la pregunta contextual de cada zona.
    """
    return RegionService.get_all_regions_form_configs()


@router.get(
    "/api/regions/{region_id}/form-config",
    response_model=RegionFormConfigResponse,
    summary="Obtener configuración de formulario y reglas de una zona específica",
)
def get_region_form_config(region_id: RegionSanLuis):
    """
    Retorna el diagnóstico climático, condición de campo contextual y reglas de riesgo para la zona elegida.
    """
    return RegionService.get_region_form_config(region_id)


@router.get(
    "/api/regions/delimitador",
    response_model=DelimiterInfoResponse,
    summary="Ver configuración del delimitador territorial de San Luis",
)
def get_san_luis_delimiter():
    """
    Muestra los límites geográficos de San Luis y la regla delimitadora
    (mínimo 50% de la superficie de la tierra dentro de San Luis).
    """
    return RegionService.get_delimiter_info()


@router.get(
    "/api/regions/{region_id}",
    response_model=RegionDetailResponse,
    summary="Obtener detalle de una región específica (norte, centro o sur)",
)
def get_region_by_id(region_id: RegionSanLuis):
    """
    Retorna la información climática, de suelos, reglas y cultivos recomendados para la región seleccionada.
    """
    return RegionService.get_region_detail(region_id)


@router.post(
    "/api/regions/validar-tierra",
    summary="Validar un objeto Tierra dentro del delimitador de San Luis",
)
def validate_land(tierra: Tierra):
    """
    Valida que el objeto Tierra (`nombre`, `region`) esté dentro de San Luis
    y cumpla con el mínimo del 50% de superficie dentro de la provincia.
    """
    return RegionService.validate_tierra_in_san_luis(tierra)


@router.get(
    "/api/users",
    response_model=List[Usuario],
    summary="Listar usuarios con su array de tierras en San Luis",
)
def get_users():
    """
    Retorna la lista de usuarios registrados, cada uno con su array de objetos `Tierra` (`nombre`, `region`).
    """
    return RegionService.list_users()


@router.post(
    "/api/users",
    response_model=Usuario,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un usuario con su array de tierras",
)
def create_user(usuario: Usuario):
    """
    Crea un nuevo `Usuario` con su lista de objetos `Tierra` (`nombre`, `region`),
    verificando automáticamente el delimitador de San Luis (mínimo 50% en la provincia).
    """
    return RegionService.create_user(usuario)


@router.post(
    "/api/users/{user_id}/tierras",
    response_model=Usuario,
    summary="Agregar una nueva Tierra (región, nombre) a un usuario",
)
def add_land_to_user(user_id: str, tierra: Tierra):
    """
    Añade un objeto `Tierra` (`nombre`, `region`) al array de tierras de un usuario existente.
    """
    return RegionService.add_tierra_to_user(user_id, tierra)
