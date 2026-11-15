"""Descarga NASA POWER para las zonas Norte y Sur (Centro ya existe) y genera
data/processed/power_monthly_<zona>.csv con las mismas columnas que
power_monthly.csv. Coordenadas desde data/zonas.yaml.

Uso:  python pipeline/fetch_power_zonas.py
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

import requests
import yaml

from common import RAW, PROCESSED, START, END

URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
VARS = "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN,GWETTOP,GWETROOT,EVLAND"
ZONAS = Path(__file__).resolve().parent.parent / "data" / "zonas.yaml"
COLS = ["year_month", "year", "month", "temp_mean_c", "temp_max_c", "temp_min_c",
        "precip_mm_sum", "frost_days", "heat_days_35", "soil_wet_root_mean",
        "evap_land_mm_sum", "total_days"]


def fetch(zona, lat, lon):
    out = RAW / f"power_{zona}.json"
    if out.exists():
        print("ya existe", out)
        return json.loads(out.read_text())
    r = requests.get(URL, params={"parameters": VARS, "community": "AG",
                                  "latitude": lat, "longitude": lon,
                                  "start": START, "end": END, "format": "JSON"},
                     timeout=180)
    r.raise_for_status()
    out.write_text(json.dumps(r.json()))
    print("guardado", out)
    return r.json()


def val(p, var, d):
    v = p.get(var, {}).get(d)
    return None if v is None or v <= -999 else v


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 3) if xs else ""


def monthly(raw):
    p = raw["properties"]["parameter"]
    by = defaultdict(list)
    for d in p["T2M"]:
        by[d[:6]].append(d)
    rows = []
    for ym in sorted(by):
        ds = by[ym]
        tmax = [val(p, "T2M_MAX", d) for d in ds]
        tmin = [val(p, "T2M_MIN", d) for d in ds]
        pr = [max(val(p, "PRECTOTCORR", d), 0) for d in ds if val(p, "PRECTOTCORR", d) is not None]
        ev = [val(p, "EVLAND", d) for d in ds if val(p, "EVLAND", d) is not None]
        rows.append([
            f"{ym[:4]}-{ym[4:]}", int(ym[:4]), int(ym[4:]),
            round(mean([val(p, "T2M", d) for d in ds]), 2) if mean([val(p, "T2M", d) for d in ds]) != "" else "",
            max([x for x in tmax if x is not None], default=""),
            min([x for x in tmin if x is not None], default=""),
            round(sum(pr), 2), sum(1 for x in tmin if x is not None and x < 0),
            sum(1 for x in tmax if x is not None and x >= 35),
            mean([val(p, "GWETROOT", d) for d in ds]), round(sum(ev), 2), len(ds)])
    return rows


def main():
    zonas = yaml.safe_load(ZONAS.read_text(encoding="utf-8"))
    for zona in ("norte", "sur"):
        pt = zonas[zona]["punto_referencia"]
        rows = monthly(fetch(zona, pt["lat"], pt["lon"]))
        path = PROCESSED / f"power_monthly_{zona}.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(COLS)
            w.writerows(rows)
        anual = sum(r[6] for r in rows) / (len(rows) / 12)
        print(f"{zona}: {len(rows)} meses, lluvia media ≈ {anual:.0f} mm/año -> {path}")


if __name__ == "__main__":
    main()
