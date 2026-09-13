# 协作者交接文档

## 当前目标

将已修改代码、数值证据及S7/S8论文交付提交到chore/cleanup-paper-artifacts分支；不合并main，不强制推送。以下最新状态覆盖后文历史S6记录。

## 本次变更

- 同步新数值代码、四Excel、六张主结果CSV、图形、结果契约与论文，Q3=205818s、Q4=182969.5s，缩短11.1013%。
- 更新迭代容差、残差、水分收支、事件夹逼、表面重构、N1280/dt0.5联合加密和三格顺序对照论述，保留物理验证局限。
- 重建S7分章审计与全文修订，生成Word原生公式和真实LibreOffice PDF；三线表、摘要单页、统一字体、图表分页约束。
- 删除16张本地渲染PNG及一次性sync_paper_revision.py，共17文件、3105040字节。保留layout_checks.json、可复用页面检查脚本和S7审计依赖。
- 正式提交汇报见docs/SUBMISSION_REPORT.md；所有变更在cleanup分支，不触碰main。

## 工作流状态

当前workflow guard为S8、下一步DONE；S0-S8全部通过。authoring_state与format_check_report均为新鲜PASS。没有手工修改运行哈希或验收状态。

## 验证结果

- S7分章、合并和最终源稿检查通过，S8必需LibreOffice渲染通过。
- PDF61页：摘要1页、正文22页、附录38页；PDF1757617字节，低于20MB。
- 附录前有效字符18218、汉字11145；119个源公式全部对应119个可编辑OMML，26个独立公式。
- 6幅图、13张Word表、6条文献、14处正文引用，无未引用文献；页面检查未发现左右边距越界文字。
- 8项排版回归测试通过；历史S6数值附件审计PASS仅代表数值范围，不冒充完整提交包验收。
- 提交前开启NUMBA_BOUNDSCHECK=1运行全部12项测试，均通过；清理后guard仍为S8/DONE，git diff --check通过。

## 已知问题

- AI工具使用详情.pdf尚未生成。参赛队必须按真实使用历史补充工具版本、过程及人工核验；论文中的AI声明不替代该支撑文件。
- 尚未制作并验收竞赛支撑ZIP/RAR的20MB限制；result2.xlsx原始文件约27.46MB，不能由论文PDF小于20MB推断支撑包合规。
- verify_delivery.py默认完整交付检查仍含旧版期望，不能将其结果当作本轮完整验收；数值附件使用--s6，论文使用S7/S8和layout检查。
- 缺少独立内部场观测及第四种析因组合；潜热、吸附闭合等限制保留。最后一小时情景单元阈值与中心重构的微小差异已在正文披露。

## 下一步

完成参赛队人工审查、AI使用详情和支撑包体积核验。分支先保留供审阅，未经用户另行授权不合并main。

## 关键文件/技能建议

交付：paper_output/final_paper_source.md、final_paper.docx、qa/rendered/final_paper.pdf。证据：results/、tables/、qa/model_validation_checks.json、format_check_report.json。恢复写作以paper-workflow-orchestrator当前guard为准；修改代码必须真实重算相关证据，不复用旧哈希。

## 历史状态：S6完成后暂停

2026-09-12已完成S3数据准备、S4代码修订、S5真实计算与S6证据检查。最新指令为“完成q4收尾并推进到s6后暂停汇报”。本次未修改论文源稿、Word或PDF。

## 已完成内容

- 只使用题面与附件数据；未引入潜热参数、吸附参数或新的实测数据。
- 数据：环境241条、半径145条，原始值保留；最后一小时环境平均按时间积分计算。
- 代码：物理时间采样、终态独立返回、阈值夹逼、Picard容差与方程残差、水分收支诊断；不剪裁解或掩盖未收敛。精简了不相关的通用脚手架。
- 原N80含水率场的加密差异超标，已保存失败比较并继续加密，未放宽阈值。正式配置选定N=1280、dt=0.5s，最多50轮并以容差停止；不是每步固定运行50轮。
- Q3/Q4均通过与N2560、dt0.25参考配置的交叉比较。最大温差分别0.000435354、0.000474706 K；最大含水率差分别0.000452145、0.000322393 kg/kg；时长相对差分别0.002672%、0.000820%。
- 已运行三格顺序对照及Ce低/高、最后一小时环境均值延拓情景；各自独立检测终点。三格仅用于指定路径的模型内分析，不识别交互。
- 四份Excel、六张主结果CSV、现有图表、指标、结论和运行清单已实际生成并同步。
- Q4导出检查曾发现半径恰为1.2cm时的浮点坐标误判，导致951行错误空白。已用整数索引生成0.1cm输出坐标，重新运行Q4并更新真实运行记录，复检域错误为0。

## 最新计算结果

| 情景 | 秒 | 小时 |
|---|---:|---:|
| Q3，附录3＋固定半径 | 205818.0 | 57.1717 |
| Q4，附录4＋附件2收缩 | 182969.5 | 50.8249 |
| 顺序对照，附录4＋固定半径 | 464739.5 | 129.0943 |

Q4相对Q3缩短11.1013%。顺序贡献统一以Q3为分母：物性变化+125.8012%，随后几何变化−136.9025%；只代表先物性后几何的指定路径。

Q3边界情景：Ce×0.8为205160.0s（−0.3197%），Ce×1.2为206770.5s（+0.4628%），最后一小时均值延拓为206934.5s（+0.5425%）。这些是数值情景，不是实测误差区间或真实药材试验。

## 验收结果与证据位置

- paper_output/qa/model_validation_checks.json：PASS；含完整加密、迭代、守恒与情景记录。全部长程验证的最大归一水分收支误差小于6e-14。
- paper_output/qa/delivery_audit.json：PASS（明确仅S6数值附件范围）；Q1补充加密通过；六张Excel工作表逐行时间、有限值、CSV一致性、Q4域外留空检查均通过。
- paper_output/qa/evidence_gate_report.json及.md：official PASS；输入哈希由真实检查生成。
- workflow guard --step S6：PASS；随后--status显示当前S6、下一步S7。
- 开启NUMBA_BOUNDSCHECK的4项回归测试通过；源码语法检查和git diff --check通过。
- 无新建项目文件，未commit、push、发布或删除文件。使用-B避免创建Python字节码文件。

## 复现入口

使用F:/Anaconda_envs/envs/mathmodel-skill-standard/python.exe；默认系统Python缺openpyxl，不用于本项目。

```text
python -B paper_output/code/data_processing/prepare_a_data.py
python -B paper_output/code/visualization/run_numerical_validation.py
python -B paper_output/code/modeling/run_modeling.py
python -B paper_output/code/qa/verify_delivery.py --s6
python -B .agents/skills/quality-assurance-auditor/scripts/evidence_gate.py --mode official
```

run_modeling.py 4可只重算第四问并保留其余真实运行记录；修改核心求解器则需重新验证相关全部结果，不能手改运行哈希。

## 后续工作（本次不执行）

等待用户明确继续S7。现有final_paper_source.md、final_paper.docx和PDF仍为旧版，含旧数字、旧验证论述与旧源码，不能视为本轮最终论文。S7应按新证据原位修订摘要、正文表格、验证与敏感性、结论和源码附录。

之前删除的分章草稿和写作状态文件仍不存在；用户要求不新增文件，后续需保持原位修订并说明标准分章门禁的适配范围，不伪造PASS。保留初始假设与未显式建模潜热等局限，不将数值验证视为独立物理验证。

result2.xlsx约27.46MB；竞赛支撑包压缩体积及Word/PDF最终格式尚待后续交付检查。本次S6通过不等于竞赛提交包或S7/S8通过。
