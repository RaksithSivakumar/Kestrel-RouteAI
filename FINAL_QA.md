# Final QA

Recorded after running the commands below on this machine (25 Sep 2026). Values are from `artifacts/metrics.json` and those command outputs, not invented.

## Final model

**tfidf_word_svc** — word TF-IDF (1–2 grams) + LinearSVC. Canonical labels: Installations → Installs & Demo, Consumables → Filters & Consumables.

Structured/keyword/character extras were trained and **not** selected: they did not beat word TF-IDF + LinearSVC on the same holdout.

## Validation

| Protocol | Rows | Accuracy | Macro F1 | Weighted F1 | Errors |
| --- | ---: | ---: | ---: | ---: | ---: |
| Stratified 80/20 holdout, seed 42 | 2,165 (train partition 8,657) | 0.9575 | 0.9570 | 0.9575 | 92 |
| 5-fold CV on the 8,657 | — | mean 0.9574 (std 0.0071) | — | — | — |
| Chronological: < 2026-04-01 train / Apr–Jun 2026 val | 2,135 val (8,687 train) | 0.9508 | 0.9493 | 0.9508 | 105 |

Full labelled rows: **10,822**. Error rate holdout **4.25%**.

## 90% target

**Achieved** on holdout, CV mean, and chronological validation. Hidden labels were not available.

## Hidden-test range

Based on holdout 95.75%, CV mean 95.74% (std 0.71%), chronological 95.08%, and similar product/channel mix on Jul–Sep 2026 CRM rows: estimate **approximately 93–96%** accuracy, point estimate near **95%**. Not a measured hidden score.

## Hardest classes / errors

Holdout F1 lowest: Filters & Consumables (0.937). Largest confusion: Repairs ↔ Filters & Consumables. Other types: payment language on non-billing jobs; warranty vs advice; vague callbacks; product vs text mismatch. Historical “purifier not working” is often labelled consumables (202 of 238), so a leak + “not working” ticket can follow that pattern.

## Cost

Current bot ₹3,20,000/year. Local model/API ₹0/prediction; ₹0/month at 700 requests for inference. Potential licence saving ₹3,20,000/year. Hosting not measured.

## Tests actually run

- `python scripts/validate_submission.py` → **VALID**
- `python -m pytest -q` → **17 passed**
- `cd frontend && npm test` → **7 passed** (3 files)

## API / frontend

Exercised on this machine:

- `GET http://127.0.0.1:8000/health` → `200 {"status":"ok","model_loaded":true}`
- `POST /predict` blank-display air fryer → `200` team **Repairs**, score_type `softmax_of_decision_function`
- empty `request_text` → `422`
- Next.js desk loaded at `http://localhost:3000` (form + empty-state result pane). Full click-through of the form in the automation browser was not completed (form fill blocked); API contract was verified with httpx and frontend unit tests.

## predictions.csv

2,178 rows; columns `request_id,team`; ids match sample/test; teams restricted to the seven current names.

## Git privacy

`.gitignore` excludes client extracts, `.venv`, `node_modules`, `.env`, `.next`. Staged-file checks are required before each commit.

## Known limitations

- Target is the vendor bot, not `final_team` (~23% transferred).
- 90% label match ≠ production transfer reduction.
- Scores are softmax of decision function, not calibrated probabilities.

## Decision

Shadow deploy; do not switch the vendor bot off on validation alone.
