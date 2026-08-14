"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _fit_text_box(text_obj: dict[str, Any], canvas_width: int, canvas_height: int) -> dict[str, Any]:
    obj = deepcopy(text_obj)
    lines = str(obj["text"]).splitlines() or [str(obj["text"])]
    font_size = float(obj["fontSize"])
    spacing = float(obj.get("letterSpacing") or 0)
    line_height = float(obj.get("lineHeight") or 1.0)
    draw = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    max_width = canvas_width - 100
    max_height = canvas_height - 80

    while font_size > 8:
        font = _load_font(
            obj["fontFamily"],
            font_size,
            obj.get("fontWeight"),
            str(obj.get("fontStyle") or "").lower() == "italic",
        )
        widths = [_line_width(draw, line, font, spacing) for line in lines]
        total_h = len(lines) * font_size * line_height
        if (max(widths or [0]) <= max_width) and total_h <= max_height:
            break
        font_size *= 0.94

    obj["fontSize"] = font_size
    obj["width"] = min(max_width, max(max(widths or [0]), 80) + 24)
    obj["height"] = max(len(lines) * font_size * line_height + 12, font_size + 12)
    obj["x"] = (canvas_width - obj["width"]) / 2
    obj["y"] = (canvas_height - obj["height"]) / 2
    return obj


__all__ = ["_fit_text_box"]
