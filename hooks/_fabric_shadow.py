"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _fabric_shadow(text_obj: dict[str, Any]) -> dict[str, Any] | None:
    shadow = _clean_hex(text_obj.get("shadowColor"), "")
    if not shadow:
        return None
    blur = float(text_obj.get("shadowBlur") or 0)
    offset_x = float(text_obj.get("shadowOffsetX") or 0)
    offset_y = float(text_obj.get("shadowOffsetY") or 0)
    if blur <= 0 and abs(offset_x) <= 0.01 and abs(offset_y) <= 0.01:
        return None
    return {
        "color": shadow,
        "blur": blur,
        "offsetX": offset_x,
        "offsetY": offset_y,
        "affectStroke": False,
        "nonScaling": False,
    }


__all__ = ["_fabric_shadow"]
