"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _apply_modern_composition_design(
    children: list[dict[str, Any]],
    kind: str,
    index: int,
    rng: random.Random,
    randomize_designs: bool,
    used_designs: set[tuple[str, str]],
    used_palettes: set[str],
    used_effects: set[str],
) -> tuple[list[dict[str, Any]], str, str]:
    palette, effect = _modern_design_choices(
        index,
        rng,
        randomize_designs,
        used_designs,
        used_palettes,
        used_effects,
    )
    fill_mode = str(effect.get("fillMode") or "primary")
    stroke_mode = str(effect.get("strokeMode") or "")
    shadow_mode = str(effect.get("shadowMode") or "")
    base_stroke = float(effect.get("strokeWidth") or 0)
    base_shadow_blur = float(effect.get("shadowBlur") or 0)
    base_shadow_x = float(effect.get("shadowOffsetX") or 0)
    base_shadow_y = float(effect.get("shadowOffsetY") or 0)
    effect_name = str(effect.get("name") or "custom")
    designed = deepcopy(children)

    for child in designed:
        if not isinstance(child, dict) or child.get("type") != "Text":
            continue
        role = str(child.get("magicWriteRole") or "main")
        is_main = role == "main" or len(designed) == 1
        role_fill_mode = fill_mode if is_main else ("secondary" if fill_mode != "secondary" else "primary")
        if effect_name in {"glow_tube", "warm_neon"}:
            role_fill_mode = "light"
        elif effect_name == "reverse_outline" and not is_main:
            role_fill_mode = "primary"
        elif effect_name == "sticker" and not is_main:
            role_fill_mode = "primary"
        child["fill"] = _modern_palette_value(palette, role_fill_mode) or str(child.get("fill") or "#111111")

        stroke = _modern_palette_value(palette, stroke_mode)
        if effect_name == "solid" and not is_main:
            stroke = ""
        child["stroke"] = stroke
        child["strokeWidth"] = base_stroke if stroke else 0

        shadow = _modern_palette_value(palette, shadow_mode)
        child["shadowColor"] = shadow
        child["shadowBlur"] = base_shadow_blur if shadow else 0
        child["shadowOffsetX"] = base_shadow_x if shadow else 0
        child["shadowOffsetY"] = base_shadow_y if shadow else 0

        if role in {"script", "serif"}:
            child["letterSpacing"] = min(float(child.get("letterSpacing") or 0), 0.6)
            child["rotation"] = 0
        elif role in {"top", "sub"}:
            child["letterSpacing"] = max(float(child.get("letterSpacing") or 0), 1.2 + (index % 3) * 0.4)
        else:
            child["letterSpacing"] = max(float(child.get("letterSpacing") or 0), (index % 4) * 0.25)

        if kind in {"light_script", "neon_glow", "neon_open"} and effect_name in {"glow_tube", "warm_neon"}:
            child["fill"] = _modern_palette_value(palette, "light") or "#FFFFFF"
            child["stroke"] = _modern_palette_value(palette, "accent") or child["stroke"]
            child["strokeWidth"] = max(float(child.get("strokeWidth") or 0), 1.1)
            child["shadowColor"] = _modern_palette_value(palette, "glow") or child["stroke"]
            child["shadowBlur"] = max(float(child.get("shadowBlur") or 0), 16 + (index % 3) * 2)
            child["shadowOffsetX"] = 0
            child["shadowOffsetY"] = 0
        elif kind in {"golden_hour", "editorial_caps"} and effect_name == "solid":
            child["shadowColor"] = _modern_palette_value(palette, "shadow")
            child["shadowBlur"] = 1.2
            child["shadowOffsetX"] = 1.5
            child["shadowOffsetY"] = 2.2
        elif kind == "preview_brush_sticker":
            child["fill"] = _modern_palette_value(palette, "secondary") or "#FF6B6B"
            child["stroke"] = _modern_palette_value(palette, "light") or "#FFFFFF"
            child["strokeWidth"] = max(float(child.get("strokeWidth") or 0), 2.4)
            child["shadowColor"] = _modern_palette_value(palette, "accent") or "#FFC3A6"
            child["shadowBlur"] = 0.8
            child["shadowOffsetX"] = 1.2
            child["shadowOffsetY"] = 1.8
        elif kind == "preview_glow_script":
            child["fill"] = _modern_palette_value(palette, "light") or "#FFF8D8"
            child["stroke"] = _modern_palette_value(palette, "accent") or "#FFD66B"
            child["strokeWidth"] = max(float(child.get("strokeWidth") or 0), 1.0)
            child["shadowColor"] = _modern_palette_value(palette, "glow") or "#FFE58A"
            child["shadowBlur"] = 22
            child["shadowOffsetX"] = 0
            child["shadowOffsetY"] = 0
        elif kind == "preview_comic_offset":
            child["fill"] = _modern_palette_value(palette, "primary") or "#20A9D6"
            child["stroke"] = _modern_palette_value(palette, "light") or "#FFFFFF"
            child["strokeWidth"] = max(float(child.get("strokeWidth") or 0), 2.0)
            child["shadowColor"] = _modern_palette_value(palette, "secondary") or "#FF4F61"
            child["shadowBlur"] = 0
            child["shadowOffsetX"] = 4.5
            child["shadowOffsetY"] = 0
        elif kind in {"preview_sale_stack", "preview_neon_stack", "preview_chrome_shadow", "preview_script_block_mix", "preview_serif_luxe"}:
            if role == "main":
                child["strokeWidth"] = max(float(child.get("strokeWidth") or 0), 1.5 if kind != "preview_chrome_shadow" else 2.2)
                child["shadowBlur"] = 18 if kind == "preview_neon_stack" else 0 if kind in {"preview_sale_stack", "preview_chrome_shadow"} else float(child.get("shadowBlur") or 0)
                child["shadowOffsetX"] = 0 if kind == "preview_neon_stack" else min(max(float(child.get("shadowOffsetX") or 0), 1.2), 2.4)
                child["shadowOffsetY"] = 0 if kind == "preview_neon_stack" else min(max(float(child.get("shadowOffsetY") or 0), 1.4), 2.8)
        elif kind in {"graduation_varsity_stack", "graduation_script_block", "graduation_badge_shadow", "graduation_neon_label", "graduation_serif_split", "graduation_champ_stamp"}:
            if role == "main":
                child["fill"] = _modern_palette_value(palette, "accent") or "#F6C84B"
                child["stroke"] = _modern_palette_value(palette, "primary") or "#123A6F"
                child["strokeWidth"] = max(float(child.get("strokeWidth") or 0), 2.4)
                child["shadowColor"] = _modern_palette_value(palette, "shadow") or _modern_palette_value(palette, "secondary") or "#0B2448"
                child["shadowBlur"] = 0
                child["shadowOffsetX"] = 4.5 + (index % 3)
                child["shadowOffsetY"] = 5.0 + (index % 3)
            elif role in {"script", "sub"}:
                child["fill"] = _modern_palette_value(palette, "secondary") or "#FF4F61"
                child["stroke"] = _modern_palette_value(palette, "light") or "#FFFFFF"
                child["strokeWidth"] = max(float(child.get("strokeWidth") or 0), 1.0)
                child["shadowColor"] = _modern_palette_value(palette, "shadow") or "#123A6F"
                child["shadowBlur"] = 0
                child["shadowOffsetX"] = 1.6
                child["shadowOffsetY"] = 2.0

    return designed, str(palette["name"]), effect_name


__all__ = ["_apply_modern_composition_design"]
