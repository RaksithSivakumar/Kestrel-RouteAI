"""Human-readable routing reasons from text, structured fields, and model scores."""

from __future__ import annotations

import re

import numpy as np

from src.features import normalize_text

TEAM_CUES: dict[str, list[tuple[str, str]]] = {
    "Repairs": [
        (r"not working|not turning on|breakdown|fault", "The request describes a product fault or breakdown."),
        (r"leak", "The request mentions a leak, which is handled as a repair."),
        (r"noise|loud", "The request mentions abnormal noise."),
        (r"error|error code|blank|display", "The request mentions an error or display fault."),
        (r"burnt|smell|overheat|tripping|mcb", "The request describes an electrical or heating fault."),
        (r"motor", "The request mentions a motor issue associated with technician repair."),
    ],
    "Filters & Consumables": [
        (r"filter|candle|membrane|cartridge|amc", "The request is about a filter, membrane, or AMC kit."),
        (r"spare|jar|blade|brush", "The request asks for a spare or consumable part, not a fault repair."),
    ],
    "Installs & Demo": [
        (r"install|installer|demo|wall.?mount", "The request concerns installation or a demo visit."),
        (r"slot|reschedule", "The request is about booking or rescheduling an installation slot."),
    ],
    "Billing": [
        (r"\bgst\b|invoice", "The request is about an invoice or GST."),
        (r"refund|emi|coupon", "The request is about a payment, EMI, coupon, or refund."),
        (r"double charg|charged twice|payment", "The request treats payment itself as the problem."),
    ],
    "Returns & Replacement": [
        (r"wrong model|wrong .*delivered|damaged|missing part|incomplete", "The request concerns a damaged, wrong, or incomplete delivery."),
        (r"\breturn\b|exchange|cancel and return", "The request asks to return or exchange the product."),
    ],
    "Warranty Claims": [
        (r"claim status|warranty rejected|register", "The request is about a warranty or Shield claim or registration."),
        (r"covered under|shield plan|warranty", "The request asks about warranty or Shield coverage."),
    ],
    "Product Advice": [
        (r"how to|difference between|which model|usage|clean", "The request is a usage or product-advice question rather than a fault."),
        (r"power consumption", "The request asks about usage characteristics, not a repair."),
    ],
}


def relative_confidence(scores: np.ndarray) -> float:
    ordered = np.sort(scores)[::-1]
    if ordered[0] <= 0:
        return float(ordered[0])
    if len(ordered) == 1:
        return float(ordered[0])
    gap = float(ordered[0] - ordered[1])
    return float(0.5 * ordered[0] + 0.5 * min(1.0, gap / max(ordered[0], 1e-9)))


def explain_prediction(
    *,
    predicted_team: str,
    request_text: str,
    product_family: str,
    warranty_status: str,
    scores: np.ndarray,
    class_names: list[str],
) -> list[str]:
    reasons: list[str] = []
    text = normalize_text(request_text)

    for pattern, reason in TEAM_CUES.get(predicted_team, []):
        if re.search(pattern, text):
            reasons.append(reason)
        if len(reasons) >= 2:
            break

    if product_family:
        reasons.append(f"The request is tagged to product family {product_family}.")
    if warranty_status == "shield" and predicted_team in {"Warranty Claims", "Repairs", "Filters & Consumables"}:
        reasons.append("The request indicates an active Kestrel Shield plan.")
    elif warranty_status == "in_warranty" and predicted_team == "Warranty Claims":
        reasons.append("The request is marked in-warranty and concerns coverage or a claim.")
    elif warranty_status == "out_of_warranty" and predicted_team == "Filters & Consumables":
        reasons.append("The unit is out of warranty, which often routes spare and filter requests to consumables.")

    idx = class_names.index(predicted_team) if predicted_team in class_names else int(np.argmax(scores))
    top_score = float(scores[idx])
    runner_up = class_names[int(np.argsort(scores)[-2])] if len(class_names) > 1 else ""
    reasons.append(
        f"The local routing model scored {predicted_team} highest "
        f"(relative confidence {top_score:.2f}"
        + (f"; next team {runner_up}" if runner_up else "")
        + ")."
    )

    # Keep explanations short and operator-friendly.
    deduped: list[str] = []
    for item in reasons:
        if item not in deduped:
            deduped.append(item)
    return deduped[:4]
