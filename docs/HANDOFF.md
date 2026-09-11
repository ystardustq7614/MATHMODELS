# 协作者交接文档

## 当前目标

交付A题S7/S8修复版本，维护可复核的论文、代码和报告，通过贡献分支及PR交接。

## 本次变更

完成全文修订和证据一致性修复，清除内部指标键及无依据的析因结果；统一图表编号、物质坐标方程、一阶时间推进和逐秒阈值检测的说明。AQ2输出已延续至206433秒，6张计算结果表与核心结果保持一致。修复格式脚本的链接路径、附录识别和表格缩进问题，增加A4、页码与完整源码附录。新增CONTRIBUTING及交付核验脚本。

## 工作流状态

以 paper_output/qa/workflow_guard_report.json、paper_output/format_check_report.json、paper_output/qa/delivery_audit.json 的新鲜状态为准。S7章节、合并稿、最终稿已重审；S8使用真实LibreOffice的required模式。输入清单更新后已依次刷新loader、运行清单、S6、写作计划及下游报告，不手改哈希。

## 验证结果

- 6项格式回归测试、pip check通过；S7各写作单元及最终稿审计通过。
- 正文字数采用附录前口径：15442有效字符、9433汉字。PDF附录前22页（含摘要1页），总70页，其中48页为附录；符合项目18页下限及本地正文30页上限。
- 90个源公式与90个原生OMML匹配，独立公式20个；6幅图、8张论文结果/统计表，加符号表共9张Word表格；6条文献、14组正文引用。
- 6张计算结果表的288个数据单元与CSV一致；四个Excel的6个工作表已核验时间连续、终点、列数及有限值。result2每表206434行（含表头）、22列。
- 已查看70页缩略图并抽查关键公式及数值表，修复了小数断行；未发现文字超出页面边界。
- AQ3仍为57.3425 h，AQ4仍为50.8572 h，综合时间缩短11.31%。

## 已知问题

- 远期环境延拓对照存在共用终点窗口限制；缺少迭代次数独立测试、完整四组合析因实验和内部含水率实测验证。论文已明确研究边界，不再声称完成这些实验。
- 早期章节及合并稿保留为写作历史；全文修订后的正式交付源是final_paper_source.md。
- 本地2026规范要求支撑材料压缩包不超过20MB。本次未制作竞赛提交包，result2.xlsx本身约27.5MB，仓库推送不等于竞赛打包提交。
- LibreOffice为项目本地工具，.local-tools、旧Word桥接文件、锁文件及页面PNG不提交。跨机器渲染需要真实LibreOffice及中文字体。

## 下一步

审阅贡献分支的PR并按仓库流程合并。若只改正文，从最终审计重新开始；若改输入或模型，依照CONTRIBUTING刷新所有受影响报告。不要重跑preflight后继续沿用旧loader和运行哈希。

## 关键文件/技能建议

- 正式产物：paper_output/final_paper_source.md、final_paper.docx、qa/rendered/final_paper.pdf。
- 验收：paper_output/qa/s7_s8_revision_review.md、delivery_audit.json、format_check_report.json。
- 复现：paper_output/code/modeling/、paper_output/code/qa/、requirements-qa.txt。
- 规范：AGENTS.md、CONTRIBUTING.md、paper-workflow-orchestrator、paper-formal-writer。
