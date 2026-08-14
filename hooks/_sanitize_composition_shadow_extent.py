"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _sanitize_composition_shadow_extent(children: list[dict[str, Any]]) -> list[dict[str, Any]]:
    adjusted = deepcopy(children)
    for child in adjusted:
        if not isinstance(child, dict) or child.get("type") != "Text":
            continue
        shadow = _clean_hex(child.get("shadowColor"), "")
        if not shadow:
            continue
        blur = float(child.get("shadowBlur") or 0)
        offset_x = float(child.get("shadowOffsetX") or 0)
        offset_y = float(child.get("shadowOffsetY") or 0)
        shadow_is_dark = _hex_luminance(shadow) < 0.18
        max_blur = 3.0 if shadow_is_dark else 6.0
        child["shadowBlur"] = min(blur, max_blur)
        child["shadowOffsetX"] = _clamp_number(offset_x, 0, -3.0, 3.0)
        child["shadowOffsetY"] = _clamp_number(offset_y, 0, -3.0, 3.0)
    return adjusted


__all__ = ["_sanitize_composition_shadow_extent"]
