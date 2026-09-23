#!/usr/bin/env python3
"""Calculate deterministic monthly KPI variances and a scorecard."""

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path

from validate_input import number, validate

BASELINES = ["budget", "prior_month", "prior_year", "current_forecast", "original_investment_case"]


def serial(value):
    return float(value) if isinstance(value, Decimal) else value


def variance(actual, comparison, percent_kpi):
    if comparison is None:
        return None
    absolute = actual - comparison
    percentage = "not_meaningful" if comparison == 0 else absolute / abs(comparison) * Decimal("100")
    result = {"comparison": comparison, "absolute_variance": absolute, "percentage_variance": percentage}
    if percent_kpi:
        result["percentage_point_difference"] = absolute
        result["basis_point_difference"] = absolute * Decimal("100")
    return result


def materiality(result, kind, threshold):
    if result is None:
        return "not_assessable"
    if kind == "absolute":
        measure = abs(result["absolute_variance"])
    elif kind == "bps":
        measure = abs(result["basis_point_difference"])
    else:
        if result["percentage_variance"] == "not_meaningful":
            return "not_assessable"
        measure = abs(result["percentage_variance"])
    return "material" if measure >= threshold else "non_material"


def favorability(result, direction):
    if result is None:
        return "not_assessable"
    delta = result["absolute_variance"]
    if delta == 0 or direction == "neutral":
        return "neutral"
    favorable = delta > 0 if direction == "higher_is_favorable" else delta < 0
    return "favorable" if favorable else "unfavorable"


def evidence(row, budget_result, budget_materiality):
    driver, source = row["management_driver"].strip(), row["evidence_source"].strip()
    if not driver:
        return "missing_evidence" if budget_materiality == "material" else "calculated_fact"
    if not source:
        return "missing_evidence"
    delta = budget_result["absolute_variance"] if budget_result else Decimal("0")
    lowered = driver.lower()
    up = any(word in lowered for word in ("increase", "increased", "higher", "above", "grew", "growth"))
    down = any(word in lowered for word in ("decrease", "decreased", "lower", "below", "fell", "decline"))
    if (delta < 0 and up) or (delta > 0 and down):
        return "contradictory_evidence"
    return "source_supported"


def calculate(rows, period):
    selected = [r for r in rows if r["period"] == period]
    output = []
    for row in selected:
        actual = number(row["actual"])
        percent_kpi = row["unit"] == "%"
        comparisons = {name: variance(actual, number(row[name]), percent_kpi) for name in BASELINES}
        threshold = number(row["materiality_threshold"])
        for name, result in comparisons.items():
            if result is not None:
                result["materiality"] = materiality(result, row["materiality_type"], threshold)
                result["favorability"] = favorability(result, row["favorable_direction"])
        budget = comparisons["budget"]
        budget_mat = budget["materiality"] if budget else "not_assessable"
        fy_actual, fy_case = number(row["current_full_year_forecast"]), number(row["original_investment_case_full_year"])
        fy_revision = variance(fy_actual, fy_case, percent_kpi) if fy_actual is not None and fy_case is not None else None
        item = {
            "kpi": row["kpi"], "kpi_type": row["kpi_type"], "actual": actual,
            "currency": row["currency"], "unit": row["unit"], "direction": row["favorable_direction"],
            "materiality_type": row["materiality_type"], "materiality_threshold": threshold,
            "comparisons": comparisons, "full_year_forecast_revision": fy_revision,
            "evidence_class": evidence(row, budget, budget_mat), "management_driver": row["management_driver"],
            "evidence_source": row["evidence_source"], "management_action": row["management_action"],
            "action_owner": row["action_owner"], "expected_completion_date": row["expected_completion_date"],
        }
        output.append(item)
    return output


def convert(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert(v) for v in obj]
    return obj


def display(value, unit):
    if value is None:
        return "n/a"
    suffix = "%" if unit == "%" else ""
    return f"{float(value):.1f}{suffix}"


def markdown(company, period, results, warnings):
    lines = [f"# Synthetic monthly scorecard — {company} — {period}", "", "| KPI | Actual | Budget | Variance | Prior month | Materiality | Favorability |", "|---|---:|---:|---:|---:|---|---|"]
    for item in results:
        budget = item["comparisons"]["budget"]
        prior = item["comparisons"]["prior_month"]
        if budget is None:
            bval, variance_text, mat, fav = "n/a", "n/a", "not_assessable", "not_assessable"
        else:
            bval = display(budget["comparison"], item["unit"])
            if item["unit"] == "%":
                variance_text = f"{float(budget['percentage_point_difference']):+.1f}pp / {float(budget['basis_point_difference']):+.0f}bps"
            else:
                pct = budget["percentage_variance"]
                pct_text = "not meaningful" if pct == "not_meaningful" else f"{float(pct):+.1f}%"
                variance_text = f"{float(budget['absolute_variance']):+.1f} ({pct_text})"
            mat, fav = budget["materiality"], budget["favorability"]
        prior_text = "n/a" if prior is None else f"{display(prior['comparison'], item['unit'])}; Δ {float(prior['absolute_variance']):+.1f}"
        lines.append(f"| {item['kpi']} | {display(item['actual'], item['unit'])} | {bval} | {variance_text} | {prior_text} | {mat} | {fav} |")
    lines.extend(["", "## Data-quality warnings", ""])
    lines.extend([f"- {warning}" for warning in warnings] or ["- None."])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv")
    parser.add_argument("--period", required=True)
    parser.add_argument("--output-json")
    parser.add_argument("--output-markdown")
    args = parser.parse_args()
    rows, errors, warnings = validate(args.input_csv)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    results = calculate(rows, args.period)
    if not results:
        print(f"ERROR: no rows found for period {args.period}", file=sys.stderr)
        return 1
    company = results and next(r["company"] for r in rows if r["period"] == args.period)
    payload = {"synthetic": all(r["synthetic"].lower() == "true" for r in rows), "company": company, "period": args.period, "validation_warnings": warnings, "results": results}
    rendered = json.dumps(convert(payload), indent=2)
    if args.output_json:
        Path(args.output_json).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    if args.output_markdown:
        Path(args.output_markdown).write_text(markdown(company, args.period, results, warnings), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
