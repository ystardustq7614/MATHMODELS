"""S3 only: inspect A inputs, convert units, plot observations, emit handoffs."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'paper_output'
sys.path.insert(0, str(ROOT / '.agents/skills/data-cleaning-and-visualization/scripts'))
import robust_loader as loader
import numpy as np
from openpyxl import load_workbook
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(name, data):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def main():
    started = time.perf_counter()
    stamp = datetime.now(timezone.utc).isoformat()
    manifest_path = OUT / 'input_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    analysis = json.loads((OUT / 'step1/problem_analysis.json').read_text(encoding='utf-8'))
    route = json.loads((OUT / 'plan/model_route.json').read_text(encoding='utf-8'))
    allowed = {d['path'] for d in analysis['data_files'] if d['role'] == 'raw_data'}
    entries = [e for e in manifest['entries'] if e['path'] in allowed]
    assert len(entries) == 2
    assert all(e['role'] == 'raw_data' and e['usable_for_modeling'] for e in entries)
    assert all(digest(ROOT / e['path']) == e['sha256'] for e in entries)
    diagnostics = [loader.inspect_xlsx(ROOT / e['path']) for e in entries]
    report = dict(schema_version='1.0', generated_by='paper_output/code/data_processing/prepare_a_data.py',
                  generated_at=stamp, status='PASS' if all(d['readable'] for d in diagnostics) else 'FAIL',
                  input_manifest_used=True, input_manifest_sha256=digest(manifest_path),
                  data_files=diagnostics, selected_problem='A',
                  skipped_files=[{'path': e['path'], 'role': e['role'], 'reason': 'outside_A_raw_data'}
                                 for e in manifest['entries'] if e['path'] not in allowed],
                  errors=[err for d in diagnostics for err in d['errors']])
    save_json('data_cleaned/load_report.json', report)
    assert report['status'] == 'PASS'

    arrays, datasets = [], []
    settings = [
        ('a_environment.csv', ['时间', '温度', '水分浓度'],
         ['time_s', 'temperature_C', 'air_moisture_kgkg', 'temperature_K'], ['s', 'degC', 'kg/kg', 'K'], 60, 14400),
        ('a_radius.csv', ['时间', '半径'], ['time_s', 'radius_cm', 'radius_m'], ['s', 'cm', 'm'], 1800, 259200),
    ]
    for entry, (name, headers, columns, units, step, end) in zip(entries, settings):
        wb = load_workbook(ROOT / entry['path'], read_only=True, data_only=True)
        rows = list(wb['Sheet1'].values)
        wb.close()
        assert list(rows[0]) == headers
        values = np.asarray(rows[1:], dtype=float)
        assert np.isfinite(values).all(), 'Missing or non-finite observation: do not impute automatically'
        assert values[0, 0] == 0 and values[-1, 0] == end
        assert np.all(np.diff(values[:, 0]) == step)
        assert (values[:, 1:] > 0).all()
        converted = np.column_stack([values, values[:, 1] + 273.15 if end == 14400 else values[:, 1] / 100])
        path = OUT / 'data_cleaned' / name
        np.savetxt(path, converted, delimiter=',', header=','.join(columns), comments='', fmt='%.12g')
        check = np.loadtxt(path, delimiter=',', skiprows=1)
        np.testing.assert_allclose(check, converted, rtol=0, atol=1e-10)
        arrays.append(converted)
        datasets.append(dict(path=entry['path'], sha256=entry['sha256'], role='raw_data',
                             cleaned_output=path.relative_to(ROOT).as_posix(), cleaned_sha256=digest(path),
                             rows=len(values), columns=columns, units=dict(zip(columns, units)),
                             missing_values=0, duplicate_times=0, removed_rows=0, imputed_values=0,
                             time_start_s=0, time_end_s=end, interval_s=step,
                             min_values=dict(zip(columns, converted.min(axis=0).tolist())),
                             max_values=dict(zip(columns, converted.max(axis=0).tolist())),
                             question_ids=['AQ1', 'AQ2', 'AQ3', 'AQ4'] if end == 14400 else ['AQ4']))

    env, rad = arrays
    tail = env[env[:, 0] >= 10800]
    environment = dict(interpolation='piecewise_linear', support_s=[0, 14400],
                       extension='hold_last', last_temperature_C=float(env[-1, 1]),
                       last_Ce=float(env[-1, 2]), sensitivity_window_s=[10800, 14400],
                       tail_mean_temperature_C=float(tail[:, 1].mean()), tail_mean_Ce=float(tail[:, 2].mean()),
                       tail_std_temperature_C=float(tail[:, 1].std(ddof=1)),
                       tail_std_Ce=float(tail[:, 2].std(ddof=1)), extension_is_observed=False)
    radius = dict(interpolation='piecewise_linear', support_s=[0, 259200], extension='hold_last',
                  last_radius_m=float(rad[-1, 2]), nonincreasing=bool(np.all(np.diff(rad[:, 2]) <= 0)),
                  increasing_intervals=int(np.count_nonzero(np.diff(rad[:, 2]) > 0)),
                  extension_is_observed=False)
    report.update(summary=dict(data_file_count=2, readable_data_file_count=2, total_observations=len(env)+len(rad)),
                  quality=datasets, boundary_statistics=environment, radius_statistics=radius)
    save_json('data_cleaned/load_report.json', report)

    figdir = OUT / 'figures'
    figdir.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True, layout='constrained')
    axes[0].plot(env[:, 0]/3600, env[:, 1], color='#16697a', lw=1.5)
    axes[0].set(ylabel='Air temperature (deg C)', title='Observed chamber inputs: 0-4 h')
    axes[1].plot(env[:, 0]/3600, env[:, 2], color='#c06c35', lw=1.5)
    axes[1].set(xlabel='Time (h)', ylabel='Air moisture (kg/kg)')
    for ax in axes:
        ax.grid(alpha=0.2)
    fig.savefig(figdir / 'fig_a_environment.png', dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4), layout='constrained')
    ax.plot(rad[:, 0]/3600, rad[:, 1], color='#16697a', lw=1.5)
    ax.scatter(rad[::6, 0]/3600, rad[::6, 1], s=12, color='#16697a')
    ax.set(xlabel='Time (h)', ylabel='Radius (cm)', title='Observed radius: 0-72 h')
    ax.grid(alpha=0.2)
    fig.savefig(figdir / 'fig_a_radius.png', dpi=180)
    plt.close(fig)

    figure_items = []
    for fid, title, source, qids in [
        ('fig_a_environment', '烘房温度与水分浓度实测输入', datasets[0], ['AQ1','AQ2','AQ3','AQ4']),
        ('fig_a_radius', '药材半径实测输入', datasets[1], ['AQ4'])]:
        path = OUT / 'figures' / (fid + '.png')
        figure_items.append(dict(figure_id=fid, title=title, path=path.relative_to(ROOT).as_posix(),
                                 expected_path=path.relative_to(ROOT).as_posix(), question_ids=qids,
                                 source_data=source['cleaned_output'], source_sha256=source['cleaned_sha256'],
                                 sha256=digest(path), bytes=path.stat().st_size, status='generated',
                                 ok=True, exists=True, placeholder=False, evidence_type='input_observation',
                                 interpretation='展示官方输入，不是模型预测或独立验证。', paper_section='2 数据与问题分析'))
    future = {f['figure_id']: f for q in route['questions'] for f in q['figures']}
    save_json('figure_index.json', dict(schema_version='1.0', generated_at=stamp, figures=figure_items))
    save_json('plan/visualization_plan.json', dict(schema_version='1.0', generated_at=stamp,
              figures=figure_items, future_model_figures=list(future.values()),
              note='只有实际生成的S3输入图进入figure_index；模型图待S5。'))
    save_json('plan/data_plan.json', dict(schema_version='1.0', generated_at=stamp, selected_problem='A',
              input_manifest_sha256=digest(manifest_path), model_route_sha256=digest(OUT/'plan/model_route.json'),
              data_files=datasets, environment=environment, radius=radius,
              cleaning_policy='检查全表；不填补、不平滑、不去趋势，保留原始观测波动；只增加SI单位列。',
              interpolation_policy='S4按本计划在计算时插值，S3清洗文件只保留实测节点。',
              output_sampling={'AQ1': '1 s, 0.1 cm, through 1800 s',
                               'AQ2': '1 s, 0.1 cm, through AQ3 event; tables at 0.5 h through 3 h',
                               'AQ3': '60 s, 0.1 cm, append event',
                               'AQ4': '60 s, valid physical 0.1 cm nodes and true surface; append event'},
              external_validation={'dataset_acquired': False, 'required_for_numerical_execution': False},
              figure_ids=[f['figure_id'] for f in figure_items]))

    outputs = [OUT/'data_cleaned/load_report.json', OUT/'plan/data_plan.json',
               OUT/'plan/visualization_plan.json', OUT/'figure_index.json']
    outputs += [OUT/'data_cleaned'/s[0] for s in settings]
    outputs += [ROOT/f['path'] for f in figure_items]
    tracked_inputs = [manifest_path, OUT/'step1/problem_analysis.json', OUT/'plan/model_route.json']
    tracked_inputs += [ROOT/e['path'] for e in entries]
    record = lambda p: dict(path=p.relative_to(ROOT).as_posix(), sha256=digest(p), bytes=p.stat().st_size)
    save_json('data_cleaned/data_pipeline_run.json', dict(schema_version='1.0', stage='S3', status='PASS',
              generated_at=stamp, exit_code=0, elapsed_s=time.perf_counter()-started,
              command='F:/Anaconda_envs/envs/mathmodel-skill-standard/python.exe -X utf8 paper_output/code/data_processing/prepare_a_data.py',
              executable=sys.executable, python=sys.version, numpy=np.__version__, matplotlib=matplotlib.__version__,
              scripts=[record(Path(__file__)), record(Path(loader.__file__))],
              inputs=[record(p) for p in tracked_inputs], outputs=[record(p) for p in outputs],
              note='数据处理运行证据；不是S5模型运行记录。'))
    print(json.dumps({'stage': 'S3', 'status': 'PASS', 'rows': [len(env),len(rad)],
                      'figures': len(figure_items), 'environment': environment, 'radius': radius}, ensure_ascii=False))


if __name__ == '__main__':
    main()
