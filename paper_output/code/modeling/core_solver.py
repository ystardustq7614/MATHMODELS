# Core solver module for radial finite volume method and Thomas algorithm
from __future__ import annotations

import numba
import numpy as np
import pandas as pd
from pathlib import Path


@numba.njit
def solve_thomas(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    n = len(d)
    cp = np.zeros(n, dtype=np.float64)
    dp = np.zeros(n, dtype=np.float64)
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        denom = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / denom if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / denom
    x = np.zeros(n, dtype=np.float64)
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


@numba.njit
def interp_env(t: float, t_env: np.ndarray, T_env: np.ndarray, C_env: np.ndarray) -> tuple[float, float]:
    if t <= 0.0:
        return T_env[0], C_env[0]
    if t >= t_env[-1]:
        return T_env[-1], C_env[-1]
    idx = int(t / 60.0)
    if idx >= len(t_env) - 1:
        return T_env[-1], C_env[-1]
    dt_seg = t_env[idx + 1] - t_env[idx]
    frac = (t - t_env[idx]) / dt_seg if dt_seg > 0.0 else 0.0
    T_air = T_env[idx] + frac * (T_env[idx + 1] - T_env[idx])
    C_e = C_env[idx] + frac * (C_env[idx + 1] - C_env[idx])
    return T_air, C_e


@numba.njit
def interp_radius(t: float, t_rad: np.ndarray, R_rad: np.ndarray) -> float:
    if t <= 0.0:
        return R_rad[0]
    if t >= t_rad[-1]:
        return R_rad[-1]
    idx = int(t / 1800.0)
    if idx >= len(t_rad) - 1:
        return R_rad[-1]
    dt_seg = t_rad[idx + 1] - t_rad[idx]
    frac = (t - t_rad[idx]) / dt_seg if dt_seg > 0.0 else 0.0
    return R_rad[idx] + frac * (R_rad[idx + 1] - R_rad[idx])


@numba.njit
def simulate_fvm_fixed(
    t_env: np.ndarray,
    T_env: np.ndarray,
    C_env: np.ndarray,
    total_seconds: int,
    formula_mode: int,  # 1 Appx 2 (AQ1), 2 Appx 3 (AQ2/AQ3), 3 Appx 4 fixed-domain reference only (AQ4)
    sample_every_s: int = 1,
    N: int = 80,
    R: float = 0.02,
    h: float = 25.0,
    hm: float = 8e-7,
    dt: float = 1.0,
    stop_at_cmax: float = -1.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, int]:
    dr = R / N
    r_faces = np.linspace(0.0, R, N + 1)
    vols = np.pi * (r_faces[1:]**2 - r_faces[:-1]**2)
    areas = 2.0 * np.pi * r_faces

    T = np.full(N, 301.15, dtype=np.float64)
    C = np.full(N, 2.55, dtype=np.float64)

    max_records = total_seconds // sample_every_s + 2
    times_out = np.zeros(max_records, dtype=np.float64)
    T_history = np.zeros((max_records, N), dtype=np.float64)
    C_history = np.zeros((max_records, N), dtype=np.float64)

    rec_idx = 0
    times_out[rec_idx] = 0.0
    T_history[rec_idx] = T
    C_history[rec_idx] = C
    rec_idx += 1

    D_face = np.zeros(N + 1, dtype=np.float64)
    k_face = np.zeros(N + 1, dtype=np.float64)

    a_C = np.zeros(N, dtype=np.float64)
    b_C = np.zeros(N, dtype=np.float64)
    c_C = np.zeros(N, dtype=np.float64)
    d_C = np.zeros(N, dtype=np.float64)

    a_T = np.zeros(N, dtype=np.float64)
    b_T = np.zeros(N, dtype=np.float64)
    c_T = np.zeros(N, dtype=np.float64)
    d_T = np.zeros(N, dtype=np.float64)

    t = 0.0
    step = 0
    actual_end_time = float(total_seconds)

    while t < total_seconds:
        t_next = t + dt
        T_air, C_e = interp_env(t_next, t_env, T_env, C_env)

        C_old = C.copy()
        T_old = T.copy()
        C_iter = C.copy()
        T_iter = T.copy()

        for _it in range(2):
            if formula_mode == 1:
                rho = np.full(N, 820.0, dtype=np.float64)
                cp = np.full(N, 2600.0, dtype=np.float64)
                k = np.full(N, 0.36, dtype=np.float64)
                D = 7.0e-9 * np.exp(-0.89 / C_iter)
            elif formula_mode == 2:
                rho = 650.0 + 128.0 * C_iter
                cp = 1450.0 + 2736.0 * (C_iter / (C_iter + 1.0))
                k = 0.21 + 0.38 * (C_iter / (C_iter + 1.0))
                D = 2.4e-3 * np.exp(-0.45 / C_iter - 3850.0 / T_iter)
            else:  # formula_mode=3: Appendix 4 fixed-domain reference
                rho = 760.0 + 90.0 * C_iter
                cp = 1850.0 + 2150.0 * (C_iter / (C_iter + 1.0))
                k = 0.12 + 0.20 * (C_iter / (C_iter + 1.0))
                D = 4.2e-4 * np.exp(-0.30 / C_iter - 3850.0 / T_iter)

            for i in range(1, N):
                D_face[i] = 2.0 * D[i - 1] * D[i] / (D[i - 1] + D[i])
            gamma_s = 1.0 / (1.0 / hm + 0.5 * dr / D[N - 1])

            for i in range(N):
                d_C[i] = vols[i] * C_old[i] / dt

            fl = areas[1] * D_face[1] / dr
            b_C[0] = vols[0] / dt + fl
            c_C[0] = -fl
            a_C[0] = 0.0

            for i in range(1, N - 1):
                fl = areas[i] * D_face[i] / dr
                fr = areas[i + 1] * D_face[i + 1] / dr
                a_C[i] = -fl
                b_C[i] = vols[i] / dt + fl + fr
                c_C[i] = -fr

            fl = areas[N - 1] * D_face[N - 1] / dr
            fr_s = areas[N] * gamma_s
            a_C[N - 1] = -fl
            b_C[N - 1] = vols[N - 1] / dt + fl + fr_s
            c_C[N - 1] = 0.0
            d_C[N - 1] += fr_s * C_e

            C_iter = solve_thomas(a_C, b_C, c_C, d_C)

            for i in range(1, N):
                k_face[i] = 2.0 * k[i - 1] * k[i] / (k[i - 1] + k[i])
            gamma_T_s = 1.0 / (1.0 / h + 0.5 * dr / k[N - 1])

            for i in range(N):
                d_T[i] = vols[i] * rho[i] * cp[i] * T_old[i] / dt

            fl_T = areas[1] * k_face[1] / dr
            b_T[0] = vols[0] * rho[0] * cp[0] / dt + fl_T
            c_T[0] = -fl_T
            a_T[0] = 0.0

            for i in range(1, N - 1):
                fl = areas[i] * k_face[i] / dr
                fr = areas[i + 1] * k_face[i + 1] / dr
                a_T[i] = -fl
                b_T[i] = vols[i] * rho[i] * cp[i] / dt + fl + fr
                c_T[i] = -fr

            fl = areas[N - 1] * k_face[N - 1] / dr
            fr_s = areas[N] * gamma_T_s
            a_T[N - 1] = -fl
            b_T[N - 1] = vols[N - 1] * rho[N - 1] * cp[N - 1] / dt + fl + fr_s
            c_T[N - 1] = 0.0
            d_T[N - 1] += fr_s * T_air

            T_iter = solve_thomas(a_T, b_T, c_T, d_T)

        C = C_iter
        T = T_iter
        t = t_next
        step += 1

        if step % sample_every_s == 0:
            times_out[rec_idx] = t
            T_history[rec_idx] = T
            C_history[rec_idx] = C
            rec_idx += 1

        if stop_at_cmax > 0.0 and C.max() < stop_at_cmax:
            actual_end_time = t
            if step % sample_every_s != 0:
                times_out[rec_idx] = t
                T_history[rec_idx] = T
                C_history[rec_idx] = C
                rec_idx += 1
            break

    return times_out[:rec_idx], T_history[:rec_idx], C_history[:rec_idx], actual_end_time, rec_idx


@numba.njit
def simulate_fvm_moving(
    t_env: np.ndarray,
    T_env: np.ndarray,
    C_env: np.ndarray,
    t_rad: np.ndarray,
    R_rad: np.ndarray,
    total_seconds: int,
    sample_every_s: int = 60,
    N: int = 80,
    h: float = 25.0,
    hm: float = 8e-7,
    dt: float = 1.0,
    stop_at_cmax: float = 0.15,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float, int]:
    dxi = 1.0 / N
    xi_faces = np.linspace(0.0, 1.0, N + 1)
    vols_xi = np.pi * (xi_faces[1:]**2 - xi_faces[:-1]**2)
    areas_xi = 2.0 * np.pi * xi_faces

    T = np.full(N, 301.15, dtype=np.float64)
    C = np.full(N, 2.55, dtype=np.float64)

    max_records = total_seconds // sample_every_s + 2
    times_out = np.zeros(max_records, dtype=np.float64)
    radius_out = np.zeros(max_records, dtype=np.float64)
    T_history = np.zeros((max_records, N), dtype=np.float64)
    C_history = np.zeros((max_records, N), dtype=np.float64)

    rec_idx = 0
    times_out[rec_idx] = 0.0
    radius_out[rec_idx] = R_rad[0]
    T_history[rec_idx] = T
    C_history[rec_idx] = C
    rec_idx += 1

    D_face = np.zeros(N + 1, dtype=np.float64)
    k_face = np.zeros(N + 1, dtype=np.float64)

    a_C = np.zeros(N, dtype=np.float64)
    b_C = np.zeros(N, dtype=np.float64)
    c_C = np.zeros(N, dtype=np.float64)
    d_C = np.zeros(N, dtype=np.float64)

    a_T = np.zeros(N, dtype=np.float64)
    b_T = np.zeros(N, dtype=np.float64)
    c_T = np.zeros(N, dtype=np.float64)
    d_T = np.zeros(N, dtype=np.float64)

    t = 0.0
    step = 0
    actual_end_time = float(total_seconds)

    while t < total_seconds:
        t_next = t + dt
        T_air, C_e = interp_env(t_next, t_env, T_env, C_env)
        R_curr = interp_radius(t_next, t_rad, R_rad)

        C_old = C.copy()
        T_old = T.copy()
        C_iter = C.copy()
        T_iter = T.copy()

        for _it in range(2):
            rho = 760.0 + 90.0 * C_iter
            cp = 1850.0 + 2150.0 * (C_iter / (C_iter + 1.0))
            k = 0.12 + 0.20 * (C_iter / (C_iter + 1.0))
            D = 4.2e-4 * np.exp(-0.30 / C_iter - 3850.0 / T_iter)

            D_eff = D / (R_curr * R_curr)
            for i in range(1, N):
                D_face[i] = 2.0 * D_eff[i - 1] * D_eff[i] / (D_eff[i - 1] + D_eff[i])
            gamma_s_eff = 1.0 / ((0.5 * dxi * R_curr) / D[N - 1] + 1.0 / hm) / R_curr

            for i in range(N):
                d_C[i] = vols_xi[i] * C_old[i] / dt

            fl = areas_xi[1] * D_face[1] / dxi
            b_C[0] = vols_xi[0] / dt + fl
            c_C[0] = -fl
            a_C[0] = 0.0

            for i in range(1, N - 1):
                fl = areas_xi[i] * D_face[i] / dxi
                fr = areas_xi[i + 1] * D_face[i + 1] / dxi
                a_C[i] = -fl
                b_C[i] = vols_xi[i] / dt + fl + fr
                c_C[i] = -fr

            fl = areas_xi[N - 1] * D_face[N - 1] / dxi
            fr_s = areas_xi[N] * gamma_s_eff
            a_C[N - 1] = -fl
            b_C[N - 1] = vols_xi[N - 1] / dt + fl + fr_s
            c_C[N - 1] = 0.0
            d_C[N - 1] += fr_s * C_e

            C_iter = solve_thomas(a_C, b_C, c_C, d_C)

            k_eff = k / (R_curr * R_curr)
            for i in range(1, N):
                k_face[i] = 2.0 * k_eff[i - 1] * k_eff[i] / (k_eff[i - 1] + k_eff[i])
            gamma_T_eff = 1.0 / ((0.5 * dxi * R_curr) / k[N - 1] + 1.0 / h) / R_curr

            for i in range(N):
                d_T[i] = vols_xi[i] * rho[i] * cp[i] * T_old[i] / dt

            fl_T = areas_xi[1] * k_face[1] / dxi
            b_T[0] = vols_xi[0] * rho[0] * cp[0] / dt + fl_T
            c_T[0] = -fl_T
            a_T[0] = 0.0

            for i in range(1, N - 1):
                fl = areas_xi[i] * k_face[i] / dxi
                fr = areas_xi[i + 1] * k_face[i + 1] / dxi
                a_T[i] = -fl
                b_T[i] = vols_xi[i] * rho[i] * cp[i] / dt + fl + fr
                c_T[i] = -fr

            fl = areas_xi[N - 1] * k_face[N - 1] / dxi
            fr_s = areas_xi[N] * gamma_T_eff
            a_T[N - 1] = -fl
            b_T[N - 1] = vols_xi[N - 1] * rho[N - 1] * cp[N - 1] / dt + fl + fr_s
            c_T[N - 1] = 0.0
            d_T[N - 1] += fr_s * T_air

            T_iter = solve_thomas(a_T, b_T, c_T, d_T)

        C = C_iter
        T = T_iter
        t = t_next
        step += 1

        if step % sample_every_s == 0:
            times_out[rec_idx] = t
            radius_out[rec_idx] = R_curr
            T_history[rec_idx] = T
            C_history[rec_idx] = C
            rec_idx += 1

        if stop_at_cmax > 0.0 and C.max() < stop_at_cmax:
            actual_end_time = t
            if step % sample_every_s != 0:
                times_out[rec_idx] = t
                radius_out[rec_idx] = R_curr
                T_history[rec_idx] = T
                C_history[rec_idx] = C
                rec_idx += 1
            break

    return times_out[:rec_idx], radius_out[:rec_idx], T_history[:rec_idx], C_history[:rec_idx], actual_end_time, rec_idx


def sample_and_interpolate_fixed(
    times_raw: np.ndarray,
    T_raw: np.ndarray,
    C_raw: np.ndarray,
    N: int,
    R: float,
    r_target_cm: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    r_faces = np.linspace(0.0, R, N + 1)
    r_centers = 0.5 * (r_faces[:-1] + r_faces[1:])
    r_target_m = r_target_cm / 100.0
    n_steps = len(times_raw)
    n_radii = len(r_target_m)
    T_interp = np.zeros((n_steps, n_radii), dtype=np.float64)
    C_interp = np.zeros((n_steps, n_radii), dtype=np.float64)
    for s in range(n_steps):
        T_interp[s] = np.interp(r_target_m, r_centers, T_raw[s])
        C_interp[s] = np.interp(r_target_m, r_centers, C_raw[s])
    return T_interp, C_interp


def sample_and_interpolate_moving(
    times_raw: np.ndarray,
    radius_raw: np.ndarray,
    C_raw: np.ndarray,
    N: int,
    r_target_cm: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    xi_faces = np.linspace(0.0, 1.0, N + 1)
    xi_centers = 0.5 * (xi_faces[:-1] + xi_faces[1:])
    r_target_m = r_target_cm / 100.0
    n_steps = len(times_raw)
    n_radii = len(r_target_m)
    C_interp = np.full((n_steps, n_radii), np.nan, dtype=np.float64)
    C_surface = C_raw[:, -1].copy()
    for s in range(n_steps):
        R_s = radius_raw[s]
        valid_mask = r_target_m <= R_s
        if np.any(valid_mask):
            xi_targets = r_target_m[valid_mask] / R_s
            C_interp[s, valid_mask] = np.interp(xi_targets, xi_centers, C_raw[s])
    return C_interp, C_surface
