"""Sklearn routing classifier construction, training, and metrics."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.svm import LinearSVC

from src.config import CATEGORICAL_FEATURES, CURRENT_TEAMS, RANDOM_SEED, TEXT_FEATURE
from src.features import KEYWORD_FEATURES

KEYWORD_COLUMNS = list(KEYWORD_FEATURES.keys())


def _logistic(class_weight: str | None) -> OneVsRestClassifier:
    return OneVsRestClassifier(
        LogisticRegression(
            max_iter=250,
            class_weight=class_weight,
            random_state=RANDOM_SEED,
            solver="liblinear",
        )
    )


def build_pipeline(
    model_name: str = "word_char_struct_svc",
    class_weight: str | None = None,
) -> Pipeline:
    word = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 2),
        min_df=2,
        max_features=40_000,
        sublinear_tf=True,
    )
    char = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=3,
        max_features=20_000,
        sublinear_tf=True,
    )
    categoricals = OneHotEncoder(handle_unknown="ignore")

    if model_name == "word_lr":
        preprocess = ColumnTransformer(
            [("text", word, TEXT_FEATURE)],
            remainder="drop",
        )
        clf = _logistic(class_weight)
    elif model_name == "word_svc":
        preprocess = ColumnTransformer(
            [("text", word, TEXT_FEATURE)],
            remainder="drop",
        )
        clf = LinearSVC(class_weight=class_weight, random_state=RANDOM_SEED, dual="auto")
    elif model_name == "char_svc":
        preprocess = ColumnTransformer(
            [("text", char, TEXT_FEATURE)],
            remainder="drop",
        )
        clf = LinearSVC(class_weight=class_weight, random_state=RANDOM_SEED, dual="auto")
    elif model_name == "word_char_svc":
        preprocess = ColumnTransformer(
            [
                ("word", word, TEXT_FEATURE),
                ("char", char, TEXT_FEATURE),
            ],
            remainder="drop",
        )
        clf = LinearSVC(class_weight=class_weight, random_state=RANDOM_SEED, dual="auto")
    elif model_name == "word_char_struct_lr":
        preprocess = ColumnTransformer(
            [
                ("word", word, TEXT_FEATURE),
                ("char", char, TEXT_FEATURE),
                ("cat", categoricals, CATEGORICAL_FEATURES),
                ("kw", "passthrough", KEYWORD_COLUMNS),
            ],
            remainder="drop",
        )
        clf = _logistic(class_weight)
    else:
        preprocess = ColumnTransformer(
            [
                ("word", word, TEXT_FEATURE),
                ("char", char, TEXT_FEATURE),
                ("cat", categoricals, CATEGORICAL_FEATURES),
                ("kw", "passthrough", KEYWORD_COLUMNS),
            ],
            remainder="drop",
        )
        clf = LinearSVC(class_weight=class_weight, random_state=RANDOM_SEED, dual="auto")

    return Pipeline(
        [
            ("features", preprocess),
            ("clf", clf),
        ]
    )


def scores_from_estimator(estimator, X) -> np.ndarray:
    clf = estimator.named_steps["clf"]
    if hasattr(clf, "predict_proba"):
        transformed = estimator.named_steps["features"].transform(X)
        return clf.predict_proba(transformed)
    transformed = estimator.named_steps["features"].transform(X)
    raw = clf.decision_function(transformed)
    if raw.ndim == 1:
        raw = np.vstack([-raw, raw]).T
    exp = np.exp(raw - raw.max(axis=1, keepdims=True))
    return exp / exp.sum(axis=1, keepdims=True)


def evaluate(y_true, y_pred, labels=None) -> dict[str, Any]:
    labels = labels or CURRENT_TEAMS
    acc = float(accuracy_score(y_true, y_pred))
    return {
        "accuracy": acc,
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", labels=labels, zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, average="weighted", labels=labels, zero_division=0)),
        "error_rate": 1.0 - acc,
        "n": int(len(y_true)),
        "n_incorrect": int((np.array(y_true) != np.array(y_pred)).sum()),
        "report": classification_report(
            y_true, y_pred, labels=labels, digits=4, zero_division=0, output_dict=True
        ),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
        "labels": labels,
    }


def metrics_table_row(name: str, metrics: dict[str, Any], notes: str = "") -> dict[str, Any]:
    return {
        "model": name,
        "accuracy": round(metrics["accuracy"], 4),
        "macro_f1": round(metrics["macro_f1"], 4),
        "weighted_f1": round(metrics["weighted_f1"], 4),
        "error_rate": round(metrics["error_rate"], 4),
        "n_incorrect": metrics["n_incorrect"],
        "notes": notes,
    }
