"""Validate predictions.csv against sample_submission.csv and the seven current teams."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import CURRENT_TEAMS, PREDICTIONS_PATH, SAMPLE_SUBMISSION_PATH, TEST_PATH  # noqa: E402


def validate(pred_path=None, sample_path=None, test_path=None) -> list[str]:
    pred_path = Path(pred_path or PREDICTIONS_PATH)
    sample_path = Path(sample_path or SAMPLE_SUBMISSION_PATH)
    test_path = Path(test_path or TEST_PATH)
    errors: list[str] = []
    if not pred_path.exists():
        return [f"Missing {pred_path}"]
    pred = pd.read_csv(pred_path)
    if list(pred.columns) != ["request_id", "team"]:
        errors.append(f"Expected columns [request_id, team], got {list(pred.columns)}")
    if pred["request_id"].duplicated().any():
        errors.append("Duplicate request_id in predictions")
    if pred["team"].isna().any():
        errors.append("Missing team values")
    bad_teams = sorted(set(pred["team"].dropna()) - set(CURRENT_TEAMS))
    if bad_teams:
        errors.append(f"Invalid team names: {bad_teams}")

    expected_ids = None
    if sample_path.exists():
        sample = pd.read_csv(sample_path)
        expected_ids = sample["request_id"].tolist()
    elif test_path.exists():
        expected_ids = pd.read_csv(test_path)["request_id"].tolist()
    if expected_ids is not None:
        if len(pred) != len(expected_ids):
            errors.append(f"Row count {len(pred)} != expected {len(expected_ids)}")
        if set(pred["request_id"]) != set(expected_ids):
            errors.append("request_id set does not match sample/test ids")
        if expected_ids and pred["request_id"].tolist() != expected_ids:
            errors.append("request_id order does not match sample/test file")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        print("INVALID")
        for err in errors:
            print("-", err)
        raise SystemExit(1)
    print("VALID: predictions.csv matches expected ids, count, columns, and team names.")


if __name__ == "__main__":
    main()
