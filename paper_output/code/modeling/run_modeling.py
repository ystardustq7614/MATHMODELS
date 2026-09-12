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
