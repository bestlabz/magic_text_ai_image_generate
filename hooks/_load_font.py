"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _load_font(family: str, size: float, weight: str | None = None, italic: bool = False) -> ImageFont.FreeTypeFont:
    bold = str(weight or "").strip().lower() in {"bold", "700", "600", "semibold", "semi-bold"}
    path = (
        _font_cache_path(family, bold, italic)
        or _system_font_path(family, bold, allow_default=False)
        or _download_google_font(family, bold, italic)
        or _system_font_path(family, bold, allow_default=True)
    )
    if path:
        return ImageFont.truetype(str(path), max(int(round(size)), 1))
    return ImageFont.load_default()


__all__ = ["_load_font"]
