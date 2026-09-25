"""FastAPI contract tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import CURRENT_TEAMS, MODEL_PATH  # noqa: E402


@pytest.fixture(scope="module")
def client():
    from api.main import app

    return TestClient(app)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "model_loaded" in body


@pytest.mark.skipif(not MODEL_PATH.exists(), reason="Production model artifact required")
def test_predict_valid(client):
    response = client.post(
        "/predict",
        json={
            "request_id": "SR510822",
            "request_text": "display of air fryer gone blank pls call back",
            "product_family": "Air Fryer",
            "warranty_status": "in_warranty",
            "channel": "chat",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["request_id"] == "SR510822"
    assert body["predicted_team"] in CURRENT_TEAMS
    assert isinstance(body["reasons"], list)
    assert "confidence_score" in body
    assert body["score_type"]


def test_predict_empty_text(client):
    response = client.post(
        "/predict",
        json={"request_id": "SRX", "request_text": "   "},
    )
    assert response.status_code == 422


def test_predict_malformed_channel(client):
    response = client.post(
        "/predict",
        json={
            "request_id": "SRX",
            "request_text": "need help with mixer",
            "channel": "carrier-pigeon",
        },
    )
    assert response.status_code == 422


def test_predict_missing_text(client):
    response = client.post("/predict", json={"request_id": "SRX"})
    assert response.status_code == 422
