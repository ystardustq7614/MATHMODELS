"""圆柱径向有限体积：后向欧拉、Picard迭代和三对角求解。"""
from __future__ import annotations
import numba
import numpy as np


@numba.njit
def solve_thomas(a, b, c, d):
    n = len(d)
    upper = np.zeros(n)
    rhs = np.zeros(n)
    upper[0] = c[0] / b[0]
    rhs[0] = d[0] / b[0]
    for i in range(1, n):
        pivot = b[i] - a[i] * upper[i-1]
        upper[i] = c[i] / pivot
        rhs[i] = (d[i] - a[i] * rhs[i-1]) / pivot
    x = rhs.copy()
    for i in range(n-2, -1, -1):
        x[i] -= upper[i] * x[i+1]
    return x


@numba.njit
def interp_env(t, t_env, T_env, C_env):
    return np.interp(t, t_env, T_env), np.interp(t, t_env, C_env)


@numba.njit
def interp_radius(t, t_rad, R_rad):
    return np.interp(t, t_rad, R_rad)


@numba.njit
def properties(T, C, mode):
    if mode == 1:
        rho = np.full(len(C), 820.)
        cp = np.full(len(C), 2600.)
        k = np.full(len(C), .36)
        D = 7e-9 * np.exp(-.89 / C)
    elif mode == 2:
        rho = 650 + 128*C
        cp = 1450 + 2736*C/(1+C)
        k = .21 + .38*C/(1+C)
        D = 2.4e-3 * np.exp(-.45/C - 3850/T)
    else:
        rho = 760 + 90*C
        cp = 1850 + 2150*C/(1+C)
        k = .12 + .20*C/(1+C)
        D = 4.2e-4 * np.exp(-.30/C - 3850/T)
    return rho*cp, k, D


@numba.njit
def system(coef, storage, old, weights, R, dt, transfer, exterior):
    # 用xi环面积权重；内部通量成对抵消，表面采用半格串联阻力。
    n = len(old)
    dxi = 1. / n
    face = 2*coef[:-1]*coef[1:]/(coef[:-1]+coef[1:])
    g = 2*np.arange(1,n)*face/(R*R)
    a = np.zeros(n)
    c = np.zeros(n)
    a[1:] = -g
    c[:-1] = -g
    mass = weights*storage/dt
    b = mass-a-c
    rhs = mass*old
    gamma = 1/(1/transfer + .5*dxi*R/coef[-1])
    b[-1] += 2*gamma/R
    rhs[-1] += 2*gamma/R*exterior
    return a,b,c,rhs,gamma


@numba.njit
def residual(a,b,c,rhs,x):
    r = b*x-rhs
    scale = np.abs(b*x)+np.abs(rhs)
    r[1:] += a[1:]*x[:-1]
    r[:-1] += c[:-1]*x[1:]
    scale[1:] += np.abs(a[1:]*x[:-1])
    scale[:-1] += np.abs(c[:-1]*x[1:])
    return np.max(np.abs(r)/np.maximum(scale,1e-30))


@numba.njit
def _simulate(t_env,T_env,C_env,t_rad,R_rad,total_seconds,formula_mode,
              sample_every_s,N,h,hm,dt,stop_at_cmax,max_iterations,converge,
              initial_T,initial_C):
    edges = np.linspace(0.,1.,N+1)
    weights = edges[1:]**2-edges[:-1]**2
    one = np.ones(N)
    T = np.full(N,initial_T)
    C = np.full(N,initial_C)
    capacity = int(np.floor(total_seconds/sample_every_s))+2
    times = np.zeros(capacity)
    radii = np.zeros(capacity)
    Th = np.zeros((capacity,N))
    Ch = np.zeros((capacity,N))
    radii[0] = R_rad[0]
    Th[0],Ch[0] = T,C
    rec = 1
    sample_index = 1
    t = 0.
    steps = 0
    iterations_sum = 0
    max_it = 0
    flux_sum = 0.
    balance_max = 0.
    step_balance_max = 0.
    residual_C_max = 0.
    residual_T_max = 0.
    delta_C_max = 0.
    delta_T_max = 0.
    center_excess_max = 0.
    left_t = 0.
    left_C = initial_C
    status = 0
    while t < total_seconds-1e-10:
        step_dt = min(dt,total_seconds-t)
        t_new = t+step_dt
        R = interp_radius(t_new,t_rad,R_rad)
        air,Ce = interp_env(t_new,t_env,T_env,C_env)
        T_old,C_old = T.copy(),C.copy()
        Ti,Ci = T.copy(),C.copy()
        accepted = False
        rc,rt,dc,dT = 0.,0.,0.,0.
        for it in range(max_iterations):
            storage,k,D = properties(Ti,Ci,formula_mode)
            ac,bc,cc,fc,gamma = system(D,one,C_old,weights,R,step_dt,hm,Ce)
            at,bt,ct,ft,_ = system(k,storage,T_old,weights,R,step_dt,h,air)
            Cn = solve_thomas(ac,bc,cc,fc)
            Tn = solve_thomas(at,bt,ct,ft)
            dc = np.max(np.abs(Cn-Ci))
            dT = np.max(np.abs(Tn-Ti))
            Ci,Ti = Cn,Tn
            # 接近收敛时，重组最终状态的非线性方程并检查残差。
            if (dc <= 1e-10 and dT <= 1e-7) or it == max_iterations-1:
                sn,kn,Dn = properties(Ti,Ci,formula_mode)
                aa,bb,ccn,ff,_ = system(Dn,one,C_old,weights,R,step_dt,hm,Ce)
                rc = residual(aa,bb,ccn,ff,Ci)
                aa,bb,ccn,ff,_ = system(kn,sn,T_old,weights,R,step_dt,h,air)
                rt = residual(aa,bb,ccn,ff,Ti)
                if not converge or (dc<=1e-10 and dT<=1e-7 and max(rc,rt)<=1e-10):
                    accepted = True
                    break
        if not accepted or not np.isfinite(Ci).all() or not np.isfinite(Ti).all() or np.min(Ci)<=0:
            status = -1
            break
        iterations_sum += it+1
        max_it = max(max_it,it+1)
        residual_C_max = max(residual_C_max,rc)
        residual_T_max = max(residual_T_max,rt)
        delta_C_max = max(delta_C_max,dc)
        delta_T_max = max(delta_T_max,dT)
        # gamma为本步实际水分矩阵采用的系数，不用重组系数替代它。
        outward = 2*gamma/R*(Ci[-1]-Ce)*step_dt
        flux_sum += outward
        mean_new = np.sum(weights*Ci)
        step_balance_max = max(step_balance_max,abs(np.sum(weights*(Ci-C_old))+outward)/initial_C)
        balance_max = max(balance_max,abs(mean_new-initial_C+flux_sum)/initial_C)
        center_excess_max = max(center_excess_max,(Ci[0]-Ci[1])/8)
        # 输出不改变积分步长。跨越输出点时作线性输出插值；本题验证节点整除步长。
        while sample_index*sample_every_s <= t_new+1e-10:
            if rec >= capacity:
                raise IndexError('output capacity')
            ts = sample_index*sample_every_s
            alpha = (ts-t)/step_dt
            times[rec] = ts
            radii[rec] = interp_radius(ts,t_rad,R_rad)
            Th[rec] = T_old+alpha*(Ti-T_old)
            Ch[rec] = C_old+alpha*(Ci-C_old)
            rec += 1
            sample_index += 1
        left_t,left_C = t,np.max(C_old)
        t,T,C = t_new,Ti,Ci
        steps += 1
        if stop_at_cmax > 0 and np.max(C) < stop_at_cmax:
            status = 1
            break
    if abs(times[rec-1]-t)>1e-9:
        times[rec] = t
        radii[rec] = interp_radius(t,t_rad,R_rad)
        Th[rec],Ch[rec] = T,C
        rec += 1
    diag = np.array([status,left_t,t,left_C,np.max(C),balance_max,step_balance_max,
                     residual_C_max,residual_T_max,max_it,iterations_sum/max(steps,1),
                     steps,center_excess_max,delta_C_max,delta_T_max])
    return times[:rec],radii[:rec],Th[:rec],Ch[:rec],t,rec,diag


def _finish(result, moving, return_diagnostics):
    keys = ['status_code','left_time_s','end_time_s','left_max_C','final_max_C',
            'water_balance','step_water_balance','residual_C','residual_T',
            'max_iterations','mean_iterations','steps','center_excess_bound',
            'last_iteration_delta_C_max','last_iteration_delta_T_max']
    diag = dict(zip(keys,result[-1].tolist()))
    diag['status'] = {-1:'solver_failed',0:'not_reached',1:'reached'}[int(diag['status_code'])]
    values = result[:-1] if moving else (result[0],result[2],result[3],result[4],result[5])
    if return_diagnostics:
        return (*values,diag)
    if diag['status_code'] == -1:
        raise RuntimeError(f"Nonlinear solve failed after t={result[4]} s")
    return values


def simulate_fvm_fixed(t_env,T_env,C_env,total_seconds,formula_mode,sample_every_s=1,
                       N=80,R=.02,h=25.,hm=8e-7,dt=1.,stop_at_cmax=-1.,
                       max_iterations=50,converge=True,return_diagnostics=False,
                       initial_T=301.15,initial_C=2.55):
    result = _simulate(t_env,T_env,C_env,np.array([0.,float(total_seconds)]),
        np.array([R,R]),total_seconds,formula_mode,sample_every_s,N,h,hm,dt,
        stop_at_cmax,max_iterations,converge,initial_T,initial_C)
    return _finish(result,False,return_diagnostics)


def simulate_fvm_moving(t_env,T_env,C_env,t_rad,R_rad,total_seconds,sample_every_s=60,
                        N=80,h=25.,hm=8e-7,dt=1.,stop_at_cmax=.15,
                        max_iterations=50,converge=True,return_diagnostics=False,
                        initial_T=301.15,initial_C=2.55):
    result = _simulate(t_env,T_env,C_env,t_rad,R_rad,total_seconds,3,sample_every_s,N,h,hm,
                      dt,stop_at_cmax,max_iterations,converge,initial_T,initial_C)
    return _finish(result,True,return_diagnostics)


def reconstruct_surface(
    times: np.ndarray,
    T_outer: np.ndarray,
    C_outer: np.ndarray,
    delta: float | np.ndarray,
    t_env: np.ndarray,
    T_env: np.ndarray,
    C_env: np.ndarray,
    formula_mode: int,
    h: float,
    hm: float,
) -> tuple[np.ndarray, np.ndarray]:
    if formula_mode == 1:
        k = 0.36
        D = 7.0e-9 * np.exp(-0.89 / C_outer)
    elif formula_mode == 2:
        k = 0.21 + 0.38 * (C_outer / (C_outer + 1.0))
        D = 2.4e-3 * np.exp(-0.45 / C_outer - 3850.0 / T_outer)
    else:  # Appendix 4
        k = 0.12 + 0.20 * (C_outer / (C_outer + 1.0))
        D = 4.2e-4 * np.exp(-0.30 / C_outer - 3850.0 / T_outer)

    T_air = np.interp(times, t_env, T_env)
    C_air = np.interp(times, t_env, C_env)
    # Match the half-cell resistance used by the Robin boundary.
    T_surface = (k * T_outer + h * delta * T_air) / (k + h * delta)
    C_surface = (D * C_outer + hm * delta * C_air) / (D + hm * delta)
    # The initial condition specifies a uniform field, including the surface.
    T_surface[times == 0.0] = T_outer[times == 0.0]
    C_surface[times == 0.0] = C_outer[times == 0.0]
    return T_surface, C_surface


def sample_and_interpolate_fixed(
    times_raw: np.ndarray,
    T_raw: np.ndarray,
    C_raw: np.ndarray,
    N: int,
    R: float,
    r_target_cm: np.ndarray,
    t_env: np.ndarray,
    T_env: np.ndarray,
    C_env: np.ndarray,
    formula_mode: int,
    h: float = 25.0,
    hm: float = 8e-7,
) -> tuple[np.ndarray, np.ndarray]:
    r_faces = np.linspace(0.0, R, N + 1)
    r_centers = 0.5 * (r_faces[:-1] + r_faces[1:])
    r_target_m = r_target_cm / 100.0
    n_steps = len(times_raw)
    n_radii = len(r_target_m)
    T_interp = np.zeros((n_steps, n_radii), dtype=np.float64)
    C_interp = np.zeros((n_steps, n_radii), dtype=np.float64)
    T_surface, C_surface = reconstruct_surface(
        times_raw, T_raw[:, -1], C_raw[:, -1], R / (2 * N),
        t_env, T_env, C_env, formula_mode, h, hm,
    )
    r_nodes = np.append(r_centers, R)
    for s in range(n_steps):
        T_interp[s] = np.interp(r_target_m, r_nodes, np.append(T_raw[s], T_surface[s]))
        C_interp[s] = np.interp(r_target_m, r_nodes, np.append(C_raw[s], C_surface[s]))
    return T_interp, C_interp


def sample_and_interpolate_moving(
    times_raw: np.ndarray,
    radius_raw: np.ndarray,
    T_raw: np.ndarray,
    C_raw: np.ndarray,
    N: int,
    r_target_cm: np.ndarray,
    t_env: np.ndarray,
    T_env: np.ndarray,
    C_env: np.ndarray,
    h: float = 25.0,
    hm: float = 8e-7,
) -> tuple[np.ndarray, np.ndarray]:
    xi_faces = np.linspace(0.0, 1.0, N + 1)
    xi_centers = 0.5 * (xi_faces[:-1] + xi_faces[1:])
    r_target_m = r_target_cm / 100.0
    n_steps = len(times_raw)
    n_radii = len(r_target_m)
    C_interp = np.full((n_steps, n_radii), np.nan, dtype=np.float64)
    _, C_surface = reconstruct_surface(
        times_raw, T_raw[:, -1], C_raw[:, -1], radius_raw / (2 * N),
        t_env, T_env, C_env, 3, h, hm,
    )
    xi_nodes = np.append(xi_centers, 1.0)
    for s in range(n_steps):
        R_s = radius_raw[s]
        valid_mask = r_target_m <= R_s
        if np.any(valid_mask):
            xi_targets = r_target_m[valid_mask] / R_s
            C_interp[s, valid_mask] = np.interp(xi_targets, xi_nodes, np.append(C_raw[s], C_surface[s]))
    return C_interp, C_surface
