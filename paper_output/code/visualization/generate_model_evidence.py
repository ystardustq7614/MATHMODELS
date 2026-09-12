"""Generate reproducible AQ1-AQ4 figures."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "paper_output"
TABLES = OUT / "tables"
FIGURES = OUT / "figures"


def read_csv(name: str) -> tuple[list[str], list[list[float]]]:
    with (TABLES / name).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    header = rows[0]
    values = []
    for row in rows[1:]:
        parsed = []
        if row[0].startswith('烘干结束时间'):
            row[0]=re.search(r'([0-9.]+) h',row[0]).group(1)
        for value in row:
            try:
                parsed.append(float(value))
            except ValueError:
                parsed.append(math.nan)
        if parsed and math.isfinite(parsed[0]):
            values.append(parsed)
    return header, values


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(fig: plt.Figure, name: str) -> Path:
    path = FIGURES / name
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    _, q1t = read_csv("table_aq1_temperature.csv")
    _, q1m = read_csv("table_aq1_moisture.csv")
    q2t_h, q2t = read_csv("table_aq2_temperature.csv")
    _, q2m = read_csv("table_aq2_moisture.csv")
    _, q3 = read_csv("table_aq3_drying_moisture.csv")
    _, q4 = read_csv("table_aq4_shrinkage_moisture.csv")

    # AQ1: temporal evolution of centre/surface temperature and moisture.
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    t = [row[0] / 60 for row in q1t]
    axes[0].plot(t, [row[1] for row in q1t], label="center")
    axes[0].plot(t, [row[-1] for row in q1t], label="surface")
    axes[0].set(xlabel="Time (min)", ylabel="Temperature (°C)", title="AQ1 temperature field")
    axes[1].plot([row[0] / 60 for row in q1m], [row[1] for row in q1m], label="center")
    axes[1].plot([row[0] / 60 for row in q1m], [row[-1] for row in q1m], label="surface")
    axes[1].set(xlabel="Time (min)", ylabel="Dry-basis moisture", title="AQ1 moisture field")
    for axis in axes:
        axis.legend(); axis.grid(alpha=0.25)
    p1 = save(fig, "fig_aq1_fields.png")

    # AQ2: radial profiles at each reported time.
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    radius = [float(label.split()[0]) for label in q2t_h[1:]]
    for row in q2t:
        axes[0].plot(radius, row[1:], marker="o", label=f"{row[0]:g} h")
    for row in q2m:
        axes[1].plot(radius, row[1:], marker="o", label=f"{row[0]:g} h")
    axes[0].set(xlabel="Radius (cm)", ylabel="Temperature (°C)", title="AQ2 radial temperature")
    axes[1].set(xlabel="Radius (cm)", ylabel="Dry-basis moisture", title="AQ2 radial moisture")
    for axis in axes:
        axis.legend(fontsize=7); axis.grid(alpha=0.25)
    p2 = save(fig, "fig_aq2_profiles.png")

    # AQ3: whole-domain maximum versus threshold.
    fig, axis = plt.subplots(figsize=(6, 4))
    hours = [row[0] for row in q3]
    maxima = [max(value for value in row[1:] if math.isfinite(value)) for row in q3]
    axis.plot(hours, maxima, marker="o", label="domain maximum")
    axis.axhline(0.15, color="crimson", linestyle="--", label="threshold 0.15")
    axis.set(xlabel="Time (h)", ylabel="Dry-basis moisture", title="AQ3 drying threshold")
    axis.grid(alpha=0.25); axis.legend()
    p3 = save(fig, "fig_aq3_threshold.png")

    # AQ4: moving boundary and moisture profiles.
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    hours = [row[0] for row in q4]
    axes[0].plot(hours, [row[-1] for row in q4], marker="o", color="black")
    axes[0].set(xlabel="Time (h)", ylabel="Radius (cm)", title="AQ4 shrinking domain")
    for row in q4:
        values = [value for value in row[1:5] if math.isfinite(value)]
        axes[1].plot([.5*i for i in range(len(values))]+[row[-1]], values+[row[-2]], marker="o", label=f"{row[0]:g} h")
    axes[1].set(xlabel="Radius (cm)", ylabel="Dry-basis moisture", title="AQ4 moisture profiles")
    axes[1].legend(fontsize=7); axes[0].grid(alpha=0.25); axes[1].grid(alpha=0.25)
    p4 = save(fig, "fig_aq4_shrinkage.png")

    # Numerical validation is produced by run_numerical_validation.py; keep it separate from plotting.
    source_map = {
        "fig_aq1_fields": (p1, ["AQ1"], "table_aq1_temperature.csv"),
        "fig_aq2_profiles": (p2, ["AQ2"], "table_aq2_temperature.csv"),
        "fig_aq3_threshold": (p3, ["AQ3"], "table_aq3_drying_moisture.csv"),
        "fig_aq4_shrinkage": (p4, ["AQ4"], "table_aq4_shrinkage_moisture.csv"),
    }
    existing = json.loads((OUT / "figure_index.json").read_text(encoding="utf-8")) if (OUT / "figure_index.json").exists() else {}
    index = {"schema_version": "1.0", "generated_at": datetime.now(timezone.utc).isoformat(), "generated_by": "paper_output/code/visualization/generate_model_evidence.py", "figures": existing.get("figures", [])}
    for fid, source, qids in (("fig_a_environment", "a_environment.csv", ["AQ1", "AQ2", "AQ3", "AQ4"]), ("fig_a_radius", "a_radius.csv", ["AQ4"])):
        path = OUT / "figures" / f"{fid}.png"
        data = OUT / "data_cleaned" / source
        if path.exists() and data.exists() and not any(x.get("figure_id") == fid for x in index["figures"]):
            index["figures"].append({"figure_id": fid, "title": fid, "path": path.relative_to(ROOT).as_posix(), "expected_path": path.relative_to(ROOT).as_posix(), "question_ids": qids, "source_data": data.relative_to(ROOT).as_posix(), "source_sha256": sha256(data), "sha256": sha256(path), "bytes": path.stat().st_size, "status": "generated", "ok": True, "exists": True, "placeholder": False, "evidence_type": "input_observation"})
    for figure_id, (path, qids, source) in source_map.items():
        item = {"figure_id": figure_id, "title": figure_id, "path": path.relative_to(ROOT).as_posix(), "expected_path": path.relative_to(ROOT).as_posix(), "question_ids": qids, "question_id": qids[0], "source_data": f"paper_output/tables/{source}", "source_sha256": sha256(TABLES / source), "sha256": sha256(path), "bytes": path.stat().st_size, "status": "generated", "ok": True, "exists": True, "placeholder": False, "evidence_type": "model_result"}
        index["figures"] = [x for x in index["figures"] if x.get("figure_id") != figure_id] + [item]
    (OUT / "figure_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
