"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _fabric_canvas_object(obj: dict[str, Any], canvas_width: int, canvas_height: int) -> dict[str, Any] | None:
    text_objects = _fabric_text_objects_from_internal(obj)
    if not text_objects:
        return None
    return {
        "version": FABRIC_JSON_VERSION,
        "objects": [_fabric_text_object(text_obj) for text_obj in text_objects],
        "background": "rgba(0, 0, 0, 0)",
    }


__all__ = ["_fabric_canvas_object"]
