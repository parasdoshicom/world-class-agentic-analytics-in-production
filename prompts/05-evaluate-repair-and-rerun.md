# Step 5: Flag, review, promote, and rerun

```text
For the live workshop, continue with the included CSV lab. Read evals.yaml. Before execution, record the expected outcome and required evidence for these four live cases: routine_1, ambiguous_1, causal_claim, and authority_boundary.

Run those four cases one at a time. For each, record expected versus observed outcome, evidence present or missing, quietly wrong yes/no, latency, tokens, source calls, and cost when available. Mark unavailable telemetry honestly. Do not average away a failed high-risk case.

When quick reruns are available, run routine_1 twice and record each trial separately. Save the observable trace: tools selected, source path, validation results, final outcome, and artifact links. Do not ask for or store hidden reasoning. Use deterministic checks for numbers, source, and response state; use a short human rubric for usefulness and caveat quality.

When Python 3.9+ is available, run:
- python3 verify.py --inject-impossible-row
- python3 verify.py --inject-benchmark-conflict

The impossible-row command must Refuse and exit 2. The benchmark conflict must return Review. Do not choose a winning source when no approved precedence rule exists. Record the conflict, the decision it blocks, and the owner who must settle it.

If Python 3.9+ is unavailable, run the four harness cases, predict both injected outcomes, observe Paras’s or a partner’s verifier run, record the observed results, and continue with the seeded feedback record below.

Now operate one complete feedback loop. Open feedback/flagged_answer.yaml. Student A, or your first harness session, writes work/05_feedback.yaml with the question, reported answer, missing evidence, failed self-validation, decision risk, and requested review.

Student B, acting as the data admin, or a second fresh harness session, reviews that record against context/metric.yaml, context/business_changes.md, and work/04_proof.yaml. Save work/05_admin_decision.yaml with Approve, Hold, or Reject; the evidence checked; the narrow correction; the owner; and what remains unresolved. Do not invent a source-precedence rule or causal proof.

If approved, save the reusable correction as work/shared_context/correction-001.yaml and the affected test as work/05_regression_case.yaml. Do not modify the lab’s data/ or context/ files. Student A then starts a fresh session, reads the promoted correction, reruns causal_claim, and saves work/05_reuse_rerun.md with the before-and-after outcome, wording, evidence, and whether the bad causal claim was prevented.

Save work/05_eval_results.csv and work/05_observed_operations.csv. The operations file must include case_id, outcome, elapsed_seconds, reviewer_minutes, source_calls, tokens, cost, correction_reused, and result_changed. Mark unavailable fields honestly. Stop if any high-risk case is quietly wrong. Keep the remaining four cases as the extension pack after class.
```

`--inject-impossible-row` exits with code 2 by design. The refusal is the passing result.
