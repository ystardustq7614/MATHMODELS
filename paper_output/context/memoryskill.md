# A题当前工作记忆

## 长期准则

- 仅处理2026 A题；所有赛题生成物写paper_output。
- 简洁Python，经典PDE/优化与朴素数值算法；不使用用户禁止的模型或元启发式。
- S4先静态编写再检查建模依赖；指定环境mathmodel-skill-standard。
- 逐节点记录进度并查询额度；任一可用窗口剩余低于15%时保留下一节点后暂停。
- S6证据通过之后完整章节写作、全文统稿；Word原生公式及PDF渲染通过之前不称最终稿。

## 短期工作台

- S2/S3已完成并通过workflow guard；按用户要求停在S4之前。
- 当前四问来源：step1/problem_analysis.json；唯一模型闭合与验证说明：plan/scoring_strategy.md。
- S2正式文件：model_route.json、rubric_alignment.json、scoring_strategy.md。
- S3已真实执行：code/data_processing/prepare_a_data.py。
- 数据：环境241条、半径145条；无缺失和重复时刻，不删点、不填补、不平滑；保留SI换算列。
- 数据文件：data_cleaned/a_environment.csv、data_cleaned/a_radius.csv。
- 实际图件：figures/fig_a_environment.png、figures/fig_a_radius.png，已人工视觉核对；只是输入图。
- 运行证据：data_cleaned/data_pipeline_run.json，保存输入/脚本/输出哈希，已重新核验。
- 没有S4建模模块，没有S5结果，不曾产生烘干时长。
- 原三题比较、历史JSON字段、旧审阅草案和断点已清除，替代关系见stage_checkpoint.md。

## 外部资料与局限

- 没有获得独立原始验证数据集。检索线索与访问限制见plan/scoring_strategy.md第5节。
- 工程闭合把经验rho用于热容量、把气相字段用作有效传质边界；必须披露干基质量解释与吸附/潜热资料不足，不能夸大实证准确度。

## 下一步

等待用户继续。届时读取stage_checkpoint.md，重查guard，进入S4静态实现；不得因推荐下一节点而自动执行。
