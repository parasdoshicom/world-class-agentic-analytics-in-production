# Step 5: Evaluate, repair, and rerun

```text
For the live workshop, continue with the included CSV lab. Read evals.yaml. Before execution, record the expected outcome and required evidence for these four live cases: routine_1, ambiguous_1, causal_claim, and authority_boundary.

Run those four cases one at a time. For each, record expected versus observed outcome, evidence present or missing, quietly wrong yes/no, latency, tokens, source calls, and cost when available. Mark unavailable telemetry honestly. Do not average away a failed high-risk case.

When quick reruns are available, run routine_1 twice and record each trial separately. Save the observable trace: tools selected, source path, validation results, final outcome, and artifact links. Do not ask for or store hidden reasoning. Use deterministic checks for numbers, source, and response state; use a short human rubric for usefulness and caveat quality.

Then run:
- python3 verify.py --inject-impossible-row
- python3 verify.py --inject-benchmark-conflict

If Python is unavailable, run the four harness cases, predict both injected outcomes, observe Paras’s or a partner’s verifier run, record the observed results, and rejoin at the correction step.

Pick one failure or unsupported claim. Identify whether it came from a missing asset, retrieval miss, context conflict, application error, query error, or source-data error. Write a feedback record with the question, response outcome, evidence gap, user impact, self-validation result, and failure layer. Write the smallest proposed repair under work/, append work/correction.yaml, and rerun every affected case. Do not modify the lab’s data/ or context/ files. Once the repair is approved, keep the failure as a regression case.

Save work/05_eval_results.csv. Stop if any high-risk case is quietly wrong. Keep the remaining four cases as the extension pack after class.
```

`--inject-impossible-row` exits with code 2 by design. The refusal is the passing result.
