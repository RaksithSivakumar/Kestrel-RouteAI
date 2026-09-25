# Leakage analysis

A field is usable only if it would be known **when a new request arrives**, before a human or bot assigns a queue.

## Column decisions

| Field | Classification | Use in model | Why |
| --- | --- | --- | --- |
| request_id | identifier | No | Sequential key; not a routing reason. |
| created_at_ist | metadata / weak feature | Not used in the final model | Available at intake, but test is a later time window; using time can overfit seasonality/rename rather than issue type. Rename is handled by canonical labels instead. |
| channel | usable feature | Yes | Known at intake (ivr/chat/whatsapp/email). |
| product_family | usable feature | Yes | Known at intake. |
| warranty_status | usable feature | Yes | Known at intake (`in_warranty` / `out_of_warranty` / `shield`). |
| request_text | usable feature | Yes | Customer opening message / IVR transcript at creation. |
| source | metadata | No | Available, but test is 100% `crm`. It mainly encodes pre/post 1 Oct 2025 system cutover, not the customer issue. |
| team_label | target | Target only | Bot queue at creation. |
| first_team | leakage | **Excluded** | Identical to `team_label` on 100% of train rows. It is the routing outcome, not an intake field. |
| final_team | leakage | **Excluded** | Team that **closed** the ticket; known only after handling and transfers (policy §3, Tanmay’s email). |
| transfers | leakage | **Excluded** | Count of post-routing handoffs. |
| resolved_at | leakage | **Excluded** | Closure timestamp; legacy values even mix UTC vs IST. |
| renamed_to / handles (teams.csv) | documentation | Indirect | Used to canonicalise names, not as row-level features. |

## resolution_log.csv

One row per **train** request. Test ids have **no** resolution rows (open / not exported). Tanmay: log exists only for closed requests, “so not the latest ones”.

Using anything from this file to predict `team_label` would be circular (`first_team`) or would use information that does not exist for a new ticket (`final_team`, transfers, resolved_at).

`final_team` is operationally interesting (true destination) but **is not the assignment target**. Training on it would optimise a different problem than “match historical routing labels”.

## Other leakage checks

- Do not use test_unlabelled.csv for fitting, vocabulary mining for tuning, or threshold search.
- Do not use future months as features.
- Keyword flags are derived only from `request_text` (intake).
- Canonical name mapping uses the policy date, not resolution data.

## Excluded from git / publish

Client tables and the policy/email pack must not be published. See `.gitignore` and `docs/git_history.md`.
