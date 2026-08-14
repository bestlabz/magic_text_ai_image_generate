"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _fit_composition_children_to_canvas(
    children: list[dict[str, Any]],
    canvas_width: int,
    canvas_height: int,
) -> list[dict[str, Any]]:
    fitted = deepcopy(children)
    bbox = _composition_alpha_bbox(fitted, canvas_width, canvas_height)
    if not bbox:
        return fitted

    left, top, right, bottom = bbox
    bbox_w = max(right - left, 1)
    bbox_h = max(bottom - top, 1)
    min_w = canvas_width * 0.72
    min_h = canvas_height * 0.26
    max_w = canvas_width * 0.90
    max_h = canvas_height * 0.64

    max_fit = min(max_w / bbox_w, max_h / bbox_h)
    is_very_wide = bbox_w / bbox_h > 5.2
    effective_min_h = canvas_height * (0.20 if is_very_wide else 0.26)
    grow = max(min_w / bbox_w, effective_min_h / bbox_h, 1.0)
    factor = min(grow, max_fit, 1.9) if grow > 1.0 else min(max_fit, 1.0)
    if factor > 1.01 or factor < 0.99:
        origin = ((left + right) / 2, (top + bottom) / 2)
        for child in fitted:
            if isinstance(child, dict) and child.get("type") == "Text":
                _scale_child_geometry(child, origin, factor)

    bbox = _composition_alpha_bbox(fitted, canvas_width, canvas_height)
    if not bbox:
        return fitted
    left, top, right, bottom = bbox
    target_cx = canvas_width / 2
    target_cy = canvas_height / 2
    dx = target_cx - (left + right) / 2
    dy = target_cy - (top + bottom) / 2
    pad = canvas_width * 0.04
    if left + dx < pad:
        dx += pad - (left + dx)
    if right + dx > canvas_width - pad:
        dx -= (right + dx) - (canvas_width - pad)
    if top + dy < pad:
        dy += pad - (top + dy)
    if bottom + dy > canvas_height - pad:
        dy -= (bottom + dy) - (canvas_height - pad)
    for child in fitted:
        if isinstance(child, dict) and child.get("type") == "Text":
            _shift_child_geometry(child, dx, dy)

    return fitted


__all__ = ["_fit_composition_children_to_canvas"]
