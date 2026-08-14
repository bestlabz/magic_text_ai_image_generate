"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _font_pool_for_style(style: dict[str, Any]) -> list[str]:
    category = str(style.get("category") or "").lower()
    layout = str(style.get("previewLayout") or "").lower()
    name = str(style.get("name") or "").lower()
    current_family = str(style.get("fontFamily") or "")

    if any(token in f"{category} {layout} {name}" for token in ("signature", "script", "brush")):
        return CANVA_FONT_GROUPS["script"]
    if any(token in f"{category} {layout} {name}" for token in ("serif", "luxury", "editorial", "coming")):
        return CANVA_FONT_GROUPS["serif"]
    if any(token in f"{category} {layout} {name}" for token in ("sale", "title", "heading", "outline", "marker", "caps")):
        return CANVA_FONT_GROUPS["display"] + CANVA_FONT_GROUPS["sans"]
    if any(token in f"{category} {layout} {name}" for token in ("tattoo", "arc", "decorative")):
        return CANVA_FONT_GROUPS["decorative"] + CANVA_FONT_GROUPS["serif"]
    if "mono" in f"{category} {layout} {name}":
        return CANVA_FONT_GROUPS["mono"]

    kind = _font_kind(current_family)
    return CANVA_FONT_GROUPS.get(kind, CANVA_FONT_FAMILIES)


__all__ = ["_font_pool_for_style"]
