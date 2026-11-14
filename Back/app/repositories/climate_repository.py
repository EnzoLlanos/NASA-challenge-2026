from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import yaml
from app.schemas.simulation import PowerMonthlyRow

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
MONTHLY_CSV_PATH = DATA_DIR / "processed" / "power_monthly.csv"
DAILY_CSV_PATH = DATA_DIR / "processed" / "power_daily.csv"
CROPS_YAML_PATH = DATA_DIR / "crops.yaml"


class ClimateRepository:
    """
    Capa de persistencia / acceso a datos.
    Responsabilidad única: leer los datasets ('power_monthly.csv', 'power_daily.csv' y 'crops.yaml')
    y entregar los datos crudos al Service sin aplicar reglas de negocio.
    """

    def __init__(
        self,
        monthly_csv_path: Path = MONTHLY_CSV_PATH,
        daily_csv_path: Path = DAILY_CSV_PATH,
        crops_yaml_path: Path = CROPS_YAML_PATH,
    ):
        self.monthly_csv_path = monthly_csv_path
        self.daily_csv_path = daily_csv_path
        self.crops_yaml_path = crops_yaml_path

    def get_monthly_dataframe(self) -> pd.DataFrame:
        """Lee 'power_monthly.csv' (312 meses) y devuelve el DataFrame crudo."""
        if not self.monthly_csv_path.exists():
            raise FileNotFoundError(f"No se encontró el dataset mensual en: {self.monthly_csv_path}")
        return pd.read_csv(self.monthly_csv_path)

    def get_daily_dataframe(self) -> pd.DataFrame:
        """Lee 'power_daily.csv' (9497 días) y devuelve el DataFrame crudo."""
        if not self.daily_csv_path.exists():
            raise FileNotFoundError(f"No se encontró el dataset diario en: {self.daily_csv_path}")
        return pd.read_csv(self.daily_csv_path)

    def get_crops_catalog(self) -> Dict[str, Dict[str, Any]]:
        """Lee 'data/crops.yaml' y devuelve el diccionario crudo de cultivos y sus rasgos."""
        if not self.crops_yaml_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo de cultivos en: {self.crops_yaml_path}")
        with open(self.crops_yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_all_monthly_rows(self) -> List[PowerMonthlyRow]:
        """Devuelve las filas crudas del CSV mensual mapeadas a PowerMonthlyRow."""
        df = self.get_monthly_dataframe()
        records = df.to_dict(orient="records")
        return [PowerMonthlyRow(**row) for row in records]
