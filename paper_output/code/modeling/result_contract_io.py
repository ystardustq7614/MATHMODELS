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
