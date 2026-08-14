"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _style_candidates(text: str, count: int, mood: str | None,
                      randomize_fonts: bool = True,
                      randomize_designs: bool = True,
                      rng: random.Random | None = None) -> list[dict[str, Any]]:
    rng = rng or _make_rng()
    base_styles = _local_style_library(text, mood, rng, randomize_fonts)
    used_fonts: set[str] = set()
    used_designs: set[tuple[Any, ...]] = set()
    styles: list[dict[str, Any]] = []

    for index in range(count):
        base = deepcopy(base_styles[index % len(base_styles)])
        style = _variant_from_preset(base, index // len(base_styles))
        if randomize_fonts:
            style = _randomize_style_font(style, rng, used_fonts)
        if randomize_designs:
            style = _apply_random_design(style, rng, index, used_designs)
        styles.append(style)
    return styles


__all__ = ["_style_candidates"]
