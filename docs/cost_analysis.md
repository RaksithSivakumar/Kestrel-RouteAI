# Cost analysis

Figures below use **only** numbers stated in the assignment pack or derived from them by arithmetic. Hosting was not measured.

## Current vendor routing bot

- Annual licence: **₹3,20,000** (policy §4; Farhan’s email).
- Monthly equivalent: ₹3,20,000 / 12 = **₹26,666.67**.
- Stated volume: **700 requests/month**.
- Annual volume: 700 × 12 = **8,400** requests.
- Bot cost per request: ₹3,20,000 / 8,400 = **₹38.095…** (₹38.10 when rounded to paise).

## Local RouteAI model

- Inference: sklearn LinearSVC (or the selected local model) on this machine.
- Paid model API calls: **none**.
- Cost per prediction for the model/API itself: **₹0**.
- Monthly model/API cost at 700 requests: 700 × ₹0 = **₹0**.
- Annual model/API cost: 8,400 × ₹0 = **₹0**.

Potential **software/API licence** saving versus the vendor bot: **₹3,20,000/year**.

This is **not** guaranteed total savings. Not included (not measured here):

- VM or container hosting
- Monitoring and logging
- Engineering time to shadow-deploy and support
- Agent time still spent on transfers (~22.8% of historical tickets closed on a different team than the bot)

## Transfer economics (context, not a saving claim)

Policy §4: each transfer costs ₹305 in handling time; a misroute also generates on average one extra contact at ₹260.

On the labelled set, 2,471 / 10,822 tickets (22.83%) closed on a different team than `team_label`. Matching the bot at 90% does **not** automatically cut that transfer rate, because the labels themselves include those misroutes.

## Recommendation for finance

Write the monthly run cost of the replacement as **₹0 model/API** plus whatever infra Kestrel already uses to host an internal Python service. Do not swap a flat ₹3.2 lakh licence for a usage-priced LLM API.
