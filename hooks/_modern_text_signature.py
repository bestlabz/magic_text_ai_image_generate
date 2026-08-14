"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _modern_text_signature(obj: dict[str, Any]) -> tuple[Any, ...]:
    return (
        str(obj.get("text") or ""),
        str(obj.get("fontFamily") or ""),
        str(obj.get("fontWeight") or ""),
        str(obj.get("fontStyle") or ""),
        str(obj.get("fill") or ""),
        str(obj.get("stroke") or ""),
        round(float(obj.get("strokeWidth") or 0), 2),
        str(obj.get("shadowColor") or ""),
        round(float(obj.get("shadowBlur") or 0), 2),
        round(float(obj.get("shadowOffsetX") or 0), 2),
        round(float(obj.get("shadowOffsetY") or 0), 2),
        round(float(obj.get("letterSpacing") or 0), 2),
    )


__all__ = ["_modern_text_signature"]
