*All inputs and analysis are synthetic.*

## Executive summary

Northstar Components’ August 2026 customer churn was **1.2%**, versus a **0.0% budget**, an unfavorable variance of **1.2 percentage points (120 bps)**. This exceeds the **50-bps materiality threshold**; percentage variance is **not meaningful** because the budget is zero. No supported explanation was supplied: **Driver not provided; management input required.** `[calculated_fact; missing_evidence]`

## KPI scorecard

| KPI | Actual | Budget | Variance to budget | Materiality | Favorability |
|---|---:|---:|---:|---|---|
| Customer churn | 1.2% | 0.0% | +1.2pp / +120bps; percentage variance not meaningful | Material | Unfavorable |

Additional context:

| Comparison | Baseline | Difference | Materiality |
|---|---:|---:|---|
| Prior month | 1.1% | +0.1pp / +10bps | Non-material |
| Prior year | 1.0% | +0.2pp / +20bps | Non-material |
| Current forecast | 1.0% | +0.2pp / +20bps | Non-material |
| Original investment case | 0.9% | +0.3pp / +30bps | Non-material |

All comparisons are mechanically unfavorable because lower churn is favorable. `[calculated_fact]`

## What changed and why

Churn increased from **1.1% in July to 1.2% in August**, a non-material deterioration of **10 bps**. It was also **20 bps above** both prior year and current forecast, and **30 bps above** the original investment case; each difference remains below the 50-bps threshold. `[calculated_fact]`

The budget variance is material solely on the configured basis-point test. No management driver or evidence source accompanies the churn result. **Driver not provided; management input required.** `[missing_evidence]`

## Key risks and opportunities

- **Risk:** August churn materially missed the zero budget, while also deteriorating against every other available comparator. `[calculated_fact]`
- **Risk:** The unexplained movement prevents assessment of whether churn is concentrated by customer, segment, product, or cause. `[missing_evidence]`
- **Opportunity:** None is supported by the supplied churn data or commentary.

## Questions for management

- Is the **0.0% August budget** intentional, and what operating assumptions support a zero-churn target?
- What caused August churn to rise to **1.2%**, and how much is attributable to specific customers, segments, products, or contract events?
- Is the increase expected to persist, and does it require an update to the current forecast?
- What retention action, owner, timing, and measurable churn impact should be recorded?

## Supported follow-up actions

No management action, owner, or completion date was supplied for customer churn. No unsupported action has been inferred.

## Data-quality and evidence warnings

- The source dataset passed validation: **90 rows, with two warnings**.
- Customer churn lacks both a management driver and evidence source despite its material budget variance.
- The zero budget makes percentage variance mathematically not meaningful; the valid comparison is **+1.2pp / +120bps**.
- The broader dataset contains a contradictory Revenue driver at source row 77 and inconsistent Production volume units (`count` and `units`). Neither warning changes the churn calculation.
- All underlying company information is explicitly synthetic.

## Calculation reconciliation

**PASS** — Every displayed churn figure reconciles to the calculation output, the zero-budget rule was applied without division by zero, the 50-bps threshold was applied correctly, and the material unexplained movement is classified as `missing_evidence`.