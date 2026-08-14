"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _design_signature(style: dict[str, Any]) -> tuple[Any, ...]:
    return (
        str(style.get("fill") or ""),
        str(style.get("stroke") or ""),
        round(float(style.get("strokeWidth") or 0), 2),
        str(style.get("shadowColor") or ""),
        round(float(style.get("shadowBlur") or 0), 2),
        round(float(style.get("shadowOffsetX") or 0), 2),
        round(float(style.get("shadowOffsetY") or 0), 2),
        str(style.get("textDecoration") or ""),
        round(float(style.get("letterSpacing") or 0), 2),
        round(float(style.get("rotation") or 0), 2),
        str(style.get("previewLayout") or "stacked"),
    )


__all__ = ["_design_signature"]
