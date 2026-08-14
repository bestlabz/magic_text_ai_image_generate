"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _clean_hex(value: Any, default: str = "") -> str:
    if not isinstance(value, str):
        return default
    value = value.strip()
    if not value:
        return default
    if not value.startswith("#"):
        value = f"#{value}"
    if len(value) == 4 and re.fullmatch(r"#[0-9A-Fa-f]{3}", value):
        value = "#" + "".join(ch * 2 for ch in value[1:])
    return value.upper() if HEX_RE.match(value) else default


__all__ = ["_clean_hex"]
