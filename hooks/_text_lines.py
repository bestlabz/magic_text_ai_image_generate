"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _text_lines(text: str) -> list[str]:
    lines = [line.strip() for line in str(text or "").splitlines() if line.strip()]
    if lines:
        return lines
    words = re.findall(r"\S+", str(text or ""))
    return words or [str(text or "").strip() or "Text"]


__all__ = ["_text_lines"]
