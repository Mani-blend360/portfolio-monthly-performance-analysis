# Interaction and Ask Codex contract

Keep filtering and selection local to the dashboard:

- KPI group: all, financial, or operational.
- Comparison: budget, prior month, prior year, current forecast, or investment case.
- Material-only toggle.
- Overview, Questions, and Actions tabs.
- KPI row selection updates one detail panel.

For an investigation action, call `window.openai.sendFollowUpMessage({ prompt, title })` when available. The prompt must include:

- Company and reporting period.
- Selected KPI, actual value, and selected comparison value.
- Absolute and percentage, pp, or bps variance exactly as supplied.
- Materiality and favorability.
- Evidence class, driver, evidence source, and current management question.
- A request to distinguish calculated facts from supported, missing, contradictory, or hypothetical evidence.
- A prohibition on inventing drivers, values, actions, owners, dates, or investment recommendations.

Label the action `Ask Codex to investigate <KPI>`. Provide separate collection-level actions only when useful, such as preparing a management agenda or reviewing action coverage. Never transmit raw CSV content when the reconciled KPI context is sufficient.
