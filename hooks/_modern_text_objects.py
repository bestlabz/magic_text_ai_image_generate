"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _modern_text_objects(
    text: str,
    count: int | None,
    canvas_width: int,
    canvas_height: int,
    rng: random.Random,
    randomize_designs: bool = True,
) -> list[dict[str, Any]]:
    requested = count or len(MODERN_TEXT_EXPORT_STYLES)
    objects: list[dict[str, Any]] = []
    used_signatures: set[tuple[Any, ...]] = set()
    max_candidates = max(requested * 40, requested + 256)
    candidate_indices = list(range(max_candidates))
    if randomize_designs:
        rng.shuffle(candidate_indices)
    for candidate_index in candidate_indices:
        if len(objects) >= requested:
            break
        style = _modern_text_style_for_index(candidate_index)
        styled_text = _apply_text_transform(text, style.get("textTransform"))
        obj = _layer_text(
            styled_text,
            style,
            z_index=len(objects) + 1,
            x=canvas_width * 0.08,
            y=canvas_height * 0.36,
            width=canvas_width * 0.84,
            height=canvas_height * 0.24,
        )
        obj = _polish_export_text_shadow(obj)
        obj = _fit_export_text_object_to_canvas(obj, canvas_width, canvas_height)
        signature = _modern_text_signature(obj)
        if signature in used_signatures:
            continue
        used_signatures.add(signature)
        objects.append(obj)
    return objects


__all__ = ["_modern_text_objects"]
