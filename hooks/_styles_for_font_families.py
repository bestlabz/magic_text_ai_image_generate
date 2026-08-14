"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _styles_for_font_families(font_families: list[str] | tuple[str, ...] | str | None,
                              count: int | None = None,
                              randomize_fonts: bool = True,
                              randomize_designs: bool = True,
                              rng: random.Random | None = None) -> list[dict[str, Any]]:
    rng = rng or _make_rng()
    families = _balanced_font_families(
        _normalize_font_families(font_families),
        randomize_fonts=randomize_fonts,
        rng=rng,
    )
    if count is not None and count > 0:
        families = families[:count]
    styles = [_font_family_style(family, index) for index, family in enumerate(families)]
    if randomize_designs:
        used_designs: set[tuple[Any, ...]] = set()
        styles = [_apply_random_design(style, rng, index, used_designs) for index, style in enumerate(styles)]
    return styles


__all__ = ["_styles_for_font_families"]
