from typing import List, Optional, Dict
import unicodedata
from app.schemas.crop import CropResponse


def _normalize_key(text: str) -> str:
    """Normaliza texto eliminando acentos y convirtiendo a minúsculas."""
    text = text.lower().strip()
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")
    return text


CROPS_DATABASE: Dict[str, dict] = {
    "maiz": {
        "id": "maiz",
        "name": "Maíz",
        "water_consumption_mm": 500.0,
        "drought_tolerance": 0.35,
        "nitrogen_fixation": False,
        "root_depth_cm": 140,
        "market_potential": "alto",
        "cycle_season": "estival",
    },
    "soja": {
        "id": "soja",
        "name": "Soja",
        "water_consumption_mm": 450.0,
        "drought_tolerance": 0.50,
        "nitrogen_fixation": True,
        "root_depth_cm": 100,
        "market_potential": "alto",
        "cycle_season": "estival",
    },
    "sorgo": {
        "id": "sorgo",
        "name": "Sorgo granífero",
        "water_consumption_mm": 380.0,
        "drought_tolerance": 0.85,
        "nitrogen_fixation": False,
        "root_depth_cm": 160,
        "market_potential": "medio",
        "cycle_season": "estival",
    },
    "trigo": {
        "id": "trigo",
        "name": "Trigo",
        "water_consumption_mm": 350.0,
        "drought_tolerance": 0.60,
        "nitrogen_fixation": False,
        "root_depth_cm": 110,
        "market_potential": "medio",
        "cycle_season": "invernal",
    },
    "cobertura": {
        "id": "cobertura",
        "name": "Cultivo de cobertura (Vicia / Centeno)",
        "water_consumption_mm": 220.0,
        "drought_tolerance": 0.75,
        "nitrogen_fixation": True,
        "root_depth_cm": 120,
        "market_potential": "bajo",
        "cycle_season": "cobertura",
    },
    "girasol": {
        "id": "girasol",
        "name": "Girasol",
        "water_consumption_mm": 400.0,
        "drought_tolerance": 0.80,
        "nitrogen_fixation": False,
        "root_depth_cm": 180,
        "market_potential": "medio",
        "cycle_season": "estival",
    },
}

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
    "cobertura": "cobertura",
    "cultivo de cobertura": "cobertura",
    "vicia": "cobertura",
    "centeno": "cobertura",
    "vicia/centeno": "cobertura",
    "cultivo de cobertura (vicia/centeno)": "cobertura",
    "cover crop": "cobertura",
    "girasol": "girasol",
    "sunflower": "girasol",
}


class CropRepository:
    """Repositorio para acceder a los rasgos agronómicos de los cultivos."""

    @staticmethod
    def get_all(season: Optional[str] = None) -> List[CropResponse]:
        """
        Devuelve los cultivos disponibles con sus rasgos.
        Permite filtrado opcional por estación de ciclo (estival, invernal, cobertura).
        """
        crops = [CropResponse(**data) for data in CROPS_DATABASE.values()]
        if season and isinstance(season, str) and season.strip():
            season_norm = _normalize_key(season)
            crops = [c for c in crops if _normalize_key(c.cycle_season) == season_norm]
        return crops


    @staticmethod
    def find_by_name_or_id(identifier: str) -> Optional[dict]:
        """Busca un cultivo por id o nombre normalizado."""
        norm = _normalize_key(identifier)
        crop_id = ALIAS_MAP.get(norm, norm)
        return CROPS_DATABASE.get(crop_id)

    @staticmethod
    def get_by_id(crop_id: str) -> Optional[CropResponse]:
        """Obtiene un cultivo por su identificador estricto."""
        data = CROPS_DATABASE.get(crop_id)
        if data:
            return CropResponse(**data)
        return None
