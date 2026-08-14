"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _polish_export_text_shadow(text_obj: dict[str, Any]) -> dict[str, Any]:
    obj = deepcopy(text_obj)
    fill = _clean_hex(obj.get("fill"), "#111111")
    shadow = _clean_hex(obj.get("shadowColor"), "")
    stroke = _clean_hex(obj.get("stroke"), "")
    blur = float(obj.get("shadowBlur") or 0)
    offset_x = float(obj.get("shadowOffsetX") or 0)
    offset_y = float(obj.get("shadowOffsetY") or 0)
    kind = _font_kind(str(obj.get("fontFamily") or ""))
    luminance = _hex_luminance(fill)

    if not shadow or blur <= 0 and abs(offset_x) <= 0.01 and abs(offset_y) <= 0.01:
        return obj

    if kind == "script":
        obj["shadowColor"] = fill if luminance < 0.72 else (stroke or "#D8A919")
        obj["shadowBlur"] = min(blur, 3.0)
        obj["shadowOffsetX"] = _clamp_number(offset_x, 0, -1.4, 1.4)
        obj["shadowOffsetY"] = _clamp_number(offset_y, 0, -1.4, 1.8)
        if luminance > 0.76 and not stroke:
            obj["stroke"] = "#FFFFFF"
            obj["strokeWidth"] = max(float(obj.get("strokeWidth") or 0), 0.7)
        return obj

    if kind == "serif":
        obj["shadowBlur"] = min(blur, 2.8)
        obj["shadowOffsetX"] = _clamp_number(offset_x, 0, -1.8, 1.8)
        obj["shadowOffsetY"] = _clamp_number(offset_y, 0, -1.8, 2.6)
        return obj

    if blur > 6:
        obj["shadowBlur"] = 4.0
        obj["shadowOffsetX"] = _clamp_number(offset_x, 0, -2.0, 2.0)
        obj["shadowOffsetY"] = _clamp_number(offset_y, 0, -2.0, 2.4)
    elif blur > 0:
        obj["shadowBlur"] = min(blur, 3.2)

    return obj


__all__ = ["_polish_export_text_shadow"]
