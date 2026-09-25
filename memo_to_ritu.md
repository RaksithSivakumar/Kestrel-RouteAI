# Memo to Ritu Deshpande

**To:** Ritu Deshpande, Head of D2C Operations  
**From:** Routing replacement workstream  
**Date:** 25 Sep 2026  
**Subject:** Can we retire the vendor routing bot?

## Decision

Do **not** switch the vendor bot off this week. Put RouteAI in **shadow mode** (bot still assigns the live queue; RouteAI scores every ticket and we compare). A controlled pilot on one channel can follow if shadow agreement stays high.

## What we measured

On held-out historical labels (the same target you asked us to match):

- Accuracy **95.8%** (2,165 requests; 92 wrong)
- Error rate **4.2%**
- A time-based check on Apr–Jun 2026 (closest to “future months”) was **95.1%**
- Five-fold cross-check averaged **95.7%**

The 90% bar **was met** on every check we ran. That is still not a hidden-test score. Unlabelled July–September tickets have no answers yet; a fair range for those is about **93–96%**, based on the time-based check and the small spread across folds.

## Cost

- Current bot: **₹3.2 lakh/year** (~₹26,667/month; about ₹38 per request at 700/month).
- Replacement model/API: **₹0 per prediction** (runs on our own machine; no paid AI calls).
- Potential **licence** saving: **₹3.2 lakh/year**. This is not guaranteed total saving. Hosting, monitoring, and agent time are extra.

## Main risk

The labels are **the old bot**, including tickets Meenal already said were dumped into Billing and Consumables and then transferred. Matching the bot well does **not** by itself cut transfers (about **23%** of closed tickets ended on a different team). If we want fewer transfers, we would need a second project aimed at the team that actually closes the job.

Busiest queue in history: **Repairs**, then Billing, then advice/returns.

## Next week

1. Shadow RouteAI against the live bot for one week; review disagreements daily with Meenal.  
2. Keep Farhan’s ₹0-per-ticket model unless infra is quoted separately.  
3. Do not plan headcount off RouteAI volume until the shadow week is in.
