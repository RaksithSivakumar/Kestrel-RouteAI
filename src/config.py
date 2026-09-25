"""Paths, labels, and reproducibility settings."""

from pathlib import Path

RANDOM_SEED = 42
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
REPORTS_DIR = PROJECT_ROOT / "reports"
DOCS_DIR = PROJECT_ROOT / "docs"

TRAIN_PATH = DATA_DIR / "train.csv"
TEST_PATH = DATA_DIR / "test_unlabelled.csv"
RESOLUTION_PATH = DATA_DIR / "resolution_log.csv"
SAMPLE_SUBMISSION_PATH = DATA_DIR / "sample_submission.csv"
PREDICTIONS_PATH = PROJECT_ROOT / "predictions.csv"
MODEL_PATH = ARTIFACTS_DIR / "routing_model.joblib"

# Historical names mapped to current queue names (policy §5: responsibilities unchanged).
LABEL_CANONICAL = {
    "Installations": "Installs & Demo",
    "Consumables": "Filters & Consumables",
}

CURRENT_TEAMS = [
    "Billing",
    "Filters & Consumables",
    "Installs & Demo",
    "Product Advice",
    "Repairs",
    "Returns & Replacement",
    "Warranty Claims",
]

RENAME_EFFECTIVE = "2026-01-15"

INTAKE_COLUMNS = [
    "request_id",
    "created_at_ist",
    "channel",
    "product_family",
    "warranty_status",
    "request_text",
    "source",
]

CATEGORICAL_FEATURES = ["channel", "product_family", "warranty_status"]
TEXT_FEATURE = "text_combined"
TARGET_COLUMN = "team_canonical"
