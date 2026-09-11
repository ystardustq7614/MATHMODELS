# Changelog

## Unreleased

### Fixed

- 完成 S7 全文修订，清除正文指标键和无证据实验，统一图表编号、物性关系、逐秒阈值检测与一阶时间格式的说明。
- 将 AQ2 完整附件从前3小时扩展至206433秒达标终点，保持表3/4和既有核心结果不变，重跑运行证据及数值检验。
- 修复 S8 对图片链接路径和“附录4的经验式”的误判；正文篇幅统计排除附录源码；源码中的数值不再充当正文证据。
- 修复 Word 表格继承正文首行缩进导致的小数断行；启用A4、页脚页码、摘要独立页及图片与图题同页约束。

### Added

- 正式源稿、原生公式 Word、真实 LibreOffice 26.2.6.3 必需渲染 PDF，附录含10份完整可运行源程序。
- 6项格式回归测试、完整Excel及图表公式核验脚本、独立交付审计报告和 `CONTRIBUTING.md`。
- 更新 S0-S8 报告链与工作流记忆；记录模型的数值验证范围和未完成实验，避免把机器通过等同于实验准确度。

## 2026-09-11 — A题 S6 基线

### Added

- 根级 `AGENTS.md`、滚动式 `docs/HANDOFF.md`、`CHANGELOG.md` 和 POSIX `.githooks/pre-push`；本地 `core.hooksPath=.githooks`。
- AQ1–AQ4 四张模型结果图及登记，`figure_index` 共 6 项。
- AQ1–AQ4 数值验证契约与 13 个有限 validation metrics。

### Changed

- `.gitattributes` 保证 `paper_output` 原始字节及 `cr-at-eol`；requirements 声明 `numba`。
- 结果契约、run manifest 和一致 cwd command 使用仓库相对路径；输入范围收敛为 A 题，7 条 input manifest 记录全部可读且哈希匹配。
- AQ1–AQ4 已重跑：AQ3 为 57.3425 h，AQ4 为 50.8572 h，约缩短 11.31%；run manifest 为 4 runs/30 records/0 mismatch。
- 当前工作流停在新鲜 S6 PASS，下一阶段为 S7 正式写作。

### Removed

- 移除与 A 题无关的 B 题 3 个输入文件及 C 题 10 个输入文件；相关 preflight 与加载诊断已重建为仅 A 题范围。

### Fixed

- 修复 Windows 检出下证据哈希变化，并清除 active model/evidence contracts 中的协作者绝对路径。
- 完成四 Excel 结构验收、网格/有限值/移动域尾部空值检查及四图文件来源哈希核验。

## 已完成提交

- `ba95f29`：完成 A 题 S4–S6 建模代码、数值求解、结果契约和证据门禁。
- `91db1fa`：修复 Windows 检出导致的证据哈希变化。
- `361acfe`：完成 A 题 S2/S3 交接、数据清洗与规划产物。
- `c9037fa`：初始化 MathModel 工作区及标准工作流技能。

## 验证摘要

- official evidence gate：新鲜 `PASS`；workflow guard/memory：`current=S6`、`next=S7`、推荐 `paper-formal-writer`。
- validation：AQ1 spatial `T=9.3109543e-05 K, C=1.7913447e-04 kg/kg`；temporal `T=6.0011006e-04 K, C=4.4772887e-05 kg/kg`；AQ3 两种边界延拓均 `206433 s`；AQ4 全剖面 `T=1.1937118e-12 K, C=2.4424907e-14`。
- 环境与质量检查：已安装仓库声明的 `pypdf 6.18.0`，`pip check`、依赖导入、`py_compile`、`git diff --check` 均通过；待本轮提交与 push。

## 2026-09-11 — 产物整理

- 按用户授权清理130个中间文件（移入回收站），共23164083字节；清单见paper_output/cleanup_manifest.json。
- 保留最初S2/S3的5份plan、正式源稿/Word/PDF、当前代码及真实计算证据，未回滚原有未提交修改。
- 新增paper_output/整理最终报告.md，归纳模型方案、修改建议、历史验收及后续验证事项；交接与AGENTS入口更新为该报告。
- 清理前guard为S5完成、S6因结果变更过期；没有沿用旧S8 PASS。71个保留文件逐个SHA-256核对无差异。
