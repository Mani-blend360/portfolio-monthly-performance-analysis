# August 2026 performance analysis

*All data and conclusions below are synthetic and relate to fictional Northstar Components.*

## Executive summary

August revenue was **USD 57.0m, USD 3.0m (5.0%) below the USD 60.0m budget**; the variance is material because it equals the 5.0% threshold. Management’s statement that price increases lifted revenue **above budget is contradicted by the data**. Average selling price was only USD 0.3 (0.6%) above budget and non-material, while production volume was 80 units (6.9%) below budget and material; a reconciled price-volume bridge is needed before any revenue benefit is attributed to pricing. `[calculated_fact; contradictory_evidence]`

## KPI scorecard

| KPI | Actual | Budget | Variance to budget | Materiality | Evidence class |
|---|---:|---:|---:|---|---|
| Revenue | USD 57.0m | USD 60.0m | USD (3.0)m / (5.0%) | Material | Contradictory evidence |
| Gross profit | USD 22.8m | USD 24.0m | USD (1.2)m / (5.0%) | Material | Source supported |
| Gross margin | 40.0% | 40.0% | 0.0pp / 0bps | Non-material | Calculated fact |
| EBITDA | USD 8.1m | USD 9.24m | USD (1.14)m / (12.3%) | Material | Source supported |
| EBITDA margin | 14.2% | 15.4% | (1.2)pp / (120)bps | Material | Source supported |
| Operating expenses | USD 14.7m | USD 15.0m | USD (0.3)m / (2.0%) | Non-material | Source supported |
| Capital expenditure | USD 5.5m | USD 5.0m | USD 0.5m / 10.0% | Material | Source supported |
| Operating cash flow | USD 5.6m | USD 6.5m | USD (0.9)m / (13.8%) | Material | Missing evidence |
| Net debt | USD 74.0m | USD 65.0m | USD 9.0m / 13.8% | Material | Missing evidence |
| Order intake | USD 70.0m | USD 62.0m | USD 8.0m / 12.9% | Material | Source supported |
| Backlog | USD 168.0m | USD 148.0m | USD 20.0m / 13.5% | Material | Source supported |
| Production volume | 1,080 | 1,160 | (80) / (6.9%) | Material | Source supported |
| Average selling price | USD 52.8 | USD 52.5 | USD 0.3 / 0.6% | Non-material | Source supported |
| Customer churn | 1.2% | 0.0% | 1.2pp / 120bps | Material | Missing evidence |
| Headcount | 501 | 500 | 1 / 0.2% | Non-material | Source supported |

`[calculated_fact]`

## What changed and why

- **Revenue:** USD 57.0m was USD 3.0m below budget, USD 1.0m below July, and USD 2.0m below current forecast. It remained USD 5.0m (9.6%) above prior year. Management’s “above budget” assertion is numerically false. `[calculated_fact; contradictory_evidence]`
- **Pricing and volume:** Average selling price exceeded budget by only 0.6%, versus production volume being 6.9% below budget. The maintenance log attributes lower output to unplanned downtime, but the supplied data do not provide a reconciled price-volume-mix revenue bridge. `[source_supported; missing_evidence]`
- **Profitability:** Gross profit was USD 1.2m (5.0%) below budget, attributed to mix and lower plant utilization. EBITDA was USD 1.14m (12.3%) below budget and EBITDA margin was 120bps below budget, with lower revenue and plant under-absorption cited as drivers. `[source_supported]`
- **Cash and leverage:** Operating cash flow missed budget by USD 0.9m, while net debt was USD 9.0m above budget. **Driver not provided; management input required.** `[missing_evidence]`
- **Commercial indicators:** Order intake was USD 8.0m above budget and backlog USD 20.0m above budget, supported by the CRM order report and two large customer awards. These indicators do not by themselves establish when backlog will convert to revenue. `[source_supported]`
- **Customer churn:** Churn was 1.2% against a zero budget, a material 120bps adverse variance; percentage variance against zero is **not meaningful**. **Driver not provided; management input required.** `[calculated_fact; missing_evidence]`
- **Full-year outlook:** Revenue’s full-year forecast is USD 690m, USD 30m (4.2%) below the original investment case of USD 720m. `[calculated_fact]`

## Key risks and opportunities

- **Risk:** Continued downtime and below-budget production volume may constrain revenue conversion and sustain under-absorption pressure. `[source_supported]`
- **Risk:** Weak operating cash flow and higher net debt are material but unexplained. `[missing_evidence]`
- **Risk:** The unsupported revenue narrative could obscure the underlying volume shortfall. `[contradictory_evidence]`
- **Opportunity:** Above-budget order intake and backlog provide potential future revenue coverage, subject to production capacity, shipment timing, and confirmed conversion schedules. `[source_supported; hypothesis]`
- **Opportunity:** Contracted price increases are evidenced, but their incremental revenue contribution has not been quantified. `[source_supported; missing_evidence]`

## Questions for management

1. Please correct or clarify the statement that revenue was “above budget,” given the USD 3.0m shortfall.
2. Provide a reconciled price-volume-mix and shipment-timing bridge from USD 60.0m budget revenue to USD 57.0m actual revenue.
3. Quantify how much incremental August revenue came from contracted price increases and reconcile this to the 0.6% average-selling-price variance.
4. Identify the causes of the operating-cash-flow shortfall and USD 9.0m net-debt overrun, including working-capital and capex bridges.
5. Explain the 120bps churn variance and identify affected customers or revenue exposure.
6. Provide the backlog conversion schedule and confirm whether production capacity can support the planned delivery dates.

## Supported follow-up actions

| Action | Owner | Due date |
|---|---|---|
| Recover delayed shipments | COO | 2026-09-30 |
| Improve line scheduling | Operations VP | 2026-10-15 |
| Complete safety-equipment installation | Plant Director | 2026-09-20 |
| Confirm production slots | Commercial Director | 2026-09-15 |
| Complete reliability work | Plant Director | 2026-09-30 |
| Monitor pricing realization | Commercial Director | 2026-09-30 |
| Complete priority hiring | HR Director | 2026-10-31 |

## Data-quality and evidence warnings

- Validation passed for all **90 source rows**.
- Row 77’s management driver conflicts with actual revenue versus budget.
- Production volume has inconsistent units across periods: `count` and `units`.
- A named “Management monthly commentary” source does not resolve the direct contradiction in the revenue assertion.
- No supported drivers were supplied for operating cash flow, net debt, or customer churn.

## Calculation reconciliation

**PASS** — all displayed figures reconcile to `RESULTS.json`; threshold equality was treated as material, the zero churn budget was not used as a percentage denominator, and every material driver assertion was evidence-classified.