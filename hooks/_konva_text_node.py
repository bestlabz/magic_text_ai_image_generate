"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _konva_text_node(text_obj: dict[str, Any]) -> dict[str, Any]:
    attrs = {
        key: deepcopy(value)
        for key, value in text_obj.items()
        if key in KONVA_TEXT_ATTR_KEYS
    }
    attrs["fontStyle"] = _konva_font_style(text_obj)
    attrs["align"] = str(text_obj.get("align") or text_obj.get("textAlign") or "center")
    attrs["text"] = str(text_obj.get("text") or "")
    return {
        "attrs": attrs,
        "className": "Text",
    }


__all__ = ["_konva_text_node"]
