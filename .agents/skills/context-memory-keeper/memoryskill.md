# Context Memory (Active)

> Instructions for Agent:
> 1. Read this file before long MathModel workflows.
> 2. Keep long-term principles stable unless the user explicitly changes them.
> 3. Update the short-term workbench after major steps: problem parsing, data processing, QA, paper generation, and final delivery.
> 4. When this file becomes too long, move obsolete details to `memory_archive.md` and keep only durable conclusions here.

## 1. Long-Term Principles

- Role: mathematical modeling workflow assistant.
- Output language: Chinese academic style unless the user asks otherwise.
- Delivery target: keep Markdown and Word outputs aligned when a full paper is requested.
- Workflow rule: Standard S0-S8; evidence gate before complete-section authoring, then global revision and Word/PDF validation. Micro-units are only for authorized legacy use or triggered repair.
- Script rule: treat bundled `scripts/` as reusable code templates and code-level prompts; adapt them to the current problem before trusting outputs.

## 2. Short-Term Workbench

- Active project memory: `paper_output/context/memoryskill.md` (relative to project root).
- Current stage and handoff: `paper_output/context/stage_checkpoint.md` and generated `paper_output/context/workflow_memory.json`.
- Keep current-contest details in those files; this entry remains a pointer to avoid duplicated stale records.

## 3. External Resources / Literature

- Current source status: `paper_output/plan/scoring_strategy.md`, section 5; source links do not establish an acquired validation dataset.

## 4. Open Todos

- Read the current checkpoint before continuing. A requested pause takes precedence over the workflow recommendation.
