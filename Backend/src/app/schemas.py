# Redirección y compatibilidad con Back/app/schemas.py
import sys
from pathlib import Path

back_app = Path(__file__).resolve().parents[3] / "Back"
if str(back_app) not in sys.path:
    sys.path.insert(0, str(back_app))

from app.schemas import *  # noqa: F401, F403
