#!/usr/bin/env python3
"""Run portfolio analysis and build a standalone local dashboard."""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANALYSIS = ROOT / "portfolio-monthly-performance-analysis"
DASHBOARD = ROOT / "portfolio-performance-dashboard"


def run(command):
    completed = subprocess.run(command, text=True, check=False)
    return completed.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(ANALYSIS / "assets" / "synthetic_monthly_data.csv"))
    parser.add_argument("--period", default="2026-08")
    parser.add_argument("--output-dir", default=str(ROOT / "local-demo"))
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    results = output_dir / "results.json"
    scorecard = output_dir / "scorecard.md"
    dashboard = output_dir / "index.html"

    analysis_code = run([
        sys.executable, str(ANALYSIS / "scripts" / "calculate_variances.py"),
        str(Path(args.input).resolve()), "--period", args.period,
        "--output-json", str(results), "--output-markdown", str(scorecard),
    ])
    if not results.exists():
        return analysis_code or 1

    run([sys.executable, str(DASHBOARD / "scripts" / "validate_dashboard_input.py"), str(results)])
    render_code = run([
        sys.executable, str(DASHBOARD / "scripts" / "render_dashboard.py"),
        str(results), "--output", str(dashboard),
    ])

    print("\nGenerated:")
    print(f"  Results:   {results}")
    if scorecard.exists():
        print(f"  Scorecard: {scorecard}")
    print(f"  Dashboard: {dashboard}")
    print("\nServe it locally with:")
    print(f"  {sys.executable} -m http.server 8765 --directory {output_dir}")
    print("Then open http://127.0.0.1:8765")
    return render_code if render_code else analysis_code


if __name__ == "__main__":
    sys.exit(main())
