"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _apply_text_transform(text: str, transform: str | None) -> str:
    normalized = str(transform or "none").strip().lower()
    if normalized == "upper":
        return text.upper()
    if normalized == "lower":
        return text.lower()
    if normalized == "title":
        return text.title()
    return text


__all__ = ["_apply_text_transform"]
