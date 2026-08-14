"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _is_bold_font_weight(value: Any) -> bool:
    normalized = str(value or "").strip().lower()
    if normalized in {"bold", "bolder"}:
        return True
    try:
        return int(float(normalized)) >= 600
    except ValueError:
        return False


__all__ = ["_is_bold_font_weight"]
