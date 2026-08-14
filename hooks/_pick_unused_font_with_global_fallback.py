"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _pick_unused_font_with_global_fallback(candidates: list[str], rng: random.Random,
                                           used_fonts: set[str]) -> str:
    primary = _normalize_font_families(candidates)
    primary_available = [family for family in primary if family.lower() not in used_fonts]
    if primary_available:
        family = rng.choice(primary_available)
        used_fonts.add(family.lower())
        return family

    global_available = [
        family
        for family in CANVA_FONT_FAMILIES
        if family.lower() not in used_fonts
    ]
    if global_available:
        family = rng.choice(global_available)
        used_fonts.add(family.lower())
        return family

    return _pick_unused_font(primary, rng, used_fonts)


__all__ = ["_pick_unused_font_with_global_fallback"]
