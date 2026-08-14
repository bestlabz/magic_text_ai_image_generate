"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _composition_text_object(
    name: str,
    category: str,
    children: list[dict[str, Any]],
    z_index: int,
    canvas_width: int,
    canvas_height: int,
) -> dict[str, Any]:
    text_children = [deepcopy(child) for child in children if isinstance(child, dict) and child.get("type") == "Text"]
    if not text_children:
        return _konva_text("Text", {"name": name, "category": category}, z_index, canvas_width, canvas_height)
    for index, child in enumerate(sorted(text_children, key=lambda child: int(child.get("zIndex") or 0)), start=1):
        child["zIndex"] = z_index * 10 + index
        child["draggable"] = True
        child["listening"] = True
    return {
        "id": f"group_{uuid.uuid4()}",
        "type": "Group",
        "name": name,
        "category": category,
        "x": 0.0,
        "y": 0.0,
        "width": canvas_width,
        "height": canvas_height,
        "zIndex": z_index,
        "draggable": True,
        "listening": True,
        "children": text_children,
    }


__all__ = ["_composition_text_object"]
