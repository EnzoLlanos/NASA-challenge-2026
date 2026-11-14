"""
build_features.py - Limpieza y generation de features para datos NASA POWER

Estructura real del JSON POWER:
{
  "properties": {
    "parameter": {
      "T2M": {"20000101": 23.86, "20000102": 24.1, ...},
      "T2M_MAX": {"20000101": 28.5, "20000102": 29.0, ...},
      ...
    }
  }
}
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

from common import RAW, PROCESSED, PILOT

# Mapeo de nombres de variables (igual que la versión original con pandas)
VAR_MAP = {
    "T2M": "temp_mean_c",
    "T2M_MAX": "temp_max_c",
    "T2M_MIN": "temp_min_c",
    "PRECTOTCORR": "precip_mm",
    "RH2M": "rh_pct",
    "ALLSKY_SFC_SW_DWN": "solar_kwh_m2",
    "GWETTOP": "soil_wet_surface",
    "GWETROOT": "soil_wet_root",
    "EVLAND": "evap_land_mm",
}

# Rutas
RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed"


def load_power():
    """Carga los datos crudos de NASA POWER y transpone a estructura unificada."""
    raw_path = RAW / f"power_{PILOT['name']}.json"
    if not raw_path.exists():
        raise FileNotFoundError(
            f"No se encuentran datos crudos en {raw_path}. "
            "Ejecuta primero fetch_power.py"
        )
    with open(raw_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    param = raw["properties"]["parameter"]

    # Transponer: obtener todas las fechas (deben ser idénticas en todas las variables)
    # y crear un diccionario {fecha: {variable: valor}}
    first_var = next(iter(param))
    all_dates = param[first_var].keys()

    # Diccionario unificado: fecha -> {variable: valor}
    unified = {}
    for date_str in all_dates:
        unified[date_str] = {}
        for var_name in param:
            if date_str in param[var_name]:
                unified[date_str][var_name] = param[var_name][date_str]

    return unified


def clean(df):
    """
    Limpia los datos transpuestos:
    - Reemplaza -999 por None
    - Elimina fechas duplicadas
    - Asegura índice diario completo
    - Renombra variables
    - Interpola huecos cortos (máx. 3 días)
    - Clausura precipitación a >= 0
    """
    # 1. Reemplazar -999 por None
    for date_str in df:
        var_dict = df[date_str]
        for var_name in var_dict:
            if var_dict[var_name] == -999:
                var_dict[var_name] = None

    # 2. Filtrar fechas que tienen al menos algunos valores no-None
    valid_dates = {}
    for date_str in df:
        var_dict = df[date_str]
        # Verificar si hay al menos un valor no-None
        has_valid = any(v is not None for v in var_dict.values())
        if has_valid:
            # Renombrar variables
            renamed = {}
            for var_name, value in var_dict.items():
                new_name = VAR_MAP.get(var_name, var_name)
                renamed[new_name] = value
            valid_dates[date_str] = renamed

    # 3. Interpolación de huecos (máx. 3 días consecutivos sin datos)
    # Primero, obtener la lista de fechas ordenadas con datos parciales
    dates_with_data = sorted(valid_dates.keys())

    # Para cada fecha, verificar qué variables tienen None y interpolar
    for date_str in dates_with_data:
        var_dict = valid_dates[date_str]
        for var_name in var_dict:
            if var_dict[var_name] is None:
                # Intentar interpolación con fechas vecinas
                var_dict[var_name] = _interpolate_value(df, valid_dates, date_str, var_name)

    # 4. Clausura precipitación a >= 0
    for date_str in valid_dates:
        if "precip_mm" in valid_dates[date_str] and valid_dates[date_str]["precip_mm"] is not None:
            if valid_dates[date_str]["precip_mm"] < 0:
                valid_dates[date_str]["precip_mm"] = 0

    return valid_dates


def _interpolate_value(df, valid_dates, target_date_str, var_name):
    """Interpolación simple: promedio de vecinos dentro de 3 días."""
    target_dt = datetime.strptime(target_date_str, "%Y%m%d")

    # Buscar fecha anterior con dato no-None dentro de 3 días
    before_val = None
    before_dt = None
    after_val = None
    after_dt = None

    for date_str in valid_dates:
        if date_str == target_date_str:
            continue
        try:
            compare_dt = datetime.strptime(date_str, "%Y%m%d")
            diff = (compare_dt - target_dt).days

            if 0 < diff <= 3:  # Próximo vecino hacia adelante
                if valid_dates[date_str][var_name] is not None:
                    if after_val is None or diff < (after_dt - target_dt).days:
                        after_val = valid_dates[date_str][var_name]
                        after_dt = compare_dt
            elif -3 <= diff < 0:  # Próximo vecino hacia atrás
                if valid_dates[date_str][var_name] is not None:
                    if before_val is None or diff > (before_dt - target_dt).days:  # Mayor diff = más lejano
                        before_val = valid_dates[date_str][var_name]
                        before_dt = compare_dt
        except ValueError:
            continue

    # Promedio ponderado por distancia (más cercano = más peso)
    if before_val is not None and after_val is not None:
        before_dist = (target_dt - before_dt).days if before_dt else 1
        after_dist = (after_dt - target_dt).days if after_dt else 1
        # Peso inverso a la distancia
        total_dist = before_dist + after_dist
        if total_dist > 0:
            result = (before_val * after_dist + after_val * before_dist) / total_dist
        else:
            result = (before_val + after_val) / 2
    elif before_val is not None:
        result = before_val
    elif after_val is not None:
        result = after_val
    else:
        result = None

    return result


def monthly_features(df):
    """
    Genera características mensuales a partir de datos diarios limpios.
    Retorna un diccionario {year_month: {estadisticas}}.
    """
    # Acumuladores por mes
    monthly_acc = {}

    for date_str in df:
        var_dict = df[date_str]
        try:
            dt = datetime.strptime(date_str, "%Y%m%d")
            year_month = f"{dt.year}-{dt.month:02d}"

            if year_month not in monthly_acc:
                monthly_acc[year_month] = {
                    "temp_means": [],
                    "temp_maxes": [],
                    "temp_mins": [],
                    "precips": [],
                    "rh": [],
                    "solar": [],
                    "soil_surface": [],
                    "soil_root": [],
                    "evap": [],
                    "frost_count": 0,
                    "heat_count": 0,
                    "total_days": 0,
                }

            monthly_acc[year_month]["total_days"] += 1

            # Acumular valores (manejar None)
            for var_key, out_key in [
                ("temp_mean_c", "temp_means"),
                ("temp_max_c", "temp_maxes"),
                ("temp_min_c", "temp_mins"),
                ("precip_mm", "precips"),
                ("rh_pct", "rh"),
                ("solar_kwh_m2", "solar"),
                ("soil_wet_surface", "soil_surface"),
                ("soil_wet_root", "soil_root"),
                ("evap_land_mm", "evap"),
            ]:
                val = var_dict.get(var_key)
                if val is not None:
                    monthly_acc[year_month][out_key].append(val)

            # Contar frost y heat days
            if "temp_min_c" in var_dict and var_dict["temp_min_c"] is not None:
                if var_dict["temp_min_c"] <= 0:
                    monthly_acc[year_month]["frost_count"] += 1
            if "temp_max_c" in var_dict and var_dict["temp_max_c"] is not None:
                if var_dict["temp_max_c"] >= 35:
                    monthly_acc[year_month]["heat_count"] += 1

        except ValueError:
            continue

    # Calcular promedios y estadísticas finales
    result = {}
    for year_month, acc in monthly_acc.items():
        # Calcular temperature mean promedio del mes
        all_temps = []
        for key in ["temp_means", "temp_maxes", "temp_mins"]:
            vals = acc[key]
            all_temps.extend([v for v in vals if v is not None])

        if all_temps:
            result[year_month] = {
                "temp_mean_c": round(sum(all_temps) / len(all_temps), 2),
                "temp_max_c": round(max(all_temps), 2),
                "temp_min_c": round(min(all_temps), 2),
                "precip_mm_sum": round(sum(acc["precips"]), 2),
                "frost_days": acc["frost_count"],
                "heat_days_35": acc["heat_count"],
                "total_days": acc["total_days"],
                "month": int(year_month.split("-")[1]),
                "year": int(year_month.split("-")[0]),
            }
        else:
            result[year_month] = {
                "temp_mean_c": None,
                "temp_max_c": None,
                "temp_min_c": None,
                "precip_mm_sum": 0,
                "frost_days": 0,
                "heat_days_35": 0,
                "total_days": 0,
                "month": int(year_month.split("-")[1]),
                "year": int(year_month.split("-")[0]),
            }

    return result


def save_daily_csv(df, path):
    """Guarda la serie diaria COMPLETA en CSV.

    Nota: df ya tiene las variables renombradas (temp_mean_c, ...), por lo
    que hay que iterar sobre los valores de VAR_MAP, no sobre sus claves.
    """
    var_names = list(VAR_MAP.values())
    with open(path, "w", encoding="utf-8") as f:
        f.write("date," + ",".join(var_names) + "\n")
        for date_str in sorted(df.keys()):
            var_dict = df[date_str]
            row = date_str
            for var_name in var_names:
                val = var_dict.get(var_name)
                row += "," + ("" if val is None else str(val))
            f.write(row + "\n")


def save_monthly_csv(monthly, path):
    """Guarda features mensuales en CSV."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("year_month,temp_mean_c,precip_mm_sum,frost_days,heat_days_35,total_days\n")
        for year_month in sorted(monthly.keys()):
            d = monthly[year_month]
            f.write(f"{year_month},{d['temp_mean_c']},{d['precip_mm_sum']},{d['frost_days']},{d['heat_days_35']},{d['total_days']}\n")


if __name__ == "__main__":
    print("=== PASO 4: Limpieza y generation de features ===")
    print(f"Región piloto: {PILOT['name']} ({PILOT['lat']}, {PILOT['lon']})")

    # Cargar datos
    print("Cargando datos...")
    df = load_power()
    print(f"Estructura: {len(df)} fechas con {len(df[list(df.keys())[0]])} variables cada una")

    # Limpiar
    print("Limpiando datos...")
    daily = clean(df)
    print(f"Fechas después de limpiez: {len(daily)}")

    # Generar features mensuales
    print("Generando features mensuales...")
    monthly = monthly_features(daily)
    print(f"Meses calculados: {len(monthly)}")

    # Guardar daily CSV (muestra)
    daily_path = PROCESSED / "power_daily.csv"
    save_daily_csv(daily, daily_path)
    print(f"Daily sample guardado en: {daily_path}")

    # Guardar monthly CSV
    monthly_path = PROCESSED / "power_monthly.csv"
    save_monthly_csv(monthly, monthly_path)
    print(f"Monthly guardado en: {monthly_path}")

    # Resumen de faltantes
    total_cells = len(daily) * len(VAR_MAP)
    none_cells = sum(1 for d in daily.values() for v in d.values() if v is None)
    # Restar las que eran -999 originales (ahora None)
    # Calcular porcentaje de huecos después de interpolación
    gap_pct = round(none_cells / total_cells * 100, 2) if total_cells > 0 else 0

    print(f"\n=== RESUMEN ===")
    print(f"Total de celdas fecha-variable: {total_cells}")
    print(f"Celdas con datos None (faltantes): {none_cells}")
    print(f"% de huecos en la tabla: {gap_pct}%")
    print(f"Meses con features: {len(monthly)}")

    # Mostrar algunas estadísticas de ejemplo
    print("\nEjemplo de features mensuales (primeros 3):")
    for i, (ym, data) in enumerate(sorted(monthly.items())):
        if i >= 3:
            break
        print(f"  {ym}: temp_mean={data['temp_mean_c']:.1f}°C, "
              f"precip={data['precip_mm_sum']:.1f}mm, "
              f"frost={data['frost_days']} días, heat={data['heat_days_35']} días, "
              f"total_días={data['total_days']}")