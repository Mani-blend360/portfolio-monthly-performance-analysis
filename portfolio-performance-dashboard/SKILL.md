---
name: portfolio-performance-dashboard
description: Present reconciled monthly portfolio-company results as a modern interactive dashboard in Codex chat. Use after portfolio performance analysis has produced RESULTS.json; do not calculate from raw CSVs or render unverified results.
---

# Portfolio Performance Dashboard

Turn reconciled portfolio-analysis JSON into a clean, responsive, interactive review inside Codex chat. This skill accepts the exact `RESULTS.json` path handed off by `$portfolio-monthly-performance-analysis` and is also directly invocable for an existing results file. Preserve source values and evidence classifications. Never recalculate financial results, invent missing values or drivers, or imply an investment recommendation.

## Workflow

1. Use the handed-off results path exactly; do not search for a different or newer JSON file. Read [references/dashboard-input-schema.md](references/dashboard-input-schema.md), then run `python3 scripts/validate_dashboard_input.py /absolute/path/to/RESULTS.json`. Treat any `blocked` result as a hard stop for the normal dashboard.
2. Read [references/ui-states.md](references/ui-states.md) and render the state returned by the validator: `ready`, `warning`, `blocked`, `empty`, or `reconciliation_failed`.
3. For `ready` or `warning`, use the available in-conversation visualization capability to produce a wide interactive dashboard. Use only values from the JSON.
4. Read [references/interaction-contract.md](references/interaction-contract.md) before adding “Ask Codex” actions.
5. Verify filters, KPI selection, tabs, narrow layout, keyboard access, missing-value display, and the primary Ask Codex action before presenting the result.

Return control to the calling analysis workflow only after the requested dashboard state has been rendered or a precise presentation failure has been reported.

For testing outside Codex, run `python3 scripts/render_dashboard.py RESULTS.json --output dashboard.html`. The standalone dashboard keeps all presentation interactions local and copies the structured investigation prompt to the clipboard because `window.openai.sendFollowUpMessage` is unavailable.

## Normal dashboard

Show a restrained company header; KPI group and comparison filters; material-only toggle; Overview, Questions, and Actions views; three decision-relevant headline KPIs; a selectable variance view; and one KPI detail panel. Keep validation warnings discoverable without overwhelming the first view.

Choose headline KPIs from material movements and important evidence exceptions. Do not invent a composite score, health rating, or ranking.

## Data boundaries

- Consume reconciled JSON, never the raw CSV.
- Display `null`, unavailable, and `not_meaningful` distinctly; never coerce them to zero.
- Preserve percentage, percentage-point, basis-point, currency, and unit semantics.
- Do not render headline KPI values when reconciliation is not `PASS`.
- Label synthetic data clearly.
- Keep evidence tags attached to commentary and management questions.
