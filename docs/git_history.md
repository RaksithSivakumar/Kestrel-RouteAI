# Git development history

This file describes **actual** commits on `main`. It is not a fictional log.

Client extract files (`train.csv`, `test_unlabelled.csv`, `resolution_log.csv`, `teams.csv`, `ops-policy.pdf`, `email-thread.txt.txt`, `README.txt`, `sample_submission.csv`) are gitignored and were never intended for GitHub.

## Milestones

1. **chore: initialize project structure** — ignore rules, requirements, Python package stub, artifact folder.
2. **docs: add assignment, data handling, and policy notes** — data audit, routing/policy notes, leakage analysis, cost and AI-usage notes.
3. **feat: add routing classifier** — loaders, text features, sklearn pipelines, train/compare script.
4. **docs: record model comparison and validation** — holdout, CV, chronological results, confusion matrix, error analysis, selected `tfidf_word_svc` artifact.
5. **feat: add explainable FastAPI routing service** — predictor, reasons, `/health` and `/predict`.
6. **feat: add Next.js routing desk** — App Router UI for intake fields and explanations.
7. **test: add backend and frontend tests** — pytest + Vitest.
8. **feat: generate validated submission predictions** — `predictions.csv` and validator.
9. **docs: add memo, submission form, and final QA** — business write-up and run evidence.

Exact hashes: run `git log --oneline`.
