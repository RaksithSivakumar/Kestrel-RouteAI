# Validation report

Selected model: **tfidf_word_svc**

## Holdout

- Split: stratified 80/20, `random_state=42`
- Validation rows: 2165
- Accuracy: 0.9575
- Macro F1: 0.9570
- Weighted F1: 0.9575
- Error rate: 0.0425
- Incorrect predictions: 92

## Cross-validation (5-fold stratified, training partition only)

- Mean accuracy: 0.9574
- Std accuracy: 0.0071
- Folds: 0.9550, 0.9538, 0.9613, 0.9480, 0.9688

## Chronological validation

- Train: requests with `created_at_ist` < 2026-04-01
- Validate: 2026-04-01 to 2026-06-30 (last three labelled months)
- Validation rows: 2135
- Accuracy: 0.9508
- Macro F1: 0.9493
- Weighted F1: 0.9508
- Error rate: 0.0492
- Incorrect predictions: 105

## Per-team holdout metrics

| Team | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Billing | 0.9499 | 0.9728 | 0.9612 | 331 |
| Filters & Consumables | 0.9293 | 0.9452 | 0.9372 | 292 |
| Installs & Demo | 0.9620 | 0.9620 | 0.9620 | 237 |
| Product Advice | 0.9454 | 0.9534 | 0.9494 | 236 |
| Repairs | 0.9770 | 0.9489 | 0.9627 | 626 |
| Returns & Replacement | 0.9538 | 0.9660 | 0.9598 | 235 |
| Warranty Claims | 0.9663 | 0.9663 | 0.9663 | 208 |

Confusion matrix image: `reports/confusion_matrix.png`

Per-class CSV: `reports/per_class_metrics.csv`

