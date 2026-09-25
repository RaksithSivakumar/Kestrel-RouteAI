# AI usage

Honest record for this engagement.

## Tools actually used

- **Cursor** (agent session in this repository), model identified in the product as **Cursor Grok 4.6**.
- No ChatGPT web session was used in this build.
- No Claude / Gemini / Copilot subscription was invoked from this workspace.
- No paid inference API (OpenAI, Anthropic, Groq, etc.) was called by the routing service or the training scripts.

## What AI helped with

- Repository and CSV/PDF inspection plan
- Drafting Python package layout (`src/`, `api/`, `scripts/`, `tests/`)
- Drafting FastAPI and Next.js files
- Drafting audit, policy, leakage, cost, README, and form prose from **measured** pandas outputs
- Gitignore and privacy reminders for client files

## What was not left to AI unverified

- Row counts, distributions, rename cutover, resolution-log join rates, and model metrics were produced by running Python on the local files.
- Tests and submission validation were run locally (see `FINAL_QA.md`).
- Hidden-test accuracy is **estimated**, not claimed as fact.

## Where AI is a weak fit / discarded

- An LLM classifier was **not** used as the router. This is labelled text classification; a local TF-IDF linear model is the right default and has ₹0 inference cost (Farhan’s constraint).
- AI-written metrics were not accepted without a training run.
- Client CSVs were not uploaded to an external model provider.

## Paid API cost

**₹0.**

## What a reviewer should still check

Human review of hours remains advisable. GitHub URL is the real `origin` remote. Google Drive was not used.
