"""Model, validation, and API tests for Kestrel RouteAI."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import CURRENT_TEAMS, MODEL_PATH, TARGET_COLUMN
from src.data import canonicalize_label
from src.features import normalize_text, prepare_frame
from src.model import build_pipeline, evaluate
from src.predictor import RoutingPredictor
from scripts.validate_submission import validate


def test_canonicalize_rename():
    assert canonicalize_label("Installations") == "Installs & Demo"
    assert canonicalize_label("Consumables") == "Filters & Consumables"
    assert canonicalize_label("Repairs") == "Repairs"


def test_normalize_text_strips_mojibake():
    cleaned = normalize_text("urgént: claim status â€¦")
    assert "urgent" in cleaned
    assert "claim" in cleaned


def test_prepare_frame_keyword_flags():
    df = prepare_frame(
        pd.DataFrame(
            [
                {
                    "request_text": "want AMC filter kit for purifier",
                    "product_family": "Water Purifier",
                    "warranty_status": "shield",
                    "channel": "chat",
                    "source": "crm",
                }
            ]
        )
    )
    assert df.loc[0, "kw_consumable"] == 1
    assert "product water purifier" in df.loc[0, "text_combined"]


def test_tiny_model_predicts_valid_team():
    texts = [
        "motor burnt smell not working",
        "gst invoice refund not issued",
        "wall mounting installation pending",
        "spare jar and filter kit",
        "how to clean robot vacuum",
        "wrong model delivered missing parts",
        "is mixer covered under shield claim status",
    ]
    labels = [
        "Repairs",
        "Billing",
        "Installs & Demo",
        "Filters & Consumables",
        "Product Advice",
        "Returns & Replacement",
        "Warranty Claims",
    ]
    # Repeat so the vectorizer has enough rows.
    df = pd.DataFrame(
        {
            "request_text": texts * 8,
            "product_family": ["Air Fryer"] * 56,
            "warranty_status": ["in_warranty"] * 56,
            "channel": ["chat"] * 56,
            "source": ["crm"] * 56,
        }
    )
    y = pd.Series(labels * 8)
    frame = prepare_frame(df)
    pipe = build_pipeline("word_svc")
    pipe.fit(frame, y)
    pred = pipe.predict(prepare_frame(df.iloc[:7]))
    assert all(p in CURRENT_TEAMS for p in pred)
    metrics = evaluate(y.iloc[:7], pred)
    assert "accuracy" in metrics


@pytest.mark.skipif(not MODEL_PATH.exists(), reason="Train the production model first")
def test_production_model_loads_and_routes():
    predictor = RoutingPredictor()
    assert predictor.loaded
    result = predictor.predict_one(
        {
            "request_id": "SRTEST1",
            "request_text": "water purifier leaking water from bottom not working",
            "product_family": "Water Purifier",
            "warranty_status": "in_warranty",
            "channel": "ivr",
        }
    )
    assert result["predicted_team"] in CURRENT_TEAMS
    assert result["request_id"] == "SRTEST1"
    assert isinstance(result["reasons"], list) and result["reasons"]
    assert "confidence_score" in result


def test_validate_predictions_schema(tmp_path):
    sample = pd.DataFrame({"request_id": ["SR1", "SR2"], "team": ["Repairs", "Repairs"]})
    pred = pd.DataFrame({"request_id": ["SR1", "SR2"], "team": ["Billing", "Repairs"]})
    sample_path = tmp_path / "sample.csv"
    pred_path = tmp_path / "pred.csv"
    sample.to_csv(sample_path, index=False)
    pred.to_csv(pred_path, index=False)
    errors = validate(pred_path, sample_path, tmp_path / "missing.csv")
    assert errors == []


def test_validate_rejects_bad_team(tmp_path):
    sample = pd.DataFrame({"request_id": ["SR1"], "team": ["Repairs"]})
    pred = pd.DataFrame({"request_id": ["SR1"], "team": ["Unknown Queue"]})
    sample.to_csv(tmp_path / "sample.csv", index=False)
    pred.to_csv(tmp_path / "pred.csv", index=False)
    errors = validate(tmp_path / "pred.csv", tmp_path / "sample.csv")
    assert any("Invalid team" in e for e in errors)
