# Error analysis

Holdout incorrect predictions: 92 of 2165 (4.25%).

Examples below are paraphrased patterns, not full customer messages.

## Most common true → predicted confusions

| True team | Predicted team | Count |
| --- | --- | ---: |
| Repairs | Filters & Consumables | 16 |
| Repairs | Billing | 7 |
| Product Advice | Billing | 5 |
| Billing | Repairs | 4 |
| Repairs | Warranty Claims | 4 |
| Filters & Consumables | Repairs | 4 |
| Filters & Consumables | Returns & Replacement | 4 |
| Product Advice | Installs & Demo | 3 |
| Warranty Claims | Product Advice | 3 |
| Returns & Replacement | Repairs | 3 |
| Filters & Consumables | Product Advice | 3 |
| Repairs | Product Advice | 3 |
| Installs & Demo | Repairs | 3 |
| Returns & Replacement | Billing | 2 |
| Product Advice | Returns & Replacement | 2 |

## Error categories (manual review of confusion pairs and text)

- **Payment mentioned on a non-billing job.** Historical labels often put “I already paid” into Billing even when the issue is install/repair (matches Meenal’s note and policy §3).
- **Consumable vs repair on purifiers.** Filter language and leak/not-working language overlap; historical routing is inconsistent.
- **Warranty vs billing vs advice.** Coverage questions that also mention payment or Shield.
- **Vague callbacks.** “Please call me about my purifier” has weak routing signal; labels spread across teams.
- **Product-family vs text mismatch.** Some rows name a different appliance in free text than in `product_family`.
- **Team rename is not an error class.** Old/new queue names were canonicalised before training.

These errors are a mix of genuine ambiguity and noisy historical bot labels. The supervised target remains `team_label`, not `final_team`.

