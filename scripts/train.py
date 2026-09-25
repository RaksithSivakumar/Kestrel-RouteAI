"""Compare routing models, validate the selected model, and save the production artifact."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import (  # noqa: E402
    ARTIFACTS_DIR,
    CURRENT_TEAMS,
    DOCS_DIR,
    MODEL_PATH,
    RANDOM_SEED,
    REPORTS_DIR,
    TARGET_COLUMN,
)
from src.data import load_train  # noqa: E402
from src.features import prepare_frame  # noqa: E402
from src.model import build_pipeline, evaluate, metrics_table_row  # noqa: E402

import joblib  # noqa: E402


def majority_predict(y_train, n: int) -> np.ndarray:
    mode = pd.Series(y_train).mode().iloc[0]
    return np.array([mode] * n)


def rule_predict(frame: pd.DataFrame) -> np.ndarray:
    """Simple keyword priority rules — baseline only, not production."""
    preds = []
    for _, row in frame.iterrows():
        if row.get("kw_billing"):
            preds.append("Billing")
        elif row.get("kw_returns"):
            preds.append("Returns & Replacement")
        elif row.get("kw_install"):
            preds.append("Installs & Demo")
        elif row.get("kw_consumable"):
            preds.append("Filters & Consumables")
        elif row.get("kw_warranty"):
            preds.append("Warranty Claims")
        elif row.get("kw_advice"):
            preds.append("Product Advice")
        elif row.get("kw_repair"):
            preds.append("Repairs")
        else:
            preds.append("Repairs")
    return np.array(preds)


def save_confusion_matrix(cm, labels, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.set_title("Validation confusion matrix")
    vmax = cm.max() if cm.max() else 1
    for i in range(len(labels)):
        for j in range(len(labels)):
            color = "white" if cm[i, j] > vmax / 2 else "black"
            ax.text(j, i, int(cm[i, j]), ha="center", va="center", color=color, fontsize=8)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)


def write_comparison_md(rows: list[dict], path: Path) -> None:
    lines = [
        "# Model comparison",
        "",
        "Target: canonical historical `team_label` (Installations → Installs & Demo, Consumables → Filters & Consumables).",
        "",
        "Validation unless noted: stratified 80/20 holdout, `random_state=42`.",
        "",
        "Test_unlabelled.csv was not used for training or tuning.",
        "",
        "| Model | Accuracy | Macro F1 | Weighted F1 | Incorrect | Notes |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['model']} | {row['accuracy']:.4f} | {row['macro_f1']:.4f} | "
            f"{row['weighted_f1']:.4f} | {row['n_incorrect']} | {row['notes']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_validation_report(holdout, cv_scores, chrono, selected, path: Path) -> None:
    labels = holdout["labels"]
    report = holdout["report"]
    lines = [
        "# Validation report",
        "",
        f"Selected model: **{selected}**",
        "",
        "## Holdout",
        "",
        "- Split: stratified 80/20, `random_state=42`",
        f"- Validation rows: {holdout['n']}",
        f"- Accuracy: {holdout['accuracy']:.4f}",
        f"- Macro F1: {holdout['macro_f1']:.4f}",
        f"- Weighted F1: {holdout['weighted_f1']:.4f}",
        f"- Error rate: {holdout['error_rate']:.4f}",
        f"- Incorrect predictions: {holdout['n_incorrect']}",
        "",
        "## Cross-validation (5-fold stratified, training partition only)",
        "",
        f"- Mean accuracy: {cv_scores.mean():.4f}",
        f"- Std accuracy: {cv_scores.std():.4f}",
        f"- Folds: {', '.join(f'{s:.4f}' for s in cv_scores)}",
        "",
        "## Chronological validation",
        "",
        "- Train: requests with `created_at_ist` < 2026-04-01",
        "- Validate: 2026-04-01 to 2026-06-30 (last three labelled months)",
        f"- Validation rows: {chrono['n']}",
        f"- Accuracy: {chrono['accuracy']:.4f}",
        f"- Macro F1: {chrono['macro_f1']:.4f}",
        f"- Weighted F1: {chrono['weighted_f1']:.4f}",
        f"- Error rate: {chrono['error_rate']:.4f}",
        f"- Incorrect predictions: {chrono['n_incorrect']}",
        "",
        "## Per-team holdout metrics",
        "",
        "| Team | Precision | Recall | F1 | Support |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for label in labels:
        stats = report.get(label, {})
        lines.append(
            f"| {label} | {stats.get('precision', 0):.4f} | {stats.get('recall', 0):.4f} | "
            f"{stats.get('f1-score', 0):.4f} | {int(stats.get('support', 0))} |"
        )
    lines.extend(
        [
            "",
            "Confusion matrix image: `reports/confusion_matrix.png`",
            "",
            "Per-class CSV: `reports/per_class_metrics.csv`",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_error_analysis(val_df: pd.DataFrame, y_true, y_pred, path: Path) -> None:
    errors = val_df.copy()
    errors["y_true"] = y_true
    errors["y_pred"] = y_pred
    wrong = errors[errors["y_true"] != errors["y_pred"]]
    pair_counts = (
        wrong.groupby(["y_true", "y_pred"]).size().sort_values(ascending=False).head(15)
    )
    lines = [
        "# Error analysis",
        "",
        f"Holdout incorrect predictions: {len(wrong)} of {len(errors)} "
        f"({len(wrong) / len(errors):.2%}).",
        "",
        "Examples below are paraphrased patterns, not full customer messages.",
        "",
        "## Most common true → predicted confusions",
        "",
        "| True team | Predicted team | Count |",
        "| --- | --- | ---: |",
    ]
    for (true_t, pred_t), count in pair_counts.items():
        lines.append(f"| {true_t} | {pred_t} | {int(count)} |")

    lines.extend(
        [
            "",
            "## Error categories (manual review of confusion pairs and text)",
            "",
            "- **Payment mentioned on a non-billing job.** Historical labels often put “I already paid” into Billing even when the issue is install/repair (matches Meenal’s note and policy §3).",
            "- **Consumable vs repair on purifiers.** Filter language and leak/not-working language overlap; historical routing is inconsistent.",
            "- **Warranty vs billing vs advice.** Coverage questions that also mention payment or Shield.",
            "- **Vague callbacks.** “Please call me about my purifier” has weak routing signal; labels spread across teams.",
            "- **Product-family vs text mismatch.** Some rows name a different appliance in free text than in `product_family`.",
            "- **Team rename is not an error class.** Old/new queue names were canonicalised before training.",
            "",
            "These errors are a mix of genuine ambiguity and noisy historical bot labels. "
            "The supervised target remains `team_label`, not `final_team`.",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_train()
    data = prepare_frame(raw)
    y = data[TARGET_COLUMN].astype(str)
    data["created_at_ist"] = pd.to_datetime(data["created_at_ist"])

    idx_train, idx_val = train_test_split(
        data.index,
        test_size=0.2,
        stratify=y,
        random_state=RANDOM_SEED,
    )
    train_df = data.loc[idx_train]
    val_df = data.loc[idx_val]
    y_train = y.loc[idx_train]
    y_val = y.loc[idx_val]

    rows = []

    maj = majority_predict(y_train, len(y_val))
    maj_m = evaluate(y_val, maj)
    rows.append(metrics_table_row("majority", maj_m, "Always predict most common canonical team"))

    rule = rule_predict(val_df)
    rule_m = evaluate(y_val, rule)
    rows.append(metrics_table_row("keyword_rules", rule_m, "Priority keyword rules; baseline only"))

    candidates = [
        ("tfidf_word_lr", "word_lr", None, "Word TF-IDF (1-2g) + Logistic Regression"),
        ("tfidf_word_svc", "word_svc", None, "Word TF-IDF (1-2g) + LinearSVC"),
        ("tfidf_word_char_svc", "word_char_svc", None, "Word + char TF-IDF + LinearSVC"),
        (
            "word_char_struct_svc",
            "word_char_struct_svc",
            None,
            "Word+char TF-IDF, product/channel/warranty, keyword flags + LinearSVC",
        ),
        (
            "word_char_struct_svc_balanced",
            "word_char_struct_svc",
            "balanced",
            "Same features with class_weight=balanced",
        ),
    ]

    holdout_metrics = {}
    fitted = {}
    for name, spec, cw, notes in candidates:
        pipe = build_pipeline(spec, class_weight=cw)
        pipe.fit(train_df, y_train)
        pred = pipe.predict(val_df)
        metrics = evaluate(y_val, pred)
        holdout_metrics[name] = metrics
        fitted[name] = pipe
        rows.append(metrics_table_row(name, metrics, notes))
        print(f"{name}: acc={metrics['accuracy']:.4f} macro={metrics['macro_f1']:.4f}", flush=True)

    selected_name = max(holdout_metrics, key=lambda k: (holdout_metrics[k]["accuracy"], holdout_metrics[k]["macro_f1"]))
    selected_pipe = fitted[selected_name]
    selected_holdout = holdout_metrics[selected_name]
    spec_map = {n: (s, cw) for n, s, cw, _ in candidates}
    sel_spec, sel_cw = spec_map[selected_name]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)
    cv_pipe = build_pipeline(sel_spec, class_weight=sel_cw)
    cv_scores = cross_val_score(cv_pipe, train_df, y_train, cv=cv, scoring="accuracy", n_jobs=1)

    chrono_cut = pd.Timestamp("2026-04-01")
    chrono_train = data[data["created_at_ist"] < chrono_cut]
    chrono_val = data[data["created_at_ist"] >= chrono_cut]
    chrono_pipe = build_pipeline(sel_spec, class_weight=sel_cw)
    chrono_pipe.fit(chrono_train, y.loc[chrono_train.index])
    chrono_pred = chrono_pipe.predict(chrono_val)
    chrono_metrics = evaluate(y.loc[chrono_val.index], chrono_pred)

    val_pred = selected_pipe.predict(val_df)
    save_confusion_matrix(
        np.array(selected_holdout["confusion_matrix"]),
        CURRENT_TEAMS,
        REPORTS_DIR / "confusion_matrix.png",
    )
    per_class = []
    for label in CURRENT_TEAMS:
        stats = selected_holdout["report"][label]
        per_class.append(
            {
                "team": label,
                "precision": stats["precision"],
                "recall": stats["recall"],
                "f1": stats["f1-score"],
                "support": stats["support"],
            }
        )
    pd.DataFrame(per_class).to_csv(REPORTS_DIR / "per_class_metrics.csv", index=False)

    write_comparison_md(rows, DOCS_DIR / "model_comparison.md")
    write_validation_report(
        selected_holdout, cv_scores, chrono_metrics, selected_name, REPORTS_DIR / "validation_report.md"
    )
    write_error_analysis(val_df, y_val.to_numpy(), val_pred, REPORTS_DIR / "error_analysis.md")

    final_pipe = build_pipeline(sel_spec, class_weight=sel_cw)
    final_pipe.fit(data, y)
    bundle = {
        "pipeline": final_pipe,
        "classes": list(final_pipe.named_steps["clf"].classes_),
        "model_name": selected_name,
        "holdout": {
            "accuracy": selected_holdout["accuracy"],
            "macro_f1": selected_holdout["macro_f1"],
            "weighted_f1": selected_holdout["weighted_f1"],
            "error_rate": selected_holdout["error_rate"],
            "n": selected_holdout["n"],
            "n_incorrect": selected_holdout["n_incorrect"],
        },
        "cv_mean_accuracy": float(cv_scores.mean()),
        "cv_std_accuracy": float(cv_scores.std()),
        "chrono": {
            "accuracy": chrono_metrics["accuracy"],
            "macro_f1": chrono_metrics["macro_f1"],
            "n": chrono_metrics["n"],
            "n_incorrect": chrono_metrics["n_incorrect"],
        },
        "seed": RANDOM_SEED,
    }
    joblib.dump(bundle, MODEL_PATH)

    summary = {
        "selected_model": selected_name,
        "holdout": bundle["holdout"],
        "cv_mean_accuracy": bundle["cv_mean_accuracy"],
        "cv_std_accuracy": bundle["cv_std_accuracy"],
        "chrono": bundle["chrono"],
        "comparison": rows,
        "n_train_full": int(len(data)),
        "n_holdout_train": int(len(train_df)),
        "n_holdout_val": int(len(val_df)),
        "n_chrono_train": int(len(chrono_train)),
        "n_chrono_val": int(len(chrono_val)),
    }
    (ARTIFACTS_DIR / "metrics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
