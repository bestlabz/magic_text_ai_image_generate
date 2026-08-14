"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def render_preview_data_uri(text_obj: dict[str, Any], canvas_width: int = DEFAULT_CANVAS_WIDTH,
                            canvas_height: int = DEFAULT_CANVAS_HEIGHT,
                            scale: int = DEFAULT_PREVIEW_SCALE) -> str:
    if text_obj.get("type") == "Group" or text_obj.get("children"):
        return _render_group_preview_data_uri(text_obj, canvas_width, canvas_height, scale)
    layout = str(text_obj.get("magicWriteLayout") or "stacked").lower()
    if layout in {"sale", "title_heading", "coming_soon", "signature", "glow_signature", "arc"}:
        return _render_modern_preview_data_uri(text_obj, canvas_width, canvas_height, scale)

    width = canvas_width * scale
    height = canvas_height * scale
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    obj = deepcopy(text_obj)
    font_size = float(obj.get("fontSize", 36)) * scale
    lines = str(obj.get("text", "")).splitlines() or [str(obj.get("text", ""))]
    letter_spacing = float(obj.get("letterSpacing") or 0) * scale
    draw = ImageDraw.Draw(img)

    box_x = float(obj.get("x", 0)) * scale
    box_y = float(obj.get("y", 0)) * scale
    box_w = float(obj.get("width", canvas_width)) * scale
    box_h = float(obj.get("height", canvas_height)) * scale
    safe_box_w = max(min(box_w, width - 72 * scale), 1)
    fill = obj.get("fill") or "#111111"
    stroke = obj.get("stroke") or ""
    stroke_width = float(obj.get("strokeWidth") or 0) * scale
    shadow = obj.get("shadowColor") or ""
    align = obj.get("align") or obj.get("textAlign") or "center"
    italic = str(obj.get("fontStyle") or "").lower() == "italic"
    fitted_size = _fit_font_size_for_lines(
        lines,
        obj.get("fontFamily", "Arial"),
        font_size,
        safe_box_w,
        max(box_h, 1),
        obj.get("fontWeight"),
        italic,
        letter_spacing,
        float(obj.get("lineHeight") or 1.0),
        8 * scale,
    )
    font = _load_font(obj.get("fontFamily", "Arial"), fitted_size, obj.get("fontWeight"), italic)
    line_height = float(obj.get("lineHeight") or 1.0) * fitted_size

    content_h = len(lines) * line_height
    y = box_y + max((box_h - content_h) / 2, 0)
    text_positions: list[tuple[str, float, float, float]] = []
    for line in lines:
        line_w = _line_width(draw, line, font, letter_spacing)
        if align == "left":
            x = box_x
        elif align == "right":
            x = box_x + box_w - line_w
        else:
            x = box_x + (box_w - line_w) / 2
        text_positions.append((line, x, y, line_w))
        y += line_height

    if shadow:
        shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        for line, x, y, _ in text_positions:
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
        img.alpha_composite(shadow_layer)

    text_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    for line, x, y, _ in text_positions:
        _draw_text_with_spacing(text_layer, (x, y), line, font, fill, letter_spacing, stroke, stroke_width)
    img.alpha_composite(text_layer)

    decoration = str(obj.get("textDecoration") or "").lower()
    if decoration in {"underline", "line-through"}:
        draw = ImageDraw.Draw(img)
        for _, x, y, line_w in text_positions:
            offset = font_size * (0.82 if decoration == "underline" else 0.48)
            line_y = y + offset
            draw.line((x, line_y, x + line_w, line_y), fill=fill, width=max(1, int(font_size * 0.05)))

    rotation = float(obj.get("rotation") or 0)
    if abs(rotation) > 0.01:
        img = img.rotate(rotation, resample=Image.Resampling.BICUBIC, expand=False, fillcolor=(0, 0, 0, 0))

    img = _trim_transparent_preview(img, scale)
    out = io.BytesIO()
    img.save(out, format="PNG")
    return "data:image/png;base64," + base64.b64encode(out.getvalue()).decode("ascii")


__all__ = ["render_preview_data_uri"]
