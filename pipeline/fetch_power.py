import json
import requests
from common import RAW, PILOT, START, END

URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

PARAMS = {
    "parameters": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN,GWETTOP,GWETROOT,EVLAND",
    "community": "AG",
    "latitude": PILOT["lat"],
    "longitude": PILOT["lon"],
    "start": START,
    "end": END,
    "format": "JSON",
}

def main():
    out = RAW / f"power_{PILOT['name']}.json"
    if out.exists():                      # caché: no volver a bajar
        print("ya existe", out)
        return
    r = requests.get(URL, params=PARAMS, timeout=120)
    r.raise_for_status()
    out.write_text(json.dumps(r.json()))
    print("guardado", out)

if __name__ == "__main__":
    main()