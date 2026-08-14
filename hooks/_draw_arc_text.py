"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _draw_arc_text(
    layer: Image.Image,
    text: str,
    center: tuple[float, float],
    radius: float,
    font: ImageFont.ImageFont,
    fill: str,
    spacing_degrees: float = 8,
) -> None:
    if not text:
        return
    total_angle = min(max(len(text) * spacing_degrees, 80), 155)
    start_angle = -90 - total_angle / 2
    for index, char in enumerate(text):
        angle = math.radians(start_angle + index * (total_angle / max(len(text) - 1, 1)))
        x = center[0] + math.cos(angle) * radius
        y = center[1] + math.sin(angle) * radius
        draw = ImageDraw.Draw(layer)
        bbox = draw.textbbox((0, 0), char, font=font)
        char_w = bbox[2] - bbox[0]
        char_h = bbox[3] - bbox[1]
        draw.text((x - char_w / 2, y - char_h / 2), char, font=font, fill=fill)


__all__ = ["_draw_arc_text"]
