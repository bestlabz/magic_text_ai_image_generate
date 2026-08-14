"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _strengthen_transparent_text_contrast(children: list[dict[str, Any]]) -> list[dict[str, Any]]:
    adjusted = deepcopy(children)
    for child in adjusted:
        if not isinstance(child, dict) or child.get("type") != "Text":
            continue
        fill = _clean_hex(child.get("fill"), "#111111")
        stroke = _clean_hex(child.get("stroke"), "")
        stroke_width = float(child.get("strokeWidth") or 0)
        shadow = _clean_hex(child.get("shadowColor"), "")
        shadow_blur = float(child.get("shadowBlur") or 0)
        has_edge = bool(stroke and stroke_width >= 0.8) or bool(shadow and shadow_blur >= 3)
        if has_edge:
            continue

        luminance = _hex_luminance(fill)
        if luminance < 0.28:
            continue
        elif luminance > 0.82:
            child["stroke"] = "#1F2937"
            child["strokeWidth"] = max(stroke_width, 0.9)
            child["shadowColor"] = "#1F2937"
            child["shadowBlur"] = max(shadow_blur, 1.2)
            child["shadowOffsetX"] = max(float(child.get("shadowOffsetX") or 0), 1.0)
            child["shadowOffsetY"] = max(float(child.get("shadowOffsetY") or 0), 1.4)
    return adjusted


__all__ = ["_strengthen_transparent_text_contrast"]
