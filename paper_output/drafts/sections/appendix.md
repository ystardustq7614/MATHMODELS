# 附录

## 附录 A：数据与求解复现说明

正文计算来自 `paper_output/code/modeling/` 下的 `q1_model.py` 至 `q4_model.py`，共同调用 `core_solver.py`。在仓库根目录、满足 `requirements.txt` 依赖的 Python 环境中运行 `python paper_output/code/modeling/run_modeling.py` 可生成模型输出。运行清单 `paper_output/results/run_manifest.json` 记录脚本、输入、输出与退出码，复算时应核对其中的文件摘要。

初始场为301.15 K和2.55 kg/kg，正式空间网格1280单元、时间步长0.5 s，最多50轮迭代并按增量及残差停止。求解器函数默认参数仅供通用调用，正式四问从验证报告读取所选配置，复现不能省略这一层配置读取。环境和半径分别读取 `paper_output/data_cleaned/a_environment.csv`、`a_radius.csv`，采用分段线性插值。三对角算法为 `core_solver.py` 中的 `solve_thomas`。

`result1.xlsx` 含温度与水分浓度两表，从1至1800 s逐秒记录；`result2.xlsx` 同样有两表，从1 s延续至205818 s，表3、表4仅是前3 h的展示切片。`result3.xlsx` 按60 s保存固定半径含水率并额外保存205818 s终点；`result4.xlsx` 按60 s保存收缩域含水率并额外保存182969.5 s终点，最后一列为真实表面。四个文件均位于 `paper_output/tables/`。域外空值表示几何上不适用，不作为数值失败，也不填补为零。

## 附录 B：正文表格与证据文件对应

表4-2、表4-3分别整理自 `table_data_profile_a_environment`、`table_data_profile_a_radius` 对应的CSV。本文将重复单位、类型字段和开尔文转换列合并为中文表头，保留样本数、缺失数和统计量含义。

表5-1至表5-6依次对应 `table1` 至 `table6`。文件为 `table_aq1_temperature.csv`、`table_aq1_moisture.csv`、`table_aq2_temperature.csv`、`table_aq2_moisture.csv`、`table_aq3_drying_moisture.csv`、`table_aq4_shrinkage_moisture.csv`，均位于 `paper_output/tables/`，正文逐行与最新CSV同步。表6-1、表6-2、表6-3分别对应 `table7`、`table8`、`table9`，整理自完整数值验证记录，正文仅作有效位舍入。六幅图见 `paper_output/figures/`。

## 附录 C：数值检验的追溯

数值对照来自 `paper_output/qa/model_validation_checks.json`，生成程序为 `paper_output/code/visualization/run_numerical_validation.py`。记录包括80单元起始对照、逐级加密、1280单元正式设置与2560单元参考设置、0.5与0.25 s时间比较、三格顺序对照及三个独立边界情景。问题一补充联合加密见 `paper_output/qa/delivery_audit.json` 的预热比较记录。数据检验和后处理不产生新实测样本。

支撑材料应包含以下文件组：模型与结果导出源码、数据整理源码及通用读取模块、可视化和验证源码、运行依赖说明、两份清洗CSV、四份结果Excel、六张主结果CSV及数据统计表、六幅图、模型结果与指标结论JSON、数值验证JSON、运行清单，以及 `AI工具使用详情.pdf`。完整源程序列于附录E，文件名与相对目录均保留以支持复算。原始赛题数据由主办方提供，不作为自主查阅数据重复解释。

AI使用详情应如实记录工具名称、用途、提示过程和采纳方式。本次修订由Codex辅助核对文件、修订论述和排版；自动检查不等价于参赛队的逐项人工审查。工具具体模型版本及此前使用历史应由参赛队据真实记录补充，不以未知版本冒充已确认信息。


## 附录 D：完整运行诊断

以下为各问实际运行的完整诊断摘要。状态0表示到达指定展示终点，状态1表示触发干燥阈值；负状态表示失败，不能作为结果。数值量采用程序原始精度，正文仅保留解释所需的有效位。

| 诊断量 | 数值 | 单位 |
| --- | --- | --- |
| aq1_left_time_s | 1799.5 | s |
| aq1_end_time_s | 1800.0 | s |
| aq1_left_max_C | 2.5499922976882003 | kg/kg |
| aq1_final_max_C | 2.549992271962013 | kg/kg |
| aq1_water_balance | 1.2060069718477192e-14 | 1 |
| aq1_step_water_balance | 2.00152224587275e-16 | 1 |
| aq1_residual_C | 3.8706802378437625e-16 | 1 |
| aq1_residual_T | 2.4453460187734737e-16 | 1 |
| aq1_max_iterations | 4.0 | count |
| aq1_mean_iterations | 4.0 | count |
| aq1_steps | 3600 | count |
| aq1_center_excess_bound | 1.59003e-10 | kg/kg |
| aq1_status_code | 0.0 | 1 |
| aq2_left_time_s | 205817.5 | s |
| aq2_end_time_s | 205818.0 | s |
| aq2_left_max_C | 0.15000010079669182 | kg/kg |
| aq2_final_max_C | 0.14999995427300694 | kg/kg |
| aq2_water_balance | 4.4757226247633767e-14 | 1 |
| aq2_step_water_balance | 2.931943095510862e-16 | 1 |
| aq2_residual_C | 1.0867260945845985e-11 | 1 |
| aq2_residual_T | 3.512785547753425e-16 | 1 |
| aq2_max_iterations | 4.0 | count |
| aq2_mean_iterations | 3.36223994014129 | count |
| aq2_steps | 411636 | count |
| aq2_center_excess_bound | 1.54901110160921e-07 | kg/kg |
| aq2_status_code | 1.0 | 1 |
| aq3_left_time_s | 205817.5 | s |
| aq3_end_time_s | 205818.0 | s |
| aq3_left_max_C | 0.15000010079669182 | kg/kg |
| aq3_final_max_C | 0.14999995427300694 | kg/kg |
| aq3_water_balance | 4.4757226247633767e-14 | 1 |
| aq3_step_water_balance | 2.931943095510862e-16 | 1 |
| aq3_residual_C | 1.0867260945845985e-11 | 1 |
| aq3_residual_T | 3.512785547753425e-16 | 1 |
| aq3_max_iterations | 4.0 | count |
| aq3_mean_iterations | 3.36223994014129 | count |
| aq3_steps | 411636 | count |
| aq3_center_excess_bound | 1.54901110160921e-07 | kg/kg |
| aq3_status_code | 1.0 | 1 |
| aq4_left_time_s | 182969 | s |
| aq4_end_time_s | 182969.5 | s |
| aq4_left_max_C | 0.15000000160267352 | kg/kg |
| aq4_final_max_C | 0.14999974327394916 | kg/kg |
| aq4_water_balance | 4.7717820979967513e-14 | 1 |
| aq4_step_water_balance | 1.285284472465843e-16 | 1 |
| aq4_residual_C | 1.4649702830163243e-11 | 1 |
| aq4_residual_T | 3.347897338265732e-16 | 1 |
| aq4_max_iterations | 4.0 | count |
| aq4_mean_iterations | 3.482017494719065 | count |
| aq4_steps | 365939 | count |
| aq4_center_excess_bound | 2.4056242708958564e-07 | kg/kg |
| aq4_status_code | 1.0 | 1 |

## 附录 E：完整可运行源程序

以下逐文件列出本次建模、结果导出、图形生成与数值验证的源程序。保持相对目录关系，在项目根目录执行附录A的复现入口。数据整理程序还调用随项目提供的通用表格读取模块，该模块一并列出。

### E.1 paper_output/code/data_processing/prepare_a_data.py

```python
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
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8', newline='\n')


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
        with path.open('w', encoding='utf-8', newline='\n') as stream:
            np.savetxt(stream, converted, delimiter=',', header=','.join(columns), comments='', fmt='%.12g')
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
                       tail_mean_temperature_C=float(np.trapezoid(tail[:, 1], tail[:, 0]) / 3600), tail_mean_Ce=float(np.trapezoid(tail[:, 2], tail[:, 0]) / 3600),
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
              command=f'{sys.executable} -B paper_output/code/data_processing/prepare_a_data.py',
              executable=sys.executable, python=sys.version, numpy=np.__version__, matplotlib=matplotlib.__version__,
              scripts=[record(Path(__file__)), record(Path(loader.__file__))],
              inputs=[record(p) for p in tracked_inputs], outputs=[record(p) for p in outputs],
              note='数据处理运行证据；不是S5模型运行记录。'))
    print(json.dumps({'stage': 'S3', 'status': 'PASS', 'rows': [len(env),len(rad)],
                      'figures': len(figure_items), 'environment': environment, 'radius': radius}, ensure_ascii=False))


if __name__ == '__main__':
    main()
```

### E.2 .agents/skills/data-cleaning-and-visualization/scripts/robust_loader.py

```python
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime
from importlib import import_module
from pathlib import Path
from typing import Any


BASE_DIR = Path.cwd().resolve()
OUTPUT_DIR = BASE_DIR / "paper_output"
REPORT_FILE = OUTPUT_DIR / "data_cleaned" / "load_report.json"
INPUT_MANIFEST_FILE = OUTPUT_DIR / "input_manifest.json"

DATA_EXTS = {".xlsx", ".xls", ".csv", ".tsv", ".json"}
PDF_EXTS = {".pdf"}


def configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def safe_import(name: str):
    try:
        return import_module(name)
    except Exception:
        return None


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(BASE_DIR).as_posix()
    except Exception:
        return str(path).replace("\\", "/")


def sha256_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_entry(path: Path, kind: str) -> dict[str, Any]:
    return {
        "path": rel(path),
        "kind": kind,
        "ext": path.suffix.lower(),
        "readable": False,
        "warnings": [],
        "errors": [],
    }


def inspect_xlsx(path: Path) -> dict[str, Any]:
    info = file_entry(path, "spreadsheet")
    openpyxl = safe_import("openpyxl")
    if openpyxl is None:
        info["errors"].append("缺少依赖 openpyxl，无法读取 .xlsx。")
        return info
    try:
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    except Exception as exc:
        info["errors"].append(f"无法打开 xlsx：{type(exc).__name__}: {exc}")
        return info
    sheets = []
    try:
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            rows = ws.max_row or 0
            cols = ws.max_column or 0
            sample_cols: list[str] = []
            if rows and cols:
                first_row = next(ws.iter_rows(min_row=1, max_row=1, max_col=min(cols, 12), values_only=True), None)
                if first_row:
                    sample_cols = [str(value) if value is not None else "" for value in first_row]
            sheets.append({"name": sheet_name, "rows": rows, "cols": cols, "sample_cols": sample_cols})
            if rows == 0 or cols == 0:
                info["warnings"].append(f"工作表 {sheet_name} 为空。")
    finally:
        wb.close()
    try:
        wb2 = openpyxl.load_workbook(path, read_only=False, data_only=True)
        merged_count = sum(len(wb2[name].merged_cells.ranges) for name in wb2.sheetnames)
        wb2.close()
        if merged_count:
            info["warnings"].append(f"检测到 {merged_count} 处合并单元格，自动读取结果需人工核对。")
    except Exception:
        pass
    info["readable"] = True
    info["sheets"] = sheets
    return info


def inspect_xls(path: Path) -> dict[str, Any]:
    info = file_entry(path, "spreadsheet")
    xlrd = safe_import("xlrd")
    if xlrd is None:
        info["errors"].append("缺少依赖 xlrd，无法读取老 .xls；建议另存为 .xlsx。")
        return info
    try:
        book = xlrd.open_workbook(str(path))
    except Exception as exc:
        info["errors"].append(f"无法打开 xls：{type(exc).__name__}: {exc}")
        return info
    info["sheets"] = [{"name": sheet.name, "rows": sheet.nrows, "cols": sheet.ncols, "sample_cols": []} for sheet in book.sheets()]
    info["readable"] = True
    return info


def inspect_csv(path: Path) -> dict[str, Any]:
    info = file_entry(path, "table")
    pandas = safe_import("pandas")
    if pandas is not None:
        last_error: Exception | None = None
        for encoding in ("utf-8-sig", "utf-8", "gbk", "gb18030"):
            for sep in (None, ",", "\t", ";"):
                try:
                    df = pandas.read_csv(path, nrows=20, encoding=encoding, sep=sep, engine="python")
                    info.update(
                        {
                            "readable": True,
                            "encoding": encoding,
                            "sep": sep if sep is not None else "auto",
                            "rows_sampled": int(len(df)),
                            "cols": int(len(df.columns)),
                            "sample_cols": [str(col) for col in df.columns.tolist()],
                        }
                    )
                    if df.empty:
                        info["warnings"].append("CSV 读取成功但样本为空。")
                    return info
                except Exception as exc:
                    last_error = exc
        info["errors"].append(f"pandas 无法读取：{type(last_error).__name__}: {last_error}")
        return info

    # Fallback without pandas.
    for encoding in ("utf-8-sig", "utf-8", "gbk", "gb18030"):
        try:
            with path.open("r", encoding=encoding, newline="") as handle:
                sample = handle.read(4096)
                dialect = csv.Sniffer().sniff(sample) if sample.strip() else csv.excel
                handle.seek(0)
                reader = csv.reader(handle, dialect)
                first = next(reader, [])
            info.update({"readable": True, "encoding": encoding, "sep": getattr(dialect, "delimiter", ","), "sample_cols": [str(item) for item in first]})
            return info
        except Exception:
            continue
    info["errors"].append("无法以常见编码读取 CSV/TSV。")
    return info


def inspect_json(path: Path) -> dict[str, Any]:
    info = file_entry(path, "json")
    for encoding in ("utf-8-sig", "utf-8", "gbk", "gb18030"):
        try:
            data = json.loads(path.read_text(encoding=encoding))
            info["readable"] = True
            info["encoding"] = encoding
            if isinstance(data, dict):
                info["top_level"] = "dict"
                info["sample_keys"] = list(data.keys())[:12]
            elif isinstance(data, list):
                info["top_level"] = "list"
                info["length"] = len(data)
                if data and isinstance(data[0], dict):
                    info["sample_keys"] = list(data[0].keys())[:12]
            else:
                info["top_level"] = type(data).__name__
            return info
        except Exception:
            continue
    info["errors"].append("JSON 无法以常见编码解析。")
    return info


def inspect_pdf(path: Path) -> dict[str, Any]:
    info = file_entry(path, "pdf_diagnostic")
    info["readable"] = False
    pypdf = safe_import("pypdf")
    if pypdf is None:
        info["warnings"].append("缺少 pypdf，无法诊断 PDF 文本。")
    else:
        try:
            reader = pypdf.PdfReader(str(path))
            total_pages = len(reader.pages)
            sample_pages = min(5, total_pages)
            char_count = 0
            for index in range(sample_pages):
                try:
                    char_count += len(reader.pages[index].extract_text() or "")
                except Exception:
                    pass
            info["pdf_pages"] = total_pages
            info["text_pages_sampled"] = sample_pages
            info["text_char_count"] = char_count
            if char_count == 0:
                info["warnings"].append("PDF 前几页未抽出文本，可能是扫描版；请 OCR 或人工转为 CSV/XLSX。")
            elif char_count < 200:
                info["warnings"].append("PDF 可抽文本很少，请核对题面/表格是否完整。")
        except Exception as exc:
            info["warnings"].append(f"PDF 文本诊断失败：{type(exc).__name__}: {exc}")

    pdfplumber = safe_import("pdfplumber")
    if pdfplumber is None:
        info["table_diagnostic"] = {"available": False, "warning": "未安装 pdfplumber，未做 PDF 表格诊断。"}
    else:
        try:
            table_count = 0
            table_samples: list[dict[str, Any]] = []
            with pdfplumber.open(path) as pdf:
                for page_index, page in enumerate(pdf.pages[:5], start=1):
                    tables = page.extract_tables() or []
                    table_count += len(tables)
                    for table in tables[:3]:
                        table_samples.append(
                            {
                                "page": page_index,
                                "rows": len(table),
                                "cols": max((len(row) for row in table), default=0),
                            }
                        )
            info["table_diagnostic"] = {
                "available": True,
                "table_count_first_5_pages": table_count,
                "samples": table_samples[:8],
                "warning": "PDF 表格抽取仅供诊断，不能直接视为可信原始数据；正式建模建议转 CSV/XLSX 后人工核对。",
            }
        except Exception as exc:
            info["table_diagnostic"] = {"available": False, "warning": f"PDF 表格诊断失败：{type(exc).__name__}: {exc}"}
    return info


def iter_input_files(input_dirs: list[str]) -> list[Path]:
    files: list[Path] = []
    for text in input_dirs:
        path = (BASE_DIR / text).resolve()
        if path.exists() and path.is_dir():
            files.extend(item for item in path.rglob("*") if item.is_file())
    return sorted(files, key=lambda item: item.as_posix().lower())


def load_input_manifest() -> dict[str, Any] | None:
    if not INPUT_MANIFEST_FILE.exists():
        return None
    try:
        data = json.loads(INPUT_MANIFEST_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def resolve_manifest_path(path_text: str) -> Path:
    path = Path(str(path_text or ""))
    if path.is_absolute():
        return path
    return BASE_DIR / path


def iter_manifest_raw_data(manifest: dict[str, Any]) -> tuple[list[Path], list[dict[str, Any]]]:
    files: list[Path] = []
    skipped: list[dict[str, Any]] = []
    entries = manifest.get("entries") if isinstance(manifest, dict) else []
    if not isinstance(entries, list):
        return files, skipped
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        path_text = str(entry.get("path") or "")
        role = str(entry.get("role") or "")
        usable = bool(entry.get("usable_for_modeling"))
        path = resolve_manifest_path(path_text)
        if role == "raw_data" and usable:
            files.append(path)
        else:
            skipped.append(
                {
                    "path": path_text,
                    "role": role,
                    "reason": "not_raw_modeling_data" if role != "raw_data" else "not_usable_for_modeling",
                }
            )
    return sorted(files, key=lambda item: item.as_posix().lower()), skipped


def inspect_file(path: Path) -> dict[str, Any] | None:
    ext = path.suffix.lower()
    if ext == ".xlsx":
        return inspect_xlsx(path)
    if ext == ".xls":
        return inspect_xls(path)
    if ext in {".csv", ".tsv"}:
        return inspect_csv(path)
    if ext == ".json":
        return inspect_json(path)
    if ext == ".pdf":
        return inspect_pdf(path)
    return None


def evaluate(input_dirs: list[str], use_manifest: bool = True) -> dict[str, Any]:
    input_manifest = load_input_manifest() if use_manifest else None
    skipped_files: list[dict[str, Any]] = []
    if input_manifest:
        files, skipped_files = iter_manifest_raw_data(input_manifest)
    else:
        files = iter_input_files(input_dirs)
    data_files: list[dict[str, Any]] = []
    pdf_diagnostics: list[dict[str, Any]] = []
    warnings: list[str] = []
    errors: list[str] = []

    if use_manifest and input_manifest is None and INPUT_MANIFEST_FILE.exists():
        warnings.append("input_manifest.json 存在但无法解析，已回退为扫描 input_dirs。")
    if input_manifest:
        warnings.extend(
            f"{item['path']}: 跳过 role={item['role']}（{item['reason']}）。"
            for item in skipped_files
            if item.get("role") in {"result_template", "problem_statement", "problem_statement_unreadable"}
        )

    for path in files:
        info = inspect_file(path)
        if info is None:
            continue
        if path.suffix.lower() in PDF_EXTS:
            pdf_diagnostics.append(info)
        else:
            data_files.append(info)
        for item in info.get("warnings", []) or []:
            warnings.append(f"{info['path']}: {item}")
        for item in info.get("errors", []) or []:
            errors.append(f"{info['path']}: {item}")

    readable_data = [item for item in data_files if item.get("readable")]
    if not data_files:
        warnings.append("未发现 xlsx/xls/csv/tsv/json 数据文件；若数据在 PDF 中，请先人工核对并转为 CSV/XLSX。")
    elif not readable_data:
        errors.append("发现数据文件但没有任何文件可读。")

    return {
        "schema_version": "1.0",
        "generated_by": "data-cleaning-and-visualization/scripts/robust_loader.py",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not errors else "FAIL",
        "input_dirs": input_dirs,
        "input_manifest_used": bool(input_manifest),
        "input_manifest": rel(INPUT_MANIFEST_FILE) if input_manifest else "",
        "input_manifest_sha256": sha256_file(INPUT_MANIFEST_FILE) if input_manifest else "",
        "skipped_files": skipped_files,
        "data_files": data_files,
        "pdf_diagnostics": pdf_diagnostics,
        "summary": {
            "file_count_scanned": len(files),
            "data_file_count": len(data_files),
            "readable_data_file_count": len(readable_data),
            "pdf_file_count": len(pdf_diagnostics),
        },
        "warnings": warnings,
        "errors": errors,
    }


def write_report(report: dict[str, Any]) -> None:
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    configure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Diagnose MathModel input data files and write load_report.json.")
    parser.add_argument("--input-dir", action="append", dest="input_dirs", default=None, help="Input directory to scan. Can be repeated.")
    args = parser.parse_args()
    input_dirs = args.input_dirs or ["problem_files", "crawled_data"]
    report = evaluate(input_dirs, use_manifest=args.input_dirs is None)
    write_report(report)
    print(f"load report: {rel(REPORT_FILE)}")
    if report["status"] == "PASS":
        print("[LOAD PASS]")
        for warning in report["warnings"][:8]:
            print(f" [warn] {warning}")
        return 0
    print("[LOAD FAIL]")
    for error in report["errors"][:12]:
        print(f" - {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

### E.3 paper_output/code/modeling/core_solver.py

```python
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
```

### E.4 paper_output/code/modeling/q1_model.py

```python
# 问题1：使用题给数据求解并导出题目要求的结果。
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
    'question_id': 'AQ1',
    'title': '预热平衡阶段温度与干基含水率',
    'task_type': '非线性扩散与热传导',
    'main_model': '隐式有限体积法 (FVM) + Picard迭代 + Thomas三对角求解',
}

def run_aq1():
    config=json.loads((OUTPUT_DIR/'qa/model_validation_checks.json').read_text(encoding='utf-8'))['selected_configuration']
    N_run,dt_run=config['N'],config['dt_s']
    env_path = DATA_CLEANED_DIR / 'a_environment.csv'
    df_env = pd.read_csv(env_path)
    t_env = df_env['time_s'].values.astype(np.float64)
    T_env = df_env['temperature_K'].values.astype(np.float64)
    C_env = df_env['air_moisture_kgkg'].values.astype(np.float64)

    # 1. Run simulation for 1800 s with formula_mode=1 (Appendix 2)
    times_raw, T_raw, C_raw, end_time, n_rec, diagnostics = simulate_fvm_fixed(
        t_env=t_env,
        T_env=T_env,
        C_env=C_env,
        total_seconds=1800,
        formula_mode=1,
        sample_every_s=1,
        N=N_run,
        R=0.02,
        h=25.0,
        hm=8e-7,
        dt=dt_run,
        return_diagnostics=True,
    )

    if diagnostics['status']=='solver_failed':
        raise RuntimeError('AQ1 nonlinear solve failed')

    # 2. Build Table 1 (Temperature) & Table 2 (Moisture)
    times_tab = np.array([100, 300, 600, 900, 1200, 1500, 1800], dtype=np.float64)
    r_tab_cm = np.array([0.0, 0.5, 1.0, 1.5, 2.0], dtype=np.float64)

    # Interpolate to table points
    T_tab, C_tab = sample_and_interpolate_fixed(times_tab, T_raw[times_tab.astype(int)], C_raw[times_tab.astype(int)], N=N_run, R=0.02, r_target_cm=r_tab_cm, t_env=t_env, T_env=T_env, C_env=C_env, formula_mode=1)

    # Convert Temperature to Celsius
    T_tab_C = T_tab - 273.15

    # Write Table 1 CSV
    table1_rows = []
    for i, t_val in enumerate(times_tab):
        row = {'时间/s': int(t_val)}
        for j, r_val in enumerate(r_tab_cm):
            row[f'{r_val:g} cm'] = f'{T_tab_C[i, j]:.4f}'
        table1_rows.append(row)
    t1_path = TABLES_DIR / 'table_aq1_temperature.csv'
    write_csv_table(t1_path, table1_rows)

    # Write Table 2 CSV
    table2_rows = []
    for i, t_val in enumerate(times_tab):
        row = {'时间/s': int(t_val)}
        for j, r_val in enumerate(r_tab_cm):
            row[f'{r_val:g} cm'] = f'{C_tab[i, j]:.4f}'
        table2_rows.append(row)
    t2_path = TABLES_DIR / 'table_aq1_moisture.csv'
    write_csv_table(t2_path, table2_rows)

    # 3. Build result1.xlsx (1800 s, 0.1 cm steps)
    r_full_cm = np.arange(0.0, 2.0001, 0.1)
    T_full, C_full = sample_and_interpolate_fixed(times_raw, T_raw, C_raw, N=N_run, R=0.02, r_target_cm=r_full_cm, t_env=t_env, T_env=T_env, C_env=C_env, formula_mode=1)
    T_full_C = T_full - 273.15

    res1_path = TABLES_DIR / 'result1.xlsx'
    wb = openpyxl.Workbook(write_only=True)
    ws_T = wb.create_sheet('温度')
    ws_C = wb.create_sheet('水分浓度')

    header = ['时间\\到药材中心的距离'] + [round(r, 1) for r in r_full_cm]
    ws_T.append(header)
    ws_C.append(header)

    # 1 to 1800 s
    for s in range(1, 1801):
        row_T = [float(times_raw[s])] + [round(val, 4) for val in T_full_C[s]]
        row_C = [float(times_raw[s])] + [round(val, 4) for val in C_full[s]]
        ws_T.append(row_T)
        ws_C.append(row_C)
    wb.save(res1_path)

    # 4. Metrics & Contracts
    r_faces = np.linspace(0.0, 0.02, N_run+1)
    vols = np.pi * (r_faces[1:]**2 - r_faces[:-1]**2)
    C_mean = np.sum(vols * C_raw[-1]) / np.sum(vols)
    metrics = [
        {'metric_name': 'aq1_final_center_temperature_C', 'metric_role': 'evaluation', 'value': round_float(T_full_C[1800, 0], 4), 'unit': '°C'},
        {'metric_name': 'aq1_final_surface_temperature_C', 'metric_role': 'evaluation', 'value': round_float(T_full_C[1800, -1], 4), 'unit': '°C'},
        {'metric_name': 'aq1_final_center_moisture', 'metric_role': 'evaluation', 'value': round_float(C_full[1800, 0], 4), 'unit': 'kg/kg'},
        {'metric_name': 'aq1_final_surface_moisture', 'metric_role': 'evaluation', 'value': round_float(C_full[1800, -1], 4), 'unit': 'kg/kg'},
        {'metric_name': 'aq1_total_moisture_loss_fraction', 'metric_role': 'evaluation', 'value': round_float((2.55 - C_mean) / 2.55, 6), 'unit': 'fraction'},
    ]

    metrics += solver_metrics(diagnostics,'AQ1')

    conclusions = [
        {
            'question_id': 'AQ1',
            'conclusion_text': f'在预热平衡阶段（0-1800 s），药材受烘房升温与对流传热驱动，中心温度由28.0000°C上升至{T_full_C[1800, 0]:.4f}°C，表面温度达到{T_full_C[1800, -1]:.4f}°C；由于对流传质阻力与内部非线性水分扩散制约，药材表面干基含水率由2.5500 kg/kg下降至{C_full[1800, -1]:.4f} kg/kg，中心干基含水率为{C_full[1800, 0]:.4f} kg/kg，体现出显著的内外梯度迟滞效应。',
            'evidence_required': ['model_results.json', 'metrics.json', 'table_index.json'],
            'evidence_status': 'computed',
        }
    ]

    tables = [
        table_entry(
            question_id='AQ1',
            table_id='table1',
            title='30分钟内药材的温度（表1）',
            purpose='展示预热阶段100-1800 s各径向截面的药材温度动态。',
            path=t1_path,
            status='computed',
        ),
        table_entry(
            question_id='AQ1',
            table_id='table2',
            title='30分钟内药材的水分浓度（表2）',
            purpose='展示预热阶段100-1800 s各径向截面的干基水分浓度分布。',
            path=t2_path,
            status='computed',
        ),
    ]

    outputs = [
        {'path': str(t1_path), 'type': 'csv'},
        {'path': str(t2_path), 'type': 'csv'},
        {'path': str(res1_path), 'type': 'xlsx'},
    ]

    summary = f'AQ1预热平衡阶段数值求解完成：1800 s时中心温度为{T_full_C[1800, 0]:.4f}°C，表面温度为{T_full_C[1800, -1]:.4f}°C；中心水分浓度为{C_full[1800, 0]:.4f} kg/kg，表面水分浓度为{C_full[1800, -1]:.4f} kg/kg。表1、表2及result1.xlsx均已导出。'

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
    print('AQ1 finished successfully.')

if __name__ == '__main__':
    run_aq1()
```

### E.5 paper_output/code/modeling/q2_model.py

```python
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
```

### E.6 paper_output/code/modeling/q3_model.py

```python
# 问题3：使用题给数据求解并导出题目要求的结果。
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
    'question_id': 'AQ3',
    'title': '固定半径下全域达标时长',
    'task_type': '阈值事件检测',
    'main_model': '烘干终点全域极值检测 + 离散阈值事件检测',
}

def run_aq3():
    config=json.loads((OUTPUT_DIR/'qa/model_validation_checks.json').read_text(encoding='utf-8'))['selected_configuration']
    N_run,dt_run=config['N'],config['dt_s']
    env_path = DATA_CLEANED_DIR / 'a_environment.csv'
    df_env = pd.read_csv(env_path)
    t_env = df_env['time_s'].values.astype(np.float64)
    T_env = df_env['temperature_K'].values.astype(np.float64)
    C_env = df_env['air_moisture_kgkg'].values.astype(np.float64)

    # 1. Run simulation until max(C) < 0.15 kg/kg (sampling every 60 s)
    # Maximum horizon 72 h = 259200 s
    times_raw, T_raw, C_raw, end_time, n_rec, diagnostics = simulate_fvm_fixed(
        t_env=t_env,
        T_env=T_env,
        C_env=C_env,
        total_seconds=259200,
        formula_mode=2,
        sample_every_s=60,
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


    t_end_s = end_time
    t_end_h = t_end_s / 3600.0

    # 2. Build Table 5 (Moisture every 6 h + drying end time)
    # Target radii: 0, 0.5, 1.0, 1.5, 2.0 cm
    r_tab_cm = np.array([0.0, 0.5, 1.0, 1.5, 2.0], dtype=np.float64)

    # 6 h intervals in seconds: 6h=21600s, 12h=43200s, ... up to t_end_s
    max_6h = int(t_end_s // 21600)
    times_6h_s = [i * 21600 for i in range(1, max_6h + 1)]
    if t_end_s not in times_6h_s:
        times_tab_s = np.array(times_6h_s + [t_end_s], dtype=np.float64)
    else:
        times_tab_s = np.array(times_6h_s, dtype=np.float64)

    # Find the matching indices in times_raw
    tab_indices = []
    for ts in times_tab_s:
        idx = np.argmin(np.abs(times_raw - ts))
        tab_indices.append(idx)
    tab_indices = np.array(tab_indices)

    T_tab, C_tab = sample_and_interpolate_fixed(
        times_tab_s,
        T_raw[tab_indices],
        C_raw[tab_indices],
        N=N_run,
        R=0.02,
        r_target_cm=r_tab_cm,
        t_env=t_env, T_env=T_env, C_env=C_env, formula_mode=2,
    )

    table5_rows = []
    for i, ts in enumerate(times_tab_s):
        if i == len(times_tab_s) - 1 and abs(ts - t_end_s) < 1e-3:
            time_label = f'烘干结束时间 ({t_end_h:.4f} h)'
        else:
            time_label = f'{ts / 3600.0:.1f}'
        row = {'时间/h': time_label}
        for j, r_val in enumerate(r_tab_cm):
            row[f'{r_val:g} cm'] = f'{C_tab[i, j]:.4f}'
        table5_rows.append(row)

    t5_path = TABLES_DIR / 'table_aq3_drying_moisture.csv'
    write_csv_table(t5_path, table5_rows)

    # 3. Build result3.xlsx (every 60 s + end time, 0.1 cm steps)
    r_full_cm = np.arange(0.0, 2.0001, 0.1)
    T_full, C_full = sample_and_interpolate_fixed(
        times_raw,
        T_raw,
        C_raw,
        N=N_run,
        R=0.02,
        r_target_cm=r_full_cm,
        t_env=t_env, T_env=T_env, C_env=C_env, formula_mode=2,
    )

    res3_path = TABLES_DIR / 'result3.xlsx'
    wb = openpyxl.Workbook(write_only=True)
    ws = wb.create_sheet('Sheet1')

    header = ['时间\\到药材中心的距离'] + [round(r, 1) for r in r_full_cm]
    ws.append(header)

    for i in range(1, len(times_raw)):
        t_sec = float(times_raw[i])
        row = [t_sec] + [round(val, 4) for val in C_full[i]]
        ws.append(row)
    wb.save(res3_path)

    # 4. Metrics & Contracts
    metrics = [
        {'metric_name': 'aq3_drying_time_s', 'metric_role': 'evaluation', 'value': round_float(t_end_s, 2), 'unit': 's'},
        {'metric_name': 'aq3_drying_time_h', 'metric_role': 'evaluation', 'value': round_float(t_end_h, 4), 'unit': 'h'},
        {'metric_name': 'aq3_final_max_moisture', 'metric_role': 'evaluation', 'value': round_float(np.max(C_full[-1]), 4), 'unit': 'kg/kg'},
        {'metric_name': 'aq3_final_min_moisture', 'metric_role': 'evaluation', 'value': round_float(np.min(C_full[-1]), 4), 'unit': 'kg/kg'},
        {'metric_name': 'aq3_final_center_moisture', 'metric_role': 'evaluation', 'value': round_float(C_full[-1, 0], 4), 'unit': 'kg/kg'},
        {'metric_name': 'aq3_final_surface_moisture', 'metric_role': 'evaluation', 'value': round_float(C_full[-1, -1], 4), 'unit': 'kg/kg'},
    ]

    metrics += solver_metrics(diagnostics,'AQ3')

    conclusions = [
        {
            'question_id': 'AQ3',
            'conclusion_text': f'在固定几何尺寸（半径2 cm）下，严格以药材全域最大含水率低于0.15 kg/kg作为烘干完成判定准则，模型计算得到烘干所需时间为{t_end_h:.4f}小时（即{t_end_s:.1f}秒）。烘干结束时刻中心含水率为{C_full[-1, 0]:.4f} kg/kg，表面含水率为{C_full[-1, -1]:.4f} kg/kg，全域最大含水率达到达标临界值0.1500 kg/kg。表5及result3.xlsx均已导出。',
            'evidence_required': ['model_results.json', 'metrics.json', 'table_index.json'],
            'evidence_status': 'computed',
        }
    ]

    tables = [
        table_entry(
            question_id='AQ3',
            table_id='table5',
            title='药材烘干过程的水分浓度（表5）',
            purpose='展示固定半径下每隔6小时及烘干结束时刻各截面含水率衰变历程。',
            path=t5_path,
            status='computed',
        ),
    ]

    outputs = [
        {'path': str(t5_path), 'type': 'csv'},
        {'path': str(res3_path), 'type': 'xlsx'},
    ]

    summary = f'AQ3固定半径烘干时长确定完成：烘干达标时长为{t_end_h:.4f} h ({t_end_s:.1f} s)；终点中心水分浓度为{C_full[-1, 0]:.4f} kg/kg，表面为{C_full[-1, -1]:.4f} kg/kg。表5与result3.xlsx已导出。'

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
    print(f'AQ3 finished successfully: t_end = {t_end_h:.4f} h ({t_end_s:.1f} s).')

if __name__ == '__main__':
    run_aq3()
```

### E.7 paper_output/code/modeling/q4_model.py

```python
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
```

### E.8 paper_output/code/modeling/result_contract_io.py

```python
"""四问共用的结果写出：CSV、指标、结论与运行来源。"""
from pathlib import Path
from datetime import datetime
import csv
import hashlib
import json
import sys

PROJECT_ROOT=Path(__file__).resolve().parents[3]
OUTPUT_DIR=PROJECT_ROOT/'paper_output'
RESULTS_DIR=OUTPUT_DIR/'results'
TABLES_DIR=OUTPUT_DIR/'tables'
DATA_CLEANED_DIR=OUTPUT_DIR/'data_cleaned'


def round_float(value,ndigits=6):
    return round(float(value),ndigits)


def rel(path):
    return Path(path).resolve().relative_to(PROJECT_ROOT).as_posix()


def write_csv_table(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)


def table_entry(question_id,table_id,title,purpose,path,status):
    return dict(question_id=question_id,table_id=table_id,title=title,purpose=purpose,
                path=rel(path),source='paper_output/code/modeling',status=status)


def solver_metrics(diag,qid):
    names={'left_time_s':'s','end_time_s':'s','left_max_C':'kg/kg','final_max_C':'kg/kg',
           'water_balance':'1','step_water_balance':'1','residual_C':'1','residual_T':'1',
           'max_iterations':'count','mean_iterations':'count','steps':'count',
           'center_excess_bound':'kg/kg','status_code':'1'}
    return [dict(metric_name=qid.lower()+'_'+key,metric_role='validation',value=diag[key],unit=unit)
            for key,unit in names.items()]


def upsert_question_contracts(question,result_summary,metrics,tables,conclusions,outputs,
                              parameters=None,status='computed'):
    stamp=datetime.now().isoformat(timespec='seconds')
    qid=question['question_id']
    runner=Path(sys.argv[0]).resolve()
    artifacts=[rel(item['path']) for item in outputs]
    provenance=dict(source_code_path=rel(runner),source_code_sha256=hashlib.sha256(runner.read_bytes()).hexdigest(),
        helper_path=rel(Path(__file__)),run_command=f'{sys.executable} -B {rel(runner)}',run_exit_code=0,
        input_files=['paper_output/data_cleaned/a_environment.csv']+(['paper_output/data_cleaned/a_radius.csv'] if qid=='AQ4' else []),
        output_artifacts=artifacts,generated_at=stamp)
    paths=[RESULTS_DIR/'model_results.json',RESULTS_DIR/'metrics.json',RESULTS_DIR/'conclusions.json',TABLES_DIR/'table_index.json']
    contracts=[json.loads(p.read_text(encoding='utf-8')) for p in paths]
    model,metric,conclusion,table=contracts
    item=dict(question_id=qid,title=question['title'],task_type=question['task_type'],result_type='simulation',
        main_model=question['main_model'],baseline_model='',result_summary=result_summary,
        outputs=[dict(x,path=rel(x['path'])) for x in outputs],parameters=parameters or [],
        evidence_status=status,status=status,execution_provenance=provenance)
    model['questions']=[x for x in model['questions'] if x['question_id']!=qid]+[item]
    metric['items']=[x for x in metric['items'] if x['question_id']!=qid]+[dict(x,question_id=qid,status=status) for x in metrics]
    conclusion['items']=[x for x in conclusion['items'] if x['question_id']!=qid]+conclusions
    ids={x['table_id'] for x in tables}
    table['tables']=[x for x in table['tables'] if x['table_id'] not in ids]+tables
    table['notes']=['各结果来自实际数值运行；显示四位小数不代表四位小数的物理准确度。']
    for path,data in zip(paths,contracts):
        data.update(schema_version='1.0',generated_by='paper_output/code/modeling/result_contract_io.py',generated_at=stamp)
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
```

### E.9 paper_output/code/modeling/run_modeling.py

```python
"""依次运行四问、更新现有图表和真实运行记录。先执行数值验证脚本。"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys
import platform

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'paper_output'
CODE=OUT/'code/modeling'


def record(path):
    return dict(path=path.relative_to(ROOT).as_posix(),exists=True,bytes=path.stat().st_size,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def main():
    validation=json.loads((OUT/'qa/model_validation_checks.json').read_text(encoding='utf-8'))
    assert validation['status']=='PASS', '先完成数值验证'
    for name,sha in validation['input_hashes'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha, name
    selected=[int(q) for q in sys.argv[1:]] if len(sys.argv)>1 else list(range(1,5))
    runs=[]
    if len(selected)<4:
        previous=json.loads((OUT/'results/run_manifest.json').read_text(encoding='utf-8'))
        runs=[r for r in previous['runs'] if not any(f'AQ{q}' in r['question_ids'] for q in selected)]
    environment=dict(os.environ,PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
    for q in selected:
        script=CODE/f'q{q}_model.py'
        started=datetime.now(timezone.utc).isoformat()
        command=[sys.executable,'-B',str(script)]
        print(f'Running AQ{q}',flush=True)
        result=subprocess.run(command,cwd=ROOT,env=environment,capture_output=True,text=True,encoding='utf-8')
        print(result.stdout,flush=True)
        if result.returncode:
            print(result.stderr,flush=True)
            raise RuntimeError(f'AQ{q} failed')
        model=json.loads((OUT/'results/model_results.json').read_text(encoding='utf-8'))
        item=next(x for x in model['questions'] if x['question_id']==f'AQ{q}')
        inputs=[OUT/'data_cleaned/a_environment.csv',CODE/'core_solver.py',CODE/'result_contract_io.py',OUT/'qa/model_validation_checks.json']
        if q==4: inputs.append(OUT/'data_cleaned/a_radius.csv')
        runs.append(dict(run_id=f'AQ{q}_{started}',script=record(script)['path'],script_sha256=record(script)['sha256'],
            question_ids=[f'AQ{q}'],command=f'{sys.executable} -B {script.relative_to(ROOT).as_posix()}',returncode=0,status='PASS',
            started_at=started,finished_at=datetime.now(timezone.utc).isoformat(),working_directory='.',
            environment=dict(python=sys.version,platform=platform.platform()),input_files=[record(p) for p in inputs],
            output_artifacts=[record(ROOT/p) for p in item['execution_provenance']['output_artifacts']],stdout_tail=result.stdout))
    plot=OUT/'code/visualization/generate_model_evidence.py'
    subprocess.run([sys.executable,'-B',str(plot)],cwd=ROOT,env=environment,check=True)
    # 验证表和顺序对照保存在已有JSON中；正文直接引用这些真实计算记录。
    metrics=json.loads((OUT/'results/metrics.json').read_text(encoding='utf-8'))
    metrics['numerical_validation']=validation
    (OUT/'results/metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    index=json.loads((OUT/'tables/table_index.json').read_text(encoding='utf-8'))
    additional=[('table7','AQ3','长程网格与时间步验证','accepted_combined_comparison'),
                ('table8','AQ4','三格顺序对照','sequential_contrast'),
                ('table9','AQ3','边界情景检验','scenarios')]
    ids={x[0] for x in additional}
    index['tables']=[x for x in index['tables'] if x['table_id'] not in ids]
    for tid,qid,title,section in additional:
        index['tables'].append(dict(table_id=tid,question_id=qid,title=title,purpose=title,
            path='paper_output/qa/model_validation_checks.json',json_section=section,status='computed',source='numerical_validation'))
    (OUT/'tables/table_index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest=dict(schema_version='1.0',generated_by='paper_output/code/modeling/run_modeling.py',
        generated_at=datetime.now(timezone.utc).isoformat(),status='PASS',runs=runs,
        validation_provenance=validation['execution_provenance'],
        validation_record=record(OUT/'qa/model_validation_checks.json'),
        figure_generator=record(plot),
        final_artifacts=[record(OUT/p) for p in ['results/model_results.json','results/metrics.json','results/conclusions.json','tables/table_index.json','figure_index.json']],
        generator=record(Path(__file__)))
    (OUT/'results/run_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Four questions and figures complete.',flush=True)


if __name__=='__main__':
    main()
```

### E.10 paper_output/code/visualization/generate_model_evidence.py

```python
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
```

### E.11 paper_output/code/visualization/run_numerical_validation.py

```python
"""数值检验与三格对照；只更新现有验证报告，不写临时轨迹文件。"""
from pathlib import Path
from datetime import datetime, timezone
import sys
import json
import hashlib
import time
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'paper_output'
sys.path.insert(0,str(OUT/'code/modeling'))
from core_solver import simulate_fvm_fixed, simulate_fvm_moving


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    f = pd.read_csv(OUT/'data_cleaned/a_environment.csv')
    r = pd.read_csv(OUT/'data_cleaned/a_radius.csv')
    return (f.time_s.to_numpy(),f.temperature_K.to_numpy(),f.air_moisture_kgkg.to_numpy()), (r.time_s.to_numpy(),r.radius_m.to_numpy())


def solve(env,rad,moving=False,mode=2,N=80,dt=1.,converge=True,horizon=259200,threshold=.15):
    settings = dict(total_seconds=horizon,N=N,dt=dt,sample_every_s=60,
                    stop_at_cmax=threshold,return_diagnostics=True,
                    max_iterations=50 if converge else 2,converge=converge)
    if moving:
        z = simulate_fvm_moving(*env,*rad,**settings)
        times,R,T,C,end,count,diag = z
    else:
        z = simulate_fvm_fixed(*env,formula_mode=mode,**settings)
        times,T,C,end,count,diag = z
        R = np.full(len(times),.02)
    return dict(times=times,R=R,T=T,C=C,diagnostics=diag,N=N,dt=dt)


def compare(a,b):
    # 只比较共同60s时刻，细网格插值到较粗网格单元中心。
    count = min(int(a['times'][-1]//60),int(b['times'][-1]//60))+1
    ra = (np.arange(a['N'])+.5)/a['N']
    rb = (np.arange(b['N'])+.5)/b['N']
    differences = {}
    for key in ['T','C']:
        err = max(np.max(np.abs(a[key][i]-np.interp(ra,rb,b[key][i]))) for i in range(count))
        differences['max_abs_'+key] = float(err)
    differences['event_relative_difference'] = float(abs(a['times'][-1]-b['times'][-1])/b['times'][-1])
    differences['pass'] = bool(differences['max_abs_T']<=.05 and differences['max_abs_C']<=5e-4
                           and differences['event_relative_difference']<=.005)
    return differences


def summarize(x):
    ids = sorted(set([0]+[i for i,t in enumerate(x['times']) if t in [1800,10800,21600,86400,172800]]+[len(x['times'])-1]))
    return dict(N=x['N'],dt_s=x['dt'],diagnostics=x['diagnostics'],
                checkpoints=[dict(time_s=float(x['times'][i]),radius_m=float(x['R'][i]),
                    center_T=float(x['T'][i,0]),surface_cell_T=float(x['T'][i,-1]),
                    max_C=float(x['C'][i].max()),min_C=float(x['C'][i].min()),
                    max_cell=int(np.argmax(x['C'][i])),
                    center_reconstructed_C=float((9*x['C'][i,0]-x['C'][i,1])/8)) for i in ids])


def short_checks(env,rad):
    checks = {}
    for dt in [.5,1.,2.]:
        z = simulate_fvm_fixed(*env,10.3,1,dt=dt,return_diagnostics=True)
        checks['sampling_'+str(dt)] = bool(np.allclose(z[0],np.r_[np.arange(11),10.3]) and z[-1]['water_balance']<1e-6)
    uniform_env=(np.array([0.,60.]),np.array([301.15,301.15]),np.array([2.55,2.55]))
    z=simulate_fvm_moving(*uniform_env,np.array([0.,60.]),np.array([.02,.019]),60,return_diagnostics=True)
    checks['uniform_moving'] = bool(np.max(abs(z[2]-301.15))<1e-8 and np.max(abs(z[3]-2.55))<1e-8)
    a=solve(env,rad,mode=3,horizon=3600,threshold=-1.)
    b=solve(env,(np.array([0.,3600.]),np.array([.02,.02])),moving=True,horizon=3600,threshold=-1.)
    checks['constant_radius'] = bool(np.max(abs(a['T']-b['T']))<1e-8 and np.max(abs(a['C']-b['C']))<1e-8)
    z=simulate_fvm_fixed(*env,1800,1,sample_every_s=60,stop_at_cmax=2.549999,return_diagnostics=True)
    checks['event_between_samples'] = bool(z[-1]['status']=='reached' and z[-1]['left_max_C']>=2.549999 and z[-1]['final_max_C']<2.549999 and z[0][-1]==z[-1]['end_time_s'])
    z=simulate_fvm_fixed(*env,2,2,return_diagnostics=True,max_iterations=1)
    checks['nonlinear_failure'] = z[-1]['status']=='solver_failed'
    checks['not_reached'] = a['diagnostics']['status']=='not_reached'
    return checks


def main():
    started=time.perf_counter()
    env,rad=inputs()
    report=dict(schema_version='2.0',generated_by='paper_output/code/visualization/run_numerical_validation.py',
        generated_at=datetime.now(timezone.utc).isoformat(),status='IN_PROGRESS',checks=short_checks(env,rad),runs={},comparisons={},scenarios={})
    path=OUT/'qa/model_validation_checks.json'
    def save():
        path.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    if not all(report['checks'].values()):
        report['status']='FAIL';save();raise RuntimeError(report['checks'])
    accepted={}
    fine_seeds={}
    for qid,moving in [('AQ3',False),('AQ4',True)]:
        batch={}
        for key,N,dt,converge in [('B0',80,1.,False),('B1',80,1.,True),('B2',160,1.,True),('B3',160,.5,True)]:
            tick=time.perf_counter()
            x=solve(env,rad,moving=moving,N=N,dt=dt,converge=converge)
            if x['diagnostics']['status']=='not_reached':
                x=solve(env,rad,moving=moving,N=N,dt=dt,converge=converge,horizon=604800)
            batch[key]=x
            item=summarize(x);item['elapsed_s']=time.perf_counter()-tick
            report['runs'][qid+'_'+key]=item
            print(qid,key,x['times'][-1],x['diagnostics']['status'],flush=True)
            save()
        report['comparisons'][qid]={label:compare(batch[a],batch[b]) for label,a,b in [
            ('iteration','B0','B1'),('space','B1','B2'),('time','B2','B3'),('combined','B1','B3')]}
        accepted[qid]=batch['B1']
        fine_seeds[qid]=batch['B3']
        save()
    selected_N,selected_dt=80,1.
    baseline_ok=all(v[k]['pass'] for v in report['comparisons'].values() for k in ['space','time','combined'])
    report['refinement_comparisons']={}
    if not baseline_ok:
        coarse=fine_seeds
        N=160
        while True:
            fine={}
            comparisons={}
            for qid,moving in [('AQ3',False),('AQ4',True)]:
                fine[qid]=solve(env,rad,moving=moving,N=2*N,dt=.5)
                report['runs'][f'{qid}_N{2*N}_dt0.5']=summarize(fine[qid])
                comparisons[qid]=compare(coarse[qid],fine[qid])
                print('REFINE',qid,N,2*N,comparisons[qid],flush=True)
            report['refinement_comparisons'][str(N)]=comparisons
            save()
            if all(x['pass'] for x in comparisons.values()):
                temporal={}
                combined={}
                for qid,moving in [('AQ3',False),('AQ4',True)]:
                    finer=solve(env,rad,moving=moving,N=2*N,dt=.25)
                    report['runs'][f'{qid}_N{2*N}_dt0.25']=summarize(finer)
                    temporal[qid]=compare(fine[qid],finer)
                    combined[qid]=compare(coarse[qid],finer)
                    print('REFINED_TIME',qid,temporal[qid],combined[qid],flush=True)
                report['accepted_time_comparison']=temporal
                report['accepted_combined_comparison']=combined
                if all(x['pass'] for x in temporal.values()) and all(x['pass'] for x in combined.values()):
                    accepted=coarse
                    selected_N,selected_dt=N,.5
                    break
            if N>=1280:
                report['status']='FAIL';save();raise RuntimeError('Refinement target not reached')
            coarse=fine
            N*=2
    report['selected_configuration']=dict(N=selected_N,dt_s=selected_dt,max_iterations=50)
    save()
    configurations=[('appendix4_fixed',3,1.,False),('Ce_low',2,.8,False),('Ce_high',2,1.2,False),('tail_hour',2,1.,True)]
    for name,mode,scale,tail in configurations:
        te,Ta,Ce=[v.copy() for v in env]
        Ce *= scale
        if tail:
            take=te>=10800
            meanT=np.trapezoid(Ta[take],te[take])/3600
            meanC=np.trapezoid(Ce[take],te[take])/3600
            te=np.r_[te,14400.+1e-6,604800.]
            Ta=np.r_[Ta,meanT,meanT];Ce=np.r_[Ce,meanC,meanC]
        x=solve((te,Ta,Ce),rad,mode=mode,N=selected_N,dt=selected_dt)
        if x['diagnostics']['status']=='not_reached':
            x=solve((te,Ta,Ce),rad,mode=mode,horizon=604800,N=selected_N,dt=selected_dt)
        report['scenarios'][name]=summarize(x)
        print(name,x['times'][-1],x['diagnostics']['status'],flush=True)
        save()
    t3=accepted['AQ3']['times'][-1];t4=accepted['AQ4']['times'][-1]
    tf=report['scenarios']['appendix4_fixed']['diagnostics']['end_time_s']
    report['sequential_contrast']=dict(t3F_s=float(t3),t4F_s=float(tf),t4S_s=float(t4),
        property_change_percent=float((tf-t3)/t3*100),geometry_change_percent=float((t4-tf)/t3*100),
        total_change_percent=float((t4-t3)/t3*100),interpretation='指定先物性后几何路径；不估计交互')
    for item in report['scenarios'].values():
        item['relative_time_change_percent']=(item['diagnostics']['end_time_s']-t3)/t3*100
    fields=[*report['runs'].values(),*report['scenarios'].values()]
    passed=all(v['diagnostics']['status']=='reached' and v['diagnostics']['water_balance']<=1e-6 for v in fields)
    passed &= baseline_ok or (all(v['pass'] for v in report['accepted_time_comparison'].values()) and all(v['pass'] for v in report['accepted_combined_comparison'].values()))
    report['status']='PASS' if passed else 'FAIL'
    report['selected_configuration']=dict(N=selected_N,dt_s=selected_dt,max_iterations=50) if passed else None
    tracked=[Path(__file__),OUT/'code/modeling/core_solver.py',OUT/'data_cleaned/a_environment.csv',OUT/'data_cleaned/a_radius.csv']
    report['input_hashes']={p.relative_to(ROOT).as_posix():digest(p) for p in tracked}
    report['elapsed_s']=time.perf_counter()-started
    report['execution_provenance']=dict(command=f'{sys.executable} -B paper_output/code/visualization/run_numerical_validation.py',returncode=0 if passed else 1)
    save()
    print(json.dumps({'status':report['status'],'comparisons':report['comparisons'],'sequential':report['sequential_contrast'],'elapsed_s':report['elapsed_s']},ensure_ascii=False),flush=True)
    return 0 if passed else 1


if __name__=='__main__':
    raise SystemExit(main())
```

### E.12 paper_output/code/visualization/solver_worker.py

```python
"""单工况诊断入口：结果打印至标准输出，不创建临时文件。"""
import sys
import json
from run_numerical_validation import inputs,solve,summarize

if __name__=='__main__':
    kind,N,dt,horizon=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4])
    env,rad=inputs()
    result=solve(env,rad,moving=kind.startswith('moving'),mode=int(kind[-1]),N=N,dt=dt,horizon=horizon)
    print(json.dumps(summarize(result),ensure_ascii=False,allow_nan=False))
```

### E.末 运行依赖

```text
numpy>=2.0,<3
numba>=0.60,<1
pandas>=2.2,<4
matplotlib>=3.8,<4
seaborn>=0.13,<1
requests>=2.32,<3
python-docx>=1.1,<2
pypdf>=5,<7
openpyxl>=3.1,<4
xlrd>=2,<3
lxml>=5,<7
latex2mathml>=3.77,<4
```

<!-- mathmodel-evidence: metric:ALL:aq1_center_excess_bound, metric:ALL:aq1_end_time_s, metric:ALL:aq1_final_max_C, metric:ALL:aq1_left_max_C, metric:ALL:aq1_left_time_s, metric:ALL:aq1_max_iterations, metric:ALL:aq1_mean_iterations, metric:ALL:aq1_residual_C, metric:ALL:aq1_residual_T, metric:ALL:aq1_status_code, metric:ALL:aq1_step_water_balance, metric:ALL:aq1_steps, metric:ALL:aq1_water_balance, metric:ALL:aq2_center_excess_bound, metric:ALL:aq2_end_time_s, metric:ALL:aq2_final_max_C, metric:ALL:aq2_left_max_C, metric:ALL:aq2_left_time_s, metric:ALL:aq2_max_iterations, metric:ALL:aq2_mean_iterations, metric:ALL:aq2_residual_C, metric:ALL:aq2_residual_T, metric:ALL:aq2_status_code, metric:ALL:aq2_step_water_balance, metric:ALL:aq2_steps, metric:ALL:aq2_water_balance, metric:ALL:aq3_center_excess_bound, metric:ALL:aq3_end_time_s, metric:ALL:aq3_final_max_C, metric:ALL:aq3_left_max_C, metric:ALL:aq3_left_time_s, metric:ALL:aq3_max_iterations, metric:ALL:aq3_mean_iterations, metric:ALL:aq3_residual_C, metric:ALL:aq3_residual_T, metric:ALL:aq3_status_code, metric:ALL:aq3_step_water_balance, metric:ALL:aq3_steps, metric:ALL:aq3_water_balance, metric:ALL:aq4_center_excess_bound, metric:ALL:aq4_end_time_s, metric:ALL:aq4_final_max_C, metric:ALL:aq4_left_max_C, metric:ALL:aq4_left_time_s, metric:ALL:aq4_max_iterations, metric:ALL:aq4_mean_iterations, metric:ALL:aq4_residual_C, metric:ALL:aq4_residual_T, metric:ALL:aq4_status_code, metric:ALL:aq4_step_water_balance, metric:ALL:aq4_steps, metric:ALL:aq4_water_balance -->
