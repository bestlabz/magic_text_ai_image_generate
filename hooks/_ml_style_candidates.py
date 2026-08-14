"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _ml_style_candidates(
    text: str,
    count: int,
    mood: str | None,
    ml_model_path: str | os.PathLike[str],
    randomize_fonts: bool,
    randomize_designs: bool,
    rng: random.Random,
) -> list[dict[str, Any]]:
    model = load_magic_write_ml_model(ml_model_path)
    predicted = predict_magic_write_styles(
        text,
        model,
        count=max(count * 4, count + 24, 1),
        mood=mood,
    )
    if not predicted:
        return _style_candidates(text, count, mood, randomize_fonts, randomize_designs, rng)
    used_fonts: set[str] = set()
    used_designs: set[tuple[Any, ...]] = set()
    seen_visuals: set[tuple[Any, ...]] = set()
    styles: list[dict[str, Any]] = []
    candidate_index = 0
    max_candidates = max(count * 40, len(predicted) * 8)
    while len(styles) < count and candidate_index < max_candidates:
        base = deepcopy(predicted[candidate_index % len(predicted)])
        style = _variant_from_preset(base, candidate_index // len(predicted))
        if randomize_fonts:
            style = _randomize_style_font(style, rng, used_fonts)
        if randomize_designs:
            style = _apply_random_design(style, rng, candidate_index, used_designs)
        signature = _style_visual_signature(style)
        if signature not in seen_visuals:
            seen_visuals.add(signature)
            styles.append(style)
        candidate_index += 1

    if len(styles) < count:
        for fallback in _style_candidates(
            text,
            count - len(styles),
            mood,
            randomize_fonts=True,
            randomize_designs=True,
            rng=rng,
        ):
            signature = _style_visual_signature(fallback)
            if signature in seen_visuals:
                continue
            seen_visuals.add(signature)
            styles.append(fallback)
            if len(styles) >= count:
                break
    return styles


__all__ = ["_ml_style_candidates"]
