"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _canvas_font_css(text_obj: dict[str, Any]) -> str:
    style = str(text_obj.get("fontStyle") or "normal").strip() or "normal"
    weight = str(text_obj.get("fontWeight") or "normal").strip() or "normal"
    size = float(text_obj.get("fontSize") or 36)
    line_height = float(text_obj.get("lineHeight") or 1)
    family = str(text_obj.get("fontFamily") or "Arial").strip() or "Arial"
    family = family.replace('"', '\\"')
    return f'{style} {weight} {size}px/{line_height} "{family}"'


__all__ = ["_canvas_font_css"]
