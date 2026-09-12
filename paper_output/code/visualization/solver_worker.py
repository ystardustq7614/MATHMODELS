"""单工况诊断入口：结果打印至标准输出，不创建临时文件。"""
import sys
import json
from run_numerical_validation import inputs,solve,summarize

if __name__=='__main__':
    kind,N,dt,horizon=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4])
    env,rad=inputs()
    result=solve(env,rad,moving=kind.startswith('moving'),mode=int(kind[-1]),N=N,dt=dt,horizon=horizon)
    print(json.dumps(summarize(result),ensure_ascii=False,allow_nan=False))
