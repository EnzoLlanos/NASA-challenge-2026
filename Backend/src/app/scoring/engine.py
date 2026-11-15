# Redirección y compatibilidad con Back/app/scoring/engine.py
import sys
from pathlib import Path

back_app = Path(__file__).resolve().parents[4] / "Back"
if str(back_app) not in sys.path:
    sys.path.insert(0, str(back_app))

from app.scoring.engine import ScoringEngine, calculate_rotation_for_zone  # noqa: F401

__all__ = ["ScoringEngine", "calculate_rotation_for_zone"]
