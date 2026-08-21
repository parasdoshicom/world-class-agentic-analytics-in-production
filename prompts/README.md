# Workshop prompt sequence

Use these prompts one at a time. Inspect what the harness creates, make corrections, and approve the output before moving forward. Do not combine them into one large prompt; the review points are part of the production workflow.

Choose the stopping point that matches your current maturity:

- **Solo, n=1:** run Steps 0–4B. Keep the artifacts local or in a private repository. The goal is one recurring workflow that is useful, verifiable, and repeatable for you.
- **Small team, n=3–10:** add Step 5. A second person should be able to run the workflow, flag a miss, review the evidence, and reuse an approved correction without the original author beside them.
- **Organization:** add Step 6 after the team handoff works. Centralize permissions, context, review, telemetry, rollout, cost, and incident controls only when shared usage creates that need.

Two fresh sessions can rehearse the team roles when you are learning alone. They do not prove multiplayer adoption; repeat the handoff with another person before scaling the infrastructure.

| Step | Prompt | Expected artifact |
| --- | --- | --- |
| 0 | [Prove readiness](00-readiness.md) | `work/00_readiness.md` |
| 1 | [Frame the work](01-frame-the-work.md) | `work/01_use_case.md` |
| 2 | [Draft and break the contract](02-contract-and-architecture.md) | `work/02_contract.yaml`, `work/02_architecture.md` |
| 3 | [Bind approved context](03-bind-approved-context.md) | `work/03_metric_proposal.yaml` |
| 4A | [Plan before execution](04a-plan-before-execution.md) | `work/04a_plan.yaml` |
| 4B | [Execute, verify, and prove](04b-execute-verify-and-prove.md) | `work/04_proof.yaml` |
| 5 | [Flag, review, promote, and rerun](05-evaluate-repair-and-rerun.md) | `work/05_feedback.yaml`, `work/05_admin_decision.yaml`, `work/shared_context/correction-001.yaml`, `work/05_regression_case.yaml`, `work/05_reuse_rerun.md`, `work/05_eval_results.csv`, `work/05_observed_operations.csv` |
| 6 | [Operate and ask for a launch decision](06-operate-and-launch.md) | `work/06_operations.md`, `work/07_launch_memo.md` |

Start with the [practice lab](../assets/agentic-analytics-lab/README.md) if you do not have an approved warehouse or local data source.
