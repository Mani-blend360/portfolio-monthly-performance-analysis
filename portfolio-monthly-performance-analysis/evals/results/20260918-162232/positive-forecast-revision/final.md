# Synthetic August 2026 full-year forecast revision

*Northstar Components — all inputs and outputs are fictional and synthetic.*

## Executive summary

The August full-year revenue forecast was reduced to **USD 690.0m**, **USD 30.0m (4.2%) below** the original investment case. EBITDA was reduced more sharply to **USD 102.0m**, **USD 13.0m (11.3%) below** the investment case. The EBITDA revision is material under the configured 5% threshold; no forecast-specific bridge was supplied.

## KPI scorecard

| KPI | Original investment case | August FY forecast | Revision | Assessment |
|---|---:|---:|---:|---|
| Revenue | USD 720.0m | USD 690.0m | USD -30.0m (-4.2%) | Non-material; unfavorable |
| EBITDA | USD 115.0m | USD 102.0m | USD -13.0m (-11.3%) | Material; unfavorable |

## What changed and why

- `[calculated_fact]` Revenue expectations decreased by USD 30.0m, or 4.2%, versus the original investment case.
- `[calculated_fact]` EBITDA expectations decreased by USD 13.0m, or 11.3%, a proportionally larger downgrade than revenue.
- `[missing_evidence]` The supplied commentary discusses August monthly performance but does not provide a specific bridge for the full-year revisions. **Driver not provided; management input required.**
- `[contradictory_evidence]` The revenue commentary states that price increases lifted revenue above budget, but August actual revenue was USD 57.0m versus USD 60.0m budget. This does not explain the full-year downgrade and requires clarification.
- `[source_supported]` August management accounts attribute the monthly EBITDA pressure to lower revenue and plant under-absorption, but the dataset does not quantify their contribution to the USD 13.0m full-year revision.

## Key risks and opportunities

- **Risk:** The EBITDA forecast declined faster than revenue, indicating weaker expected earnings conversion; the forecast bridge is not evidenced.
- **Opportunity:** Management’s supplied shipment-recovery and line-scheduling actions could support delivery, although no quantified forecast benefit was provided.

## Questions for management

1. Please provide revenue and EBITDA bridges from the original investment case to the August full-year forecast.
2. How much of the EBITDA reduction relates to revenue, mix, pricing, plant under-absorption, or other costs?
3. Please reconcile the claim that pricing lifted revenue above budget with August’s USD 3.0m revenue shortfall.
4. What quantified forecast benefit is expected from shipment recovery and improved line scheduling?

## Supported follow-up actions

- COO: recover delayed shipments by **2026-09-30**.
- Operations VP: improve line scheduling by **2026-10-15**.

## Data-quality and evidence warnings

- Revenue commentary conflicts with the actual-versus-budget result.
- No forecast-specific driver or quantified bridge was supplied.
- Input validation also identified inconsistent Production volume units (`count` versus `units`), although this does not affect the revenue or EBITDA forecast calculations.

## Calculation reconciliation

**PASS.** Revenue and EBITDA revisions reconcile to `RESULTS.json`; percentage calculations, direction rules, and the inclusive 5% materiality threshold were checked. All material assertions are evidence-classified.