from typing import List
from fastapi import HTTPException, status
from app.schemas.region import (
    RegionSanLuis,
    RegionDetailResponse,
    DelimiterInfoResponse,
    Usuario,
    Tierra,
    MIN_PORCENTAJE_TIERRA_EN_SAN_LUIS,
)
from app.repositories.region_repository import RegionRepository


class RegionService:
    """
    Capa de Servicio (Lógica de Negocio) para Regiones de San Luis (Norte, Centro, Sur),
    validación del delimitador territorial y gestión de Usuarios y sus Tierras.
    """

    @staticmethod
    def list_regions() -> List[RegionDetailResponse]:
        """Retorna las 3 regiones de San Luis (Norte, Centro y Sur)."""
        return RegionRepository.get_all_regions()

    @staticmethod
    def get_region_detail(region: RegionSanLuis) -> RegionDetailResponse:
        """Retorna el detalle agroclimático de una región específica."""
        detail = RegionRepository.get_region_by_id(region)
        if not detail:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La región '{region}' no existe en San Luis. Regiones válidas: norte, centro, sur.",
            )
        return detail

    @staticmethod
    def get_delimiter_info() -> DelimiterInfoResponse:
        """Devuelve las reglas activas del delimitador de San Luis."""
        return DelimiterInfoResponse()

    @staticmethod
    def validate_tierra_in_san_luis(tierra: Tierra) -> dict:
        """
        Verifica que una Tierra cumpla con el delimitador de San Luis
        (al menos 50% de la superficie dentro de la provincia y región válida: norte, centro o sur).
        """
        region_info = RegionRepository.get_region_by_id(tierra.region)
        return {
            "valida": True,
            "tierra": tierra,
            "region_info": region_info,
            "mensaje": (
                f"Tierra '{tierra.nombre}' validada correctamente en la {region_info.nombre} "
                f"({tierra.porcentaje_en_san_luis}% dentro de San Luis; mínimo requerido: {MIN_PORCENTAJE_TIERRA_EN_SAN_LUIS}%)."
            ),
        }

    @staticmethod
    def list_users() -> List[Usuario]:
        """Lista todos los usuarios con su array de tierras."""
        return RegionRepository.get_all_users()

    @staticmethod
    def get_user(user_id: str) -> Usuario:
        """Obtiene un usuario por su ID."""
        user = RegionRepository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado.",
            )
        return user

    @staticmethod
    def create_user(usuario: Usuario) -> Usuario:
        """
        Crea un nuevo usuario validando que todas sus tierras respeten el delimitador de San Luis.
        """
        if usuario.tierras:
            avg_in_sl = sum(t.porcentaje_en_san_luis for t in usuario.tierras) / len(usuario.tierras)
            if avg_in_sl < MIN_PORCENTAJE_TIERRA_EN_SAN_LUIS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"El promedio de tierras en San Luis ({avg_in_sl:.1f}%) es inferior al "
                        f"delimitador mínimo permitido ({MIN_PORCENTAJE_TIERRA_EN_SAN_LUIS}%)."
                    ),
                )
        return RegionRepository.save_user(usuario)

    @staticmethod
    def add_tierra_to_user(user_id: str, tierra: Tierra) -> Usuario:
        """Agrega un objeto Tierra (región, nombre) al array de tierras de un usuario."""
        updated = RegionRepository.add_land_to_user(user_id, tierra)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado para asociar la tierra '{tierra.nombre}'.",
            )
        return updated
