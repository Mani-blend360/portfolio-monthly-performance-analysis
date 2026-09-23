---
name: portfolio-monthly-performance-analysis
description: Analyze monthly financial and operational performance for a portfolio company against budget, prior periods, forecast, and investment case, producing evidence-tagged, reconciled monthly-pack commentary. Use for local CSV-based portfolio performance reviews; do not use for investment recommendations or live-system integrations.
---

# Portfolio Monthly Performance Analysis

Produce concise, management-ready analysis from supplied local data. Clearly label synthetic inputs and outputs as synthetic. Never alter source data, invent drivers, recommend an investment, or distribute the report.

## Workflow

1. Read [references/input-schema.md](references/input-schema.md), then validate with `python3 scripts/validate_input.py INPUT.csv`. Stop on errors and preserve warnings.
2. Read [references/calculation-rules.md](references/calculation-rules.md) and [references/materiality-rules.md](references/materiality-rules.md), then run `python3 scripts/calculate_variances.py INPUT.csv --period YYYY-MM --output-json RESULTS.json --output-markdown SCORECARD.md`. Treat its output as the numerical source of truth.
3. Read [references/evidence-rules.md](references/evidence-rules.md). Link a driver only when supported and tag assertions with the defined evidence class.
4. Read [references/commentary-guidelines.md](references/commentary-guidelines.md), interpret material results in business context, and draft the required sections.
5. Reconcile every displayed number to RESULTS.json. Report `PASS` only when figures match and every material assertion is classified; otherwise report `FAIL` and mismatches.

## Required output

Include an executive summary of roughly two to four sentences; KPI scorecard; What changed and why; key risks and opportunities; questions for management; supported follow-up actions; data-quality and evidence warnings; and calculation reconciliation result.

Be selective: emphasize material movements and important contradictions. Preserve business context when direction rules are only mechanical classifications.

## Hard boundaries

- Percentage variance against zero is `not meaningful`; never divide by zero.
- Percentage KPIs use percentage-point and basis-point differences for materiality.
- Equality with a threshold is material.
- A missing driver for a material movement must say: “Driver not provided; management input required.”
- If commentary conflicts with data, identify the contradiction and ask for clarification.
- Do not present hypotheses as facts, modify source financials, connect to external systems, send results, or make investment recommendations.

## Prototype example

Use [assets/synthetic_company_profile.md](assets/synthetic_company_profile.md) with [assets/synthetic_monthly_data.csv](assets/synthetic_monthly_data.csv). [assets/expected_analysis.md](assets/expected_analysis.md) demonstrates the expected August 2026 output; it is synthetic and illustrative.

For skill maintenance and behavioral testing, use [evals/eval-spec.md](evals/eval-spec.md) and `evals/cases.jsonl`. These resources are not required during ordinary analysis.
