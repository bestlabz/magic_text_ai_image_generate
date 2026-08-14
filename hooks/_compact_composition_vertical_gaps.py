"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _compact_composition_vertical_gaps(
    children: list[dict[str, Any]],
    canvas_width: int,
    canvas_height: int,
) -> list[dict[str, Any]]:
    compact = deepcopy(children)
    text_children = [child for child in compact if isinstance(child, dict) and child.get("type") == "Text"]
    if len(text_children) < 2:
        return compact

    ordered = sorted(text_children, key=lambda child: (float(child.get("y") or 0), int(child.get("zIndex") or 0)))
    max_gap = max(canvas_height * 0.035, 6)
    for index in range(len(ordered) - 1):
        current_plain = deepcopy(ordered[index])
        next_plain = deepcopy(ordered[index + 1])
        for plain in (current_plain, next_plain):
            plain["shadowColor"] = ""
            plain["shadowBlur"] = 0
            plain["shadowOffsetX"] = 0
            plain["shadowOffsetY"] = 0
        current_bbox = _composition_alpha_bbox([current_plain], canvas_width, canvas_height)
        next_bbox = _composition_alpha_bbox([next_plain], canvas_width, canvas_height)
        if not current_bbox or not next_bbox:
            continue
        gap = next_bbox[1] - current_bbox[3]
        if gap <= max_gap:
            continue
        shift = gap - max_gap
        for follower in ordered[index + 1:]:
            follower["y"] = float(follower.get("y") or 0) - shift
    return compact


__all__ = ["_compact_composition_vertical_gaps"]
