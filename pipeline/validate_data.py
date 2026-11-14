"""
validate_data.py - Reporte de consistencia de los datos procesados del
equipo Datos (NASA Space Apps 2026, región piloto San Luis, Argentina).

Valida:
  1. data/processed/power_daily.csv    (serie diaria completa)
  2. data/processed/power_monthly.csv  (features mensuales)
  3. data/crops.yaml                   (tabla de cultivos)
  4. Compatibilidad con el contrato del backend (schemas / endpoints)

Uso:
  python pipeline/validate_data.py
"""

import sys
from pathlib import Path

import pandas as pd

# Consolas Windows (cp1252) no pueden imprimir emoji/acentos sin esto
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
CROPS_YAML = ROOT / "data" / "crops.yaml"

EXPECTED_DAILY_COLS = [
    "date", "temp_mean_c", "temp_max_c", "temp_min_c", "precip_mm",
    "rh_pct", "solar_kwh_m2", "soil_wet_surface", "soil_wet_root",
    "evap_land_mm",
]
EXPECTED_MONTHLY_COLS = [
    "year_month", "year", "month", "temp_mean_c", "temp_max_c",
    "temp_min_c", "precip_mm_sum", "frost_days", "heat_days_35",
    "soil_wet_root_mean", "evap_land_mm_sum", "total_days",
]
EXPECTED_CROP_FIELDS = [
    "name", "water_consumption", "drought_tolerance", "nitrogen_fixation",
    "root_depth", "soil_coverage", "organic_matter", "market_potential",
    "adaptation_notes",
]

checks = []


def check(label, ok, detail=""):
    checks.append((label, ok, detail))
    print(f"   {'✅' if ok else '❌'} {label}" + (f" — {detail}" if detail else ""))
    return ok


def validate_daily():
    print("\n1. power_daily.csv (serie diaria)")
    path = PROCESSED / "power_daily.csv"
    if not check("Existe", path.exists(), str(path)):
        return None
    df = pd.read_csv(path)
    check("9,497 filas (2000-2025)", len(df) == 9497, f"hay {len(df)}")
    check("Columnas esperadas", list(df.columns) == EXPECTED_DAILY_COLS,
          f"hay {len(df.columns)}")
    # Fechas continuas sin duplicados
    dates = pd.to_datetime(df["date"].astype(str), format="%Y%m%d")
    check("Sin fechas duplicadas", not dates.duplicated().any())
    check("Serie diaria continua",
          (dates.diff().dropna() == pd.Timedelta(days=1)).all())
    # Faltantes y rangos físicos
    check("Sin valores None/NaN", df.isna().sum().sum() == 0,
          f"{df.isna().sum().sum()} NaN")
    check("Sin -999 (código de faltante POWER)", (df.select_dtypes("number") == -999).sum().sum() == 0)
    check("precip_mm >= 0", (df["precip_mm"] >= 0).all())
    check("Temperaturas en rango plausible (-30..55 °C)",
          df[["temp_mean_c", "temp_max_c", "temp_min_c"]].min().min() > -30 and
          df[["temp_mean_c", "temp_max_c", "temp_min_c"]].max().max() < 55)
    check("temp_max >= temp_mean >= temp_min (todas las filas)",
          bool((df["temp_max_c"] >= df["temp_mean_c"]).all() and
               (df["temp_mean_c"] >= df["temp_min_c"]).all()))
    check("Humedad suelo en [0, 1]",
          df["soil_wet_surface"].between(0, 1).all() and
          df["soil_wet_root"].between(0, 1).all())
    return df


def validate_monthly():
    print("\n2. power_monthly.csv (features mensuales)")
    path = PROCESSED / "power_monthly.csv"
    if not check("Existe", path.exists(), str(path)):
        return None
    df = pd.read_csv(path)
    check("312 filas (26 años × 12 meses)", len(df) == 312, f"hay {len(df)}")
    check("Columnas esperadas", list(df.columns) == EXPECTED_MONTHLY_COLS,
          f"hay {len(df.columns)}")
    check("Sin valores NaN", df.isna().sum().sum() == 0,
          f"{df.isna().sum().sum()} NaN")
    check("Rango de años 2000-2025",
          df["year"].min() == 2000 and df["year"].max() == 2025,
          f"{df['year'].min()}-{df['year'].max()}")
    months_per_year = df.groupby("year")["month"].count()
    check("12 meses por año (todos los años)",
          bool((months_per_year == 12).all()),
          f"min={months_per_year.min()}, max={months_per_year.max()}")
    check("Meses secuenciales sin duplicados",
          not df.duplicated(["year", "month"]).any())
    check("frost_days y heat_days_35 >= 0",
          (df["frost_days"] >= 0).all() and (df["heat_days_35"] >= 0).all())
    check("frost_days <= total_days y heat_days_35 <= total_days",
          bool((df["frost_days"] <= df["total_days"]).all() and
               (df["heat_days_35"] <= df["total_days"]).all()))
    return df


def validate_crops():
    print("\n3. data/crops.yaml (tabla de cultivos)")
    if not check("Existe", CROPS_YAML.exists(), str(CROPS_YAML)):
        return None
    try:
        import yaml
    except ImportError:
        check("PyYAML instalado", False, "pip install pyyaml")
        return None
    crops = yaml.safe_load(CROPS_YAML.read_text(encoding="utf-8"))
    check("Parsea sin error", isinstance(crops, dict))
    check("5-7 cultivos", 5 <= len(crops) <= 7, f"hay {len(crops)}: {', '.join(crops)}")
    missing_fields = []
    bad_ranges = []
    for key, c in crops.items():
        for field in EXPECTED_CROP_FIELDS:
            if field not in c:
                missing_fields.append(f"{key}.{field}")
        if not 0 <= c.get("drought_tolerance", -1) <= 1:
            bad_ranges.append(f"{key}.drought_tolerance")
        if not 0 <= c.get("soil_coverage", -1) <= 1:
            bad_ranges.append(f"{key}.soil_coverage")
        if c.get("water_consumption", -1) <= 0:
            bad_ranges.append(f"{key}.water_consumption")
        if c.get("market_potential") not in ("alto", "medio", "bajo"):
            bad_ranges.append(f"{key}.market_potential")
    check("Todos los campos requeridos presentes (schema CropInfo)",
          not missing_fields, ", ".join(missing_fields))
    check("Valores en rango (tolerancia/cobertura 0-1, agua > 0, mercado alto/medio/bajo)",
          not bad_ranges, ", ".join(bad_ranges))
    check("Unidades documentadas en comentarios",
          "mm por ciclo" in CROPS_YAML.read_text(encoding="utf-8"))
    return crops


def validate_backend_compat(monthly, crops):
    print("\n4. Compatibilidad con backend / frontend")
    if monthly is not None:
        # El script de indicadores de Juan usa year y month
        check("Columnas year/month disponibles (script indicadores_estacionales)",
              {"year", "month"}.issubset(monthly.columns))
        # Campos que consume el mock de field-profile del backend
        check("Campos climate_summary disponibles (temp_mean_c, precip_mm_sum, frost_days, heat_days_35)",
              {"temp_mean_c", "precip_mm_sum", "frost_days", "heat_days_35"}
              .issubset(monthly.columns))
    if crops is not None:
        check("Nombres de cultivos compatibles con engine.py (maíz, soja, trigo)",
              all(k in crops for k in ("maíz", "soja", "trigo")))


def main():
    print("=" * 66)
    print("VALIDACIÓN DE DATOS PROCESADOS — Equipo Datos (Martin)")
    print("Región piloto: San Luis, Argentina | Período: 2000-2025")
    print("=" * 66)

    daily = validate_daily()
    monthly = validate_monthly()
    crops = validate_crops()
    validate_backend_compat(monthly, crops)

    failed = [c for c in checks if not c[1]]
    print("\n" + "=" * 66)
    print(f"RESULTADO: {len(checks) - len(failed)}/{len(checks)} checks OK"
          + (f" | {len(failed)} FALLOS" if failed else " — TODO CONSISTENTE"))
    if failed:
        print("Fallas:")
        for label, _, detail in failed:
            print(f"  - {label} {detail}")
    print("=" * 66)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
