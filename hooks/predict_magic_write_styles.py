"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def predict_magic_write_styles(
    text: str,
    model: dict[str, Any],
    count: int = 12,
    mood: str | None = None,
) -> list[dict[str, Any]]:
    """Predict ranked style records for input text using a saved ML model."""
    tokens = _ml_tokens(f"{text} {mood or ''}")
    labels = [str(label) for label in model.get("labels", [])]
    class_log_prior = model.get("class_log_prior") if isinstance(model.get("class_log_prior"), dict) else {}
    feature_log_prob = model.get("feature_log_prob") if isinstance(model.get("feature_log_prob"), dict) else {}
    default_log_prob = model.get("default_log_prob") if isinstance(model.get("default_log_prob"), dict) else {}
    style_lookup = model.get("style_lookup") if isinstance(model.get("style_lookup"), dict) else {}
    scores: list[tuple[float, str]] = []
    for label in labels:
        score = float(class_log_prior.get(label, -9999.0))
        label_features = feature_log_prob.get(label) if isinstance(feature_log_prob.get(label), dict) else {}
        fallback = float(default_log_prob.get(label, -20.0))
        for token in tokens:
            score += float(label_features.get(token, fallback))
        scores.append((score, label))
    scores.sort(key=lambda item: item[0], reverse=True)
    selected: list[dict[str, Any]] = []
    for _, label in scores[:max(count, 1)]:
        style = style_lookup.get(label)
        if isinstance(style, dict):
            selected.append(deepcopy(style))
    return selected


__all__ = ["predict_magic_write_styles"]
