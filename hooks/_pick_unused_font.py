"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _pick_unused_font(candidates: list[str], rng: random.Random, used_fonts: set[str],
                      fallback: str | None = None) -> str:
    normalized = _normalize_font_families(candidates or ([fallback] if fallback else None))
    available = [family for family in normalized if family.lower() not in used_fonts]
    pool = available or normalized or CANVA_FONT_FAMILIES[:]
    family = rng.choice(pool)
    used_fonts.add(family.lower())
    return family


__all__ = ["_pick_unused_font"]
