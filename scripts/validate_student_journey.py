#!/usr/bin/env python3
"""Exercise the workshop the way a student receives it: as downloaded files."""

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import zipfile
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "index.html"
PREVIEW = ROOT / "examples" / "workshop-data.html"
LAB_ZIP = ROOT / "assets" / "agentic-analytics-workshop-lab.zip"
PROMPTS = ROOT / "prompts"
WORKFLOW = ROOT / ".github" / "workflows" / "quality-and-pages.yml"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self.links.append({key: value or "" for key, value in attrs})


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_verifier(folder: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "verify.py", *args],
        cwd=folder,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def check_named_downloads() -> None:
    parser = LinkParser()
    parser.feed(COURSE.read_text(encoding="utf-8"))
    expected = {
        "assets/agentic-analytics-workshop-lab.zip": "agentic-analytics-workshop-lab.zip",
        "assets/agentic-analytics-lab/data/funnel_segments.csv": "funnel_segments.csv",
        "assets/agentic-analytics-lab/data/wbr_benchmark.csv": "wbr_benchmark.csv",
    }
    by_href = {link.get("href", ""): link for link in parser.links}
    for href, filename in expected.items():
        require(href in by_href, f"course is missing download link: {href}")
        require(
            by_href[href].get("download") == filename,
            f"download must preserve filename {filename}: {href}",
        )
    require(
        any(link.get("href") == "examples/workshop-data.html" for link in parser.links),
        "course is missing the browser-friendly data preview",
    )


def check_preview_contract() -> None:
    source = PREVIEW.read_text(encoding="utf-8")
    for required in (
        'id="calculation-table"',
        'id="benchmark-table"',
        'download="funnel_segments.csv"',
        'download="wbr_benchmark.csv"',
        "data/funnel_segments.csv",
        "data/wbr_benchmark.csv",
    ):
        require(required in source, f"data preview is missing: {required}")


def check_prompt_contract() -> None:
    prompt_files = sorted(PROMPTS.glob("[0-9]*.md"))
    require(len(prompt_files) == 8, f"expected 8 staged prompts, found {len(prompt_files)}")
    prompt_text = "\n".join(path.read_text(encoding="utf-8") for path in prompt_files)
    expected_outputs = (
        "work/00_readiness.md",
        "work/01_use_case.md",
        "work/02_contract.yaml",
        "work/02_architecture.md",
        "work/03_metric_proposal.yaml",
        "work/04a_plan.yaml",
        "work/04_proof.yaml",
        "work/05_feedback.yaml",
        "work/05_admin_decision.yaml",
        "work/shared_context/correction-001.yaml",
        "work/05_regression_case.yaml",
        "work/05_reuse_rerun.md",
        "work/05_eval_results.csv",
        "work/05_observed_operations.csv",
        "work/06_operations.md",
        "work/07_launch_memo.md",
    )
    for output in expected_outputs:
        require(output in prompt_text, f"prompt sequence does not name expected output: {output}")
    require(
        "Do not overwrite the approved context/metric.yaml" in prompt_text,
        "metric prompt must preserve the read-only approved context",
    )
    require(
        "Do not modify the lab’s data/ or context/ files" in prompt_text,
        "eval prompt must preserve the read-only source boundary",
    )
    require(
        "If the tool list includes ChatData, a warehouse, a company MCP" in prompt_text,
        "readiness prompt must stop when real-company tools are connected",
    )


def check_release_policy() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    require(
        "group: pages-${{ github.workflow }}-${{ github.ref }}" in workflow,
        "GitHub Actions concurrency must be scoped by ref",
    )
    require(
        "github.event_name != 'pull_request' && github.ref == 'refs/heads/main'" in workflow,
        "GitHub Pages may deploy only from main",
    )
    global_permissions = workflow.split("jobs:", maxsplit=1)[0]
    require("pages: write" not in global_permissions, "quality jobs must not receive Pages write access")
    require("id-token: write" not in global_permissions, "quality jobs must not receive id-token write access")
    require("pages: write" in workflow and "id-token: write" in workflow, "deploy job needs Pages permissions")


def check_downloaded_lab() -> None:
    with tempfile.TemporaryDirectory(prefix="agentic-analytics-student-") as temp_name:
        temp = Path(temp_name)
        downloaded = temp / "agentic-analytics-workshop-lab.zip"
        downloaded.write_bytes(LAB_ZIP.read_bytes())
        require(zipfile.is_zipfile(downloaded), "downloaded lab is not a valid ZIP")

        lab = temp / "lab"
        lab.mkdir()
        with zipfile.ZipFile(downloaded) as archive:
            for member in archive.infolist():
                target = (lab / member.filename).resolve()
                require(target.is_relative_to(lab.resolve()), f"unsafe ZIP path: {member.filename}")
            archive.extractall(lab)

        expected_files = (
            "README.md",
            "verify.py",
            "evals.yaml",
            "data/funnel_segments.csv",
            "data/wbr_benchmark.csv",
            "context/metric.yaml",
            "context/business_changes.md",
            "feedback/flagged_answer.yaml",
            "work/.gitkeep",
        )
        for relative in expected_files:
            require((lab / relative).is_file(), f"downloaded lab is missing: {relative}")

        feedback_text = (lab / "feedback/flagged_answer.yaml").read_text(encoding="utf-8")
        for required in ("reported_claim: Paid search caused the decline.", "self_validation: failed", "requested_action:"):
            require(required in feedback_text, f"seeded feedback is missing: {required}")

        with (lab / "data/funnel_segments.csv").open(newline="", encoding="utf-8") as handle:
            calculation_rows = list(csv.DictReader(handle))
        with (lab / "data/wbr_benchmark.csv").open(newline="", encoding="utf-8") as handle:
            benchmark_rows = list(csv.DictReader(handle))
        require(len(calculation_rows) == 16, "calculation CSV must contain 16 data rows")
        require(len(benchmark_rows) == 3, "benchmark CSV must contain 3 data rows")

        clean = run_verifier(lab)
        require(clean.returncode == 0, f"clean verifier failed:\n{clean.stdout}")
        for expected in ("OUTCOME: Review", "8.40%", "6.90%", "change_pp: -1.50"):
            require(expected in clean.stdout, f"clean verifier is missing {expected!r}")

        readiness = run_verifier(lab, "--readiness-only")
        require(readiness.returncode == 0, f"readiness check failed:\n{readiness.stdout}")
        require("READINESS: PASS" in readiness.stdout, "readiness check must report PASS")
        for spoiler in ("OUTCOME:", "8.40%", "6.90%", "change_pp"):
            require(spoiler not in readiness.stdout, f"readiness check leaked the answer: {spoiler}")

        impossible = run_verifier(lab, "--inject-impossible-row")
        require(impossible.returncode == 2, "impossible-row drill must exit 2")
        require("OUTCOME: Refuse" in impossible.stdout, "impossible-row drill must refuse")

        conflict = run_verifier(lab, "--inject-benchmark-conflict")
        require(conflict.returncode == 0, f"benchmark-conflict drill crashed:\n{conflict.stdout}")
        require("OUTCOME: Review" in conflict.stdout, "benchmark conflict must route to Review")
        require("beyond the approved tolerance" in conflict.stdout, "benchmark conflict must explain why")

        missing_column = run_verifier(lab, "--inject-missing-column")
        require(missing_column.returncode == 2, "missing-column drill must fail closed")
        require("OUTCOME: Refuse" in missing_column.stdout, "missing-column drill must refuse")

        missing_benchmark = run_verifier(lab, "--inject-missing-benchmark")
        require(missing_benchmark.returncode == 0, "missing benchmark should produce a reviewable result")
        require("OUTCOME: Review" in missing_benchmark.stdout, "missing benchmark must route to Review")
        require("benchmark missing complete week" in missing_benchmark.stdout, "missing benchmark must be visible")

        benchmark_path = lab / "data/wbr_benchmark.csv"
        original_benchmark = benchmark_path.read_bytes()
        benchmark_lines = original_benchmark.decode("utf-8").splitlines()
        benchmark_lines[1] = ",".join(benchmark_lines[1].split(",")[:-1])
        benchmark_path.write_text("\n".join(benchmark_lines) + "\n", encoding="utf-8")
        truncated_benchmark = run_verifier(lab)
        require(truncated_benchmark.returncode == 0, "an incomplete benchmark row should route to review")
        require("OUTCOME: Review" in truncated_benchmark.stdout, "an incomplete benchmark row must route to Review")
        require("benchmark CSV line 2 missing values" in truncated_benchmark.stdout, "an incomplete benchmark row must be visible")
        require("Traceback" not in truncated_benchmark.stdout, "an incomplete benchmark row must not crash")
        benchmark_path.write_bytes(original_benchmark)

        funnel_path = lab / "data/funnel_segments.csv"
        original_funnel = funnel_path.read_bytes()

        lines = original_funnel.decode("utf-8").splitlines()
        lines[1] = ",".join(lines[1].split(",")[:-2])
        funnel_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        truncated = run_verifier(lab)
        require(truncated.returncode == 2, "a truncated CSV row must fail closed")
        require("OUTCOME: Refuse" in truncated.stdout, "a truncated CSV row must refuse")
        require("Traceback" not in truncated.stdout, "a truncated CSV row must not crash")

        funnel_path.write_bytes(original_funnel)
        with funnel_path.open(newline="", encoding="utf-8") as handle:
            zero_baseline_rows = list(csv.DictReader(handle))
            fieldnames = list(zero_baseline_rows[0])
        for row in zero_baseline_rows:
            if row["week_start"] == "2026-08-03" and row["population"] == "eligible" and row["is_complete"] == "true":
                row["qualified_signups"] = "0"
        with funnel_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(zero_baseline_rows)
        zero_baseline = run_verifier(lab)
        require(zero_baseline.returncode == 0, "a zero prior baseline must not crash")
        require("relative_change_pct: not_applicable" in zero_baseline.stdout, "a zero prior baseline must report an undefined relative change")
        require("Traceback" not in zero_baseline.stdout, "a zero prior baseline must not produce a traceback")

        funnel_path.write_bytes(original_funnel)
        with funnel_path.open(newline="", encoding="utf-8") as handle:
            zero_gap_rows = list(csv.DictReader(handle))
            fieldnames = list(zero_gap_rows[0])
        prior_by_segment = {
            (row["channel"], row["device"], row["landing_page"]): (row["qualified_sessions"], row["qualified_signups"])
            for row in zero_gap_rows
            if row["week_start"] == "2026-08-03" and row["population"] == "eligible" and row["is_complete"] == "true"
        }
        for row in zero_gap_rows:
            key = (row["channel"], row["device"], row["landing_page"])
            if row["week_start"] == "2026-08-10" and row["population"] == "eligible" and row["is_complete"] == "true":
                row["qualified_sessions"], row["qualified_signups"] = prior_by_segment[key]
        with funnel_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(zero_gap_rows)
        zero_gap = run_verifier(lab)
        require(zero_gap.returncode == 0, "zero segment-rate underperformance must not crash")
        require("paid_search_share_of_underperformance: not_applicable" in zero_gap.stdout, "a zero underperformance denominator must be explicit")
        require("Traceback" not in zero_gap.stdout, "zero underperformance must not produce a traceback")

        funnel_path.write_bytes(original_funnel)

        for output in (
            "00_readiness.md",
            "01_use_case.md",
            "02_contract.yaml",
            "02_architecture.md",
            "03_metric_proposal.yaml",
            "04a_plan.yaml",
            "04_proof.yaml",
            "05_feedback.yaml",
            "05_admin_decision.yaml",
            "shared_context/correction-001.yaml",
            "05_regression_case.yaml",
            "05_reuse_rerun.md",
            "05_eval_results.csv",
            "05_observed_operations.csv",
            "06_operations.md",
            "07_launch_memo.md",
        ):
            path = lab / "work" / output
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("student acceptance artifact\n", encoding="utf-8")
            require(path.is_file(), f"student cannot write expected artifact: work/{output}")

        operator_artifacts = {
            "05_feedback.yaml": "outcome: Answer\nself_validation: failed\nrequested_review: true\n",
            "05_admin_decision.yaml": "decision: Approve\ncorrection: largest observed contributor, not root cause\n",
            "shared_context/correction-001.yaml": "id: CORR-001\nrequired_outcome: Review\nforbid_claim: paid search caused the decline\n",
            "05_regression_case.yaml": "case_id: causal_claim\nexpected_outcome: Review\n",
            "05_reuse_rerun.md": "# Fresh-session rerun\nBefore: Answer\nAfter: Review\nUnsupported causal claim prevented: yes\n",
            "05_observed_operations.csv": "case_id,outcome,elapsed_seconds,reviewer_minutes,source_calls,tokens,cost,correction_reused,result_changed\ncausal_claim,Review,42,6,2,unavailable,unavailable,true,true\n",
        }
        for relative, content in operator_artifacts.items():
            path = lab / "work" / relative
            path.write_text(content, encoding="utf-8")
            require(path.read_text(encoding="utf-8") == content, f"operating-loop artifact did not persist: work/{relative}")


def main() -> int:
    try:
        check_named_downloads()
        check_preview_contract()
        check_prompt_contract()
        check_release_policy()
        check_downloaded_lab()
    except (AssertionError, OSError, zipfile.BadZipFile) as error:
        print(f"FAIL: {error}")
        return 1
    print("PASS: named downloads, data preview, prompt outputs, clean ZIP, verifier drills, and work boundary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
