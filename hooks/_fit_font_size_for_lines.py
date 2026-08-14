"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _fit_font_size_for_lines(
    lines: list[str],
    family: str,
    base_size: float,
    max_width: float,
    max_height: float,
    weight: str | None = None,
    italic: bool = False,
    spacing: float = 0,
    line_height: float = 1.0,
    min_size: float = 8,
) -> float:
    size = max(base_size, min_size)
    while size > min_size:
        font = _load_font(family, size, weight, italic)
        widths = [_modern_line_width(line, font, spacing) for line in lines]
        height = len(lines) * size * line_height
        if max(widths or [0]) <= max_width and height <= max_height:
            return size
        size *= 0.92
    return min_size


__all__ = ["_fit_font_size_for_lines"]
