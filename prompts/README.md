# Workshop prompt sequence

Use these prompts one at a time. Inspect what the harness creates, make corrections, and approve the output before moving forward. Do not combine them into one large prompt; the review points are part of the production workflow.

| Step | Prompt | Expected artifact |
| --- | --- | --- |
| 0 | [Prove readiness](00-readiness.md) | `work/00_readiness.md` |
| 1 | [Frame the work](01-frame-the-work.md) | `work/01_use_case.md` |
| 2 | [Draft and break the contract](02-contract-and-architecture.md) | `work/02_contract.yaml`, `work/02_architecture.md` |
| 3 | [Bind approved context](03-bind-approved-context.md) | `work/03_metric_proposal.yaml` |
| 4A | [Plan before execution](04a-plan-before-execution.md) | `work/04a_plan.yaml` |
| 4B | [Execute, verify, and prove](04b-execute-verify-and-prove.md) | `work/04_proof.yaml` |
| 5 | [Evaluate, repair, and rerun](05-evaluate-repair-and-rerun.md) | `work/correction.yaml`, `work/05_eval_results.csv` |
| 6 | [Operate and ask for a launch decision](06-operate-and-launch.md) | `work/06_operations.md`, `work/07_launch_memo.md` |

Start with the [practice lab](../assets/agentic-analytics-lab/README.md) if you do not have an approved warehouse or local data source.
