"""Run real solver comparisons for S6 convergence and sensitivity evidence."""
from __future__ import annotations

import hashlib
import json
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "paper_output" / "code" / "modeling"))
from core_solver import simulate_fvm_fixed, simulate_fvm_moving

DATA = ROOT / "paper_output" / "data_cleaned"
OUT = ROOT / "paper_output" / "qa" / "model_validation_checks.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def env():
    frame = pd.read_csv(DATA / "a_environment.csv")
    return (frame.time_s.to_numpy(float), frame.temperature_K.to_numpy(float), frame.air_moisture_kgkg.to_numpy(float))


def max_common_difference(a: np.ndarray, b: np.ndarray, n_a: int, n_b: int) -> float:
    ra = (np.arange(n_a) + 0.5) * 0.02 / n_a
    rb = (np.arange(n_b) + 0.5) * 0.02 / n_b
    common = np.linspace(ra[0], ra[-1], n_a)
    return float(np.max(np.abs(np.interp(common, rb, b) - np.interp(common, ra, a))))


def worker(kind: str, n: int, dt: float, total: int, output: Path) -> dict[str, np.ndarray]:
    code = (ROOT / "paper_output" / "code" / "visualization" / "solver_worker.py")
    subprocess.run([sys.executable, str(code), kind, str(n), str(dt), str(total), str(output)], check=True)
    with np.load(output) as data:
        return {key: data[key].copy() for key in data.files}


def main() -> None:
    tmp = ROOT / "paper_output" / "qa" / "_validation_tmp.npz"
    b0 = worker("fixed1", 80, 1.0, 1800, tmp); T0, C0 = b0["T"], b0["C"]
    bf = worker("fixed1", 160, 1.0, 1800, tmp); Tf, Cf = bf["T"], bf["C"]
    bt = worker("fixed1", 80, 0.5, 1800, tmp); Tt, Ct = bt["T"], bt["C"]
    base = {"N": 80, "dt_s": 1.0, "total_seconds": 1800, "formula_mode": 1}
    spatial = {"N": 160, "dt_s": 1.0, "total_seconds": 1800, "formula_mode": 1}
    temporal = {"N": 80, "dt_s": 0.5, "total_seconds": 1800, "formula_mode": 1}
    convergence = {
        "tolerance": 0.05,
        "baseline": {"config": base},
        "baseline_terminal_center_surface": {"T_C": [float(T0[0] - 273.15), float(T0[-1] - 273.15)], "C": [float(C0[0]), float(C0[-1])]},
        "spatial_refinement": {"config": spatial, "max_abs_T_K": max_common_difference(T0, Tf, 80, 160), "max_abs_C": max_common_difference(C0, Cf, 80, 160)},
        "temporal_refinement": {"config": temporal, "max_abs_T_K": float(np.max(np.abs(T0 - Tt))), "max_abs_C": float(np.max(np.abs(C0 - Ct)))},
    }
    convergence["pass"] = all(value <= convergence["tolerance"] for key in ("spatial_refinement", "temporal_refinement") for value in (convergence[key]["max_abs_T_K"], convergence[key]["max_abs_C"]))

    te, Te, Ce = env()
    tail_T = float(np.mean(Te[-10:])); tail_C = float(np.mean(Ce[-10:]))
    boundary_total = 206433
    bd = worker("fixed2", 80, 1.0, boundary_total, tmp); be = worker("tail2", 80, 1.0, boundary_total, tmp)
    end_d, end_e = float(bd["end"]), float(be["end"])
    boundary = {"tolerance_relative": 0.02, "default_boundary": "hold_last_value", "tail_extension": {"tail_samples": 10, "T_air_K": tail_T, "C_air": tail_C, "end_time_s": boundary_total}, "default_threshold_time_s": float(end_d), "tail_extension_threshold_time_s": float(end_e)}
    boundary["relative_difference"] = abs(end_e - end_d) / end_d
    boundary["pass"] = boundary["relative_difference"] <= boundary["tolerance_relative"]

    total = 3600
    fixed = worker("fixed3", 80, 1.0, total, tmp); moving = worker("moving3", 80, 1.0, total, tmp)
    Tfix, Cfix, Tmov, Cmov = fixed["T"], fixed["C"], moving["T"], moving["C"]
    degeneration = {"config": {"N": 80, "dt_s": 1.0, "total_seconds": total, "formula_mode": 3, "radius_m": 0.02}, "tolerance": 1e-10, "terminal_max_abs_T_K": float(np.max(np.abs(Tfix - Tmov))), "terminal_max_abs_C": float(np.max(np.abs(Cfix - Cmov)))}
    degeneration["pass"] = degeneration["terminal_max_abs_T_K"] <= degeneration["tolerance"] and degeneration["terminal_max_abs_C"] <= degeneration["tolerance"]

    result = {"schema_version": "1.0", "generated_by": "paper_output/code/visualization/run_numerical_validation.py", "generated_at": datetime.now(timezone.utc).isoformat(), "inputs": {"environment": {"path": "paper_output/data_cleaned/a_environment.csv", "sha256": digest(DATA / "a_environment.csv")}, "solver": {"path": "paper_output/code/modeling/core_solver.py", "sha256": digest(ROOT / "paper_output/code/modeling/core_solver.py")}, "validation_script": {"path": "paper_output/code/visualization/run_numerical_validation.py", "sha256": digest(Path(__file__))}, "worker": {"path": "paper_output/code/visualization/solver_worker.py", "sha256": digest(Path(__file__).with_name("solver_worker.py"))}}, "checks": {"aq1_convergence": convergence, "aq3_boundary_extension": boundary, "aq4_fixed_moving_degeneracy": degeneration}}
    result["status"] = "PASS" if all(item["pass"] for item in result["checks"].values()) else "FAIL"
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    metrics_path = ROOT / "paper_output" / "results" / "metrics.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8")); metrics["validation_generated_by"] = "paper_output/code/visualization/run_numerical_validation.py"; metrics["generated_by"] = "paper_output/code/modeling/result_contract_io.py"; metrics["items"] = [x for x in metrics["items"] if not str(x.get("metric_name", "")).startswith("validation_")]
    values = [("AQ1", "aq1_spatial_T_max_abs", convergence["spatial_refinement"]["max_abs_T_K"], "K"), ("AQ1", "aq1_spatial_C_max_abs", convergence["spatial_refinement"]["max_abs_C"], "kg/kg"), ("AQ1", "aq1_spatial_pass", int(convergence["pass"]), "boolean"), ("AQ1", "aq1_temporal_T_max_abs", convergence["temporal_refinement"]["max_abs_T_K"], "K"), ("AQ1", "aq1_temporal_C_max_abs", convergence["temporal_refinement"]["max_abs_C"], "kg/kg"), ("AQ1", "aq1_temporal_pass", int(convergence["pass"]), "boolean"), ("AQ3", "aq3_default_threshold_time_s", boundary["default_threshold_time_s"], "s"), ("AQ3", "aq3_tail_mean_threshold_time_s", boundary["tail_extension_threshold_time_s"], "s"), ("AQ3", "aq3_boundary_relative_difference", boundary["relative_difference"], "fraction"), ("AQ3", "aq3_boundary_pass", int(boundary["pass"]), "boolean"), ("AQ4", "aq4_fixed_moving_T_max_abs", degeneration["terminal_max_abs_T_K"], "K"), ("AQ4", "aq4_fixed_moving_C_max_abs", degeneration["terminal_max_abs_C"], "kg/kg"), ("AQ4", "aq4_fixed_moving_pass", int(degeneration["pass"]), "boolean")]
    for qid, name, value, unit in values:
        metrics["items"].append({"question_id": qid, "status": "computed", "metric_name": f"validation_{name}", "metric_role": "validation", "value": value, "unit": unit, "source": "paper_output/qa/model_validation_checks.json"})
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    if tmp.exists(): tmp.unlink()


if __name__ == "__main__":
    main()
