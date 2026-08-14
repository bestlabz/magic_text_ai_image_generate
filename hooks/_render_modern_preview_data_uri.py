"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _render_modern_preview_data_uri(
    text_obj: dict[str, Any],
    canvas_width: int,
    canvas_height: int,
    scale: int,
) -> str:
    width = canvas_width * scale
    height = canvas_height * scale
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    obj = deepcopy(text_obj)
    layout = str(obj.get("magicWriteLayout") or "stacked").lower()
    lines = [line for line in str(obj.get("text", "")).splitlines() if line.strip()]
    if not lines:
        lines = [str(obj.get("text", ""))]

    family = obj.get("fontFamily", "Arial")
    fill = obj.get("fill") or "#111111"
    stroke = obj.get("stroke") or ""
    accent = obj.get("accentFill") or fill
    shadow = obj.get("shadowColor") or ""
    stroke_width = float(obj.get("strokeWidth") or 0) * scale
    shadow_blur = float(obj.get("shadowBlur") or 0) * scale
    shadow_offset = (
        float(obj.get("shadowOffsetX") or 0) * scale,
        float(obj.get("shadowOffsetY") or 0) * scale,
    )
    spacing = float(obj.get("letterSpacing") or 0) * scale
    safe_w = width - 72 * scale
    safe_h = height - 72 * scale

    if layout == "sale":
        main = lines[0] if lines else "30%"
        second = lines[1] if len(lines) > 1 else "OFF"
        third = " ".join(lines[2:]) if len(lines) > 2 else ""
        base = min(float(obj.get("fontSize", 64)) * 2.1, 96) * scale
        main_size = _fit_font_size_for_lines([main], family, base, safe_w * 0.58, safe_h, obj.get("fontWeight"), False, -2 * scale, 0.8, 18 * scale)
        tall_font = _load_font(family, main_size, obj.get("fontWeight"), False)
        off_size = max(main_size * 0.32, 14 * scale)
        off_font = _load_font("Montserrat", off_size, "bold", False)
        small_font = _load_font("Montserrat", max(off_size * 0.44, 8 * scale), "bold", False)
        main_w = _modern_line_width(main, tall_font, -2 * scale)
        group_w = main_w + 14 * scale + max(_modern_line_width(second, off_font, 0), _modern_line_width(third, small_font, 0))
        x = (width - group_w) / 2
        y = (height - main_size * 1.05) / 2
        _draw_text_with_spacing(img, (x + 3 * scale, y + 4 * scale), main, tall_font, "#CFCFCF", -2 * scale, "", 0)
        _draw_text_with_spacing(img, (x, y), main, tall_font, fill, -2 * scale, "", 0)
        right_x = x + main_w + 14 * scale
        _draw_text_with_spacing(img, (right_x, y + main_size * 0.36), second, off_font, accent, 0, "", 0)
        if third:
            _draw_text_with_spacing(img, (right_x, y + main_size * 0.72), third, small_font, "#777777", 0, "", 0)
    elif layout == "title_heading":
        first = lines[0] if lines else "Title"
        second = lines[1] if len(lines) > 1 else "HEADING"
        title_size = _fit_font_size_for_lines([first], family, 58 * scale, safe_w, safe_h * 0.62, "bold", False, -0.4 * scale, 0.9, 14 * scale)
        heading_size = min(title_size * 0.5, 28 * scale)
        heading_size = _fit_font_size_for_lines([second.upper()], "Montserrat", heading_size, safe_w, safe_h * 0.34, "bold", True, 0.8 * scale, 0.9, 10 * scale)
        title_font = _load_font(family, title_size, "bold", False)
        heading_font = _load_font("Montserrat", heading_size, "bold", True)
        y = (height - (title_size + heading_size + 12 * scale)) / 2
        _draw_centered_line(img, first, y, title_font, fill, -0.4 * scale)
        _draw_centered_line(img, second.upper(), y + title_size + 12 * scale, heading_font, fill, 0.8 * scale)
    elif layout == "coming_soon":
        main_lines = lines[:2] if len(lines) > 1 else [lines[0]]
        sub = lines[2] if len(lines) > 2 else "Stay Tuned"
        main_size = _fit_font_size_for_lines([line.upper() for line in main_lines], family, float(obj.get("fontSize", 44)) * scale, safe_w, safe_h * 0.72, obj.get("fontWeight"), True, 0.2 * scale, 0.92, 12 * scale)
        sub_size = min(main_size * 0.6, 26 * scale)
        main_font = _load_font(family, main_size, obj.get("fontWeight"), True)
        sub_font = _load_font("Great Vibes", sub_size, "normal", False)
        total_h = len(main_lines) * main_size * 0.92 + sub_size + 16 * scale
        y = (height - total_h) / 2
        for line in main_lines:
            _draw_centered_line(img, line.upper(), y, main_font, fill, 0.2 * scale)
            y += main_size * 0.92
        _draw_centered_line(img, sub, y + 8 * scale, sub_font, fill, 0)
    elif layout in {"signature", "glow_signature"}:
        fitted = _fit_font_size_for_lines(lines, family, float(obj.get("fontSize", 48)) * scale, safe_w, safe_h, obj.get("fontWeight"), False, spacing, 0.78, 10 * scale)
        font = _load_font(family, fitted, obj.get("fontWeight"), False)
        total_h = len(lines) * fitted * 0.78
        y = (height - total_h) / 2
        for line in lines:
            _draw_centered_line(
                img,
                line,
                y,
                font,
                fill,
                spacing,
                stroke,
                stroke_width,
                shadow,
                shadow_blur,
                shadow_offset,
            )
            y += fitted * 0.78
    elif layout == "arc":
        arc_line = lines[0].upper()
        sub = lines[1] if len(lines) > 1 else ""
        arc_size = _fit_font_size_for_lines([arc_line], family, 42 * scale, safe_w, safe_h * 0.5, obj.get("fontWeight"), False, 0, 1.0, 12 * scale)
        arc_font = _load_font(family, arc_size, obj.get("fontWeight"), False)
        sub_font = _load_font("Great Vibes", min(arc_size * 0.55, 22 * scale), "normal", False)
        _draw_arc_text(img, arc_line, (width / 2, height * 0.6), min(90 * scale, safe_w * 0.28), arc_font, fill)
        if sub:
            _draw_centered_line(img, sub, height * 0.55, sub_font, fill, 0)
    else:
        italic = str(obj.get("fontStyle") or "") == "italic"
        fitted = _fit_font_size_for_lines(lines, family, float(obj.get("fontSize", 40)) * scale, safe_w, safe_h, obj.get("fontWeight"), italic, spacing, float(obj.get("lineHeight") or 1), 10 * scale)
        font = _load_font(family, fitted, obj.get("fontWeight"), italic)
        total_h = len(lines) * fitted * float(obj.get("lineHeight") or 1)
        y = (height - total_h) / 2
        for line in lines:
            _draw_centered_line(img, line, y, font, fill, spacing, stroke, stroke_width, shadow, shadow_blur, shadow_offset)
            y += fitted * float(obj.get("lineHeight") or 1)

    img = _trim_transparent_preview(img, scale)
    out = io.BytesIO()
    img.save(out, format="PNG")
    return "data:image/png;base64," + base64.b64encode(out.getvalue()).decode("ascii")


__all__ = ["_render_modern_preview_data_uri"]
