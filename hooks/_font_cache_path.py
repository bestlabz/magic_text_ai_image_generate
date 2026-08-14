"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _font_cache_path(family: str, bold: bool, italic: bool = False) -> Path | None:
    family_key = re.sub(r"[^a-zA-Z0-9]+", "_", family).strip("_").lower()
    variants = []
    if bold and italic:
        variants.extend(["700italic", "italic", "700", "regular"])
    elif bold:
        variants.extend(["700", "regular"])
    elif italic:
        variants.extend(["italic", "regular"])
    else:
        variants.extend(["regular", "700"])
    for cache_dir in FONT_CACHE_DIRS:
        for variant in variants:
            path = cache_dir / f"{family_key}__{variant}.ttf"
            if path.exists():
                return path
    return None


__all__ = ["_font_cache_path"]
