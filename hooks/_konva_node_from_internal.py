"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _konva_node_from_internal(obj: dict[str, Any]) -> dict[str, Any] | None:
    if obj.get("type") == "Text":
        return _konva_text_node(obj)
    children = obj.get("children")
    if not isinstance(children, list):
        return None
    node_children = [
        _konva_node_from_internal(child)
        for child in sorted(
            [child for child in children if isinstance(child, dict)],
            key=lambda child: int(child.get("zIndex") or 0),
        )
    ]
    node_children = [child for child in node_children if child is not None]
    if not node_children:
        return None
    attrs = {
        key: deepcopy(value)
        for key, value in obj.items()
        if key in KONVA_NODE_ATTR_KEYS
    }
    return {
        "attrs": attrs,
        "className": "Group",
        "children": node_children,
    }


__all__ = ["_konva_node_from_internal"]
