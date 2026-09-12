# 贡献约定

## 分支与提交

从当前 `origin/main` 建立用途明确的贡献分支，保留已有作者的改动。提交前阅读 `AGENTS.md` 和 `docs/HANDOFF.md`，检查实际文件与工作流报告，不以历史聊天或旧 memory 推断阶段。

使用说明问题及行为变化的提交标题，通过 Pull Request 请求合并。不要强制推送共享分支。每个分支的推送末端提交必须同时更新 `CHANGELOG.md` 与 `docs/HANDOFF.md`，并通过仓库的 `.githooks/pre-push`；使用 `git config core.hooksPath .githooks` 启用检查。

## 论文修改与验证

纯正文修订保留计算证据，按顺序执行最终源稿审计、Word 导出、必需渲染、workflow status 和 memory 更新。修改过章节草稿时，先执行对应章节审计、确定性合并及合并稿审计，再完成全文修订。不得复制合并稿冒充全文修订。

若改变预检输入清单，须重新运行数据读取诊断；改变任一运行输入或建模代码，须重新执行建模、数值检验及 S6，再准备新的写作计划并重新审计。禁止手工填补 SHA-256、运行记录或 PASS 状态。渲染完成后不要再运行会改写上游契约的命令而不刷新下游报告。

```powershell
python -m unittest discover -s tests -v
python .agents/skills/paper-formal-writer/scripts/validate_authoring.py --final
python .agents/skills/paper-formal-writer/scripts/format_formal_docx.py
python .agents/skills/paper-formal-writer/scripts/check_paper_format.py --render required
python .agents/skills/paper-workflow-orchestrator/scripts/workflow_guard.py --status
python .agents/skills/context-memory-keeper/scripts/update_workflow_memory.py
python paper_output/code/qa/verify_delivery.py
git diff --check
```

使用真实 LibreOffice，必要时将 `LIBREOFFICE_PATH` 指向它的 `soffice.com` 或可执行文件，禁止用其他渲染器伪装。安装 `requirements-qa.txt` 后，可用 `python paper_output/code/qa/render_review.py` 生成页面图和缩略图用于目检。页面 PNG 属本地检查缓存，不提交；提交源稿、正式 DOCX/PDF、必要证据与机器报告。

## 代码与报告的对应

当前论文附录D为运行诊断，附录E为数据整理、通用读取、建模、图形及数值验证的完整源码。代码变化后须按实际文件更新源码附录并重新执行S7/S8；不要使用已清除的append_source_listing.py或一次性迁移脚本。当前默认verify_delivery.py仍含历史完整检查期望，数值附件用--s6，论文使用新鲜S7/S8及layout_checks.json；完整提交包须另外核验。

正文应区分已运行结果、数学推导和未验证设想。内部指标键、文件路径与布尔检查标志放在附录；图题使用与正文一致的编号及说明。模板、未运行实验和代码注释中的数字不能充当正文证据。

## PR 内容

说明修复的问题、最终行为、实际执行的验证及剩余限制。涉及论文时列出字数统计口径、正文与附录页数、原生公式匹配、图表和引用数。自动门禁通过不等于实验准确度或竞赛提交资格；已知模型限制与额外包装要求应如实说明。
