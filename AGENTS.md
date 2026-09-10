# Agent 协作规则

- 开始任何复杂任务前，先阅读 `docs/HANDOFF.md`、`CHANGELOG.md`、`paper_output/qa/workflow_guard_report.json` 和 `paper_output/context/workflow_memory.json`。
- 以 workflow guard 和当前证据哈希为准，不凭聊天记录推断阶段，不手工修改证据哈希、PASS/FAIL 状态或运行清单。
- 修改完成后运行与任务匹配的验证，并在 push 前更新 `CHANGELOG.md` 与 `docs/HANDOFF.md`，记录真实结果、遗留问题和下一步。
- 不未经用户授权 commit、push、发布或删除文件；协作者之间遵守明确的文件所有权。
- push 前必须通过 `.githooks/pre-push`；该检查只覆盖分支的非删除推送。
