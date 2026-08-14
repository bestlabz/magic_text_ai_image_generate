"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _font_family_style(font_family: str, index: int) -> dict[str, Any]:
    kind = _font_kind(font_family)
    preset_by_kind = {
        "script": "engaged_script",
        "serif": "gold_serif",
        "display": "like_subscribe_hollow",
        "mono": "red_stamp_hollow",
        "decorative": "yellow_pop_outline",
        "sans": "neon_glow",
    }
    fallback_preset = STYLE_PRESETS[index % len(STYLE_PRESETS)]
    preset_name = preset_by_kind.get(kind)
    preset = next((style for style in STYLE_PRESETS if style.get("name") == preset_name), fallback_preset)
    style = _variant_from_preset(preset, index // len(STYLE_PRESETS))
    palette = [
        ("#111111", "", ""),
        ("#D8A919", "", "#E8D187"),
        ("#FF6F72", "#FFF0CB", "#FFB0A6"),
        ("#1B45F5", "#31FF38", ""),
        ("#FF5BB4", "#FF8BD0", "#FF44B0"),
        ("#0F6B5B", "", "#CFF7E4"),
        ("#F56C2D", "#FFE6A7", "#2EC4B6"),
        ("#FFFFFF", "#8B7DFF", "#8179FF"),
        ("#EF4E56", "#EF4E56", ""),
        ("#23B7E5", "", "#FF7A22"),
    ]
    fill, stroke, shadow = palette[index % len(palette)]
    style.update({
        "name": f"font_{re.sub(r'[^a-zA-Z0-9]+', '_', font_family).strip('_').lower() or index}",
        "fontFamily": font_family,
        "fill": fill,
        "stroke": stroke,
        "shadowColor": shadow,
        "strokeWidth": 2.4 if stroke else 0,
        "shadowBlur": 10 if shadow and index % 4 == 0 else style.get("shadowBlur", 0),
        "letterSpacing": 1.4 if kind in {"display", "mono", "decorative"} else 0,
        "fontStyle": "italic" if kind in {"script", "serif"} and index % 2 else "normal",
        "fontWeight": "normal" if kind == "script" else "bold",
        "lineHeight": 0.9 if kind in {"script", "serif"} else 0.98,
    })
    if kind == "script":
        style["fontSize"] = 50
    elif kind == "display":
        style["fontSize"] = 42
    elif kind == "mono":
        style["fontSize"] = 36
    elif kind == "decorative":
        style["fontSize"] = 38
        style["strokeWidth"] = 2.8 if style.get("stroke") else 0
    else:
        style["fontSize"] = 40
    return style


__all__ = ["_font_family_style"]
