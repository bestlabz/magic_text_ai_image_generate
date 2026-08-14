"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _normalize_font_families(font_families: list[str] | tuple[str, ...] | str | None) -> list[str]:
    if font_families is None:
        return CANVA_FONT_FAMILIES[:]
    if isinstance(font_families, str):
        raw_values = font_families.split(",")
    else:
        raw_values = list(font_families)

    families: list[str] = []
    seen = set()
    for value in raw_values:
        family = str(value or "").strip()
        if not family:
            continue
        key = family.lower()
        if key in seen:
            continue
        families.append(family[:80])
        seen.add(key)
    return families or CANVA_FONT_FAMILIES[:]


__all__ = ["_normalize_font_families"]
