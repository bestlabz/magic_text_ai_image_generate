"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _modern_design_choices(
    index: int,
    rng: random.Random,
    randomize_designs: bool,
    used_designs: set[tuple[str, str]],
    used_palettes: set[str],
    used_effects: set[str],
) -> tuple[dict[str, str], dict[str, Any]]:
    palettes_by_name = {str(palette["name"]): palette for palette in MODERN_COMPOSITION_PALETTES}
    effects_by_name = {str(effect["name"]): effect for effect in MODERN_COMPOSITION_EFFECTS}
    featured = [
        (palettes_by_name[palette_name], effects_by_name[effect_name])
        for palette_name, effect_name in MODERN_FEATURED_DESIGN_SEQUENCE
        if palette_name in palettes_by_name and effect_name in effects_by_name
    ]
    for offset in range(len(featured)):
        palette, effect = featured[(index + offset) % len(featured)]
        signature = (str(palette["name"]), str(effect["name"]))
        if signature not in used_designs:
            used_designs.add(signature)
            used_palettes.add(str(palette["name"]))
            used_effects.add(str(effect["name"]))
            return palette, effect

    palettes = _shuffle_copy(MODERN_COMPOSITION_PALETTES, rng) if randomize_designs else MODERN_COMPOSITION_PALETTES[:]
    effects = _shuffle_copy(MODERN_COMPOSITION_EFFECTS, rng) if randomize_designs else MODERN_COMPOSITION_EFFECTS[:]
    palette_pool = [palette for palette in palettes if str(palette["name"]) not in used_palettes] or palettes
    effect_pool = [effect for effect in effects if str(effect["name"]) not in used_effects] or effects

    for palette in palette_pool:
        for effect in effect_pool:
            signature = (str(palette["name"]), str(effect["name"]))
            if signature not in used_designs:
                used_designs.add(signature)
                used_palettes.add(str(palette["name"]))
                used_effects.add(str(effect["name"]))
                return palette, effect

    palette = palettes[index % len(palettes)]
    effect = effects[(index // len(palettes)) % len(effects)]
    used_designs.add((str(palette["name"]), str(effect["name"])))
    used_palettes.add(str(palette["name"]))
    used_effects.add(str(effect["name"]))
    return palette, effect


__all__ = ["_modern_design_choices"]
