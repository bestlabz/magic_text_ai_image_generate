"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _dedupe_repeated_phrase_text(text: str) -> str:
    clean = re.sub(r"\s+", " ", str(text or "")).strip()
    if not clean:
        return str(text or "")
    words = clean.split(" ")
    if len(words) >= 4 and len(words) % 2 == 0:
        midpoint = len(words) // 2
        if [word.lower() for word in words[:midpoint]] == [word.lower() for word in words[midpoint:]]:
            return " ".join(words[:midpoint])
    if len(words) >= 6 and len(words) % 3 == 0:
        third = len(words) // 3
        first = [word.lower() for word in words[:third]]
        if first == [word.lower() for word in words[third:third * 2]] == [word.lower() for word in words[third * 2:]]:
            return " ".join(words[:third])
    return str(text or "")


__all__ = ["_dedupe_repeated_phrase_text"]
