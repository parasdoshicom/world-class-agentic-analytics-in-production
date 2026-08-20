# Step 5: Evaluate, repair, and rerun

```text
Read evals.yaml. Before execution, record the expected outcome and required evidence for these four live cases: routine_1, ambiguous_1, causal_claim, and authority_boundary.

Run those four cases one at a time. For each, record expected versus observed outcome, evidence present or missing, quietly wrong yes/no, latency, tokens, source calls, and cost when available. Mark unavailable telemetry honestly. Do not average away a failed high-risk case.

Then run:
- python3 verify.py --inject-impossible-row
- python3 verify.py --inject-benchmark-conflict

Pick one failure or unsupported claim. Identify whether it came from a missing asset, retrieval miss, context conflict, application error, query error, or source-data error. Write the smallest proposed repair under work/, append work/correction.yaml, and rerun every affected case. Do not modify the lab’s data/ or context/ files.

Save work/05_eval_results.csv. Stop if any high-risk case is quietly wrong. Keep the other six cases as the extension pack after class.
```

`--inject-impossible-row` exits with code 2 by design. The refusal is the passing result.
