"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _normalize_repeated_child_text(children: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = deepcopy(children)
    for child in normalized:
        if isinstance(child, dict) and child.get("type") == "Text":
            child["text"] = _dedupe_repeated_phrase_text(str(child.get("text") or ""))
    return normalized


__all__ = ["_normalize_repeated_child_text"]
