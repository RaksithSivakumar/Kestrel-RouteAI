"""Load the saved routing model and return a single team with reasons."""

from __future__ import annotations

from typing import Any

import joblib
import numpy as np
import pandas as pd

from src.config import CURRENT_TEAMS, MODEL_PATH
from src.explanations import explain_prediction, relative_confidence
from src.features import prepare_frame
from src.model import scores_from_estimator


class ModelNotLoadedError(RuntimeError):
    pass


class RoutingPredictor:
    def __init__(self, model_path=None):
        self.model_path = model_path or MODEL_PATH
        self.bundle: dict[str, Any] | None = None
        self._load()

    def _load(self) -> None:
        if not self.model_path.exists():
            self.bundle = None
            return
        self.bundle = joblib.load(self.model_path)

    @property
    def loaded(self) -> bool:
        return self.bundle is not None

    def predict_one(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.loaded:
            raise ModelNotLoadedError(
                "Routing model artifact is missing. Run: python scripts/train.py"
            )
        request_id = str(payload.get("request_id") or "").strip() or "UNKNOWN"
        row = {
            "request_id": request_id,
            "created_at_ist": payload.get("created_at_ist") or "",
            "channel": payload.get("channel") or "",
            "product_family": payload.get("product_family") or "",
            "warranty_status": payload.get("warranty_status") or "",
            "request_text": payload.get("request_text") or "",
            "source": payload.get("source") or "crm",
        }
        frame = prepare_frame(pd.DataFrame([row]))
        pipeline = self.bundle["pipeline"]
        classes = list(self.bundle.get("classes") or CURRENT_TEAMS)
        pred = pipeline.predict(frame)[0]
        if pred not in CURRENT_TEAMS:
            pred = CURRENT_TEAMS[0]
        scores = scores_from_estimator(pipeline, frame)[0]
        # Align score vector to stored class order from the estimator.
        clf = pipeline.named_steps["clf"]
        model_classes = [str(c) for c in clf.classes_]
        score_map = {cls: float(scores[i]) for i, cls in enumerate(model_classes)}
        aligned = [score_map.get(cls, 0.0) for cls in classes]
        aligned_arr = np.array(aligned)
        conf = relative_confidence(aligned_arr)
        reasons = explain_prediction(
            predicted_team=str(pred),
            request_text=row["request_text"],
            product_family=row["product_family"],
            warranty_status=row["warranty_status"],
            scores=aligned_arr,
            class_names=classes,
        )
        return {
            "request_id": request_id,
            "predicted_team": str(pred),
            "confidence_score": round(float(max(aligned)), 4),
            "relative_confidence": round(float(conf), 4),
            "score_type": "softmax_of_decision_function",
            "reasons": reasons,
        }

    def predict_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.loaded:
            raise ModelNotLoadedError("Routing model artifact is missing.")
        frame = prepare_frame(df)
        pipeline = self.bundle["pipeline"]
        preds = pipeline.predict(frame)
        out = df.copy()
        out["team"] = preds
        return out
