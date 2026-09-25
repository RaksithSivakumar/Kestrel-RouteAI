# Submission form

## 1. What did you build, and what business decision does it support?

An offline classifier (TF-IDF + LinearSVC) plus FastAPI and a Next.js desk that routes a new Kestrel service request to one of seven queues. It supports the decision **whether the ₹3.2 lakh/year vendor bot can be replaced**, and how to do that without a usage-priced AI bill.

## 2. State the number and rupees.

Vendor bot: **₹3,20,000 / year**. Local model inference: **₹0 / prediction**. Potential software/API licence saving: **₹3,20,000 / year** (hosting not included).

## 3. What score do you expect predictions.csv to get on hidden outcomes?

Approximately **93–96% accuracy**, with a point estimate near **95%**. This is an estimate, not a measured hidden score.

## 4. Which metric and why?

**Accuracy**, because the client asked to match historical `team_label` at 90% or better.

## 5. How was the estimate made?

Stratified holdout accuracy 95.75% (n=2,165), 5-fold CV mean 95.74% (std 0.71%) on the training partition, chronological validation 95.08% on Apr–Jun 2026. Test requests are the following three months, all CRM, after the 15 Jan 2026 rename — closest to the chronological protocol. Range uses that protocol plus observed fold spread; no hidden labels were used.

## 6. How do you know it works?

Training and validation were run on `train.csv` only. `scripts/validate_submission.py` passed on `predictions.csv`. Pytest and frontend Vitest were run. FastAPI `/health` and `/predict` were exercised locally.

## 7. Validation split.

Stratified 80/20, `random_state=42`: 8,657 train / 2,165 validation from 10,822 labelled rows. Also 5-fold CV on the 8,657 and a chronological split (8,687 before 2026-04-01 / 2,135 after).

## 8. Error rate.

Holdout **4.25%** (92 / 2,165). Chronological **4.92%** (105 / 2,135).

## 9. Error types.

Repairs confused with Filters & Consumables; payment language on non-billing jobs; warranty vs advice; vague “please call back” texts; product-family vs free-text mismatch. See `reports/error_analysis.md`.

## 10. Did you change/narrow/push back on the client's ask?

Pushed back on **switching the bot off solely because validation ≥ 90%**. Recommended shadow deployment first. Did not retarget to `final_team` even though that is closer to “correct” ops routing.

## 11. What is wrong with the solution/data?

Historical labels include known misroutes (~23% later transferred). Duplicate texts with conflicting labels (89 texts). Legacy encoding noise. Product column sometimes disagrees with the message. Test has no labels so hidden accuracy is unknown.

## 12. What columns were not trusted?

`first_team`, `final_team`, `transfers`, `resolved_at` (post-routing). `request_id` (identifier). `source` (system cutover, not the issue). Time was not used as a feature.

## 13. What rows looked suspicious?

1,140 legacy rows with `resolved_at` before `created_at_ist` (UTC vs IST). Conflicting labels on identical text. Product/text mismatches. Billing labels on install/repair jobs that mention payment.

## 14. What did you deliberately leave out?

Resolution-log features; LLM/paid APIs; hard-coded policy override of historical labels; `final_team` as the training target.

## 15. Anything built/found that nobody asked for?

Chronological validation, transfer-rate vs bot-match distinction, and a small Next.js desk with reasons. Team rename canonicalisation was required to score current queue names.

## 16. What AI tools were used?

Cursor (this repository). See `docs/ai_usage.md`.

## 17. Which models/tools?

Cursor Grok 4.6 for coding assistance. Routing model: sklearn TF-IDF + LinearSVC. No paid inference API.

## 18. Where AI helped.

Scaffolding, documentation drafts, test stubs, structured project layout.

## 19. Where AI wasted time.

None material beyond a first training attempt on a broken system NumPy/Matplotlib combo, which was replaced by a project venv.

## 20. What was discarded.

LLM routing; class-weighted and extra structured/char features (they did not beat word TF-IDF + LinearSVC on holdout); training on `final_team`.

## 21. Google Drive link.

[TO BE FILLED]

## 22. Three things a person needs to know on Monday.

1. Shadow RouteAI; do not cut the vendor bot yet.  
2. Validation beat 90% on labels, but labels are the old bot, not “correct” ops.  
3. Inference cost is ₹0; keep it that way (no per-ticket LLM).

## 23. Honest hours spent.

[TO BE FILLED]

## 24. GitHub repository link.

[TO BE FILLED]

## 25. Cost per prediction.

**₹0** (local model; no paid API).

## 26. Monthly cost at 700 requests/month.

**₹0** model/API. Hosting not measured. Current bot monthly equivalent **₹26,666.67**.
