"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _konva_text(text: str, style: dict[str, Any], z_index: int, canvas_width: int, canvas_height: int) -> dict[str, Any]:
    raw_text = text
    layout = _adaptive_modern_layout(style, raw_text)
    if layout in {"sale", "title_heading", "coming_soon", "signature", "glow_signature", "arc"}:
        text = raw_text
    else:
        text = _apply_text_transform(raw_text, style.get("textTransform"))
    fill = _clean_hex(style.get("fill"), "#111111")
    stroke = _clean_hex(style.get("stroke"), "")
    shadow = _clean_hex(style.get("shadowColor"), "")
    decoration = str(style.get("textDecoration") or "").strip().lower()
    if decoration not in {"", "underline", "line-through"}:
        decoration = ""
    font_style = str(style.get("fontStyle") or "normal").strip().lower()
    if font_style not in {"normal", "italic"}:
        font_style = "normal"
    align = str(style.get("align") or style.get("textAlign") or "center").strip().lower()
    if align not in {"left", "center", "right"}:
        align = "center"

    stroke_width = _clamp_number(style.get("strokeWidth"), 0, 0, 8) if stroke else 0
    obj = {
        "id": f"text_{uuid.uuid4()}",
        "type": "Text",
        "x": 50.0,
        "y": 154.0,
        "width": canvas_width - 100,
        "height": 112,
        "scaleX": 1,
        "scaleY": 1,
        "rotation": 0,
        "opacity": 1,
        "draggable": True,
        "zIndex": z_index,
        "text": text,
        "fontSize": _clamp_number(style.get("fontSize"), 36, 8, 96),
        "fontFamily": str(style.get("fontFamily") or "Arial").strip()[:80] or "Arial",
        "fontWeight": str(style.get("fontWeight") or "normal").strip()[:20] or "normal",
        "fontStyle": font_style,
        "fill": fill,
        "align": align,
        "textAlign": align,
        "wrap": "none",
        "letterSpacing": _clamp_number(style.get("letterSpacing"), 0, -1, 6),
        "lineHeight": _clamp_number(style.get("lineHeight"), 1.0, 0.75, 1.5),
        "padding": 0,
        "textDecoration": decoration,
        "shadowColor": shadow,
        "shadowBlur": _clamp_number(style.get("shadowBlur"), 0, 0, 30),
        "shadowOffsetX": _clamp_number(style.get("shadowOffsetX"), 0, -20, 20),
        "shadowOffsetY": _clamp_number(style.get("shadowOffsetY"), 0, -20, 20),
        "stroke": stroke,
        "strokeWidth": stroke_width,
        "ellipsis": False,
        "listening": True,
        "magicWriteStyle": str(style.get("name") or ""),
        "magicWriteCategory": str(style.get("category") or ""),
        "magicWriteLayout": layout,
        "textTransform": str(style.get("textTransform") or "none"),
        "accentFill": _clean_hex(style.get("accentFill"), ""),
    }
    return _fit_text_box(obj, canvas_width, canvas_height)


__all__ = ["_konva_text"]
