# Test results

Tested locally with Python standard library only.

- Synthetic CSV validation: PASS, 90 rows; two deliberate warnings detected (revenue driver contradiction and production-volume unit inconsistency).
- Unit tests: PASS, 10 tests.
- Covered percentage and absolute variances, 120 bps margin difference, zero-budget handling, inclusive threshold equality, favorable-direction rules, non-material suppression signal, missing and contradictory evidence, forecast revision, invalid numeric input, duplicate rows, and CLI output completeness.
- Sample output completeness and key-figure reconciliation: PASS.
- Behavioral eval set: PASS, exactly 10 cases (5 positive and 5 negative; 6 deterministic and 4 reviewer-graded) across calculations, evidence, validation, forecast, and scope boundaries.
- Official `quick_validate.py`: PASS (`Skill is valid!`).

Command used:

```bash
python3 -m unittest discover -s tests -v
```
