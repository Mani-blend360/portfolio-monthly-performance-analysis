#!/usr/bin/env python3
"""Run skill eval prompts with Codex and collect all artifacts in one folder."""

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from validate_eval_set import validate_eval_set


def copy_workspace(source, destination):
    ignored = shutil.ignore_patterns(
        ".venv", ".DS_Store", "__pycache__", "*.pyc", "results.json",
        "scorecard.md", "artifacts", "results",
    )
    shutil.copytree(source, destination, ignore=ignored)


def write_summary(run_dir, records):
    counts = {
        "total": len(records),
        "completed": sum(record["execution_status"] == "completed" for record in records),
        "failed": sum(record["execution_status"] == "failed" for record in records),
        "timed_out": sum(record["execution_status"] == "timed_out" for record in records),
    }
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": counts,
        "cases": records,
        "grading_status": "pending_review",
    }
    (run_dir / "summary.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Skill evaluation run",
        "",
        f"- Total: {counts['total']}",
        f"- Completed: {counts['completed']}",
        f"- Failed: {counts['failed']}",
        f"- Timed out: {counts['timed_out']}",
        "- Behavioral grading: pending review against each case's expected and prohibited criteria",
        "",
        "| Case | Polarity | Mode | Execution | Exit code | Duration (s) |",
        "|---|---|---|---|---:|---:|",
    ]
    for record in records:
        exit_code = "n/a" if record["exit_code"] is None else record["exit_code"]
        lines.append(
            f"| {record['id']} | {record['polarity']} | {record['grading_mode']} | "
            f"{record['execution_status']} | {exit_code} | {record['duration_seconds']:.1f} |"
        )
    (run_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-set", default="evals/cases.jsonl")
    parser.add_argument("--results-root", default="evals/results")
    parser.add_argument("--case", action="append", dest="case_ids", help="run only this case ID; repeatable")
    parser.add_argument("--timeout", type=int, default=900, help="seconds allowed per case")
    parser.add_argument("--codex", default="codex", help="Codex CLI executable")
    parser.add_argument("--dry-run", action="store_true", help="prepare folders and prompts without invoking Codex")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    eval_path = (skill_root / args.eval_set).resolve()
    cases, errors = validate_eval_set(eval_path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.case_ids:
        requested = set(args.case_ids)
        known = {case["id"] for case in cases}
        unknown = requested - known
        if unknown:
            print(f"ERROR: unknown case IDs: {', '.join(sorted(unknown))}", file=sys.stderr)
            return 1
        cases = [case for case in cases if case["id"] in requested]

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = (skill_root / args.results_root / stamp).resolve()
    run_dir.mkdir(parents=True)
    records = []

    for index, case in enumerate(cases, 1):
        case_dir = run_dir / case["id"]
        workspace = case_dir / "workspace"
        case_dir.mkdir()
        copy_workspace(skill_root, workspace)
        (case_dir / "case.json").write_text(json.dumps(case, indent=2) + "\n", encoding="utf-8")

        prompt = (
            "$portfolio-monthly-performance-analysis\n\n"
            + case["prompt"]
            + "\n\nUse only files in this isolated workspace. Do not access live systems. "
              "Return the complete final response in this task."
        )
        (case_dir / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")
        trace_path = case_dir / "trace.jsonl"
        final_path = case_dir / "final.md"
        stderr_path = case_dir / "stderr.log"

        print(f"[{index}/{len(cases)}] {case['id']}", flush=True)
        started = time.monotonic()
        exit_code = None
        status = "prepared"
        if not args.dry_run:
            command = [
                args.codex, "exec", "--json", "--ephemeral", "--skip-git-repo-check",
                "--approve-for-me", "-C", str(workspace),
                "-o", str(final_path), prompt,
            ]
            try:
                with trace_path.open("w", encoding="utf-8") as trace, stderr_path.open("w", encoding="utf-8") as stderr:
                    completed = subprocess.run(
                        command, stdout=trace, stderr=stderr, text=True,
                        timeout=args.timeout, check=False,
                    )
                exit_code = completed.returncode
                status = "completed" if exit_code == 0 else "failed"
            except subprocess.TimeoutExpired:
                status = "timed_out"
                stderr_path.write_text(f"Timed out after {args.timeout} seconds.\n", encoding="utf-8")
            except OSError as exc:
                status = "failed"
                stderr_path.write_text(f"Could not start Codex: {exc}\n", encoding="utf-8")
        duration = time.monotonic() - started
        records.append({
            "id": case["id"],
            "polarity": case["polarity"],
            "grading_mode": case["grading"]["mode"],
            "execution_status": status,
            "exit_code": exit_code,
            "duration_seconds": round(duration, 3),
            "case_directory": str(case_dir.relative_to(run_dir)),
        })
        write_summary(run_dir, records)

    print(f"Results: {run_dir}")
    return 0 if all(record["execution_status"] in {"completed", "prepared"} for record in records) else 1


if __name__ == "__main__":
    sys.exit(main())
