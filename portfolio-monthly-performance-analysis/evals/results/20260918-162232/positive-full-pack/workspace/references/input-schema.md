# Input schema

Use a long-form UTF-8 CSV with one row per `period` and `kpi`. Required columns are `company`, `synthetic`, `period`, `kpi`, `kpi_type`, `actual`, `budget`, `prior_month`, `prior_year`, `current_forecast`, `original_investment_case`, `current_full_year_forecast`, `original_investment_case_full_year`, `currency`, `unit`, `favorable_direction`, `materiality_type`, `materiality_threshold`, `management_driver`, `evidence_source`, `management_action`, `action_owner`, and `expected_completion_date`.

- Period is `YYYY-MM`; rows are unique by company, period, and KPI.
- `synthetic` is `true` or `false`; prototype assets use `true`.
- Numeric fields may be blank when unavailable. Actual and threshold are required numbers.
- KPI type is `financial` or `operational`.
- Direction is `higher_is_favorable`, `lower_is_favorable`, or `neutral`.
- Materiality type is `percent`, `absolute`, or `bps`; use `bps` for percentage KPIs.
- Unit remains consistent for a KPI across periods. Percentage units use `%`; prototype financial amounts use `USDm`.
- Currency may be blank for non-monetary KPIs. Monetary KPIs require currency.
- Dates use ISO `YYYY-MM-DD`.
- A management driver is supported only when an evidence source is populated.

Structural, enum, date, duplicate, and numeric failures are errors. Cross-period currency/unit changes, stale prior-month values, missing evidence, and directional driver conflicts are warnings so analysis can proceed while surfacing them.
