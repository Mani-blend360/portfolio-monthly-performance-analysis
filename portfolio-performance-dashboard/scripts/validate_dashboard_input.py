#!/usr/bin/env python3
"""Validate reconciled portfolio results before dashboard rendering."""

import argparse
import json
import sys
from pathlib import Path

TOP_STATUSES = {"ready", "warning", "blocked", "empty"}
VALIDATION_STATUSES = {"PASS", "FAIL"}
RECONCILIATION_STATUSES = {"PASS", "FAIL", "NOT_RUN"}
KPI_TYPES = {"financial", "operational"}
EVIDENCE_CLASSES = {
    "calculated_fact", "source_supported", "hypothesis",
    "missing_evidence", "contradictory_evidence",
}
BASELINES = {
    "budget", "prior_month", "prior_year", "current_forecast",
    "original_investment_case",
}


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8")), []
    except OSError as exc:
        return None, [f"cannot read results JSON: {exc}"]
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]


def validate(payload):
    errors, warnings = [], []
    if not isinstance(payload, dict):
        return ["top-level JSON value must be an object"], []

    required = {"schema_version", "status", "period", "source", "validation", "reconciliation", "results"}
    missing = sorted(required - payload.keys())
    if missing:
        errors.append(f"missing required top-level fields: {', '.join(missing)}")
        return errors, warnings

    status = payload.get("status")
    if status not in TOP_STATUSES:
        errors.append(f"invalid status '{status}'")
    if not isinstance(payload.get("period"), str) or not payload["period"]:
        errors.append("period must be a non-empty string")
    if not isinstance(payload.get("source"), dict):
        errors.append("source must be an object")

    validation = payload.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        if validation.get("status") not in VALIDATION_STATUSES:
            errors.append("validation.status must be PASS or FAIL")
        for field in ("errors", "warnings"):
            if not isinstance(validation.get(field), list):
                errors.append(f"validation.{field} must be an array")

    reconciliation = payload.get("reconciliation")
    if not isinstance(reconciliation, dict):
        errors.append("reconciliation must be an object")
    else:
        if reconciliation.get("status") not in RECONCILIATION_STATUSES:
            errors.append("reconciliation.status must be PASS, FAIL, or NOT_RUN")
        if not isinstance(reconciliation.get("mismatches"), list):
            errors.append("reconciliation.mismatches must be an array")

    results = payload.get("results")
    if not isinstance(results, list):
        errors.append("results must be an array")
        return errors, warnings

    if status in {"ready", "warning"}:
        if validation.get("status") != "PASS":
            errors.append(f"status '{status}' requires validation PASS")
        if reconciliation.get("status") != "PASS":
            errors.append(f"status '{status}' requires reconciliation PASS")
        if not results:
            errors.append(f"status '{status}' requires at least one KPI result")
    if status == "blocked" and validation.get("status") != "FAIL":
        errors.append("blocked status requires validation FAIL")
    if status == "empty" and results:
        errors.append("empty status requires an empty results array")

    names = set()
    for index, item in enumerate(results):
        label = f"results[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in ("kpi", "kpi_type", "actual", "unit", "direction", "materiality_type", "materiality_threshold", "comparisons", "evidence_class"):
            if field not in item:
                errors.append(f"{label}.{field} is required")
        name = item.get("kpi")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{label}.kpi must be a non-empty string")
        elif name in names:
            errors.append(f"duplicate KPI name '{name}'")
        names.add(name)
        if item.get("kpi_type") not in KPI_TYPES:
            errors.append(f"{label}.kpi_type is invalid")
        if item.get("evidence_class") not in EVIDENCE_CLASSES:
            errors.append(f"{label}.evidence_class is invalid")
        if not isinstance(item.get("actual"), (int, float)):
            errors.append(f"{label}.actual must be numeric")
        comparisons = item.get("comparisons")
        if not isinstance(comparisons, dict):
            errors.append(f"{label}.comparisons must be an object")
            continue
        missing_baselines = BASELINES - comparisons.keys()
        if missing_baselines:
            errors.append(f"{label}.comparisons missing: {', '.join(sorted(missing_baselines))}")
        for baseline, comparison in comparisons.items():
            if baseline not in BASELINES:
                warnings.append(f"{label}.comparisons contains unknown baseline '{baseline}'")
            if comparison is None:
                continue
            if not isinstance(comparison, dict):
                errors.append(f"{label}.comparisons.{baseline} must be an object or null")
                continue
            for field in ("comparison", "absolute_variance", "percentage_variance", "materiality", "favorability"):
                if field not in comparison:
                    errors.append(f"{label}.comparisons.{baseline}.{field} is required")
            percentage = comparison.get("percentage_variance")
            if not isinstance(percentage, (int, float)) and percentage != "not_meaningful":
                errors.append(f"{label}.comparisons.{baseline}.percentage_variance must be numeric or not_meaningful")
    return errors, warnings


def presentation_state(payload, errors):
    if payload is None or not isinstance(payload, dict):
        return "blocked"
    reconciliation = payload.get("reconciliation")
    validation = payload.get("validation")
    if (isinstance(validation, dict) and validation.get("status") == "PASS"
            and isinstance(reconciliation, dict) and reconciliation.get("status") == "FAIL"):
        return "reconciliation_failed"
    if errors:
        return "blocked"
    return payload["status"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results_json")
    parser.add_argument("--json", action="store_true", help="emit machine-readable validation")
    args = parser.parse_args()
    payload, load_errors = load(args.results_json)
    errors, warnings = (load_errors, []) if load_errors else validate(payload)
    result = {
        "valid": not errors,
        "presentation_state": presentation_state(payload, errors),
        "errors": errors,
        "warnings": warnings,
        "kpi_count": len(payload.get("results", [])) if isinstance(payload, dict) and isinstance(payload.get("results"), list) else 0,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Dashboard input: {'PASS' if not errors else 'FAIL'}")
        print(f"Presentation state: {result['presentation_state']}")
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
