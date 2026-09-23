#!/usr/bin/env python3

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
ASSETS = ROOT / "assets"
sys.path.insert(0, str(SCRIPTS))

from calculate_variances import calculate  # noqa: E402
from validate_input import validate  # noqa: E402
from validate_eval_set import validate_eval_set  # noqa: E402


class PerformanceAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.errors, cls.warnings = validate(ASSETS / "synthetic_monthly_data.csv")
        cls.results = {item["kpi"]: item for item in calculate(cls.rows, "2026-08")}

    def test_synthetic_input_valid_with_expected_warning(self):
        self.assertEqual([], self.errors)
        self.assertTrue(any("inconsistent units" in w for w in self.warnings))

    def test_percentage_and_direction(self):
        revenue = self.results["Revenue"]["comparisons"]["budget"]
        self.assertEqual(-3, revenue["absolute_variance"])
        self.assertEqual(-5, revenue["percentage_variance"])
        self.assertEqual("material", revenue["materiality"])
        self.assertEqual("unfavorable", revenue["favorability"])
        opex = self.results["Operating expenses"]["comparisons"]["budget"]
        self.assertEqual("favorable", opex["favorability"])
        self.assertEqual("non_material", opex["materiality"])

    def test_basis_points(self):
        margin = self.results["EBITDA margin"]["comparisons"]["budget"]
        self.assertEqual(-120, margin["basis_point_difference"])
        self.assertEqual("material", margin["materiality"])

    def test_zero_budget(self):
        churn = self.results["Customer churn"]["comparisons"]["budget"]
        self.assertEqual("not_meaningful", churn["percentage_variance"])
        self.assertEqual("material", churn["materiality"])

    def test_threshold_equality(self):
        capex = self.results["Capital expenditure"]["comparisons"]["budget"]
        self.assertEqual(10, capex["percentage_variance"])
        self.assertEqual("material", capex["materiality"])

    def test_evidence_classes_and_forecast_revision(self):
        self.assertEqual("contradictory_evidence", self.results["Revenue"]["evidence_class"])
        self.assertEqual("missing_evidence", self.results["Net debt"]["evidence_class"])
        revision = self.results["Revenue"]["full_year_forecast_revision"]
        self.assertEqual(-30, revision["absolute_variance"])

    def test_invalid_fixtures(self):
        for name in ("invalid_numeric.csv", "invalid_duplicate.csv"):
            _, errors, _ = validate(ROOT / "tests" / "fixtures" / name)
            self.assertTrue(errors, name)

    def test_cli_output_completeness(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_json = Path(tmp) / "results.json"
            output_md = Path(tmp) / "scorecard.md"
            completed = subprocess.run(
                [sys.executable, str(SCRIPTS / "calculate_variances.py"), str(ASSETS / "synthetic_monthly_data.csv"),
                 "--period", "2026-08", "--output-json", str(output_json), "--output-markdown", str(output_md)],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            payload = json.loads(output_json.read_text())
            self.assertEqual(15, len(payload["results"]))
            scorecard = output_md.read_text()
            self.assertIn("Revenue", scorecard)
            self.assertIn("Data-quality warnings", scorecard)

    def test_sample_analysis_is_complete_and_reconciled(self):
        sample = (ASSETS / "expected_analysis.md").read_text()
        for heading in (
            "Executive summary", "KPI scorecard", "What changed and why",
            "Key risks and opportunities", "Questions for management",
            "Follow-up actions", "Data-quality and evidence warnings",
            "Calculation reconciliation",
        ):
            self.assertIn(heading, sample)
        checks = {
            "Revenue": ("USD 57.0m", "USD 60.0m", "USD -3.0m (-5.0%)"),
            "EBITDA margin": ("14.2%", "15.4%", "-1.2 pp / -120 bps"),
            "Net debt": ("USD 74.0m", "USD 65.0m", "USD +9.0m (+13.8%)"),
        }
        for kpi, values in checks.items():
            line = next(line for line in sample.splitlines() if line.startswith(f"| {kpi} |"))
            for value in values:
                self.assertIn(value, line)
        self.assertIn("percentage variance not meaningful", sample)
        self.assertIn("**PASS.**", sample)

    def test_eval_set_schema_and_coverage(self):
        cases, errors = validate_eval_set(ROOT / "evals" / "cases.jsonl")
        self.assertEqual([], errors)
        self.assertEqual(10, len(cases))
        self.assertEqual(5, sum(case["polarity"] == "positive" for case in cases))
        self.assertEqual(5, sum(case["polarity"] == "negative" for case in cases))
        ids = {case["id"] for case in cases}
        self.assertIn("positive-zero-budget", ids)
        self.assertIn("negative-missing-driver", ids)
        self.assertIn("negative-investment-advice", ids)

    def test_eval_runner_dry_run_collects_one_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            completed = subprocess.run(
                [sys.executable, str(SCRIPTS / "run_eval_cases.py"),
                 "--dry-run", "--case", "positive-bps-calculation",
                 "--results-root", tmp],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            result_root = next(Path(tmp).iterdir())
            summary = json.loads((result_root / "summary.json").read_text())
            self.assertEqual(1, summary["counts"]["total"])
            self.assertEqual("prepared", summary["cases"][0]["execution_status"])
            case_dir = result_root / "positive-bps-calculation"
            self.assertTrue((case_dir / "case.json").is_file())
            self.assertTrue((case_dir / "prompt.txt").is_file())


if __name__ == "__main__":
    unittest.main()
