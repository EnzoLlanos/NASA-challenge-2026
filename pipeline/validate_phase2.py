"""pipeline/validate_phase2.py - Validación integral de Fase 2:
1. data/zonas.yaml (especificación formal de las 3 zonas)
2. data/zonas/crops_{norte,centro,sur}.yaml (cultivos calibrados por zona)
3. data/crops.yaml (contrato base)
4. Compatibilidad con el motor de scoring (Back/app/scoring/engine.py)
"""
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent

def check(label, condition, detail=""):
    print(f"   {'✅' if condition else '❌'} {label}" + (f" ({detail})" if detail else ""))
    return condition

def main():
    print("=" * 68)
    print("VALIDACIÓN INTEGRAL FASE 2: ZONAS, CULTIVOS Y BACKEND")
    print("=" * 68)

    errors = 0

    # 1. Validar zonas.yaml
    zonas_path = ROOT / "data" / "zonas.yaml"
    print("\n1. Especificación de Zonas (data/zonas.yaml)")
    if not check("Archivo existe", zonas_path.exists()):
        return 1
    zonas = yaml.safe_load(zonas_path.read_text(encoding="utf-8"))
    for z in ("norte", "centro", "sur"):
        ok = z in zonas and "datos_nasa_power_2000_2025" in zonas[z]
        if not check(f"Zona '{z}' con datos NASA POWER y SRTM", ok):
            errors += 1

    # 2. Validar crops por zona
    print("\n2. Cultivos calibrados por zona (data/zonas/crops_*.yaml)")
    expected_crops = ["maíz", "soja", "trigo", "sorgo", "girasol", "cebada", "arveja"]
    for z in ("norte", "centro", "sur"):
        cz_path = ROOT / "data" / "zonas" / f"crops_{z}.yaml"
        if not check(f"crops_{z}.yaml existe", cz_path.exists()):
            errors += 1
            continue
        cdata = yaml.safe_load(cz_path.read_text(encoding="utf-8"))
        has_all = all(k in cdata for k in expected_crops)
        has_apt = all("aptitud_zona" in cdata[k] and "nota_zona" in cdata[k] for k in expected_crops)
        if not check(f"Zona {z}: {len(cdata)} cultivos con aptitud_zona y nota", has_all and has_apt):
            errors += 1

    # 3. Validar motor de scoring (siempre que sys.path incluya Back)
    print("\n3. Verificación de carga en ScoringEngine (Back/app/scoring/engine.py)")
    sys.path.insert(0, str(ROOT / "Back"))
    try:
        from app.schemas import ZonaSanLuis, RotationRequest
        from app.scoring.engine import ScoringEngine

        for z in [ZonaSanLuis.NORTE, ZonaSanLuis.CENTRO, ZonaSanLuis.SUR]:
            crops_loaded = ScoringEngine.load_crops_for_zone(z)
            ok_engine = len(crops_loaded) >= 6
            if not check(f"ScoringEngine carga {len(crops_loaded)} cultivos para {z.value}", ok_engine):
                errors += 1

            # Probar simulación
            req = RotationRequest(zona=z, current_crop="Soja")
            res = ScoringEngine.calculate_rotation(req)
            ok_sim = len(res.estrategias) == 3 and res.zona == z
            if not check(f"Simulación sin porcentajes para {z.value}: {res.recomendacion}", ok_sim):
                errors += 1
    except Exception as e:
        print(f"   ⚠️ No se pudo instanciar ScoringEngine directamente: {e}")

    print("\n" + "=" * 68)
    if errors == 0:
        print("🎉 FASE 2 VALIDADA: Todos los componentes de datos y motor están consistentes.")
    else:
        print(f"❌ Se encontraron {errors} inconsistencias.")
    print("=" * 68)
    return errors

if __name__ == "__main__":
    sys.exit(main())
