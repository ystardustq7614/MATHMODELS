from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "modeling"))
from core_solver import simulate_fvm_fixed, simulate_fvm_moving

root = Path(__file__).resolve().parents[3]
d = pd.read_csv(root / "paper_output/data_cleaned/a_environment.csv")
t, T, C = d.time_s.to_numpy(float), d.temperature_K.to_numpy(float), d.air_moisture_kgkg.to_numpy(float)
kind, n, dt, total, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5])
if kind == "tail2":
    t = np.r_[t, np.arange(t[-1] + 60, total + 1, 60)]; T = np.r_[T, np.full(len(t) - len(d), T[-10:].mean())]; C = np.r_[C, np.full(len(t) - len(d), C[-10:].mean())]
if kind.startswith("moving"):
    x = simulate_fvm_moving(t, T, C, np.array([0., float(total)]), np.array([.02, .02]), total, sample_every_s=3600, N=n, dt=dt, stop_at_cmax=-1.)
    np.savez(out, T=x[2][-1], C=x[3][-1], end=x[4])
else:
    mode = int(kind[-1]); sample = 1800 if dt < 1.0 else (60 if total > 10000 else 1); x = simulate_fvm_fixed(t, T, C, total, mode, sample_every_s=sample, N=n, R=.02, h=25., hm=8e-7, dt=dt, stop_at_cmax=.15 if mode == 2 else -1.)
    np.savez(out, T=x[1][-1], C=x[2][-1], end=x[3])
