-- DuckDB route for the synthetic workshop lab.
-- Run from the lab folder. The CSV files remain read-only.

CREATE OR REPLACE TEMP VIEW funnel_segments AS
SELECT * FROM read_csv_auto('data/funnel_segments.csv', header = true);

CREATE OR REPLACE TEMP VIEW wbr_benchmark AS
SELECT * FROM read_csv_auto('data/wbr_benchmark.csv', header = true);

CREATE OR REPLACE TEMP VIEW eligible_complete AS
SELECT *
FROM funnel_segments
WHERE population = 'eligible'
  AND is_complete = true;

-- Overall calculation and benchmark tie-out.
WITH calculated AS (
  SELECT
    week_start,
    SUM(qualified_sessions) AS sessions,
    SUM(qualified_signups) AS signups,
    100.0 * SUM(qualified_signups) / NULLIF(SUM(qualified_sessions), 0) AS conversion_pct
  FROM eligible_complete
  GROUP BY week_start
)
SELECT
  c.week_start,
  c.sessions,
  c.signups,
  ROUND(c.conversion_pct, 2) AS calculated_pct,
  b.conversion_pct AS benchmark_pct,
  ROUND(ABS(c.conversion_pct - b.conversion_pct), 2) AS benchmark_delta_pp
FROM calculated c
JOIN wbr_benchmark b USING (week_start)
WHERE b.is_complete = true
ORDER BY c.week_start;

-- Segment-rate underperformance at the current traffic mix.
WITH prior AS (
  SELECT
    channel,
    device,
    landing_page,
    1.0 * qualified_signups / NULLIF(qualified_sessions, 0) AS prior_rate
  FROM eligible_complete
  WHERE week_start = DATE '2026-08-03'
), current_period AS (
  SELECT *
  FROM eligible_complete
  WHERE week_start = DATE '2026-08-10'
)
SELECT
  c.channel,
  ROUND(SUM(c.qualified_sessions * p.prior_rate), 1) AS expected_signups_at_prior_rates,
  SUM(c.qualified_signups) AS actual_signups,
  ROUND(SUM(c.qualified_sessions * p.prior_rate - c.qualified_signups), 1) AS performance_loss
FROM current_period c
JOIN prior p USING (channel, device, landing_page)
GROUP BY c.channel
ORDER BY performance_loss DESC;

-- Structural failures must stop the answer.
SELECT *
FROM funnel_segments
WHERE qualified_sessions < 0
   OR qualified_signups < 0
   OR qualified_signups > qualified_sessions;
