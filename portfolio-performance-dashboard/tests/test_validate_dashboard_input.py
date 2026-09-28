#!/usr/bin/env python3

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_dashboard_input.py"


def comparison():
    return {
        "comparison": 60.0,
        "absolute_variance": -3.0,
        "percentage_variance": -5.0,
        "materiality": "material",
        "favorability": "unfavorable",
    }


def ready_payload():
    return {
        "schema_version": "1.0",
        "status": "ready",
        "synthetic": True,
        "company": "Northstar Components",
        "period": "2026-08",
        "source": {"file": "sample.csv", "row_count": 1},
        "validation": {"status": "PASS", "errors": [], "warnings": []},
        "reconciliation": {"status": "PASS", "mismatches": []},
        "results": [{
            "kpi": "Revenue", "kpi_type": "financial", "actual": 57.0,
            "unit": "USDm", "direction": "higher_is_favorable",
            "materiality_type": "percent", "materiality_threshold": 5.0,
            "comparisons": {
                "budget": comparison(), "prior_month": None, "prior_year": None,
                "current_forecast": None, "original_investment_case": None,
            },
            "evidence_class": "contradictory_evidence",
        }],
    }


class DashboardInputTests(unittest.TestCase):
    def run_validator(self, payload):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "results.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(path), "--json"],
                text=True, capture_output=True, check=False,
            )
            return completed, json.loads(completed.stdout)

    def test_ready_payload(self):
        completed, result = self.run_validator(ready_payload())
        self.assertEqual(0, completed.returncode)
        self.assertTrue(result["valid"])
        self.assertEqual("ready", result["presentation_state"])

    def test_missing_comparison_is_valid(self):
        payload = ready_payload()
        payload["results"][0]["comparisons"]["budget"] = None
        completed, result = self.run_validator(payload)
        self.assertEqual(0, completed.returncode)
        self.assertTrue(result["valid"])

    def test_invalid_json_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.json"
            path.write_text("{broken", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(path), "--json"],
                text=True, capture_output=True, check=False,
            )
            result = json.loads(completed.stdout)
            self.assertNotEqual(0, completed.returncode)
            self.assertEqual("blocked", result["presentation_state"])
            self.assertIn("invalid JSON", result["errors"][0])

    def test_ready_cannot_hide_failed_reconciliation(self):
        payload = ready_payload()
        payload["reconciliation"]["status"] = "FAIL"
        completed, result = self.run_validator(payload)
        self.assertNotEqual(0, completed.returncode)
        self.assertEqual("reconciliation_failed", result["presentation_state"])

    def test_explicit_reconciliation_failure_state(self):
        payload = ready_payload()
        payload["status"] = "warning"
        payload["reconciliation"] = {"status": "FAIL", "mismatches": ["Revenue actual mismatch"]}
        payload["validation"]["warnings"] = ["reconciliation failed"]
        completed, result = self.run_validator(payload)
        self.assertNotEqual(0, completed.returncode)
        self.assertEqual("reconciliation_failed", result["presentation_state"])

    def test_blocked_payload(self):
        payload = ready_payload()
        payload.update({"status": "blocked", "company": None, "results": []})
        payload["validation"] = {"status": "FAIL", "errors": ["actual must be numeric"], "warnings": []}
        payload["reconciliation"] = {"status": "NOT_RUN", "mismatches": []}
        completed, result = self.run_validator(payload)
        self.assertEqual(0, completed.returncode)
        self.assertEqual("blocked", result["presentation_state"])

    def test_empty_payload(self):
        payload = ready_payload()
        payload.update({"status": "empty", "results": []})
        payload["reconciliation"] = {"status": "NOT_RUN", "mismatches": []}
        completed, result = self.run_validator(payload)
        self.assertEqual(0, completed.returncode)
        self.assertEqual("empty", result["presentation_state"])

    def test_duplicate_kpi_rejected(self):
        payload = ready_payload()
        payload["results"].append(copy.deepcopy(payload["results"][0]))
        completed, result = self.run_validator(payload)
        self.assertNotEqual(0, completed.returncode)
        self.assertTrue(any("duplicate KPI" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
