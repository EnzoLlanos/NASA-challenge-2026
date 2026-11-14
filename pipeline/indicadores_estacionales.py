"""
indicadores_estacionales.py - Análisis de tendencias climáticas para San Luis, Argentina

Script que calcula indicadores a 26 años (2000-2025) desde los datos NASA POWER
procesados en power_monthly.csv. Estos indicadores serán usados por el backend
para el motor de puntuación de rotaciones de cultivos.

Datos de entrada: data/processed/power_monthly.csv (formato: year_month, temp_mean_c, precip_mm_sum, frost_days, heat_days_35, total_days)
Salida: Diccionario de indicadores impreso en consola y guardado en JSON
"""

import csv
import json
import sys
from pathlib import Path
from collections import defaultdict

# Consolas Windows (cp1252) no pueden imprimir símbolos como ≤ sin esto
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# Rutas
PROCESSED = Path('data/processed')
MONTHLY_CSV = PROCESSED / 'power_monthly.csv'


def parse_year_month(ym_str):
    """Parsear '2000-01' -> (2000, 1)."""
    parts = ym_str.split('-')
    return int(parts[0]), int(parts[1])


def load_data():
    """Cargar datos mensuales procesados desde CSV."""
    rows = []
    with open(MONTHLY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    
    print(f"Datos cargados: {len(rows)} meses ({rows[0]['year_month']}-{rows[-1]['year_month']})")
    return rows


def calculate_annual_precip_trend(rows):
    """Calculate annual rainfall trend from CSV rows."""
    # Agrupar por año
    rain_by_year = defaultdict(float)
    for row in rows:
        year, month = parse_year_month(row['year_month'])
        precip = float(row['precip_mm_sum'])
        rain_by_year[year] += precip
    
    years_sorted = sorted(rain_by_year.keys())
    first_year = years_sorted[0]
    last_year = years_sorted[-1]
    first_rain = rain_by_year[first_year]
    last_rain = rain_by_year[last_year]
    
    trend = "aumento" if last_rain > first_rain else "reducción"
    total = sum(rain_by_year.values())
    
    # Valores por año
    yearly_values = {str(y): round(rain_by_year[y], 1) for y in years_sorted}
    
    return {
        "annual_total_mm": round(total, 1),
        "trend": trend,
        "year_start": first_year,
        "year_end": last_year,
        "yearly_values": yearly_values
    }


def calculate_heat_days_by_decade(rows):
    """Calculate days of heat (>35°C) per decade."""
    # Agrupar por década
    heat_by_decade = defaultdict(int)
    for row in rows:
        year, month = parse_year_month(row['year_month'])
        heat = int(row['heat_days_35'])
        decade = (year // 10) * 10
        heat_by_decade[decade] += heat
    
    decades_sorted = sorted(heat_by_decade.keys())
    first_decade = decades_sorted[0]
    last_decade = decades_sorted[-1]
    
    trend = "aumento" if heat_by_decade[last_decade] > heat_by_decade[first_decade] else "reducción"
    
    result = {}
    for d in decades_sorted:
        result[str(d)] = heat_by_decade[d]
    
    result["trend"] = trend
    result["first_decade"] = first_decade
    result["last_decade"] = last_decade
    return result


def calculate_frost_days_by_decade(rows):
    """Calculate days of frost (≤0°C) per decade."""
    frost_by_decade = defaultdict(int)
    for row in rows:
        year, month = parse_year_month(row['year_month'])
        frost = int(row['frost_days'])
        decade = (year // 10) * 10
        frost_by_decade[decade] += frost
    
    decades_sorted = sorted(frost_by_decade.keys())
    first_decade = decades_sorted[0]
    last_decade = decades_sorted[-1]
    
    trend = "aumento" if frost_by_decade[last_decade] > frost_by_decade[first_decade] else "reducción"
    
    result = {}
    for d in decades_sorted:
        result[str(d)] = frost_by_decade[d]
    
    result["trend"] = trend
    result["first_decade"] = first_decade
    result["last_decade"] = last_decade
    return result


def calculate_summer_statistics(rows):
    """Calculate summer (DJF) statistics."""
    # Diciembre=12, Enero=1, Febrero=2
    summer_years = set()
    summer_temp_sum = 0
    summer_precip_sum = 0
    summer_frost_sum = 0
    summer_heat_sum = 0
    summer_count = 0
    
    for row in rows:
        year, month = parse_year_month(row['year_month'])
        if month in [12, 1, 2]:  # DJF
            summer_years.add(year)
            summer_temp_sum += float(row['temp_mean_c'])
            summer_precip_sum += float(row['precip_mm_sum'])
            summer_frost_sum += int(row['frost_days'])
            summer_heat_sum += int(row['heat_days_35'])
            summer_count += 1
    
    if summer_count == 0:
        return None
    
    result = {
        "temp_mean_c": round(summer_temp_sum / summer_count, 2),
        "precip_mm_sum": round(summer_precip_sum / summer_count, 2),
        "frost_days_mean": round(summer_frost_sum / summer_count, 1),
        "heat_days_35_mean": round(summer_heat_sum / summer_count, 1),
        "total_months": summer_count,
        "years_covered": f"{min(summer_years)}-{max(summer_years)}"
    }
    return result


def calculate_dry_wet_balance(rows):
    """Calculate dry vs wet months balance."""
    # Dry: precip < 50mm, Wet: precip >= 100mm
    dry_count = 0
    wet_count = 0
    total = len(rows)
    
    for row in rows:
        precip = float(row['precip_mm_sum'])
        if precip < 50:
            dry_count += 1
        elif precip >= 100:
            wet_count += 1
    
    normal_count = total - dry_count - wet_count
    
    return {
        "dry_months": dry_count,
        "dry_percentage": round(dry_count / total * 100, 1) if total > 0 else 0,
        "wet_months": wet_count,
        "wet_percentage": round(wet_count / total * 100, 1) if total > 0 else 0,
        "normal_months": normal_count,
        "total_months": total
    }


def main():
    print("=== INDICADORES ESTACIONALES PARA SAN LUIS, ARGENTINA ===")
    print(f"Período: 2000-2025 (26 años)")
    print()
    
    rows = load_data()
    
    # 1. Tendencia de lluvia anual
    print("1. TENDENCIA ANUAL DE LLUVIA")
    precip_data = calculate_annual_precip_trend(rows)
    print(f"   - Lluvia total 2000-2025: {precip_data['annual_total_mm']} mm")
    print(f"   - Tendencia: {precip_data['trend']}")
    print(f"   - Años: {precip_data['year_start']}-{precip_data['year_end']}")
    # Print a few year values
    year_vals = precip_data['yearly_values']
    items = list(year_vals.items())[:3]
    for y, v in items:
        print(f"   - {y}: {v} mm")
    if len(year_vals) > 3:
        print(f"   - ... y {len(year_vals)-3} años más")
    print()
    
    # 2. Días de calor por década
    print("2. DÍAS DE CALOR EXTREMO (>35°C) POR DÉCADA")
    heat_data = calculate_heat_days_by_decade(rows)
    print(f"   - Década {heat_data['first_decade']}-{heat_data['first_decade']+9}: {heat_data[list(heat_data.keys())[0]]} días")
    print(f"   - Década {heat_data['last_decade']}-{heat_data['last_decade']+9}: {heat_data[list(heat_data.keys())[-1]]} días")
    print(f"   - Tendencia general: {heat_data['trend']}")
    # Print each decade
    for d in sorted([k for k in heat_data.keys() if k not in ['trend', 'first_decade', 'last_decade']]):
        print(f"   - Década {d}-{int(d)+9}: {heat_data[d]} días")
    print()
    
    # 3. Días de helada por década
    print("3. DÍAS DE HELADA (temp ≤ 0°C) POR DÉCADA")
    frost_data = calculate_frost_days_by_decade(rows)
    print(f"   - Década {frost_data['first_decade']}-{frost_data['first_decade']+9}: {frost_data[list(frost_data.keys())[0]]} días")
    print(f"   - Década {frost_data['last_decade']}-{frost_data['last_decade']+9}: {frost_data[list(frost_data.keys())[-1]]} días")
    print(f"   - Tendencia general: {frost_data['trend']}")
    for d in sorted([k for k in frost_data.keys() if k not in ['trend', 'first_decade', 'last_decade']]):
        print(f"   - Década {d}-{int(d)+9}: {frost_data[d]} días")
    print()
    
    # 4. Estadísticas estivales (DJF)
    print("4. PROMEDIO ESTIVAL (DJF: DICIEMBRE-ENERO-FEBRERO)")
    summer = calculate_summer_statistics(rows)
    if summer:
        print(f"   - Temp media estival: {summer['temp_mean_c']} °C")
        print(f"   - Precipitación estival: {summer['precip_mm_sum']} mm/mes")
        print(f"   - Días de helada estival: {summer['frost_days_mean']} días/mes")
        print(f"   - Días de calor estival: {summer['heat_days_35_mean']} días/mes")
        print(f"   - Años cubiertos: {summer['years_covered']}")
    print()
    
    # 5. Estación seca vs. húmeda
    print("5. ESTACIÓN SECA vs. HÚMEDA")
    dry_wet = calculate_dry_wet_balance(rows)
    print(f"   - Meses secos (<50mm): {dry_wet['dry_months']} ({dry_wet['dry_percentage']}%)")
    print(f"   - Meses húmedos (>=100mm): {dry_wet['wet_months']} ({dry_wet['wet_percentage']}%)")
    print(f"   - Meses normales: {dry_wet['normal_months']}")
    print()
    
    # Resumen ejecutivo
    print("6. RESUMEN EJECUTIVO")
    all_indicators = {
        "annual_precip_mm": precip_data['annual_total_mm'],
        "precip_trend": precip_data['trend'],
        "heat_days_by_decade": {k: v for k, v in heat_data.items() if k not in ['trend', 'first_decade', 'last_decade']},
        "heat_trend": heat_data['trend'],
        "frost_days_by_decade": {k: v for k, v in frost_data.items() if k not in ['trend', 'first_decade', 'last_decade']},
        "frost_trend": frost_data['trend'],
        "summer_temp_mean_c": summer['temp_mean_c'] if summer else None,
        "summer_precip_mm": summer['precip_mm_sum'] if summer else None,
        "dry_months_pct": dry_wet['dry_percentage'],
        "wet_months_pct": dry_wet['wet_percentage']
    }
    
    print("\nJSON con todos los indicadores:")
    print(json.dumps(all_indicators, indent=2))
    
    # Guardar también a archivo JSON
    output_path = Path('indicadores_calculados.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_indicators, f, indent=2)
    print(f"\n📁 Indicadores guardados en: {output_path}")


if __name__ == "__main__":
    main()