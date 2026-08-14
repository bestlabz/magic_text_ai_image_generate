"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _draw_text_object_on_layer(img: Image.Image, obj: dict[str, Any], scale: int) -> None:
    lines = str(obj.get("text", "")).splitlines() or [str(obj.get("text", ""))]
    letter_spacing = float(obj.get("letterSpacing") or 0) * scale
    box_x = float(obj.get("x", 0)) * scale
    box_y = float(obj.get("y", 0)) * scale
    box_w = float(obj.get("width", img.size[0] / scale)) * scale
    box_h = float(obj.get("height", img.size[1] / scale)) * scale
    fill = obj.get("fill") or "#111111"
    stroke = obj.get("stroke") or ""
    stroke_width = float(obj.get("strokeWidth") or 0) * scale
    shadow = obj.get("shadowColor") or ""
    align = obj.get("align") or obj.get("textAlign") or "center"
    italic = str(obj.get("fontStyle") or "").lower() == "italic"
    font_size = float(obj.get("fontSize", 36)) * scale
    fitted_size = _fit_font_size_for_lines(
        lines,
        obj.get("fontFamily", "Arial"),
        font_size,
        max(box_w, 1),
        max(box_h, 1),
        obj.get("fontWeight"),
        italic,
        letter_spacing,
        float(obj.get("lineHeight") or 1.0),
        7 * scale,
    )
    font = _load_font(obj.get("fontFamily", "Arial"), fitted_size, obj.get("fontWeight"), italic)
    draw = ImageDraw.Draw(img)
    line_height = float(obj.get("lineHeight") or 1.0) * fitted_size
    content_h = len(lines) * line_height
    y = box_y + max((box_h - content_h) / 2, 0)
    positions: list[tuple[str, float, float, float]] = []
    for line in lines:
        line_w = _line_width(draw, line, font, letter_spacing)
        if align == "left":
            x = box_x
        elif align == "right":
            x = box_x + box_w - line_w
        else:
            x = box_x + (box_w - line_w) / 2
        positions.append((line, x, y, line_w))
        y += line_height

    target = img
    rotation = float(obj.get("rotation") or 0)
    if abs(rotation) > 0.01:
        target = Image.new("RGBA", img.size, (0, 0, 0, 0))

    if shadow:
        shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        for line, x, y, _ in positions:
            _draw_text_with_spacing(
                shadow_layer,
                (x + float(obj.get("shadowOffsetX") or 0) * scale, y + float(obj.get("shadowOffsetY") or 0) * scale),
                line,
                font,
                shadow,
                letter_spacing,
                shadow,
                stroke_width,
            )
        blur = float(obj.get("shadowBlur") or 0) * scale
        if blur:
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=blur))
        target.alpha_composite(shadow_layer)

    text_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    for line, x, y, _ in positions:
        _draw_text_with_spacing(text_layer, (x, y), line, font, fill, letter_spacing, stroke, stroke_width)
    target.alpha_composite(text_layer)

    decoration = str(obj.get("textDecoration") or "").lower()
    if decoration in {"underline", "line-through"}:
        draw = ImageDraw.Draw(target)
        for _, x, y, line_w in positions:
            offset = fitted_size * (0.82 if decoration == "underline" else 0.48)
            line_y = y + offset
            draw.line((x, line_y, x + line_w, line_y), fill=fill, width=max(1, int(fitted_size * 0.05)))

    if target is not img:
        target = target.rotate(rotation, resample=Image.Resampling.BICUBIC, expand=False)
        img.alpha_composite(target)


__all__ = ["_draw_text_object_on_layer"]
