"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _tighten_composition_children(children: list[dict[str, Any]], canvas_height: int) -> list[dict[str, Any]]:
    if not children:
        return children
    ordered = sorted((deepcopy(child) for child in children), key=lambda child: int(child.get("zIndex") or 0))
    visible_text_children = [child for child in ordered if str(child.get("text") or "").strip()]
    primary_text_children = [
        child
        for child in visible_text_children
        if str(child.get("magicWriteRole") or "") != "middle"
    ]
    if len(primary_text_children) >= 2:
        sizes = [float(child.get("fontSize") or 36) for child in primary_text_children]
        balanced = _clamp_number(sum(sizes) / len(sizes), 42, 34, 54)
        for child in primary_text_children:
            child["fontSize"] = balanced
            child["height"] = max(float(child.get("height") or balanced), balanced + 8)
        visual_heights = [_text_visual_height_for_child(child) for child in primary_text_children]
        target_visual_h = max(visual_heights or [balanced])
        for child, visual_h in zip(primary_text_children, visual_heights):
            if visual_h > 0:
                child["fontSize"] = _clamp_number(
                    float(child.get("fontSize") or balanced) * (target_visual_h / visual_h),
                    balanced,
                    26,
                    58,
                )
                child["height"] = max(float(child.get("height") or 0), float(child["fontSize"]) + 8)
        for child in visible_text_children:
            if str(child.get("magicWriteRole") or "") == "middle":
                middle_size = _clamp_number(balanced * 0.72, 30, 24, 38)
                child["fontSize"] = middle_size
                child["height"] = max(float(child.get("height") or middle_size), middle_size + 6)

    compact: list[dict[str, Any]] = []
    for child in ordered:
        text = str(child.get("text") or "")
        lines = text.splitlines() or [text]
        font_size = float(child.get("fontSize") or 36)
        line_height = float(child.get("lineHeight") or 1.0)
        natural_h = max(len(lines) * font_size * line_height, font_size)
        shadow_pad = float(child.get("shadowBlur") or 0) * 1.4
        child["height"] = min(float(child.get("height") or natural_h), natural_h + 8 + shadow_pad)
        compact.append(child)

    gaps: list[float] = []
    for current, next_child in zip(compact, compact[1:]):
        current_role = str(current.get("magicWriteRole") or "")
        next_role = str(next_child.get("magicWriteRole") or "")
        if current_role == "top" and next_role == "middle":
            gaps.append(2)
        elif current_role == "middle" and next_role == "main":
            gaps.append(0)
        elif current_role in {"script", "serif", "sub"} and next_role == "main":
            gaps.append(-2)
        else:
            gaps.append(4)

    total_h = sum(float(child.get("height") or 0) for child in compact) + sum(gaps)
    y = (canvas_height - total_h) / 2
    for index, child in enumerate(compact):
        child["y"] = float(y)
        y += float(child.get("height") or 0)
        if index < len(gaps):
            y += gaps[index]
    return compact


__all__ = ["_tighten_composition_children"]
