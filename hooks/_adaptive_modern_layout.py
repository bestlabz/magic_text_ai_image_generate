"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _adaptive_modern_layout(style: dict[str, Any], text: str) -> str:
    layout = str(style.get("previewLayout") or "stacked")
    normalized = text.lower()
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if layout == "sale":
        has_discount = bool(re.search(r"\d+\s*%", text))
        has_sale_word = any(word in normalized for word in ("off", "sale", "discount"))
        return "sale" if has_discount or has_sale_word else "stacked"
    if layout == "coming_soon":
        return "coming_soon" if "coming" in normalized or "soon" in normalized else "stacked"
    if layout == "title_heading":
        heading_like = len(lines) <= 2 and any(word in normalized for word in ("title", "heading", "headline"))
        return "title_heading" if heading_like else "stacked"
    if layout == "arc":
        tattoo_like = any(word in normalized for word in ("tattoo", "studio", "brand", "logo"))
        short_arc = bool(lines and len(lines[0]) <= 14)
        return "arc" if tattoo_like or short_arc else "stacked"
    return layout


__all__ = ["_adaptive_modern_layout"]
