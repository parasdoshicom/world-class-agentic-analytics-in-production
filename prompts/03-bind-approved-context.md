# Step 3: Bind approved context

```text
Read only the supplied metric, source, and business-change material. Draft work/03_metric_proposal.yaml with the definition, formula, owner placeholders, grain, timezone, filters, exclusions, source precedence, freshness, tolerance, caveats, review date, and stop conditions. Do not overwrite the approved context/metric.yaml.

Do not invent missing values. List unresolved items.

For this question, show:
- required context
- eligible approved context
- context you actually retrieved
- context that materially changed the path, result, caveat, or outcome

For every retained context item, record its owner, retrieval trigger, freshness or expiry, and why it is needed. Keep lightweight identifiers in the working context and retrieve detailed material only when the question requires it. Remove context that does not change the route, result, caveat, or response state.

Propose two context tests: one missing-required-context case and one conflicting-context case. State the expected outcome before running them.

Show the proposed file diff and wait for approval before treating it as trusted.
```

Keep the approved input immutable. Promotion of a proposal requires the named metric owner or the team's equivalent approval path.
