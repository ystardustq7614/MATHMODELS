# 当前A题产物布局

遵循 `docs/output-layout.md` 与 Standard S0—S8 契约。所有赛题生成物保留在 `paper_output/`。

- `preflight_report.json`、`input_manifest.json`：输入与环境预检，含原始文件角色和哈希。
- `step1/problem_analysis.json`：当前A题四问；过时三题比较已清理。
- `plan/model_route.json`、`plan/rubric_alignment.json`、`plan/scoring_strategy.md`：S2正式模型与评分交接。
- `data_cleaned/data_pipeline_run.json`：S3真实数据处理记录，不替代S5的模型run_manifest。
- `context/stage_checkpoint.md`、`context/memoryskill.md`：当前节点、套餐记录和短期工作台。
- `plan/`：后续模型、评分、数据、可视化、写作计划。
- `code/data_processing/`、`code/modeling/`、`code/visualization/`、`code/qa/`：当前赛题Python代码。
- `data_cleaned/`：清洗数据与加载报告。
- `external_data/`：后续外部资料与数据，保留来源、许可和哈希。
- `results/`：真实运行清单、模型结果、指标和结构化结论。
- `tables/`：论文表1—6、result1.xlsx至result4.xlsx、table_index.json。
- `figures/`、`figure_index.json`：实际图件与索引。
- `qa/`：流程状态、证据/写作审计和渲染检查。
- `context/`：工作流记忆、审阅断点和后续写作状态。
- `drafts/sections/`、`drafts/assembled_draft.md`：S7完整章节与汇编。
- `final_paper_source.md`、`final_paper.docx`、`format_check_report.json`：后续统一正文、Word与格式门禁；通过全部门禁之前不标最终稿。

`problem_files/A题/`内原件及结果模板不覆盖。安装技能目录不存赛题代码或结果。
