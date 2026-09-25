# Model comparison

Target: canonical historical `team_label` (Installations → Installs & Demo, Consumables → Filters & Consumables).

Validation unless noted: stratified 80/20 holdout, `random_state=42`.

Test_unlabelled.csv was not used for training or tuning.

| Model | Accuracy | Macro F1 | Weighted F1 | Incorrect | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| majority | 0.2891 | 0.0641 | 0.1297 | 1539 | Always predict most common canonical team |
| keyword_rules | 0.7607 | 0.7498 | 0.7477 | 518 | Priority keyword rules; baseline only |
| tfidf_word_lr | 0.9404 | 0.9399 | 0.9405 | 129 | Word TF-IDF (1-2g) + Logistic Regression |
| tfidf_word_svc | 0.9575 | 0.9570 | 0.9575 | 92 | Word TF-IDF (1-2g) + LinearSVC |
| tfidf_word_char_svc | 0.9570 | 0.9553 | 0.9571 | 93 | Word + char TF-IDF + LinearSVC |
| word_char_struct_svc | 0.9533 | 0.9519 | 0.9534 | 101 | Word+char TF-IDF, product/channel/warranty, keyword flags + LinearSVC |
| word_char_struct_svc_balanced | 0.9510 | 0.9497 | 0.9511 | 106 | Same features with class_weight=balanced |

## Selection

**tfidf_word_svc** is the production model. It had the highest holdout accuracy and macro F1. Adding character n-grams, one-hot intake fields, keyword flags, or class weighting did not improve holdout accuracy. Keyword rules (76.1%) beat majority (28.9%) but are far behind linear text models.

A separate character-only LinearSVC was not kept after word+char already showed no gain over word unigrams/bigrams.

The selected model stays offline, fast, and easy to explain via n-gram overlap plus operator-facing reasons.

