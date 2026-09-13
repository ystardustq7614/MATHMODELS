# 问题4：使用题给数据求解并导出题目要求的结果。
from __future__ import annotations

import csv
import json
from pathlib import Path
import numpy as np
import pandas as pd
import openpyxl

from core_solver import simulate_fvm_moving, sample_and_interpolate_moving
from result_contract_io import (
    upsert_question_contracts,
    solver_metrics,
    write_csv_table,
    table_entry,
    round_float,
    PROJECT_ROOT,
    OUTPUT_DIR,
    TABLES_DIR,
    RESULTS_DIR,
    DATA_CLEANED_DIR,
)

QUESTION = {
    'question_id': 'AQ4',
    'title': '收缩域中的烘干时长',
    'task_type': '移动边界传热传质',
    'main_model': '物质坐标系(xi)移动网格FVM + 附录4公式 + 离散阈值事件检测',
}

def run_aq4():
    config=json.loads((OUTPUT_DIR/'qa/model_validation_checks.json').read_text(encoding='utf-8'))['selected_configuration']
    N_run,dt_run=config['N'],config['dt_s']
    env_path = DATA_CLEANED_DIR / 'a_environment.csv'
    df_env = pd.read_csv(env_path)
    t_env = df_env['time_s'].values.astype(np.float64)
    T_env = df_env['temperature_K'].values.astype(np.float64)
    C_env = df_env['air_moisture_kgkg'].values.astype(np.float64)

    rad_path = DATA_CLEANED_DIR / 'a_radius.csv'
    df_rad = pd.read_csv(rad_path)
    t_rad = df_rad['time_s'].values.astype(np.float64)
    R_rad = df_rad['radius_m'].values.astype(np.float64)

    # 1. Run simulation until max(C) < 0.15 kg/kg (sampling every 60 s)
    times_raw, radius_raw, T_raw, C_raw, end_time, n_rec, diagnostics = simulate_fvm_moving(
        t_env=t_env,
        T_env=T_env,
        C_env=C_env,
        t_rad=t_rad,
        R_rad=R_rad,
        total_seconds=259200,
        sample_every_s=60,
        N=N_run,
        h=25.0,
        hm=8e-7,
        dt=dt_run,
        stop_at_cmax=0.15,
        return_diagnostics=True,
    )
    if diagnostics['status'] != 'reached':
        raise RuntimeError(diagnostics['status'])


    t_end_s = end_time
    t_end_h = t_end_s / 3600.0

    # 2. Build Table 6 (Moisture every 6 h + drying end time)
    # Target radii in domain: 0, 0.5, 1.0, 1.5 cm (and 2.0 cm if applicable, plus actual surface)
    r_tab_cm = np.array([0.0, 0.5, 1.0, 1.5, 2.0], dtype=np.float64)

    max_6h = int(t_end_s // 21600)
    times_6h_s = [i * 21600 for i in range(1, max_6h + 1)]
    if t_end_s not in times_6h_s:
        times_tab_s = np.array(times_6h_s + [t_end_s], dtype=np.float64)
    else:
        times_tab_s = np.array(times_6h_s, dtype=np.float64)

    tab_indices = []
    for ts in times_tab_s:
        idx = np.argmin(np.abs(times_raw - ts))
        tab_indices.append(idx)
    tab_indices = np.array(tab_indices)

    C_tab_interp, C_tab_surf = sample_and_interpolate_moving(
        times_tab_s,
        radius_raw[tab_indices],
        T_raw[tab_indices],
        C_raw[tab_indices],
        N=N_run,
        r_target_cm=r_tab_cm,
        t_env=t_env, T_env=T_env, C_env=C_env,
    )

    table6_rows = []
    for i, ts in enumerate(times_tab_s):
        if i == len(times_tab_s) - 1 and abs(ts - t_end_s) < 1e-3:
            time_label = f'烘干结束时间 ({t_end_h:.4f} h)'
        else:
            time_label = f'{ts / 3600.0:.1f}'
        row = {'时间/h': time_label}
        for j, r_val in enumerate(r_tab_cm):
            val = C_tab_interp[i, j]
            row[f'{r_val:g} cm'] = f'{val:.4f}' if not np.isnan(val) else ''
        row['药材表面'] = f'{C_tab_surf[i]:.4f}'
        row['当前半径/cm'] = f'{radius_raw[tab_indices[i]] * 100.0:.4f}'
        table6_rows.append(row)

    t6_path = TABLES_DIR / 'table_aq4_shrinkage_moisture.csv'
    write_csv_table(t6_path, table6_rows)

    # 3. Build result4.xlsx (every 60 s + end time, 0.1 cm steps + surface)
    r_full_cm = np.arange(21) / 10.0
    C_full_interp, C_full_surf = sample_and_interpolate_moving(
        times_raw,
        radius_raw,
        T_raw,
        C_raw,
        N=N_run,
        r_target_cm=r_full_cm,
        t_env=t_env, T_env=T_env, C_env=C_env,
    )

    res4_path = TABLES_DIR / 'result4.xlsx'
    wb = openpyxl.Workbook(write_only=True)
    ws = wb.create_sheet('Sheet1')

    header = ['时间\\到药材中心的距离'] + [round(r, 1) for r in r_full_cm] + ['药材表面']
    ws.append(header)

    for i in range(1, len(times_raw)):
        t_sec = float(times_raw[i])
        row = [t_sec]
        for val in C_full_interp[i]:
            row.append(round(val, 4) if not np.isnan(val) else None)
        row.append(round(C_full_surf[i], 4))
        ws.append(row)
    wb.save(res4_path)

    prior=json.loads((RESULTS_DIR/'metrics.json').read_text(encoding='utf-8'))
    t3=next(x['value'] for x in prior['items'] if x['metric_name']=='aq3_drying_time_s')
    reduction=(t3-t_end_s)/t3*100

    # 4. Metrics & Contracts
    metrics = [
        {'metric_name': 'aq4_drying_time_s', 'metric_role': 'evaluation', 'value': round_float(t_end_s, 2), 'unit': 's'},
        {'metric_name': 'aq4_drying_time_h', 'metric_role': 'evaluation', 'value': round_float(t_end_h, 4), 'unit': 'h'},
        {'metric_name': 'aq4_final_radius_cm', 'metric_role': 'evaluation', 'value': round_float(radius_raw[-1] * 100.0, 4), 'unit': 'cm'},
        {'metric_name': 'aq4_final_max_moisture', 'metric_role': 'evaluation', 'value': round_float(np.max(C_raw[-1]), 4), 'unit': 'kg/kg'},
        {'metric_name': 'aq4_final_min_moisture', 'metric_role': 'evaluation', 'value': round_float(np.min(C_raw[-1]), 4), 'unit': 'kg/kg'},
        {'metric_name': 'aq4_final_center_moisture', 'metric_role': 'evaluation', 'value': round_float(C_raw[-1, 0], 4), 'unit': 'kg/kg'},
        {'metric_name': 'aq4_final_surface_moisture', 'metric_role': 'evaluation', 'value': round_float(C_full_surf[-1], 4), 'unit': 'kg/kg'},
        {'metric_name': 'aq4_time_reduction_vs_aq3_percent', 'metric_role': 'comparison', 'value': round_float(reduction, 2), 'unit': '%'},
    ]

    metrics += solver_metrics(diagnostics,'AQ4')

    conclusions = [
        {
            'question_id': 'AQ4',
            'conclusion_text': f'附件2收缩与附录4物性共同作用下，达标时长为{t_end_h:.4f} h（{t_end_s:.1f} s），较问题三变化{-reduction:.4f}%。该差异是联合情景变化，不全部归因于收缩。终点半径为{radius_raw[-1]*100:.4f} cm，表面含水率为{C_full_surf[-1]:.4f} kg/kg。',
            'evidence_required': ['model_results.json', 'metrics.json', 'table_index.json'],
            'evidence_status': 'computed',
        }
    ]

    tables = [
        table_entry(
            question_id='AQ4',
            table_id='table6',
            title='药材烘干过程的水分浓度（表6）',
            purpose='展示收缩域中每隔6小时及烘干结束时刻各物理截面及真实表面的含水率分布。',
            path=t6_path,
            status='computed',
        ),
    ]

    outputs = [
        {'path': str(t6_path), 'type': 'csv'},
        {'path': str(res4_path), 'type': 'xlsx'},
    ]

    summary = f'AQ4收缩域烘干时长求解完成：烘干达标时长为{t_end_h:.4f} h ({t_end_s:.1f} s)；终点半径为{radius_raw[-1] * 100.0:.4f} cm，中心含水率为{C_raw[-1, 0]:.4f} kg/kg，表面为{C_full_surf[-1]:.4f} kg/kg。表6与result4.xlsx已导出。'

    upsert_question_contracts(
        question=QUESTION,
        result_summary=summary,
        metrics=metrics,
        tables=tables,
        conclusions=conclusions,
        outputs=outputs,
        status='computed',
        parameters=[{'name':'N','value':N_run},{'name':'dt_s','value':dt_run},{'name':'event_status','value':diagnostics['status']}],
    )
    print(f'AQ4 finished successfully: t_end = {t_end_h:.4f} h ({t_end_s:.1f} s).')

if __name__ == '__main__':
    run_aq4()
