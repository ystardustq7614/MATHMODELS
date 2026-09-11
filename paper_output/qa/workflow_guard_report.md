# Workflow Guard Report

- Target step: `S6`
- Status: `INCOMPLETE`
- Generated at: `2026-09-11T22:20:07`
- Current step: `S5`
- Next step: `S6`
- Recommended skill: `quality-assurance-auditor`
- Next action: 运行 evidence_gate.py --mode official，未通过则回补结果证据。

## Steps
- S0 准入预检: `PASS`
- S1 审题分析: `PASS`
- S2 模型路线: `PASS`
- S3 数据与图表计划: `PASS`
- S4 建模代码: `PASS`
- S5 结果证据: `PASS`
- S6 证据门禁: `FAIL`
  - 证据门禁报告已过期，输入发生变化：paper_output/results/model_results.json
  - 证据门禁报告已过期，输入发生变化：paper_output/results/run_manifest.json
  - 证据门禁报告已过期，输入发生变化：paper_output/results/metrics.json
  - 证据门禁报告已过期，输入发生变化：paper_output/results/conclusions.json
  - 证据门禁报告已过期，输入发生变化：paper_output/tables/table_index.json
