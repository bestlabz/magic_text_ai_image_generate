"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _use_single_font_family_per_group(children: list[dict[str, Any]]) -> list[dict[str, Any]]:
    primary = next(
        (
            child
            for child in children
            if isinstance(child, dict) and str(child.get("magicWriteRole") or "") == "main"
        ),
        None,
    )
    fallback = next((child for child in children if isinstance(child, dict)), None)
    family = str((primary or fallback or {}).get("fontFamily") or "").strip()
    if not family:
        return children
    for child in children:
        if isinstance(child, dict) and child.get("type") == "Text":
            child["fontFamily"] = family
    return children


__all__ = ["_use_single_font_family_per_group"]
