"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _modern_text_style_for_index(index: int) -> dict[str, Any]:
    base_count = len(MODERN_TEXT_EXPORT_STYLES)
    base_index = index % base_count
    style = deepcopy(MODERN_TEXT_EXPORT_STYLES[base_index])
    cycle = index // base_count
    if cycle == 0:
        return style

    kind = _font_kind(str(style.get("fontFamily") or ""))
    font_pool = MODERN_TEXT_VARIANT_FONTS.get(kind) or MODERN_TEXT_VARIANT_FONTS["sans"]
    original_fill = _clean_hex(style.get("fill"), "")
    original_stroke = _clean_hex(style.get("stroke"), "")
    palette_index = (cycle * 7 + base_index * 3) % len(MODERN_TEXT_VARIANT_PALETTES)
    for offset in range(len(MODERN_TEXT_VARIANT_PALETTES)):
        palette = MODERN_TEXT_VARIANT_PALETTES[(palette_index + offset) % len(MODERN_TEXT_VARIANT_PALETTES)]
        if palette["fill"] != original_fill and palette["stroke"] != original_stroke:
            break
    effect = MODERN_TEXT_VARIANT_EFFECTS[(cycle * 2 + base_index) % len(MODERN_TEXT_VARIANT_EFFECTS)]

    style["name"] = f"{style.get('name', 'modern_text')}_{effect['name']}_{cycle}"
    style["fontFamily"] = font_pool[(cycle * 3 + base_index + 1) % len(font_pool)]
    style["fill"] = palette["fill"]
    style["stroke"] = palette["stroke"] if effect["strokeWidth"] else ""
    style["strokeWidth"] = float(effect["strokeWidth"]) if style["stroke"] else 0
    style["shadowColor"] = palette["shadow"] if effect["shadowBlur"] or effect["shadowOffsetX"] or effect["shadowOffsetY"] else ""
    style["shadowBlur"] = float(effect["shadowBlur"]) if style["shadowColor"] else 0
    style["shadowOffsetX"] = float(effect["shadowOffsetX"]) if style["shadowColor"] else 0
    style["shadowOffsetY"] = float(effect["shadowOffsetY"]) if style["shadowColor"] else 0
    style["fontSize"] = _clamp_number(float(style.get("fontSize") or 60) * (0.9 + (cycle % 5) * 0.035), 60, 38, 86)
    style["letterSpacing"] = _clamp_number(float(style.get("letterSpacing") or 0) + ((cycle + index) % 5) * 0.28, 0, -0.5, 2.4)
    style["textTransform"] = "upper" if (cycle + index) % 3 == 0 else style.get("textTransform", "title")
    if _font_kind(str(style["fontFamily"])) == "script":
        style["fontStyle"] = "italic"
        style["fontWeight"] = "normal" if (cycle + index) % 2 else "bold"
        style["letterSpacing"] = min(float(style["letterSpacing"]), 0.6)
    else:
        style["fontStyle"] = "normal"
        style["fontWeight"] = "bold" if _font_kind(str(style["fontFamily"])) in {"display", "sans"} else style.get("fontWeight", "bold")
    return style


__all__ = ["_modern_text_style_for_index"]
