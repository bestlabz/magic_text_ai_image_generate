"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _draw_text_with_spacing(
    layer: Image.Image,
    xy: tuple[float, float],
    text: str,
    font: ImageFont.ImageFont,
    fill: str,
    spacing: float,
    stroke: str,
    stroke_width: float,
) -> None:
    draw = ImageDraw.Draw(layer)
    x, y = xy
    for ch in text:
        draw.text(
            (x, y),
            ch,
            font=font,
            fill=fill,
            stroke_width=max(int(round(stroke_width)), 0),
            stroke_fill=stroke or fill,
        )
        x += draw.textlength(ch, font=font) + spacing


__all__ = ["_draw_text_with_spacing"]
