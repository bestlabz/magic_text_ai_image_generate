"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _fabric_char_spacing(text_obj: dict[str, Any]) -> float:
    font_size = float(text_obj.get("fontSize") or 36)
    if font_size <= 0:
        return 0
    return round((float(text_obj.get("letterSpacing") or 0) / font_size) * 1000, 3)


__all__ = ["_fabric_char_spacing"]
