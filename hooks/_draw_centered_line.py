"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _draw_centered_line(
    layer: Image.Image,
    text: str,
    y: float,
    font: ImageFont.ImageFont,
    fill: str,
    spacing: float = 0,
    stroke: str = "",
    stroke_width: float = 0,
    shadow: str = "",
    shadow_blur: float = 0,
    shadow_offset: tuple[float, float] = (0, 0),
) -> float:
    width, _ = layer.size
    line_w = _modern_line_width(text, font, spacing)
    x = (width - line_w) / 2
    if shadow:
        shadow_layer = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        _draw_text_with_spacing(
            shadow_layer,
            (x + shadow_offset[0], y + shadow_offset[1]),
            text,
            font,
            shadow,
            spacing,
            shadow,
            stroke_width,
        )
        if shadow_blur:
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
        layer.alpha_composite(shadow_layer)
    _draw_text_with_spacing(layer, (x, y), text, font, fill, spacing, stroke, stroke_width)
    return line_w


__all__ = ["_draw_centered_line"]
