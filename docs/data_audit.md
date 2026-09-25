# Data audit

This note records **measured** facts from the files in this workspace. No predictions were made during the audit.

## Files inspected

| File | Role |
| --- | --- |
| `train.csv` | Labelled historical requests |
| `test_unlabelled.csv` | Recent requests without `team_label` |
| `resolution_log.csv` | Closure / transfer log for train ids |
| `teams.csv` | Seven teams, two historical renames |
| `ops-policy.pdf` | Operations policy v4.1 |
| `email-thread.txt.txt` | Pre-assignment email thread |
| `README.txt` | Column documentation |
| `sample_submission.csv` | Submission layout |

## Row counts

| Dataset | Rows | Columns |
| --- | ---: | ---: |
| train.csv | 10,822 | 8 |
| test_unlabelled.csv | 2,178 | 7 |
| resolution_log.csv | 10,822 | 5 |
| teams.csv | 7 | 3 |
| sample_submission.csv | 2,178 | 2 |

Header-only line counts in editors can read one or two lines higher because of CSV quoting.

## Schemas

### train.csv

`request_id`, `created_at_ist`, `channel`, `product_family`, `warranty_status`, `request_text`, `source`, `team_label`

All stored as strings in pandas (`object`). No numeric intake features.

### test_unlabelled.csv

Same columns **except** `team_label`.

### resolution_log.csv

`request_id`, `first_team`, `final_team`, `transfers` (int64), `resolved_at`

## Missing values and duplicates

- Missing cells: **0** in train, test, and resolution_log.
- Full-row duplicates: **0**.
- Duplicate `request_id`: **0** in each file.
- Empty `request_text`: **0**.

## Identifiers

- Train ids: `SR500000` … `SR510821` (10,822 unique).
- Test ids: `SR510822` … `SR512999` (2,178 unique).
- Train ∩ test ids: **0**.
- Resolution log ids **exactly equal** the train id set.
- `sample_submission.csv` ids **exactly equal** the test id set.

## Date / time

| Set | Min `created_at_ist` | Max |
| --- | --- | --- |
| train | 2025-04-01 00:31 | 2026-06-30 23:33 |
| test | 2026-07-01 00:31 | 2026-09-30 23:00 |

That is 15 labelled months and 3 unlabelled months. README describes “18 months”; the files cover Apr 2025–Sep 2026.

`source` matches policy §9 exactly:

- `legacy_zoho`: 4,320 rows, 2025-04-01 through 2025-09-30
- `crm`: 6,502 train rows from 2025-10-01; **all 2,178 test rows are `crm`**

## Target distribution (`team_label`)

Nine strings appear because two queues were renamed on **15 Jan 2026** (policy §5). Responsibilities did not change.

| team_label | Count | % |
| --- | ---: | ---: |
| Repairs | 3,129 | 28.91 |
| Billing | 1,656 | 15.30 |
| Product Advice | 1,180 | 10.90 |
| Returns & Replacement | 1,174 | 10.85 |
| Warranty Claims | 1,040 | 9.61 |
| Consumables | 927 | 8.57 |
| Installations | 745 | 6.88 |
| Filters & Consumables | 531 | 4.91 |
| Installs & Demo | 440 | 4.07 |

Before 15 Jan 2026: old names only. On/after 15 Jan 2026: new names only. **0** mixed-name leaks across the cutover.

## Categorical fields

**channel (train / test):** chat 3,337 / 633; whatsapp 3,230 / 661; ivr 3,141 / 659; email 1,114 / 225.

**product_family:** Water Purifier, Air Fryer, Mixer Grinder, Induction Cooktop, Room Heater, Ceiling Fan, Robot Vacuum (same seven in train and test).

**warranty_status (train / test):** in_warranty 5,887 / 1,192; out_of_warranty 2,728 / 555; shield 2,207 / 431.

## Text

- Train length: mean 56.6 characters, min 10, max 233.
- Test length: mean 56.2, min 10, max 133.
- Unique train texts: 10,159; duplicate texts: 663; **89** texts appear with more than one `team_label`.
- Mojibake / encoding artefacts: **480** train rows (legacy Zoho), e.g. `â€¦`, `é` from failed UTF-8.

## Resolution log vs train

- `first_team` **equals** `team_label` on **100%** of rows.
- `first_team == final_team`: 77.17% (8,351 / 10,822 conceptually; exact match rate 0.7717).
- Transfers: mean 0.361; 8,126 with 0; 1,490 with 1; 1,206 with 2 (max 2).
- `transfers > 0` but `first_team == final_team`: 351.
- `transfers == 0` but teams differ: 126.
- `resolved_at` **before** `created_at_ist`: **1,140**, all `legacy_zoho` (UTC vs IST, matching Tanmay’s email and policy §9).

Billing first-team stay rate: 64.7% ended in Billing. Combined consumable queues stayed in a consumable queue 59.8% of the time.

## Train / test differences

- Test has no labels.
- Test is entirely CRM, after the rename, after the labelled window.
- Product / channel / warranty mixes are similar (purifier still largest).
- Sample submission fills **every** test row with `Repairs` (format only).

## Suspicious rows / fields

- Product in free text sometimes disagrees with `product_family` (e.g. Air Fryer row whose text is about a mixer).
- Payment language on non-payment jobs (see routing_logic.md).
- Resolution timestamps that precede creation on legacy rows.
- Duplicate texts with conflicting labels (label noise).
- `first_team` is a copy of the target, not an independent intake field.

## Expected submission format

`predictions.csv` must match `sample_submission.csv`:

- columns: `request_id,team`
- 2,178 rows, same ids, no duplicates
- `team` must be one of the **current** seven names (test is after the rename): Billing; Filters & Consumables; Installs & Demo; Product Advice; Repairs; Returns & Replacement; Warranty Claims
