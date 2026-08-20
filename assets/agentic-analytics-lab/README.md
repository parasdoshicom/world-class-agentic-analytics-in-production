# Agentic Analytics Workshop Lab

This is the included practice case for the workshop. It works without a warehouse or an MCP server. Python is optional and uses no extra packages.

## The question

Why did qualified-signup conversion fall in the most recent complete week, and where should Growth investigate next?

The answer supports a weekly review decision about what to investigate. It does not authorize a budget, campaign, or routing change.

## Start here

1. Start a clean local session. Disconnect ChatData, warehouse connections, company MCPs, and other real-data tools before opening the lab. A connected tool is in scope even when you do not intend to use it.
2. Open this extracted folder in Codex, Cursor, Claude Code, or another file-capable harness. This folder is the lab root. You should see `README.md`, `verify.py`, `data/`, `context/`, `evals.yaml`, and `work/` directly inside it.
3. Tell the harness to work only inside this folder, treat `data/` and `context/` as read-only, and write generated work only under `work/`. Every `work/...` path in the course is relative to this lab root.
4. Check the kit without revealing the analysis:

   ```bash
   python3 verify.py --readiness-only
   ```

   The check should print `READINESS: PASS`. If Python is unavailable, confirm the six lab-root items from step 2 and continue in the harness.
5. Copy the staged prompts from the course page. Inspect and approve each checkpoint before moving to the next.
6. Run the independent verifier during Step 4B, after you have calculated the answer in your harness:

   ```bash
   python3 verify.py
   ```

## Files

- `data/funnel_segments.csv` — the calculation source.
- `data/wbr_benchmark.csv` — an independent weekly-review benchmark.
- `context/metric.yaml` — the approved definition, filters, limits, and caveats.
- `context/business_changes.md` — a known tagging change that limits causal claims.
- `verify.py` — a standard-library Python verifier.
- `evals.yaml` — expected outcomes for routine, ambiguous, broken, and unsafe requests.
- `work/` — the only folder where the harness should save generated artifacts.

## Deliberate traps

- Test and partner-assisted rows must be excluded.
- August 17 is a partial week.
- Campaign tagging changes between the comparison periods.
- Paid search is a major driver, but removing it does not eliminate the decline.

## Failure drills

```bash
python3 verify.py --inject-impossible-row
python3 verify.py --inject-benchmark-conflict
```

The first drill should refuse to answer because signups exceed sessions. It intentionally exits with code `2`; that refusal is the passing result, not a broken lab. The second should send the result to review because the calculated value and benchmark disagree beyond tolerance.

The course dataset is designed for practice and includes known data-quality and business-context traps.
