"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _canva_text_element(text_obj: dict[str, Any], z_index: int) -> dict[str, Any]:
    decoration = str(text_obj.get("textDecoration") or "").strip().lower()
    stroke = _clean_hex(text_obj.get("stroke"), "")
    shadow = _canva_shadow(text_obj)
    return {
        "id": str(text_obj.get("id") or f"text_{z_index}"),
        "type": "text",
        "text": str(text_obj.get("text") or ""),
        "position": {
            "x": float(text_obj.get("x") or 0),
            "y": float(text_obj.get("y") or 0),
        },
        "size": {
            "width": float(text_obj.get("width") or 0),
            "height": float(text_obj.get("height") or 0),
        },
        "transform": {
            "rotation": float(text_obj.get("rotation") or 0),
            "scaleX": float(text_obj.get("scaleX") or 1),
            "scaleY": float(text_obj.get("scaleY") or 1),
            "opacity": float(text_obj.get("opacity") or 1),
        },
        "style": {
            "fontFamily": str(text_obj.get("fontFamily") or "Arial"),
            "fontSize": float(text_obj.get("fontSize") or 36),
            "fontWeight": str(text_obj.get("fontWeight") or "normal"),
            "fontStyle": str(text_obj.get("fontStyle") or "normal"),
            "color": _clean_hex(text_obj.get("fill"), "#111111"),
            "textAlign": str(text_obj.get("textAlign") or text_obj.get("align") or "center"),
            "lineHeight": float(text_obj.get("lineHeight") or 1),
            "letterSpacing": float(text_obj.get("letterSpacing") or 0),
            "underline": decoration == "underline",
            "linethrough": decoration == "line-through",
        },
        "effects": {
            "stroke": {
                "color": stroke,
                "width": float(text_obj.get("strokeWidth") or 0) if stroke else 0,
            },
            "shadow": shadow,
        },
        "layer": {
            "zIndex": z_index,
            "visible": True,
            "locked": False,
        },
    }


__all__ = ["_canva_text_element"]
