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
