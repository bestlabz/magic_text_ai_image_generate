"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _konva_font_style(text_obj: dict[str, Any]) -> str:
    parts: list[str] = []
    font_style = str(text_obj.get("fontStyle") or "normal").strip().lower()
    font_weight = str(text_obj.get("fontWeight") or "").strip().lower()
    if "italic" in font_style:
        parts.append("italic")
    if "bold" in font_style or _is_bold_font_weight(font_weight):
        parts.append("bold")
    if not parts and font_weight and font_weight not in {"normal", "400"}:
        parts.append(font_weight)
    return " ".join(parts) if parts else "normal"


__all__ = ["_konva_font_style"]
