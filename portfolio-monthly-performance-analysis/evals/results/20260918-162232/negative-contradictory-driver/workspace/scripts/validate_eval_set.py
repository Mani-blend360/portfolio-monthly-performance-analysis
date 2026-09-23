#!/usr/bin/env python3
"""Validate the portable JSONL behavioral evaluation set."""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REQUIRED = {"id", "polarity", "category", "prompt", "fixtures", "expected", "prohibited", "grading"}


def validate_eval_set(path):
    path = Path(path).resolve()
    skill_root = path.parent.parent
    errors = []
    cases = []
    ids = set()

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [], [f"cannot read eval set: {exc}"]

    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
            continue
        missing = REQUIRED - set(case)
        if missing:
            errors.append(f"line {line_number}: missing fields: {', '.join(sorted(missing))}")
            continue
        if case["id"] in ids:
            errors.append(f"line {line_number}: duplicate id '{case['id']}'")
        ids.add(case["id"])
        if case["polarity"] not in {"positive", "negative"}:
            errors.append(f"line {line_number}: polarity must be positive or negative")
        if not isinstance(case["prompt"], str) or not case["prompt"].strip():
            errors.append(f"line {line_number}: prompt must be a non-empty string")
        for field in ("fixtures", "expected", "prohibited"):
            if not isinstance(case[field], list) or not case[field]:
                errors.append(f"line {line_number}: {field} must be a non-empty list")
        if case["grading"].get("mode") not in {"deterministic", "reviewer"}:
            errors.append(f"line {line_number}: grading.mode must be deterministic or reviewer")
        for fixture in case["fixtures"]:
            if not (skill_root / fixture).is_file():
                errors.append(f"line {line_number}: fixture does not exist: {fixture}")
        cases.append(case)

    polarities = Counter(case["polarity"] for case in cases)
    if len(cases) != 10:
        errors.append(f"expected exactly 10 cases, found {len(cases)}")
    if polarities["positive"] != 5 or polarities["negative"] != 5:
        errors.append(
            "expected 5 positive and 5 negative cases, found "
            f"positive={polarities['positive']}, negative={polarities['negative']}"
        )
    return cases, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("eval_jsonl")
    args = parser.parse_args()
    cases, errors = validate_eval_set(args.eval_jsonl)
    if errors:
        print(f"Eval validation: FAIL ({len(cases)} parsed cases)")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    modes = Counter(case["grading"]["mode"] for case in cases)
    polarities = Counter(case["polarity"] for case in cases)
    categories = Counter(case["category"] for case in cases)
    print(f"Eval validation: PASS ({len(cases)} cases)")
    print("Polarity: " + ", ".join(f"{key}={value}" for key, value in sorted(polarities.items())))
    print("Modes: " + ", ".join(f"{key}={value}" for key, value in sorted(modes.items())))
    print("Categories: " + ", ".join(f"{key}={value}" for key, value in sorted(categories.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
