"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _modern_composition_groups(
    text: str,
    count: int | None,
    rng: random.Random,
    canvas_width: int,
    canvas_height: int,
    randomize_designs: bool = True,
) -> list[dict[str, Any]]:
    templates = MODERN_COMPOSITION_TEMPLATES[:]
    template_order = {
        str(template.get("kind") or template.get("name") or ""): position
        for position, template in enumerate(MODERN_COMPOSITION_TEMPLATES)
    }
    normalized = text.lower()
    graduation_kinds = {
        "graduation_varsity_stack",
        "graduation_script_block",
        "graduation_badge_shadow",
        "graduation_neon_label",
        "graduation_serif_split",
        "graduation_champ_stamp",
    }
    if any(token in normalized for token in ("class", "graduation", "graduate", "grad", "2026", "2027", "2028")):
        templates = [template for template in templates if str(template.get("kind") or "") in graduation_kinds] or templates

    def score(template: dict[str, Any]) -> int:
        kind = str(template.get("kind") or "")
        checks = {
            "retro_3d_block": ("hungry", "fresh", "bold", "sale", "block"),
            "script_3d_swoop": ("hungry", "travel", "time", "vacation", "feeling"),
            "tall_3d_comic": ("hungry", "comic", "pop", "fresh", "shop"),
            "study_mode_script": ("study", "mode", "class", "school", "learn"),
            "festival_ribbon_script": ("diwali", "festival", "happy", "celebrate", "joy"),
            "chrome_loop_script": ("good", "vibes", "chill", "hello", "feeling"),
            "gloss_burst_script": ("swipe", "simple", "shine", "sparkle"),
            "graduation_varsity_stack": ("class", "graduation", "graduate", "grad", "2026", "2027", "2028"),
            "graduation_script_block": ("class", "graduation", "graduate", "grad", "2026", "2027", "2028"),
            "graduation_badge_shadow": ("class", "graduation", "graduate", "grad", "2026", "2027", "2028"),
            "graduation_neon_label": ("class", "graduation", "graduate", "grad", "2026", "2027", "2028"),
            "graduation_serif_split": ("class", "graduation", "graduate", "grad", "2026", "2027", "2028"),
            "graduation_champ_stamp": ("class", "graduation", "graduate", "grad", "2026", "2027", "2028"),
            "light_script": ("sparkle", "light", "glow", "shine", "neon"),
            "neon_glow": ("neon", "glow", "open", "light"),
            "thank_you": ("thank", "you"),
            "bride_groom": ("bride", "groom", "wedding", "&"),
            "happy_birthday": ("happy", "birthday"),
            "golden_hour": ("golden", "hour", "luxury"),
            "script_club": ("script", "club"),
            "xoxo": ("xoxo", "love"),
            "studio_badge": ("studio", "est", "agatho"),
            "streaming_now": ("streaming", "now", "live"),
            "quarterly_targets": ("quarterly", "targets", "target"),
            "quarter_roadmap": ("quarter", "roadmap", "road map"),
            "neon_open": ("open", "now"),
            "editorial_caps": ("coming", "soon"),
        }
        return sum(1 for token in checks.get(kind, ()) if token in normalized)

    templates.sort(key=lambda template: (-score(template), template_order.get(str(template.get("kind") or ""), 999)))
    requested = count or len(templates)
    groups = []
    used_fonts: set[str] = set()
    used_designs: set[tuple[str, str]] = set()
    used_palettes: set[str] = set()
    used_effects: set[str] = set()
    for index in range(requested):
        groups.append(_modern_composition_variant(
            text,
            templates[index % len(templates)],
            index,
            rng,
            canvas_width,
            canvas_height,
            used_fonts,
            used_designs,
            used_palettes,
            used_effects,
            randomize_designs,
        ))
    return groups


__all__ = ["_modern_composition_groups"]
