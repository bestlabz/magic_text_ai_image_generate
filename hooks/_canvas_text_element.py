"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _canvas_text_element(text_obj: dict[str, Any], z_index: int) -> dict[str, Any]:
    decoration = str(text_obj.get("textDecoration") or "").strip().lower()
    stroke = _clean_hex(text_obj.get("stroke"), "")
    align = str(text_obj.get("textAlign") or text_obj.get("align") or "center")
    return {
        "id": str(text_obj.get("id") or f"text_{z_index}"),
        "type": "text",
        "zIndex": z_index,
        "text": str(text_obj.get("text") or ""),
        "x": float(text_obj.get("x") or 0),
        "y": float(text_obj.get("y") or 0),
        "width": float(text_obj.get("width") or 0),
        "height": float(text_obj.get("height") or 0),
        "rotation": float(text_obj.get("rotation") or 0),
        "scaleX": float(text_obj.get("scaleX") or 1),
        "scaleY": float(text_obj.get("scaleY") or 1),
        "opacity": float(text_obj.get("opacity") or 1),
        "font": {
            "family": str(text_obj.get("fontFamily") or "Arial"),
            "size": float(text_obj.get("fontSize") or 36),
            "weight": str(text_obj.get("fontWeight") or "normal"),
            "style": str(text_obj.get("fontStyle") or "normal"),
            "lineHeight": float(text_obj.get("lineHeight") or 1),
            "css": _canvas_font_css(text_obj),
        },
        "fillStyle": _clean_hex(text_obj.get("fill"), "#111111"),
        "strokeStyle": stroke or None,
        "lineWidth": float(text_obj.get("strokeWidth") or 0) if stroke else 0,
        "textAlign": align,
        "textBaseline": "top",
        "letterSpacing": float(text_obj.get("letterSpacing") or 0),
        "shadow": _canvas_shadow(text_obj),
        "decoration": {
            "underline": decoration == "underline",
            "lineThrough": decoration == "line-through",
        },
        "draggable": bool(text_obj.get("draggable", True)),
        "visible": bool(text_obj.get("visible", True)),
    }


__all__ = ["_canvas_text_element"]
