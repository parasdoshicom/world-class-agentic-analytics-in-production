# Step 6: Operate and ask for a launch decision

```text
Read the approved contract, metric, proof, eval results, and correction.

Create work/06_operations.md with:
- manual baseline and target, check date, and guardrail
- five owner roles and who may change the metric, source, route, model, or thresholds
- read-only scope, prohibited data, limits, timeout, retry, fallback, health check, and kill switch
- Rule of Two classification for untrusted input, sensitive access, and external action
- user-feedback intake, self-validation signal, review queue, data-admin approval, and promotion into semantic context and regression tests
- run-event fields, alert thresholds, audit sample, reviewer-capacity ceiling, and incident/resume owner
- shadow → canary → narrow-production steps and rollback rule
- model-routing rule based on task quality, latency, and cost; plus model, warehouse, and human-review cost per run and per month
- expiry and reapproval triggers

Then create work/07_launch_memo.md: business decision, pilot users and workflow, quality result, material risks, adoption and reuse measure, review burden, total cost, 30-day milestones, and the leadership decision requested: Scale, Hold, or Stop.

Do not invent names, baselines, thresholds, or deployment evidence. Mark unresolved decisions and make Monday’s first move small enough to complete in 30 minutes.
```

The launch memo should make the remaining decision visible. An unresolved owner, threshold, cost, or rollback rule is a reason to Hold, not a blank to fill with a guess.
