# Calculation rules

For each available baseline (`budget`, `prior_month`, `prior_year`, `current_forecast`, `original_investment_case`): absolute variance is `actual - comparison`; percentage variance is `(actual - comparison) / abs(comparison) * 100`; and a zero comparison produces `not_meaningful`. For `%` KPIs, percentage-point difference is `actual - comparison` and basis-point difference is `(actual - comparison) * 100`.

Round only for display and retain unrounded values in JSON. Do not compare monthly actual directly with a full-year value. Full-year forecast revision is current full-year forecast less original investment-case full-year expectation, with the same zero rule.

The explicit prior-month field is the source baseline; validation checks it against the preceding actual where available. Missing baselines remain unavailable rather than being inferred.
