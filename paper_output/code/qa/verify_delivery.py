"""Recheck manuscript, native equations, source listings and complete Excel exports."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import importlib.util
import json
import math
import re
import sys
import zipfile
from lxml import etree
from docx import Document
import pymupdf

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'paper_output'
sys.path.insert(0, str(ROOT / '.agents/skills/paper-formal-writer/scripts'))
from formula_omml import source_formula_tokens
from paper_scope import body_text


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    failures = []
    hashes = {}

    def require(condition, message):
        if not condition:
            failures.append(message)

    source_path = OUT / 'final_paper_source.md'
    text = source_path.read_text(encoding='utf-8')
    body = body_text(text)
    prose = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', body)
    require(not re.search(r'\b(?:aq\d_|validation_|fig_|table_data_)\w*|\bboolean\b|\bfraction\b', prose),
            'Internal evidence identifiers remain in body prose')
    require(not any(value in prose for value in ['51.12 h', '57.06 h', '10.85%', '0.49%']),
            'Unrun factorial results remain in the manuscript')

    docx = Document(OUT / 'final_paper.docx')
    docx_text = '\n'.join(p.text for p in docx.paragraphs)
    captions = re.findall(r'!\[([^\]]+)\]\([^)]+\)', body)
    require(len(captions) == 6, 'Expected six figure captions')
    for caption in captions:
        require(docx_text.count(caption) == 1, 'DOCX caption missing or duplicated: ' + caption)
        label = re.match(r'图\s*\d+-\d+', caption).group()
        require(len(re.findall(re.escape(label), body)) >= 2, 'Figure lacks body citation: ' + label)

    tokens = source_formula_tokens(text)
    ns = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}
    with zipfile.ZipFile(OUT / 'final_paper.docx') as package:
        xml = etree.fromstring(package.read('word/document.xml'))
    native = len(xml.findall('.//m:oMath', ns))
    require(native == len(tokens), 'Native equation count differs from source')
    for path in sorted((OUT / 'code/modeling').glob('*.py')) + sorted((OUT / 'code/visualization').glob('*.py')):
        listing = '\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines()).rstrip()
        require(listing in text, 'Incomplete source listing: '+path.name)
        hashes[path.relative_to(ROOT).as_posix()] = sha(path)

    table_files = ['table_aq1_temperature.csv', 'table_aq1_moisture.csv',
                   'table_aq2_temperature.csv', 'table_aq2_moisture.csv',
                   'table_aq3_drying_moisture.csv', 'table_aq4_shrinkage_moisture.csv']
    compared_cells = 0
    for number, name in enumerate(table_files, 1):
        tail = text.split(f'**表 5-{number} ', 1)[1]
        block = re.search(r'(?m)^\|[^\n]+\n(?:\|[^\n]+\n)+', tail).group()
        rows = [[c.strip() for c in line.strip().strip('|').split('|')] for line in block.splitlines()]
        rows = [rows[0], *rows[2:]]
        with (OUT / 'tables' / name).open(encoding='utf-8-sig', newline='') as handle:
            expected = list(csv.reader(handle))
        require(rows == expected, 'Paper table differs from computed CSV: '+name)
        compared_cells += sum(len(row) for row in expected[1:])

    report = json.loads((OUT / 'format_check_report.json').read_text(encoding='utf-8'))
    render = report['render_qa']
    require(report['status'] == 'PASS' and render['status'] == 'PASS', 'S8 did not pass')
    require(render['mode'] == 'required', 'Formal render did not use required mode')
    for name, expected in report['input_hashes'].items():
        require((ROOT / name).is_file() and sha(ROOT / name) == expected, 'Stale S8 input: '+name)
    pdf = pymupdf.open(ROOT / render['pdf'])
    require('LibreOffice' in str(pdf.metadata.get('producer')), 'PDF not produced by LibreOffice')
    require('1 问题重述' not in pdf[0].get_text() and '关键词' in pdf[0].get_text(), 'Abstract does not fit one dedicated page')
    require(all(abs(p.rect.width-595.28)<1 and abs(p.rect.height-841.89)<1 for p in pdf), 'PDF page is not A4')
    out_of_page = []
    for index, page in enumerate(pdf, 1):
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    x0,y0,x1,y1 = span['bbox']
                    if x0 < -1 or y0 < -1 or x1 > page.rect.width+1 or y1 > page.rect.height+1:
                        out_of_page.append(index)
    require(not out_of_page, 'Text outside PDF page bounds')

    workbook_checks = []
    xmlns = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
    for number, end, step, columns, sheets in [(1,1800,1,22,2),(2,206433,1,22,2),(3,206433,60,22,1),(4,183086,60,23,1)]:
        path = OUT / f'tables/result{number}.xlsx'
        hashes[path.relative_to(ROOT).as_posix()] = sha(path)
        with zipfile.ZipFile(path) as package:
            names = sorted(n for n in package.namelist() if re.fullmatch(r'xl/worksheets/sheet\d+\.xml',n))
            require(len(names)==sheets, f'result{number}: sheet count differs')
            for name in names:
                count, last_time, invalid = 0, None, 0
                with package.open(name) as stream:
                    for _, row in etree.iterparse(stream, events=('end',), tag=xmlns+'row'):
                        count += 1
                        cells = row.findall(xmlns+'c')
                        if count == 1:
                            require(len(cells)==columns, f'result{number}: header width differs')
                        else:
                            values = [(c.get('r'),c.findtext(xmlns+'v')) for c in cells]
                            t = float(values[0][1])
                            expected_time = min((count-1)*step, end)
                            require(t==expected_time, f'result{number}: discontinuous time at row {count}')
                            for _, value in values:
                                if value is not None and not math.isfinite(float(value)):
                                    invalid += 1
                            if number != 4:
                                require(len(cells)==columns, f'result{number}: incomplete row {count}')
                            last_time=t
                        row.clear()
                        while row.getprevious() is not None:
                            del row.getparent()[0]
                require(last_time==end and count==math.ceil(end/step)+1 and invalid==0,
                        f'result{number}: endpoint, row count or finite-value check failed')
                workbook_checks.append({'file':path.name,'sheet':name,'rows_including_header':count,
                                        'last_time_s':last_time,'columns':columns,'nonfinite_values':invalid})

    spec=importlib.util.spec_from_file_location('guard',ROOT/'.agents/skills/paper-workflow-orchestrator/scripts/workflow_guard.py')
    guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
    status=guard.evaluate('S8')
    require(status['status']=='PASS','Workflow current hashes do not pass: '+str(status['failures']))
    paths=[source_path,OUT/'final_paper.docx',ROOT/render['pdf'],OUT/'format_check_report.json',
           OUT/'qa/draft_audit.json',OUT/'qa/evidence_gate_report.json',Path(__file__)]
    paths+=list((ROOT/'.agents/skills/paper-formal-writer/scripts').glob('*.py'))
    for path in paths: hashes[path.relative_to(ROOT).as_posix()]=sha(path)
    result={'generated_at':datetime.now(timezone.utc).isoformat(),'generated_by':'paper_output/code/qa/verify_delivery.py',
            'status':'FAIL' if failures else 'PASS','failures':failures,
            'counts':report['counts'],'source_formula_count':len(tokens),'native_omml_count':native,
            'figure_captions':captions,'computed_table_cells_compared':compared_cells,
            'pdf_pages':len(pdf),'main_pages_before_appendix':render['paper_scope']['counted_main_pages'],
            'pdf_metadata':pdf.metadata,'out_of_page_text_count':len(out_of_page),
            'workbooks':workbook_checks,'workflow_steps':status['steps'],'input_hashes':hashes,
            'limitations':['Numerical convergence evidence covers the specified test cases, not experimental accuracy.',
                           'Boundary extension comparison has a finite-horizon censoring limitation, disclosed in section 6.3.',
                           'No complete four-combination factorial experiment or independent nonlinear residual study is claimed.']}
    (OUT/'qa/delivery_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['input_hashes','pdf_metadata','workflow_steps']},ensure_ascii=False))
    return bool(failures)


def numerical_delivery():
    """S6只核对数值附件和来源，不读取或修改论文、Word及PDF。"""
    validation=json.loads((OUT/'qa/model_validation_checks.json').read_text(encoding='utf-8'))
    metrics=json.loads((OUT/'results/metrics.json').read_text(encoding='utf-8'))
    manifest=json.loads((OUT/'results/run_manifest.json').read_text(encoding='utf-8'))
    failures=[]
    def check(ok,message):
        if not ok: failures.append(message)
    check(validation['status']=='PASS','数值验证未通过')
    check(manifest['status']=='PASS','四问运行未通过')
    for name,expected in validation['input_hashes'].items():
        check(sha(ROOT/name)==expected,'数值验证来源变化：'+name)
    for run in manifest['runs']:
        check(run['returncode']==0,'运行失败：'+run['script'])
        check(sha(ROOT/run['script'])==run['script_sha256'],'主程序来源变化')
        for entry in run['input_files']+run['output_artifacts']:
            check(sha(ROOT/entry['path'])==entry['sha256'],'运行文件变化：'+entry['path'])
    for entry in manifest['final_artifacts']:
        check(sha(ROOT/entry['path'])==entry['sha256'],'结果契约变化：'+entry['path'])
    sys.path.insert(0,str(OUT/'code/visualization'))
    from run_numerical_validation import inputs,solve,compare
    env,rad=inputs()
    config=validation['selected_configuration']
    base=solve(env,rad,mode=1,N=config['N'],dt=config['dt_s'],horizon=1800,threshold=-1.)
    finer=solve(env,rad,mode=1,N=2*config['N'],dt=config['dt_s']/2,horizon=1800,threshold=-1.)
    q1_check=compare(base,finer)
    check(q1_check['pass'],'Q1新配置加密未通过')
    vals={x['metric_name']:x['value'] for x in metrics['items']}
    t3,t4=vals['aq3_drying_time_s'],vals['aq4_drying_time_s']
    check(vals['aq2_end_time_s']==t3,'Q2/Q3终点不一致')
    for q in [2,3,4]:
        check(vals[f'aq{q}_status_code']==1,'未真正达标')
        check(vals[f'aq{q}_left_max_C']>=.15>vals[f'aq{q}_final_max_C'],'终点未夹逼阈值')
    workbook_checks=[]
    xmlns='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
    # 同时与正文用CSV核对；只读取数值，不改动附件。
    table_names={1:['table_aq1_temperature.csv','table_aq1_moisture.csv'],
                 2:['table_aq2_temperature.csv','table_aq2_moisture.csv'],
                 3:['table_aq3_drying_moisture.csv'],4:['table_aq4_shrinkage_moisture.csv']}
    for q,end,step,columns,sheets in [(1,1800.,1,22,2),(2,t3,1,22,2),(3,t3,60,22,1),(4,t4,60,23,1)]:
        path=OUT/f'tables/result{q}.xlsx'
        with zipfile.ZipFile(path) as archive:
            names=sorted(n for n in archive.namelist() if re.fullmatch(r'xl/worksheets/sheet\d+\.xml',n))
            check(len(names)==sheets,f'result{q} sheet count')
            for sheet,name in enumerate(names):
                expected={}
                with (OUT/'tables'/table_names[q][sheet]).open(encoding='utf-8-sig',newline='') as stream:
                    rows=list(csv.reader(stream))
                for row in rows[1:]:
                    ts=end if row[0].startswith('烘干结束') else float(row[0])*(1 if q==1 else 3600)
                    expected[ts]=[float(x) if x else None for x in row[1:]]
                count=0;last=0.;invalid=0;time_errors=0;table_errors=0;matched=0;domain_errors=0
                radius_data=None
                if q==4:
                    import numpy as np
                    radius_data=np.loadtxt(OUT/'data_cleaned/a_radius.csv',delimiter=',',skiprows=1)
                with archive.open(name) as stream:
                    for _,row in etree.iterparse(stream,events=('end',),tag=xmlns+'row'):
                        count+=1
                        cells=row.findall(xmlns+'c')
                        if count==1:
                            check(len(cells)==columns,f'result{q} header')
                        else:
                            values={re.sub(r'\d','',c.get('r')):float(c.findtext(xmlns+'v')) for c in cells if c.findtext(xmlns+'v') is not None}
                            last=values['A']
                            time_errors+=last!=min((count-1)*step,end)
                            invalid+=sum(not math.isfinite(v) for v in values.values())
                            if q!=4: invalid+=len(values)!=columns
                            if q==4:
                                Rcm=float(np.interp(last,radius_data[:,0],radius_data[:,1]))
                                for j in range(21):
                                    column=chr(ord('B')+j)
                                    domain_errors+=((column in values)!=(j*.1<=Rcm+1e-12))
                            if last in expected:
                                matched+=1
                                targets=expected[last]
                                for j,value in enumerate(targets[:5]):
                                    actual=values.get(chr(ord('B')+5*j))
                                    table_errors+=(actual is not None) if value is None else (actual is None or abs(actual-value)>1e-9)
                                if q==4:
                                    table_errors+=abs(values['W']-targets[5])>1e-9
                            row.clear()
                            while row.getprevious() is not None: del row.getparent()[0]
                check(last==end and count==math.ceil(end/step)+1,f'result{q} endpoint/rows')
                check(invalid==0 and time_errors==0 and domain_errors==0,f'result{q} finite/time/domain')
                check(table_errors==0 and matched==len(expected),f'result{q} CSV mismatch')
                workbook_checks.append(dict(file=path.name,sheet=name,rows=count,end_s=last,invalid=invalid,time_errors=time_errors,
                    table_errors=table_errors,matched_table_rows=matched,domain_errors=domain_errors))
        print(f'Checked result{q}.xlsx',flush=True)
    result=dict(schema_version='2.0',generated_by='paper_output/code/qa/verify_delivery.py --s6',
        generated_at=datetime.now(timezone.utc).isoformat(),scope='S6数值附件检查；不含S7/S8论文检查',
        status='FAIL' if failures else 'PASS',failures=failures,workbooks=workbook_checks,q1_refinement=q1_check,
        selected_configuration=validation['selected_configuration'],
        input_hashes={p.relative_to(ROOT).as_posix():sha(p) for p in [OUT/'qa/model_validation_checks.json',OUT/'results/run_manifest.json',OUT/'results/metrics.json',Path(__file__)]})
    (OUT/'qa/delivery_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False),flush=True)
    return bool(failures)


if __name__ == '__main__':
    for stream in (sys.stdout,sys.stderr): stream.reconfigure(encoding='utf-8')
    raise SystemExit(numerical_delivery() if '--s6' in sys.argv else main())
