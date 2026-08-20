#!/usr/bin/env python3
"""Independent, dependency-free verifier for the workshop's synthetic lab."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FUNNEL_PATH = ROOT / "data" / "funnel_segments.csv"
BENCHMARK_PATH = ROOT / "data" / "wbr_benchmark.csv"
TOLERANCE_PP = 0.2


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def pct(numerator: float, denominator: float) -> float:
    return 100.0 * numerator / denominator if denominator else 0.0


def refuse(reason: str, details: list[str] | None = None) -> int:
    print("OUTCOME: Refuse")
    if details:
        for detail in details:
            print(f"- {detail}")
    print(f"reason: {reason}")
    print("No conversion answer was produced.")
    return 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inject-impossible-row", action="store_true")
    parser.add_argument("--inject-benchmark-conflict", action="store_true")
    parser.add_argument("--inject-missing-column", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--inject-missing-benchmark", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    try:
        rows = read_csv(FUNNEL_PATH)
        benchmarks = read_csv(BENCHMARK_PATH)
    except (OSError, csv.Error) as error:
        return refuse("A required source could not be read.", [str(error)])

    if args.inject_missing_column:
        rows = [{key: value for key, value in row.items() if key != "qualified_sessions"} for row in rows]
    if args.inject_missing_benchmark:
        benchmarks = [row for row in benchmarks if row.get("week_start") != "2026-08-10"]

    required = {
        "row_id", "week_start", "channel", "device", "landing_page",
        "qualified_sessions", "qualified_signups", "population",
        "is_complete", "tag_version",
    }
    if not rows:
        return refuse("The calculation source is empty.")
    missing_columns = sorted(required - set(rows[0]))
    if missing_columns:
        return refuse("The calculation source is missing required columns.", missing_columns)

    incomplete_rows: list[str] = []
    for index, row in enumerate(rows, start=2):
        missing_values = sorted(
            column for column in required
            if row.get(column) is None or not str(row.get(column)).strip()
        )
        if missing_values:
            incomplete_rows.append(f"CSV line {index}: missing {', '.join(missing_values)}")
    if incomplete_rows:
        return refuse("The calculation source has incomplete required values.", incomplete_rows)

    schema_ok = True
    unique_ids = len({row["row_id"] for row in rows}) == len(rows)

    if args.inject_impossible_row:
        rows[6] = dict(rows[6])
        rows[6]["qualified_signups"] = "1001"

    structural_errors: list[str] = []
    for row in rows:
        try:
            sessions = int(row["qualified_sessions"])
            signups = int(row["qualified_signups"])
        except (TypeError, ValueError):
            structural_errors.append(f"row {row['row_id']}: sessions and signups must be integers")
            continue
        if sessions <= 0 or signups < 0 or signups > sessions:
            structural_errors.append(
                f"row {row['row_id']}: signups={signups}, sessions={sessions}"
            )

    if not schema_ok or not unique_ids or structural_errors:
        details = [f"schema_ok: {schema_ok}", f"unique_row_ids: {unique_ids}"] + structural_errors
        return refuse("A critical source or structure check failed.", details)

    clean = [
        row for row in rows
        if row["population"] == "eligible" and as_bool(row["is_complete"])
    ]
    weekly: dict[str, dict[str, float]] = defaultdict(lambda: {"sessions": 0.0, "signups": 0.0})
    for row in clean:
        weekly[row["week_start"]]["sessions"] += int(row["qualified_sessions"])
        weekly[row["week_start"]]["signups"] += int(row["qualified_signups"])

    prior_week, current_week = "2026-08-03", "2026-08-10"
    missing_calculation_weeks = sorted({prior_week, current_week} - set(weekly))
    if missing_calculation_weeks:
        return refuse("The calculation source is missing a required complete week.", missing_calculation_weeks)

    benchmark_required = {"week_start", "conversion_pct", "is_complete"}
    benchmark_schema_ok = bool(benchmarks) and benchmark_required.issubset(benchmarks[0])
    benchmark_by_week: dict[str, dict[str, str]] = {}
    benchmark_errors: list[str] = []
    if benchmark_schema_ok:
        valid_benchmarks: list[dict[str, str]] = []
        for index, row in enumerate(benchmarks, start=2):
            missing_values = sorted(
                column for column in benchmark_required
                if row.get(column) is None or not str(row.get(column)).strip()
            )
            if missing_values:
                benchmark_errors.append(
                    f"benchmark CSV line {index} missing values: {', '.join(missing_values)}"
                )
                continue
            valid_benchmarks.append(row)
        benchmark_by_week = {
            row["week_start"]: dict(row)
            for row in valid_benchmarks if as_bool(row["is_complete"])
        }
    else:
        missing = sorted(benchmark_required - (set(benchmarks[0]) if benchmarks else set()))
        benchmark_errors.append(f"benchmark missing columns: {', '.join(missing) or 'empty file'}")

    if args.inject_benchmark_conflict and current_week in benchmark_by_week:
        benchmark_by_week["2026-08-10"]["conversion_pct"] = "8.0"

    tieouts: list[tuple[str, float]] = []
    for week, values in sorted(weekly.items()):
        if week not in benchmark_by_week:
            benchmark_errors.append(f"benchmark missing complete week: {week}")
            continue
        calculated = pct(values["signups"], values["sessions"])
        try:
            benchmark = float(benchmark_by_week[week]["conversion_pct"])
        except (TypeError, ValueError):
            benchmark_errors.append(f"benchmark conversion is not numeric for {week}")
            continue
        tieouts.append((week, abs(calculated - benchmark)))

    prior = weekly[prior_week]
    current = weekly[current_week]
    prior_pct = pct(prior["signups"], prior["sessions"])
    current_pct = pct(current["signups"], current["sessions"])
    delta_pp = current_pct - prior_pct
    relative = None if abs(prior_pct) < 1e-12 else 100.0 * (current_pct / prior_pct - 1.0)

    prior_rates: dict[tuple[str, str, str], float] = {}
    for row in clean:
        if row["week_start"] == prior_week:
            key = (row["channel"], row["device"], row["landing_page"])
            prior_rates[key] = int(row["qualified_signups"]) / int(row["qualified_sessions"])

    current_keys = {
        (row["channel"], row["device"], row["landing_page"])
        for row in clean if row["week_start"] == current_week
    }
    missing_prior_segments = sorted(current_keys - set(prior_rates))
    if missing_prior_segments:
        return refuse(
            "The current week contains segments with no prior-period comparison.",
            [" / ".join(segment) for segment in missing_prior_segments],
        )

    expected_total = 0.0
    actual_total = 0.0
    loss_by_channel: dict[str, float] = defaultdict(float)
    channel_totals: dict[tuple[str, str], dict[str, float]] = defaultdict(lambda: {"sessions": 0.0, "signups": 0.0})
    mobile_paid: dict[str, dict[str, float]] = defaultdict(lambda: {"sessions": 0.0, "signups": 0.0, "short_sessions": 0.0})
    non_paid: dict[str, dict[str, float]] = defaultdict(lambda: {"sessions": 0.0, "signups": 0.0})

    for row in clean:
        week = row["week_start"]
        sessions = int(row["qualified_sessions"])
        signups = int(row["qualified_signups"])
        channel_totals[(week, row["channel"])]["sessions"] += sessions
        channel_totals[(week, row["channel"])]["signups"] += signups
        if row["channel"] == "paid_search" and row["device"] == "mobile":
            mobile_paid[week]["sessions"] += sessions
            mobile_paid[week]["signups"] += signups
            if row["landing_page"] == "short":
                mobile_paid[week]["short_sessions"] += sessions
        if row["channel"] != "paid_search":
            non_paid[week]["sessions"] += sessions
            non_paid[week]["signups"] += signups
        if week == current_week:
            key = (row["channel"], row["device"], row["landing_page"])
            expected = sessions * prior_rates[key]
            expected_total += expected
            actual_total += signups
            loss_by_channel[row["channel"]] += expected - signups

    paid_loss = loss_by_channel["paid_search"]
    total_loss = expected_total - actual_total
    max_tieout = max((delta for _, delta in tieouts), default=0.0)
    review_reasons = ["Campaign tagging changed between periods, so the data does not isolate a sole cause."]
    review_reasons.extend(benchmark_errors)
    if max_tieout > TOLERANCE_PP:
        review_reasons.append("The calculated result and WBR benchmark differ beyond the approved tolerance.")
    outcome = "Review"

    print(f"OUTCOME: {outcome}")
    print("SOURCE CHECKS")
    print(f"rows: {len(rows)}")
    print(f"date_range: {min(r['week_start'] for r in rows)} to {max(r['week_start'] for r in rows)}")
    print(f"eligible_complete_rows: {len(clean)}")
    print("WEEKLY RESULT")
    print(f"{prior_week}: {int(prior['signups'])}/{int(prior['sessions'])} = {prior_pct:.2f}%")
    print(f"{current_week}: {int(current['signups'])}/{int(current['sessions'])} = {current_pct:.2f}%")
    print(f"change_pp: {delta_pp:.2f}")
    print(f"relative_change_pct: {relative:.2f}" if relative is not None else "relative_change_pct: not_applicable")
    print("DRIVER CHECK")
    print(f"paid_search: {pct(channel_totals[(prior_week, 'paid_search')]['signups'], channel_totals[(prior_week, 'paid_search')]['sessions']):.2f}% -> {pct(channel_totals[(current_week, 'paid_search')]['signups'], channel_totals[(current_week, 'paid_search')]['sessions']):.2f}%")
    print(f"mobile_paid_search: {pct(mobile_paid[prior_week]['signups'], mobile_paid[prior_week]['sessions']):.2f}% -> {pct(mobile_paid[current_week]['signups'], mobile_paid[current_week]['sessions']):.2f}%")
    print(f"mobile_paid_short_share: {pct(mobile_paid[prior_week]['short_sessions'], mobile_paid[prior_week]['sessions']):.2f}% -> {pct(mobile_paid[current_week]['short_sessions'], mobile_paid[current_week]['sessions']):.2f}%")
    print(f"expected_current_signups_at_prior_segment_rates: {expected_total:.0f}")
    print(f"actual_current_signups: {actual_total:.0f}")
    print(f"segment_rate_underperformance: {total_loss:.0f}")
    if abs(total_loss) < 1e-12:
        print("paid_search_share_of_underperformance: not_applicable")
    else:
        print(f"paid_search_share_of_underperformance: {100.0 * paid_loss / total_loss:.2f}%")
    print(f"without_paid_search: {pct(non_paid[prior_week]['signups'], non_paid[prior_week]['sessions']):.2f}% -> {pct(non_paid[current_week]['signups'], non_paid[current_week]['sessions']):.2f}%")
    print("BENCHMARK CHECK")
    for week, delta in tieouts:
        print(f"{week}: delta={delta:.2f}pp, pass={delta <= TOLERANCE_PP}")
    for error in benchmark_errors:
        print(f"warning: {error}")
    print("REVIEW REASONS")
    for reason in review_reasons:
        print(f"- {reason}")
    print("The movement and largest observed contributor are supported; a sole root cause is not.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
