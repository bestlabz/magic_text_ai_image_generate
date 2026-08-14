"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _modern_palette_value(palette: dict[str, str], mode: str) -> str:
    return _clean_hex(palette.get(mode), "") if mode else ""


__all__ = ["_modern_palette_value"]
