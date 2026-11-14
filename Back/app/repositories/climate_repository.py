from pathlib import Path
from typing import List
import pandas as pd
from app.schemas.field_profile import PowerMonthlyRow

# Ruta a los datos limpios de NASA POWER (data/processed/power_monthly.csv)
CSV_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "data"
    / "processed"
    / "power_zona_humeda.csv"
)


class ClimateRepository:
    """
    Capa de persistencia / acceso a datos climáticos.
    Responsabilidad única: leer el archivo 'power_monthly.csv' y entregar
    los datos crudos al Service sin aplicar lógica de negocio.
    """

    def __init__(self, csv_path: Path = CSV_PATH):
        self.csv_path = csv_path

    def get_monthly_dataframe(self) -> pd.DataFrame:
        """Lee el CSV y devuelve el DataFrame de pandas con los 312 meses históricos."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"No se encontró el dataset en: {self.csv_path}")

        return pd.read_csv(self.csv_path)

    def get_all_monthly_rows(self) -> List[PowerMonthlyRow]:
        """Devuelve las filas crudas del CSV mapeadas a la clase PowerMonthlyRow."""
        df = self.get_monthly_dataframe()
        records = df.to_dict(orient="records")
        return [PowerMonthlyRow(**row) for row in records]
