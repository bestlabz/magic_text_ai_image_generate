"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _randomize_style_font(style: dict[str, Any], rng: random.Random, used_fonts: set[str]) -> dict[str, Any]:
    randomized = deepcopy(style)
    randomized["fontFamily"] = _pick_unused_font(
        _font_pool_for_style(randomized),
        rng,
        used_fonts,
        fallback=str(randomized.get("fontFamily") or "Arial"),
    )
    return randomized


__all__ = ["_randomize_style_font"]
