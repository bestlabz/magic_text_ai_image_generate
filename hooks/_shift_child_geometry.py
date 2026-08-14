"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _shift_child_geometry(child: dict[str, Any], dx: float, dy: float) -> None:
    child["x"] = float(child.get("x") or 0) + dx
    child["y"] = float(child.get("y") or 0) + dy


__all__ = ["_shift_child_geometry"]
