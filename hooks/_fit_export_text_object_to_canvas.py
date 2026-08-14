"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _fit_export_text_object_to_canvas(
    text_obj: dict[str, Any],
    canvas_width: int,
    canvas_height: int,
) -> dict[str, Any]:
    obj = deepcopy(text_obj)
    lines = str(obj.get("text") or "").splitlines() or [str(obj.get("text") or "")]
    spacing = float(obj.get("letterSpacing") or 0)
    line_height = float(obj.get("lineHeight") or 1.0)
    italic = str(obj.get("fontStyle") or "").lower() == "italic"
    max_width = canvas_width * 0.88
    max_height = canvas_height * 0.58
    fitted_size = _fit_font_size_for_lines(
        lines,
        obj.get("fontFamily", "Arial"),
        float(obj.get("fontSize") or 36),
        max_width - 24,
        max_height - 12,
        obj.get("fontWeight"),
        italic,
        spacing,
        line_height,
        8,
    )
    font = _load_font(obj.get("fontFamily", "Arial"), fitted_size, obj.get("fontWeight"), italic)
    draw = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    widths = [_line_width(draw, line, font, spacing) for line in lines]
    width = min(max_width, max(max(widths or [0]), 80) + 24)
    height = max(len(lines) * fitted_size * line_height + 12, fitted_size + 12)
    old_cx = float(obj.get("x") or 0) + float(obj.get("width") or width) / 2
    old_cy = float(obj.get("y") or 0) + float(obj.get("height") or height) / 2
    pad = canvas_width * 0.04
    obj["fontSize"] = fitted_size
    obj["width"] = width
    obj["height"] = height
    obj["x"] = _clamp_number(old_cx - width / 2, (canvas_width - width) / 2, pad, canvas_width - pad - width)
    obj["y"] = _clamp_number(old_cy - height / 2, (canvas_height - height) / 2, pad, canvas_height - pad - height)
    return obj


__all__ = ["_fit_export_text_object_to_canvas"]
