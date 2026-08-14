"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _konva_stage_object(obj: dict[str, Any], canvas_width: int, canvas_height: int) -> dict[str, Any] | None:
    node = _konva_node_from_internal(obj)
    if node is None:
        return None
    return {
        "attrs": {
            "width": canvas_width,
            "height": canvas_height,
        },
        "className": "Stage",
        "children": [
            {
                "attrs": {},
                "className": "Layer",
                "children": [node],
            },
        ],
    }


__all__ = ["_konva_stage_object"]
