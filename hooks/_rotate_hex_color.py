"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _rotate_hex_color(value: str, shift: int) -> str:
    color = _clean_hex(value, "")
    if not color:
        return value
    red = int(color[1:3], 16)
    green = int(color[3:5], 16)
    blue = int(color[5:7], 16)
    channels = [red, green, blue]
    shift = shift % 3
    if shift:
        channels = channels[-shift:] + channels[:-shift]
    return f"#{channels[0]:02X}{channels[1]:02X}{channels[2]:02X}"


__all__ = ["_rotate_hex_color"]
