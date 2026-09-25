# Kestrel RouteAI — Intelligent Service Request Routing System

## Overview

Kestrel RouteAI is an offline service-request router for Kestrel Home Appliances (Pune). It assigns an inbound request to one of seven operations queues using a local text classifier trained on eighteen months of historical bot labels.

## Business Problem

The vendor routing bot costs **₹3.2 lakh/year**. D2C operations asked for a replacement that matches those historical labels at **90%+** if that is realistically achievable, without a usage-priced AI bill.

## Solution

A scikit-learn pipeline (word TF-IDF + LinearSVC) served by FastAPI, with a small Next.js desk UI and human-readable reasons. Intake fields are shown to agents; they did not beat text-only TF-IDF on holdout so they are not in the selected estimator. No paid API key is required.

## Dataset

Local client files (not committed):

- `train.csv` — 10,822 labelled requests (Apr 2025–Jun 2026)
- `test_unlabelled.csv` — 2,178 requests (Jul–Sep 2026)
- `resolution_log.csv` — closure/transfer log for train ids only
- `teams.csv`, `ops-policy.pdf`, `email-thread.txt.txt`, `README.txt`

See `docs/data_audit.md`.

## Data Leakage Considerations

`first_team`, `final_team`, `transfers`, and `resolved_at` are excluded. `test_unlabelled.csv` is not used for training or tuning. Details: `docs/leakage_analysis.md`.

## Model

Canonical labels map `Installations` → `Installs & Demo` and `Consumables` → `Filters & Consumables` (policy §5).

**Selected model:** word TF-IDF (1–2 grams) + LinearSVC (`tfidf_word_svc`).

Measured validation (seed 42, stratified 80/20, n=2,165): accuracy **95.75%**, macro F1 **0.957**, error rate **4.25%** (92 errors). 5-fold CV mean accuracy **95.74%** (std 0.71%). Chronological Apr–Jun 2026: **95.08%**.

## Model Comparison

See `docs/model_comparison.md` (filled by the training script with actual scores).

## Validation

Stratified 80/20 holdout (seed 42), 5-fold CV on the training partition, and a chronological split (before vs from 2026-04-01). Reports: `reports/validation_report.md`.

## Error Analysis

See `reports/error_analysis.md`.

## Architecture

`Next.js desk (localhost:3000)` → `POST /predict` on FastAPI (`localhost:8000`) → local `artifacts/routing_model.joblib`.

## Project Structure

```
api/                FastAPI app
src/                data, features, model, predictor, explanations
scripts/            train, predict, validate_submission
tests/              pytest
frontend/           Next.js App Router desk
artifacts/          trained model + metrics.json
reports/            validation and errors
docs/               audit, leakage, cost, AI usage
```

## Requirements

- Python 3.11+
- Node.js 18+ (frontend)

## Installation

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Place the client CSVs and policy files in the project root (they are gitignored).

```bat
cd frontend
copy .env.example .env.local
npm install
```

## Training

```bat
python scripts/train.py
```

## Running the FastAPI Backend

```bat
uvicorn api.main:app --reload --port 8000
```

## Running the Next.js Frontend

```bat
cd frontend
npm run dev
```

Open http://localhost:3000

## Running Tests

```bat
pytest
cd frontend
npm test
```

## Generating predictions.csv

```bat
python scripts/predict.py
```

## Submission validation

```bat
python scripts/validate_submission.py
```

## API Documentation

Interactive docs: http://localhost:8000/docs

### GET /health

```json
{ "status": "ok", "model_loaded": true }
```

### POST /predict

## Example Request

```json
{
  "request_id": "SR510822",
  "request_text": "display of air fryer gone blank pls call back",
  "product_family": "Air Fryer",
  "warranty_status": "in_warranty",
  "channel": "chat"
}
```

## Example Response

```json
{
  "request_id": "SR510822",
  "predicted_team": "Repairs",
  "confidence_score": 0.6312,
  "relative_confidence": 0.7461,
  "score_type": "softmax_of_decision_function",
  "reasons": [
    "The request mentions an error or display fault.",
    "The request is tagged to product family Air Fryer."
  ]
}
```

Scores are **relative** (softmax of LinearSVC decision function unless the selected model is logistic regression). They are not claimed as calibrated probabilities.

## Cost

Vendor bot: ₹3,20,000 / year. Local model/API: ₹0 per prediction. See `docs/cost_analysis.md`.

## Limitations

- Labels are the old bot, including documented misroutes.
- Matching 90% of historical labels is not the same as routing to the team that should close the ticket.
- Vague “please call me” texts remain hard.

## Privacy

Do not publish `train.csv`, `test_unlabelled.csv`, `resolution_log.csv`, `teams.csv`, `ops-policy.pdf`, or the email thread. `.gitignore` excludes them.

## Git Development History

See `docs/git_history.md`.
