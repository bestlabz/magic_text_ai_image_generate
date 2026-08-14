"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _variant_from_preset(preset: dict[str, Any], cycle: int) -> dict[str, Any]:
    style = deepcopy(preset)
    if cycle <= 0:
        return style

    # Repeated requests beyond the curated set should still produce visibly
    # different options instead of exact duplicates.
    color_shift = cycle % 3
    for key in ("fill", "stroke", "shadowColor"):
        if style.get(key):
            style[key] = _rotate_hex_color(str(style[key]), color_shift)
    style["fontSize"] = _clamp_number(style.get("fontSize"), 40, 8, 96) * (0.94 + 0.03 * (cycle % 5))
    style["letterSpacing"] = _clamp_number(style.get("letterSpacing"), 0, -1, 6) + ((cycle % 4) * 0.25)
    style["rotation"] = [0, -3, 3, -5, 5][cycle % 5]
    style["name"] = f"{style.get('name', 'style')}_{cycle + 1}"
    return style


__all__ = ["_variant_from_preset"]
