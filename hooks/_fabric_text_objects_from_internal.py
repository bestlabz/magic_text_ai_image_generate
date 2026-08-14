"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _fabric_text_objects_from_internal(obj: dict[str, Any], offset_x: float = 0, offset_y: float = 0) -> list[dict[str, Any]]:
    if obj.get("type") == "Text":
        text_obj = deepcopy(obj)
        text_obj["x"] = float(text_obj.get("x") or 0) + offset_x
        text_obj["y"] = float(text_obj.get("y") or 0) + offset_y
        return [text_obj]
    children = obj.get("children")
    if not isinstance(children, list):
        return []
    group_x = offset_x + float(obj.get("x") or 0)
    group_y = offset_y + float(obj.get("y") or 0)
    text_objects: list[dict[str, Any]] = []
    for child in sorted(
        [child for child in children if isinstance(child, dict)],
        key=lambda child: int(child.get("zIndex") or 0),
    ):
        text_objects.extend(_fabric_text_objects_from_internal(child, group_x, group_y))
    return text_objects


__all__ = ["_fabric_text_objects_from_internal"]
