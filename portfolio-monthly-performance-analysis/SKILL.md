---
name: portfolio-monthly-performance-analysis
description: Analyze monthly portfolio-company performance, produce reconciled commentary and JSON, then present the result with the portfolio dashboard workflow. Use for local CSV-based monthly reviews; do not use for investment recommendations or live-system integrations.
---

# Portfolio Monthly Performance Analysis

Produce concise, management-ready analysis from supplied local data. Clearly label synthetic inputs and outputs as synthetic. Never alter source data, invent drivers, recommend an investment, or distribute the report.

## Workflow

1. Read [references/input-schema.md](references/input-schema.md), then validate with `python3 scripts/validate_input.py INPUT.csv`. Stop on errors and preserve warnings.
2. Read [references/calculation-rules.md](references/calculation-rules.md) and [references/materiality-rules.md](references/materiality-rules.md), then run `python3 scripts/calculate_variances.py INPUT.csv --period YYYY-MM --output-json RESULTS.json --output-markdown SCORECARD.md`. Treat its output as the numerical source of truth. Read [references/results-contract.md](references/results-contract.md) when another skill, dashboard, or tool will consume the JSON.
3. Read [references/evidence-rules.md](references/evidence-rules.md). Link a driver only when supported and tag assertions with the defined evidence class.
4. Read [references/commentary-guidelines.md](references/commentary-guidelines.md), interpret material results in business context, and draft the required sections.
5. Reconcile every displayed number to RESULTS.json. Report `PASS` only when figures match and every material assertion is classified; otherwise report `FAIL` and mismatches.
6. After writing `RESULTS.json`, immediately invoke `$portfolio-performance-dashboard` with the exact absolute path to that file. Load and follow the dashboard skill's own `SKILL.md`; do not imitate or duplicate its presentation workflow inside this skill. Complete the dashboard workflow before giving the user the final response. This handoff is mandatory for every analysis outcome and does not require a second user request.

When validation fails or the requested period has no rows, preserve the generated blocked or empty `RESULTS.json`; do not attempt commentary. Still invoke `$portfolio-performance-dashboard` with that file so it renders the corresponding validation or empty state instead of a normal dashboard. When reconciliation fails, hand off the failed result so the dashboard shows its blocking mismatch state without unverified KPI cards.

If the companion dashboard skill is unavailable, complete the analysis, report the results state, and say that interactive presentation could not be loaded. Do not recreate dashboard calculations or silently omit the handoff.

## Required output

Include an executive summary of roughly two to four sentences; KPI scorecard; What changed and why; key risks and opportunities; questions for management; supported follow-up actions; data-quality and evidence warnings; calculation reconciliation result; and the interactive dashboard state produced from the same `RESULTS.json`.

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
