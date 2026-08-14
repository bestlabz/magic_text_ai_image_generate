"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _style_visual_signature(style: dict[str, Any]) -> tuple[Any, ...]:
    return (
        str(style.get("fontFamily") or "").strip().lower(),
        str(style.get("fontWeight") or "").strip().lower(),
        str(style.get("fontStyle") or "").strip().lower(),
        str(style.get("fill") or "").strip().lower(),
        str(style.get("stroke") or "").strip().lower(),
        round(float(style.get("strokeWidth") or 0), 1),
        str(style.get("shadowColor") or "").strip().lower(),
        round(float(style.get("shadowBlur") or 0), 1),
        round(float(style.get("shadowOffsetX") or 0), 1),
        round(float(style.get("shadowOffsetY") or 0), 1),
        round(float(style.get("letterSpacing") or 0), 1),
        round(float(style.get("rotation") or 0), 1),
        str(style.get("previewLayout") or "stacked").strip().lower(),
        str(style.get("textTransform") or "none").strip().lower(),
    )


__all__ = ["_style_visual_signature"]
