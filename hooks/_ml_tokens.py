"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _ml_tokens(text: str) -> list[str]:
    normalized = str(text or "").lower()
    words = re.findall(r"[a-z0-9%]+", normalized)
    compact = re.sub(r"[^a-z0-9%]+", " ", normalized).strip()
    char_tokens: list[str] = []
    for word in words:
        padded = f"_{word}_"
        char_tokens.extend(padded[index:index + 3] for index in range(max(len(padded) - 2, 0)))
    return words + char_tokens + compact.split()


__all__ = ["_ml_tokens"]
