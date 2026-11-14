from typing import List, Optional, Dict
import unicodedata
from pathlib import Path
import yaml
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
    """Repositorio para acceder a los rasgos agronómicos de los cultivos con soporte para crops.yaml."""

    _cached_crops: Optional[Dict[str, dict]] = None
    _data_source: str = "calibrated_defaults"

    @classmethod
    def _find_yaml_path(cls) -> Optional[Path]:
        """Busca crops.yaml en rutas relativas probables dentro del workspace."""
        possible_paths = [
            Path("data/crops.yaml"),
            Path("../data/crops.yaml"),
            Path("../../data/crops.yaml"),
            Path(__file__).resolve().parents[3] / "data" / "crops.yaml",
        ]
        for p in possible_paths:
            if p.is_file():
                return p
        return None

    @classmethod
    def _load_data(cls) -> Dict[str, dict]:
        """Carga cultivos desde crops.yaml si existe, o recurre a la base por defecto."""
        if cls._cached_crops is not None:
            return cls._cached_crops

        yaml_path = cls._find_yaml_path()
        if yaml_path:
            try:
                with open(yaml_path, "r", encoding="utf-8") as f:
                    content = yaml.safe_load(f)
                crops_list = content.get("crops", []) if isinstance(content, dict) else content
                loaded = {}
                for item in crops_list:
                    cid = str(item.get("id") or _normalize_key(item.get("name", "")))
                    loaded[cid] = {
                        "id": cid,
                        "name": item.get("name", cid.capitalize()),
                        "water_consumption_mm": float(item.get("water_consumption_mm") or item.get("water_consumption", 400)),
                        "drought_tolerance": float(item.get("drought_tolerance", 0.5)),
                        "nitrogen_fixation": bool(item.get("nitrogen_fixation", False)),
                        "root_depth_cm": int(item.get("root_depth_cm") or item.get("root_depth", 100)),
                        "market_potential": item.get("market_potential", "medio"),
                        "cycle_season": item.get("cycle_season", "estival"),
                    }
                if loaded:
                    cls._cached_crops = loaded
                    cls._data_source = str(yaml_path)
                    return cls._cached_crops
            except Exception:
                pass

        cls._cached_crops = dict(CROPS_DATABASE)
        cls._data_source = "calibrated_defaults"
        return cls._cached_crops

    @classmethod
    def get_data_source(cls) -> str:
        """Indica si los datos provienen de crops.yaml o de valores por defecto calibrados."""
        if cls._cached_crops is None:
            cls._load_data()
        return cls._data_source

    @classmethod
    def get_all(cls, season: Optional[str] = None) -> List[CropResponse]:
        """
        Devuelve los cultivos disponibles con sus rasgos.
        Permite filtrado opcional por estación de ciclo (estival, invernal, cobertura).
        """
        db = cls._load_data()
        crops = [CropResponse(**data) for data in db.values()]
        if season and isinstance(season, str) and season.strip():
            season_norm = _normalize_key(season)
            crops = [c for c in crops if _normalize_key(c.cycle_season) == season_norm]
        return crops

    @classmethod
    def find_by_name_or_id(cls, identifier: str) -> Optional[dict]:
        """Busca un cultivo por id o nombre normalizado."""
        db = cls._load_data()
        norm = _normalize_key(identifier)
        crop_id = ALIAS_MAP.get(norm, norm)
        return db.get(crop_id)

    @classmethod
    def get_by_id(cls, crop_id: str) -> Optional[CropResponse]:
        """Obtiene un cultivo por su identificador estricto."""
        db = cls._load_data()
        data = db.get(crop_id)
        if data:
            return CropResponse(**data)
        return None

