#!/usr/bin/env python3
"""Train the local Magic Write ML style model."""

from __future__ import annotations

import argparse
import json
import math
import pickle
import random
import re
from collections import Counter
from pathlib import Path
from typing import Any

from magic_write import (
    MAGIC_WRITE_DATASET_VERSION,
    MAGIC_WRITE_ML_MODEL_FORMAT,
    MAGIC_WRITE_ML_MODEL_FORMAT_VERSION,
    _ml_tokens,
    get_magic_write_training_dataset,
    load_magic_write_ml_model,
)


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = PROJECT_DIR / "magic_write_ml_model.pkl"

PROMPT_PHRASES = [
    "create modern text style",
    "generate editable typography",
    "make bold display lettering",
    "design transparent text",
    "clean modern word art",
    "poster typography",
    "social media text design",
    "logo style text",
    "headline lettering",
    "decorative type effect",
]

CATEGORY_PROMPTS = {
    "birthday": ["happy birthday", "birthday bash", "party type", "celebration lettering"],
    "sale": ["huge sale", "free shipping", "discount offer", "shop now"],
    "wedding": ["bride groom", "wedding day", "engagement", "love story"],
    "graduation": ["class of 2026", "graduation day", "congrats grad", "graduate style"],
    "neon": ["neon sign", "glow text", "now open", "night light"],
    "luxury": ["golden hour", "premium serif", "luxury brand", "elegant title"],
    "script": ["brush script", "handwritten text", "sweet lettering", "signature style"],
    "comic": ["comic cartoon", "arcade text", "pop outline", "bold sticker"],
}


def _style_label(style: dict[str, Any], index: int) -> str:
    raw = str(style.get("name") or style.get("category") or f"style_{index}")
    label = re.sub(r"[^a-zA-Z0-9_]+", "_", raw).strip("_").lower()
    return label or f"style_{index}"


def _style_records_from_existing_model(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    model = load_magic_write_ml_model(path)
    labels = [str(label) for label in model.get("labels", [])]
    lookup = model.get("style_lookup") if isinstance(model.get("style_lookup"), dict) else {}
    records: list[dict[str, Any]] = []
    for label in labels:
        style = lookup.get(label)
        if isinstance(style, dict):
            record = dict(style)
            record["name"] = label
            records.append(record)
    return records


def _base_style_records() -> list[dict[str, Any]]:
    dataset = get_magic_write_training_dataset()
    records: list[dict[str, Any]] = []
    for key in ("style_presets", "modern_style_dataset", "modern_composition_templates"):
        for item in dataset.get(key, []):
            if isinstance(item, dict):
                records.append(dict(item))
    return records


def _category_terms(style: dict[str, Any]) -> list[str]:
    haystack = " ".join(
        str(style.get(key, ""))
        for key in ("name", "category", "fontFamily", "sample", "previewLayout", "kind")
    ).lower()
    terms: list[str] = []
    for key, prompts in CATEGORY_PROMPTS.items():
        if key in haystack or any(part in haystack for part in key.split()):
            terms.extend(prompts)
    if "class" in haystack or "grad" in haystack:
        terms.extend(CATEGORY_PROMPTS["graduation"])
    if not terms:
        terms.extend(["modern typography", "text style", "word art"])
    return terms


def _style_document(style: dict[str, Any], label: str, doc_index: int) -> str:
    fields = [
        label.replace("_", " "),
        str(style.get("category") or ""),
        str(style.get("fontFamily") or ""),
        str(style.get("sample") or ""),
        str(style.get("previewLayout") or ""),
        str(style.get("kind") or ""),
    ]
    fields = [field for field in fields if field.strip()]
    category_terms = _category_terms(style)
    phrase = PROMPT_PHRASES[doc_index % len(PROMPT_PHRASES)]
    intent = category_terms[(doc_index // len(PROMPT_PHRASES)) % len(category_terms)]
    return " ".join([phrase, intent, *fields])


def train_magic_write_ml_model(
    output_path: Path = DEFAULT_MODEL_PATH,
    target_documents: int = 1_000_000,
    alpha: float = 1.0,
    seed: int = 12345,
    base_model_path: Path = DEFAULT_MODEL_PATH,
) -> dict[str, Any]:
    records = _style_records_from_existing_model(base_model_path) or _base_style_records()
    if not records:
        raise ValueError("no style records available for training")

    labels: list[str] = []
    style_lookup: dict[str, dict[str, Any]] = {}
    seen: set[str] = set()
    for index, style in enumerate(records):
        label = _style_label(style, index)
        if label in seen:
            label = f"{label}_{index:04d}"
        seen.add(label)
        labels.append(label)
        style_lookup[label] = dict(style, name=label)

    rng = random.Random(seed)
    rng.shuffle(labels)
    requested_documents = max(int(target_documents), len(labels))
    docs_per_label = requested_documents // len(labels)
    remainder = requested_documents % len(labels)

    class_counts: Counter[str] = Counter()
    feature_counts: dict[str, Counter[str]] = {label: Counter() for label in labels}
    vocabulary: set[str] = set()

    for label_index, label in enumerate(labels):
        doc_count = docs_per_label + (1 if label_index < remainder else 0)
        style = style_lookup[label]
        class_counts[label] = doc_count
        for doc_index in range(doc_count):
            document = _style_document(style, label, doc_index)
            tokens = _ml_tokens(document)
            feature_counts[label].update(tokens)
            vocabulary.update(tokens)

    vocab = sorted(vocabulary)
    vocab_size = max(len(vocab), 1)
    total_docs = sum(class_counts.values())
    label_count = len(labels)
    class_log_prior: dict[str, float] = {}
    feature_log_prob: dict[str, dict[str, float]] = {}
    default_log_prob: dict[str, float] = {}

    for label in labels:
        class_log_prior[label] = math.log((class_counts[label] + alpha) / (total_docs + alpha * label_count))
        counts = feature_counts[label]
        token_total = sum(counts.values())
        denominator = token_total + alpha * vocab_size
        default_log_prob[label] = math.log(alpha / denominator)
        feature_log_prob[label] = {
            token: math.log((count + alpha) / denominator)
            for token, count in counts.items()
        }

    model = {
        "format": MAGIC_WRITE_ML_MODEL_FORMAT,
        "format_version": MAGIC_WRITE_ML_MODEL_FORMAT_VERSION,
        "model_type": "multinomial_naive_bayes",
        "dataset_version": MAGIC_WRITE_DATASET_VERSION,
        "labels": labels,
        "vocabulary": vocab,
        "class_log_prior": class_log_prior,
        "feature_log_prob": feature_log_prob,
        "default_log_prob": default_log_prob,
        "style_lookup": style_lookup,
        "training": {
            "documents": total_docs,
            "target_documents": requested_documents,
            "trained_documents": total_docs,
            "requested_documents": requested_documents,
            "styles": len(labels),
            "base_styles": len(records),
            "alpha": alpha,
            "seed": seed,
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(pickle.dumps(model, protocol=pickle.HIGHEST_PROTOCOL))
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train Magic Write local ML model")
    parser.add_argument("--output", default=str(DEFAULT_MODEL_PATH), help="Model path to write.")
    parser.add_argument("--target-documents", type=int, default=1_000_000, help="Synthetic training document count.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Naive Bayes smoothing.")
    parser.add_argument("--seed", type=int, default=12345, help="Deterministic training seed.")
    parser.add_argument("--base-model", default=str(DEFAULT_MODEL_PATH), help="Existing model to reuse style classes from.")
    args = parser.parse_args()

    model = train_magic_write_ml_model(
        output_path=Path(args.output),
        target_documents=args.target_documents,
        alpha=args.alpha,
        seed=args.seed,
        base_model_path=Path(args.base_model),
    )
    print(json.dumps({
        "output": args.output,
        "dataset_version": model.get("dataset_version"),
        "labels": len(model.get("labels", [])),
        "vocabulary": len(model.get("vocabulary", [])),
        "training": model.get("training", {}),
    }, indent=2))


if __name__ == "__main__":
    main()
