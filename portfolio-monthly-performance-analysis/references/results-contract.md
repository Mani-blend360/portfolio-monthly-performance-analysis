# Reconciled results contract

`RESULTS.json` is the machine-readable handoff to presentation workflows. The current `schema_version` is `1.0`.

## Top-level fields

- `status`: `ready`, `warning`, `blocked`, or `empty`.
- `synthetic`: boolean for successful inputs; `null` when validation prevents determination.
- `company` and `period`: selected review context. Company may be `null` for blocked or empty output.
- `source`: input filename and source row count.
- `validation`: `status` (`PASS` or `FAIL`), `errors`, and `warnings`.
- `reconciliation`: `status` (`PASS`, `FAIL`, or `NOT_RUN`) and `mismatches`.
- `results`: KPI objects. An empty array is valid only for `blocked` or `empty` states.

## Presentation gate

- Render the full dashboard only when validation is `PASS`, reconciliation is `PASS`, and results are non-empty.
- A `warning` status may render normally but must keep warnings discoverable.
- A `blocked` status renders a validation-error state with actionable row or field messages.
- An `empty` status renders the requested period and available-data guidance, not a zero-valued dashboard.
- A reconciliation `FAIL` renders a blocking mismatch state and must not display unverified KPI summaries.

Missing comparisons remain `null` and display as unavailable. The consumer must not coerce missing, invalid, or not-meaningful values to zero.
