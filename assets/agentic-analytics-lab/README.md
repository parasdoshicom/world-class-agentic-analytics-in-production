# Agentic Analytics Workshop Lab

This is a synthetic, public-safe case for the workshop. It works without a warehouse, an MCP server, or extra Python packages.

## The question

Why did qualified-signup conversion fall in the most recent complete week, and where should Growth investigate next?

The answer supports a weekly review decision about what to investigate. It does not authorize a budget, campaign, or routing change.

## Start here

1. Open this folder in Codex, Cursor, Claude Code, or another file-capable harness.
2. Tell the harness to work only inside this folder, treat `data/` and `context/` as read-only, and write generated work only under `work/`.
3. Copy the staged prompts from the course page. Inspect and approve each checkpoint before moving to the next.
4. Run the independent verifier at any time:

   ```bash
   python3 verify.py
   ```

5. If DuckDB is available, you can also run `analysis.sql`.

## Files

- `data/funnel_segments.csv` — the calculation source.
- `data/wbr_benchmark.csv` — an independent weekly-review benchmark.
- `context/metric.yaml` — the approved definition, filters, limits, and caveats.
- `context/business_changes.md` — a known tagging change that limits causal claims.
- `analysis.sql` — the trusted DuckDB route.
- `verify.py` — a standard-library Python verifier.
- `evals.yaml` — expected outcomes for routine, ambiguous, broken, and unsafe requests.
- `work/` — the only folder where the harness should save generated artifacts.

## Known truth

Do the work before expanding the reference answer in the course page.

- August 3: 840 / 10,000 = 8.4%.
- August 10: 690 / 10,000 = 6.9%.
- Change: -1.5 percentage points, or -17.86% relative.
- Paid search is the largest observed contributor to segment-rate underperformance.
- A tagging change means the system should recommend review, not claim a proven root cause.

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

All companies, values, and events in this lab are fictional.
