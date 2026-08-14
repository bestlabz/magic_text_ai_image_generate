"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _balanced_font_families(families: list[str], randomize_fonts: bool = True,
                            rng: random.Random | None = None) -> list[str]:
    rng = rng or _make_rng()
    groups: dict[str, list[str]] = {kind: [] for kind in FONT_KIND_ORDER}
    extras: list[str] = []
    seen = set()
    for family in families:
        family = str(family or "").strip()
        key = family.lower()
        if not family or key in seen:
            continue
        seen.add(key)
        kind = _font_kind(family)
        if kind in groups:
            groups[kind].append(family)
        else:
            extras.append(family)

    kind_order = FONT_KIND_ORDER[:]
    if randomize_fonts:
        rng.shuffle(kind_order)
        for values in groups.values():
            rng.shuffle(values)
        rng.shuffle(extras)

    ordered: list[str] = []
    while any(groups.values()):
        for kind in kind_order:
            if groups[kind]:
                ordered.append(groups[kind].pop(0))
    ordered.extend(extras)
    return ordered


__all__ = ["_balanced_font_families"]
