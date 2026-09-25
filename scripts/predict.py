"""Train on full labelled data is handled in train.py; this writes predictions.csv."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import PREDICTIONS_PATH  # noqa: E402
from src.data import load_test  # noqa: E402
from src.predictor import RoutingPredictor  # noqa: E402


def main() -> None:
    predictor = RoutingPredictor()
    if not predictor.loaded:
        raise SystemExit("Model artifact missing. Run python scripts/train.py first.")
    test = load_test()
    out = predictor.predict_frame(test)
    submission = out[["request_id", "team"]]
    submission.to_csv(PREDICTIONS_PATH, index=False)
    print(f"Wrote {len(submission)} rows to {PREDICTIONS_PATH}")


if __name__ == "__main__":
    main()
