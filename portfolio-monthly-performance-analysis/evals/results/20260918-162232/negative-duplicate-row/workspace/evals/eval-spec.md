# Evaluation specification

This test set evaluates the behavior of `portfolio-monthly-performance-analysis`; it does not call external systems or require an API key.

Each JSONL case contains:

- `id`: stable unique identifier.
- `polarity`: `positive` for a valid success path or `negative` for invalid, contradictory, unsupported, or out-of-scope behavior.
- `category`: behavioral area under test.
- `prompt`: realistic user request presented with the skill enabled.
- `fixtures`: paths relative to the skill directory.
- `expected`: observable requirements that should be satisfied.
- `prohibited`: failures that must not appear.
- `grading`: deterministic or reviewer guidance.

## Running the set

First validate the eval definition:

```bash
python3 scripts/validate_eval_set.py evals/cases.jsonl
```

Run all cases and collect traces and responses in one timestamped folder:

```bash
python3 scripts/run_eval_cases.py
```

Use `--dry-run` to prepare the folder without consuming a Codex run, or `--case CASE_ID` to run selected cases. Each case receives an isolated workspace. Results are stored below `evals/results/YYYYMMDD-HHMMSS/`, including `summary.json`, `summary.md`, and per-case `trace.jsonl`, `final.md`, `stderr.log`, `prompt.txt`, and `case.json` files.

For behavioral evaluation, run each prompt in a clean temporary task with the skill enabled and make the listed fixtures available at their relative paths. Grade every `expected` and `prohibited` item. A case passes only when all required behaviors are present and no prohibited behavior occurs.

Cases marked `deterministic` can be checked directly against calculation JSON or process exit status. Cases marked `reviewer` require semantic review because equivalent professional wording is acceptable. Do not grade exact prose except for the required missing-driver sentence.

## Aggregate acceptance criteria

- The set contains exactly 10 cases: 5 positive and 5 negative.
- All deterministic cases pass.
- No case invents a driver, divides by zero, changes source data, makes an investment recommendation, or presents synthetic information as real.
- At least 90% of reviewer criteria pass, with no critical failure in evidence classification or numerical reconciliation.
