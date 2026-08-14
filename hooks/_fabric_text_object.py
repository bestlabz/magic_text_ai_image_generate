"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _fabric_text_object(text_obj: dict[str, Any]) -> dict[str, Any]:
    decoration = str(text_obj.get("textDecoration") or "").strip().lower()
    shadow = _fabric_shadow(text_obj)
    fabric_obj = {
        "type": "text",
        "version": FABRIC_JSON_VERSION,
        "originX": "left",
        "originY": "top",
        "left": float(text_obj.get("x") or 0),
        "top": float(text_obj.get("y") or 0),
        "width": float(text_obj.get("width") or 0),
        "height": float(text_obj.get("height") or 0),
        "fill": _clean_hex(text_obj.get("fill"), "#111111"),
        "stroke": _clean_hex(text_obj.get("stroke"), "") or None,
        "strokeWidth": float(text_obj.get("strokeWidth") or 0),
        "strokeDashArray": None,
        "strokeLineCap": "butt",
        "strokeDashOffset": 0,
        "strokeLineJoin": "miter",
        "strokeUniform": False,
        "strokeMiterLimit": 4,
        "scaleX": float(text_obj.get("scaleX") or 1),
        "scaleY": float(text_obj.get("scaleY") or 1),
        "angle": float(text_obj.get("rotation") or 0),
        "flipX": False,
        "flipY": False,
        "opacity": float(text_obj.get("opacity") or 1),
        "shadow": shadow,
        "visible": True,
        "backgroundColor": "",
        "fillRule": "nonzero",
        "paintFirst": "fill",
        "globalCompositeOperation": "source-over",
        "skewX": 0,
        "skewY": 0,
        "fontFamily": str(text_obj.get("fontFamily") or "Arial"),
        "fontWeight": str(text_obj.get("fontWeight") or "normal"),
        "fontSize": float(text_obj.get("fontSize") or 36),
        "text": str(text_obj.get("text") or ""),
        "underline": decoration == "underline",
        "overline": False,
        "linethrough": decoration == "line-through",
        "textAlign": str(text_obj.get("textAlign") or text_obj.get("align") or "center"),
        "fontStyle": str(text_obj.get("fontStyle") or "normal"),
        "lineHeight": float(text_obj.get("lineHeight") or 1),
        "textBackgroundColor": "",
        "charSpacing": _fabric_char_spacing(text_obj),
        "styles": {},
        "direction": "ltr",
        "path": None,
        "pathStartOffset": 0,
        "pathSide": "left",
        "pathAlign": "baseline",
        "selectable": bool(text_obj.get("draggable", True)),
        "evented": bool(text_obj.get("listening", True)),
    }
    if fabric_obj["stroke"] is None:
        fabric_obj["strokeWidth"] = 0
    return fabric_obj


__all__ = ["_fabric_text_object"]
