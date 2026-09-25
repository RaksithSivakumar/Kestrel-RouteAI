"""FastAPI service for Kestrel service-request routing."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.predictor import ModelNotLoadedError, RoutingPredictor  # noqa: E402

ALLOWED_CHANNELS = {"ivr", "chat", "whatsapp", "email", ""}
ALLOWED_WARRANTY = {"in_warranty", "shield", "out_of_warranty", ""}

predictor = RoutingPredictor()

app = FastAPI(
    title="Kestrel RouteAI",
    description="Offline service-request routing for Kestrel Home Appliances.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    request_id: Optional[str] = Field(default="UNKNOWN")
    request_text: str = Field(..., min_length=1)
    product_family: Optional[str] = ""
    warranty_status: Optional[str] = ""
    channel: Optional[str] = ""
    source: Optional[str] = "crm"
    created_at_ist: Optional[str] = ""

    @field_validator("request_text")
    @classmethod
    def text_not_blank(cls, value: str) -> str:
        if not str(value).strip():
            raise ValueError("request_text must not be empty")
        return value

    @field_validator("channel")
    @classmethod
    def channel_ok(cls, value: Optional[str]) -> str:
        value = value or ""
        if value and value not in ALLOWED_CHANNELS:
            raise ValueError("channel must be ivr, chat, whatsapp, or email")
        return value

    @field_validator("warranty_status")
    @classmethod
    def warranty_ok(cls, value: Optional[str]) -> str:
        value = value or ""
        if value and value not in ALLOWED_WARRANTY:
            raise ValueError("warranty_status must be in_warranty, shield, or out_of_warranty")
        return value


class PredictResponse(BaseModel):
    request_id: str
    predicted_team: str
    confidence_score: float
    relative_confidence: float
    score_type: str
    reasons: list[str]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", model_loaded=predictor.loaded)


@app.post("/predict", response_model=PredictResponse)
def predict(body: PredictRequest) -> PredictResponse:
    try:
        result = predictor.predict_one(body.model_dump())
    except ModelNotLoadedError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Could not score request: {exc}") from exc
    return PredictResponse(**result)
