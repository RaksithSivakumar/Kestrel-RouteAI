# Routing logic and policy

## Seven service teams

Sources: `teams.csv`, ops-policy v4.1, README.txt, email thread.

| Current name | Historical name | Handles |
| --- | --- | --- |
| Installs & Demo | Installations (until 14 Jan 2026) | New-product installation, demo, wall-mounting |
| Repairs | (unchanged) | Faults, breakdowns, error codes, noise, leaks — technician fixes |
| Filters & Consumables | Consumables (until 14 Jan 2026) | Filters, candles, membranes, jars, brushes, blades, AMC kits. **Not faults** |
| Billing | (unchanged) | Invoice, GST, double charge, refund of a payment, EMI conversion, coupons. **Only when the problem IS the payment** |
| Returns & Replacement | (unchanged) | Damaged, wrong or incomplete deliveries; returns/exchanges in window |
| Warranty Claims | (unchanged) | Warranty and Shield registration, coverage questions, claim status |
| Product Advice | (unchanged) | Pre- and post-purchase usage questions. **No fault reported** |

Policy §5: from 15 Jan 2026 the two names changed; **responsibilities did not**.

## Policy-driven rules

- Intake channels: IVR, chat, WhatsApp, email. Bot assigns a queue at creation. Agents transfer misroutes. Closing team is `final_team`.
- Billing exclusion: mentioning that a customer **has paid** does not make it Billing (policy §3). Meenal’s email: roughly half of Billing some weeks are people who paid for install/repair and are transferred out.
- Consumables vs repairs: filter/spare language vs breakdown/leak.
- Warranty 12 months standard / 24 months some lines / optional Shield — coverage **questions** go to Warranty Claims; a fault under warranty still reads as Repairs in historical labels more often than Warranty Claims.
- Transfer cost (policy §4): ₹305 per transfer; extra contact ₹260; technician visit ₹540; vendor bot ₹3.2 lakh/year.
- Systems: Zoho until 30 Sep 2025, Kestrel CRM from 1 Oct 2025.

## Supervised target

Historical `team_label` is the **vendor bot’s queue at creation**. Tanmay: that is the label to match. Ritu: 90% match to those labels is the bar.

This project **does not** replace labels with `final_team` or with a policy rewrite. Conflicts are documented, not silently “fixed”.

## Policy vs history

Measured on train joined to resolution_log:

- 22.83% of labelled requests were closed by a **different** team than the bot (`first_team != final_team`).
- Billing: 1,656 bot labels, only 1,071 closed in Billing (64.7%). Common destinations: Repairs (192), Returns (125), Warranty Claims (106), Installations / Installs & Demo (146 combined).
- Consumables + Filters & Consumables: 1,458 bot labels, 59.8% stayed in a consumable queue; 315 closed in Repairs.

That matches Meenal: Billing and Consumables absorb work that policy would send elsewhere.

## Strong routing signals (intake)

- Explicit fault language (leak, blank display, motor, noise) → Repairs
- Filter / AMC / spare jar / blade → Filters & Consumables
- Installer / slot / wall mount / demo → Installs & Demo
- GST / invoice / EMI conversion / coupon as the problem → Billing
- Wrong model / missing parts / cancel and return → Returns & Replacement
- Claim status / covered under Shield → Warranty Claims
- How to / difference between lite and pro → Product Advice
- `product_family` and `warranty_status` are weak alone (nearly uniform team mix by product except Water Purifier, which has much more Consumables).

## Ambiguity and overlap

- “Please call back regarding [product]” (~12% of train) is spread across all teams; Meenal called this out.
- Paid + install/repair in the same sentence: policy says not Billing; history often labelled Billing.
- Purifier “filter” vs “leaking / not working”.
- Shield mentioned on a fault: Warranty Claims vs Repairs.
- Duplicate identical texts with different labels (89 texts).

## Headcount / volume (for Ritu)

Canonical train volume (old+new names combined): Repairs 3,129; Billing 1,656; Product Advice 1,180; Returns 1,174; Warranty 1,040; Consumables family 1,458; Installs family 1,185.

Test months (Jul–Sep 2026) are the production-like window: 736 / 741 / 701 requests.
