from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

# PILOT: San Luis, Argentina
# Coordinates for San Luis province center
PILOT = {"name": "san_luis_argentina", "lat": -33.30, "lon": -65.30}

START = "20000101"   # POWER usa YYYYMMDD
END = "20251231"