"""Schema and feature validation tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import CURRENT_TEAMS, PREDICTIONS_PATH, SAMPLE_SUBMISSION_PATH, TEST_PATH, TRAIN_PATH
from src.data import load_test, load_train
from src.features import prepare_frame
from scripts.validate_submission import validate


def test_missing_fields_still_prepare():
    frame = prepare_frame(pd.DataFrame([{"request_text": "hello"}]))
    assert frame.loc[0, "text_combined"]
    assert frame.loc[0, "channel"] == ""


def test_empty_request_normalizes_to_blank_keywords():
    frame = prepare_frame(pd.DataFrame([{"request_text": ""}]))
    assert int(frame[[c for c in frame.columns if c.startswith("kw_")]].sum(axis=1).iloc[0]) == 0


@pytest.mark.skipif(not TRAIN_PATH.exists(), reason="Local client train.csv not present")
def test_train_schema_and_canonical_labels():
    df = load_train()
    assert "team_canonical" in df.columns
    assert set(df["team_canonical"].unique()) <= set(CURRENT_TEAMS)


@pytest.mark.skipif(not TEST_PATH.exists(), reason="Local client test file not present")
def test_test_has_no_label():
    df = load_test()
    assert "team_label" not in df.columns


@pytest.mark.skipif(not PREDICTIONS_PATH.exists(), reason="Generate predictions.csv first")
def test_predictions_file_valid():
    errors = validate()
    assert errors == [], errors
