"""Load and prepare labelled / unlabelled request tables."""

from __future__ import annotations

import pandas as pd

from src.config import LABEL_CANONICAL, TARGET_COLUMN, TEST_PATH, TRAIN_PATH


def canonicalize_label(label: str) -> str:
    return LABEL_CANONICAL.get(str(label), str(label))


def load_train(path=None) -> pd.DataFrame:
    df = pd.read_csv(path or TRAIN_PATH)
    required = {
        "request_id",
        "created_at_ist",
        "channel",
        "product_family",
        "warranty_status",
        "request_text",
        "source",
        "team_label",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"train.csv missing columns: {sorted(missing)}")
    df = df.copy()
    df[TARGET_COLUMN] = df["team_label"].map(canonicalize_label)
    return df


def load_test(path=None) -> pd.DataFrame:
    df = pd.read_csv(path or TEST_PATH)
    required = {
        "request_id",
        "created_at_ist",
        "channel",
        "product_family",
        "warranty_status",
        "request_text",
        "source",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"test_unlabelled.csv missing columns: {sorted(missing)}")
    return df.copy()
