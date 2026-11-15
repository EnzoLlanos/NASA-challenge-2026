from typing import List, Optional, Dict
import unicodedata
from app.schemas import CropInfo, ZonaSanLuis, CropResponse
from app.scoring.engine import ScoringEngine


def _normalize_key(text: str) -> str:
    """Normaliza texto eliminando acentos y convirtiendo a minúsculas."""
    text = text.lower().strip()
    return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")


# Mapeo de sinónimos comunes para reconocer las selecciones del frontend
ALIAS_MAP: Dict[str, str] = {
    "maiz": "maiz",
    "maíz": "maiz",
    "corn": "maiz",
    "soja": "soja",
    "soy": "soja",
    "soybean": "soja",
    "sorgo": "sorgo",
    "sorghum": "sorgo",
    "trigo": "trigo",
    "wheat": "trigo",
    "cobertura": "arveja",
    "cultivo de cobertura": "arveja",
    "vicia": "arveja",
    "arveja": "arveja",
    "centeno": "cebada",
    "vicia/centeno": "arveja",
    "cover crop": "arveja",
    "girasol": "girasol",
    "sunflower": "girasol",
    "cebada": "cebada",
}


class CropRepository:
    """
    Repositorio de cultivos conectado con `data/crops.yaml` adaptado a las zonas de San Luis.
    """

    @classmethod
    def get_all(
        cls,
        season: Optional[str] = None,
        zona: Optional[ZonaSanLuis] = ZonaSanLuis.CENTRO,
    ) -> List[CropInfo]:
        """Devuelve los cultivos leídos de data/crops.yaml para la zona seleccionada."""
        crops_dict = ScoringEngine.load_crops_for_zone(zona or ZonaSanLuis.CENTRO)
        crops = list(crops_dict.values())
        if season and isinstance(season, str) and season.strip():
            season_norm = season.strip().lower()
            crops = [c for c in crops if c.season.lower() == season_norm]
        return crops

    @classmethod
    def find_by_name_or_id(
        cls,
        identifier: str,
        zona: Optional[ZonaSanLuis] = ZonaSanLuis.CENTRO,
    ) -> Optional[CropInfo]:
        """Busca un cultivo en crops.yaml por nombre o alias."""
        norm = _normalize_key(identifier)
        crop_id = ALIAS_MAP.get(norm, norm)
        crops_dict = ScoringEngine.load_crops_for_zone(zona or ZonaSanLuis.CENTRO)
        return crops_dict.get(crop_id)

    @classmethod
    def get_by_id(
        cls,
        crop_id: str,
        zona: Optional[ZonaSanLuis] = ZonaSanLuis.CENTRO,
    ) -> Optional[CropInfo]:
        """Obtiene un cultivo por su ID estricto."""
        crops_dict = ScoringEngine.load_crops_for_zone(zona or ZonaSanLuis.CENTRO)
        return crops_dict.get(crop_id)
