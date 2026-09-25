"""Text normalisation and intake-time feature construction."""

from __future__ import annotations

import re
import unicodedata

import pandas as pd

KEYWORD_FEATURES = {
    "kw_install": r"install|demo|wall.?mount|installer|slot|reschedule",
    "kw_consumable": (
        r"filter|candle|membrane|spare|jar|blade|brush|amc|"
        r"consumable|cartridge"
    ),
    "kw_billing": (
        r"\bgst\b|invoice|refund|emi|coupon|double charg|charged twice|"
        r"payment|paid extra|billing"
    ),
    "kw_returns": (
        r"\breturn\b|wrong model|missing part|damaged|incomplete|"
        r"exchange|cancel and return|delivered"
    ),
    "kw_warranty": (
        r"warranty|shield|claim status|coverage|covered under|"
        r"register.*(?:warranty|shield)|claim"
    ),
    "kw_advice": (
        r"how to|difference between|power consumption|usage|"
        r"which model|clean robot|pre.?purchase"
    ),
    "kw_repair": (
        r"not working|leak|noise|error|burnt|blank|tripping|"
        r"breakdown|fault|repair|overheat|mcb|smell|broken"
    ),
}


def normalize_text(text) -> str:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    value = str(text)
    replacements = {
        "Ã¢â‚¬Â¦": " ",
        "â€¦": " ",
        "â€“": "-",
        "â€”": "-",
        "â€™": "'",
        "â€˜": "'",
        "â€œ": '"',
        "â€": '"',
        "Â": "",
    }
    for src, dst in replacements.items():
        value = value.replace(src, dst)
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    value = re.sub(r"[^a-z0-9\s+/.-]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def combine_text(row: pd.Series) -> str:
    parts = [
        normalize_text(row.get("request_text", "")),
        f"product {normalize_text(row.get('product_family', ''))}",
        f"warranty {normalize_text(row.get('warranty_status', ''))}",
        f"channel {normalize_text(row.get('channel', ''))}",
    ]
    return " ".join(p for p in parts if p)


def add_keyword_flags(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    text = out["request_text"].map(normalize_text)
    for name, pattern in KEYWORD_FEATURES.items():
        out[name] = text.str.contains(pattern, regex=True).astype(int)
    return out


def prepare_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in ("channel", "product_family", "warranty_status", "source", "request_text"):
        if col not in out.columns:
            out[col] = ""
        out[col] = out[col].fillna("")
    out = add_keyword_flags(out)
    out["text_combined"] = out.apply(combine_text, axis=1)
    return out
