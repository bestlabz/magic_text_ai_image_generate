"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _apply_random_design(style: dict[str, Any], rng: random.Random, index: int,
                         used_designs: set[tuple[Any, ...]]) -> dict[str, Any]:
    randomized = deepcopy(style)
    kind = _font_kind(str(randomized.get("fontFamily") or ""))
    palette_order = _shuffle_copy(DESIGN_PALETTES, rng)
    effect_order = _shuffle_copy(DESIGN_EFFECTS, rng)

    selected: dict[str, Any] | None = None
    selected_palette: dict[str, Any] | None = None
    selected_effect: dict[str, Any] | None = None
    for palette in palette_order:
        for effect in effect_order:
            candidate = deepcopy(randomized)
            candidate.update(palette)
            stroke = _clean_hex(candidate.get("stroke"), "")
            candidate["stroke"] = stroke
            candidate["strokeWidth"] = float(effect["strokeWidth"]) if stroke else 0
            candidate["shadowColor"] = _clean_hex(candidate.get("shadowColor"), "")
            candidate["shadowBlur"] = float(effect["shadowBlur"]) if candidate["shadowColor"] else 0
            candidate["shadowOffsetX"] = float(effect["shadowOffsetX"]) if candidate["shadowColor"] else 0
            candidate["shadowOffsetY"] = float(effect["shadowOffsetY"]) if candidate["shadowColor"] else 0
            candidate["textDecoration"] = effect["textDecoration"]
            candidate["letterSpacing"] = float(effect["letterSpacing"])
            candidate["rotation"] = float(effect["rotation"])
            if kind == "script":
                candidate["letterSpacing"] = min(candidate["letterSpacing"], 0.4)
                candidate["fontStyle"] = rng.choice(["normal", "italic"])
            elif kind in {"display", "mono", "decorative"}:
                candidate["letterSpacing"] = max(candidate["letterSpacing"], rng.choice([0.6, 1.0, 1.4]))
                candidate["fontWeight"] = "bold"
            elif kind == "serif":
                candidate["fontStyle"] = rng.choice(["normal", "italic"])
                candidate["letterSpacing"] = max(candidate["letterSpacing"], rng.choice([0.2, 0.8, 1.2]))
            signature = _design_signature(candidate)
            if signature not in used_designs:
                selected = candidate
                selected_palette = palette
                selected_effect = effect
                break
        if selected:
            break

    if selected is None:
        selected_palette = palette_order[index % len(palette_order)]
        selected_effect = effect_order[index % len(effect_order)]
        selected = deepcopy(randomized)
        selected.update(selected_palette)
        selected["stroke"] = _clean_hex(selected.get("stroke"), "")
        selected["strokeWidth"] = float(selected_effect["strokeWidth"]) if selected["stroke"] else 0
        selected["shadowColor"] = _clean_hex(selected.get("shadowColor"), "")
        selected["shadowBlur"] = float(selected_effect["shadowBlur"]) if selected["shadowColor"] else 0
        selected["shadowOffsetX"] = float(selected_effect["shadowOffsetX"]) if selected["shadowColor"] else 0
        selected["shadowOffsetY"] = float(selected_effect["shadowOffsetY"]) if selected["shadowColor"] else 0
        selected["textDecoration"] = selected_effect["textDecoration"]
        selected["letterSpacing"] = float(selected_effect["letterSpacing"]) + (index % 5) * 0.25
        selected["rotation"] = float(selected_effect["rotation"]) + [-4, -2, 0, 2, 4][index % 5]

    base_size = _clamp_number(selected.get("fontSize"), 40, 8, 96)
    selected["fontSize"] = base_size * rng.uniform(0.88, 1.12)
    if rng.random() < 0.18:
        selected["textDecoration"] = rng.choice(["underline", ""])
    if str(selected.get("previewLayout") or "") in {"sale", "title_heading", "coming_soon", "signature", "glow_signature", "arc"}:
        selected["rotation"] = 0

    effect_name = str((selected_effect or {}).get("suffix") or "custom")
    selected["name"] = f"{selected.get('name', 'style')}_{effect_name}_{index + 1}"
    used_designs.add(_design_signature(selected))
    return selected


__all__ = ["_apply_random_design"]
