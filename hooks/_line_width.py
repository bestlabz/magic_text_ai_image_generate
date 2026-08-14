"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _line_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, spacing: float) -> float:
    if not text:
        return 0
    width = sum(draw.textlength(ch, font=font) for ch in text)
    return width + max(len(text) - 1, 0) * spacing


__all__ = ["_line_width"]
