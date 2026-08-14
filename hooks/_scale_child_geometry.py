"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _scale_child_geometry(child: dict[str, Any], origin: tuple[float, float], factor: float) -> None:
    ox, oy = origin
    child["x"] = ox + (float(child.get("x") or 0) - ox) * factor
    child["y"] = oy + (float(child.get("y") or 0) - oy) * factor
    for key in ("width", "height", "fontSize", "strokeWidth", "shadowBlur", "letterSpacing"):
        child[key] = float(child.get(key) or 0) * factor
    for key in ("shadowOffsetX", "shadowOffsetY"):
        child[key] = float(child.get(key) or 0) * factor


__all__ = ["_scale_child_geometry"]
