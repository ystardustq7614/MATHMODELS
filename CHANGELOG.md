# Changelog

## Unreleased

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
