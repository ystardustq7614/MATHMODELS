# 问题2：使用题给数据求解并导出题目要求的结果。
from __future__ import annotations

import csv
import json
from pathlib import Path
import numpy as np
import pandas as pd
import openpyxl

from core_solver import simulate_fvm_fixed, sample_and_interpolate_fixed
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
    'question_id': 'AQ2',
    'title': '统一经验物性的全过程模型',
    'task_type': '热湿非线性耦合',
    'main_model': '附录3全过程经验物性FVM模型 + Picard迭代 + Thomas三对角求解',
}

def run_aq2():
    config=json.loads((OUTPUT_DIR/'qa/model_validation_checks.json').read_text(encoding='utf-8'))['selected_configuration']
    N_run,dt_run=config['N'],config['dt_s']
    env_path = DATA_CLEANED_DIR / 'a_environment.csv'
    df_env = pd.read_csv(env_path)
    t_env = df_env['time_s'].values.astype(np.float64)
    T_env = df_env['temperature_K'].values.astype(np.float64)
    C_env = df_env['air_moisture_kgkg'].values.astype(np.float64)

    # Appendix 3 applies from t=0 until drying completes. Tables 3/4
    # show only the first 3 h; result2.xlsx must retain every second.
    times_raw, T_raw, C_raw, end_time, n_rec, diagnostics = simulate_fvm_fixed(
        t_env=t_env,
        T_env=T_env,
        C_env=C_env,
        total_seconds=259200,
        formula_mode=2,
        sample_every_s=1,
        N=N_run,
        R=0.02,
        h=25.0,
        hm=8e-7,
        dt=dt_run,
        stop_at_cmax=0.15,
        return_diagnostics=True,
    )
    if diagnostics['status'] != 'reached':
        raise RuntimeError(diagnostics['status'])


    # 2. Build Table 3 (Temperature) & Table 4 (Moisture)
    # 0.5 to 3.0 h every 0.5 h -> [1800, 3600, 5400, 7200, 9000, 10800] s
    times_tab_s = np.array([1800, 3600, 5400, 7200, 9000, 10800], dtype=np.float64)
    times_tab_h = times_tab_s / 3600.0
    r_tab_cm = np.array([0.0, 0.5, 1.0, 1.5, 2.0], dtype=np.float64)

    T_tab, C_tab = sample_and_interpolate_fixed(times_tab_s, T_raw[times_tab_s.astype(int)], C_raw[times_tab_s.astype(int)], N=N_run, R=0.02, r_target_cm=r_tab_cm, t_env=t_env, T_env=T_env, C_env=C_env, formula_mode=2)
    T_tab_C = T_tab - 273.15

    # Write Table 3 CSV
    table3_rows = []
    for i, t_h in enumerate(times_tab_h):
        row = {'时间/h': f'{t_h:.1f}'}
        for j, r_val in enumerate(r_tab_cm):
            row[f'{r_val:g} cm'] = f'{T_tab_C[i, j]:.4f}'
        table3_rows.append(row)
    t3_path = TABLES_DIR / 'table_aq2_temperature.csv'
    write_csv_table(t3_path, table3_rows)

    # Write Table 4 CSV
    table4_rows = []
    for i, t_h in enumerate(times_tab_h):
        row = {'时间/h': f'{t_h:.1f}'}
        for j, r_val in enumerate(r_tab_cm):
            row[f'{r_val:g} cm'] = f'{C_tab[i, j]:.4f}'
        table4_rows.append(row)
    t4_path = TABLES_DIR / 'table_aq2_moisture.csv'
    write_csv_table(t4_path, table4_rows)

    # 3. Build result2.xlsx (every second to the terminal event, 0.1 cm steps)
    r_full_cm = np.arange(0.0, 2.0001, 0.1)
    T_full, C_full = sample_and_interpolate_fixed(times_raw, T_raw, C_raw, N=N_run, R=0.02, r_target_cm=r_full_cm, t_env=t_env, T_env=T_env, C_env=C_env, formula_mode=2)
    T_full_C = T_full - 273.15

    res2_path = TABLES_DIR / 'result2.xlsx'
    wb = openpyxl.Workbook(write_only=True)
    ws_T = wb.create_sheet('温度')
    ws_C = wb.create_sheet('水分浓度')

    header = ['时间\\到药材中心的距离'] + [round(r, 1) for r in r_full_cm]
    ws_T.append(header)
    ws_C.append(header)

    for s in range(1, len(times_raw)):
        row_T = [float(times_raw[s])] + [round(val, 4) for val in T_full_C[s]]
        row_C = [float(times_raw[s])] + [round(val, 4) for val in C_full[s]]
        ws_T.append(row_T)
        ws_C.append(row_C)
    wb.save(res2_path)

    # 4. Metrics & Contracts
    metrics = [
        {'metric_name': 'aq2_3h_center_temperature_C', 'metric_role': 'evaluation', 'value': round_float(T_full_C[10800, 0], 4), 'unit': '°C'},
        {'metric_name': 'aq2_3h_surface_temperature_C', 'metric_role': 'evaluation', 'value': round_float(T_full_C[10800, -1], 4), 'unit': '°C'},
        {'metric_name': 'aq2_3h_center_moisture', 'metric_role': 'evaluation', 'value': round_float(C_full[10800, 0], 4), 'unit': 'kg/kg'},
        {'metric_name': 'aq2_3h_surface_moisture', 'metric_role': 'evaluation', 'value': round_float(C_full[10800, -1], 4), 'unit': 'kg/kg'},
        {'metric_name': 'aq2_1800s_surface_temperature_C', 'metric_role': 'comparison', 'value': round_float(T_full_C[1800, -1], 4), 'unit': '°C'},
        {'metric_name': 'aq2_1800s_surface_moisture', 'metric_role': 'comparison', 'value': round_float(C_full[1800, -1], 4), 'unit': 'kg/kg'},
    ]

    metrics += solver_metrics(diagnostics,'AQ2')

    conclusions = [
        {
            'question_id': 'AQ2',
            'conclusion_text': f'采用附录3全过程统一经验物性公式自t=0连续求解3 h（10800 s）：药材升温迅速并在3 h内达到中心{T_full_C[10800, 0]:.4f}°C、表面{T_full_C[10800, -1]:.4f}°C，整体贴近烘房温度（约50.2°C）；水分浓度在3 h末中心降至{C_full[10800, 0]:.4f} kg/kg，表面降至{C_full[10800, -1]:.4f} kg/kg。相较于AQ1常物性模型，附录3通过温度和含水率相关物性描述全过程，不需要拼接问题一末态。',
            'evidence_required': ['model_results.json', 'metrics.json', 'table_index.json'],
            'evidence_status': 'computed',
        }
    ]

    tables = [
        table_entry(
            question_id='AQ2',
            table_id='table3',
            title='3小时内药材的温度（表3）',
            purpose='展示全过程模型在0.5-3.0 h各半小时的温度径向分布。',
            path=t3_path,
            status='computed',
        ),
        table_entry(
            question_id='AQ2',
            table_id='table4',
            title='3小时内药材的水分浓度（表4）',
            purpose='展示全过程模型在0.5-3.0 h各半小时的干基水分浓度径向分布。',
            path=t4_path,
            status='computed',
        ),
    ]

    outputs = [
        {'path': str(t3_path), 'type': 'csv'},
        {'path': str(t4_path), 'type': 'csv'},
        {'path': str(res2_path), 'type': 'xlsx'},
    ]

    summary = f'AQ2全过程模型求解至达标时刻{end_time:.1f} s：3 h时中心温度为{T_full_C[10800, 0]:.4f}°C，表面温度为{T_full_C[10800, -1]:.4f}°C；中心水分浓度为{C_full[10800, 0]:.4f} kg/kg，表面水分浓度为{C_full[10800, -1]:.4f} kg/kg。表3、表4保留前3 h，result2.xlsx包含1 s至达标时刻的逐秒温度和含水率。'

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
    print('AQ2 finished successfully.')

if __name__ == '__main__':
    run_aq2()
