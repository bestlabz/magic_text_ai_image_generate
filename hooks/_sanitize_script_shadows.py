"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _sanitize_script_shadows(children: list[dict[str, Any]]) -> list[dict[str, Any]]:
    adjusted = deepcopy(children)
    for child in adjusted:
        if not isinstance(child, dict) or child.get("type") != "Text":
            continue
        if child.get("magicWriteKeepDuplicate"):
            continue
        role = str(child.get("magicWriteRole") or "").lower()
        family = str(child.get("fontFamily") or "")
        is_script = role == "script" or _font_kind(family) == "script"
        if not is_script:
            continue

        offset_x = float(child.get("shadowOffsetX") or 0)
        offset_y = float(child.get("shadowOffsetY") or 0)
        blur = float(child.get("shadowBlur") or 0)
        if abs(offset_x) <= 0.01 and abs(offset_y) <= 0.01:
            continue

        child["shadowBlur"] = min(max(blur, 0.6), 2.0)
        child["shadowOffsetX"] = _clamp_number(offset_x, 0, -1.8, 1.8)
        child["shadowOffsetY"] = _clamp_number(offset_y, 0, -1.8, 2.2)
        child["strokeWidth"] = min(float(child.get("strokeWidth") or 0), 2.2)
    return adjusted


__all__ = ["_sanitize_script_shadows"]
