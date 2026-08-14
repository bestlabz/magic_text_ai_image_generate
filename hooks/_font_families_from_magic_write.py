"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _font_families_from_magic_write(objects: list[dict[str, Any]], primary_per_group: bool = False) -> list[str]:
    families: list[str] = []
    seen = set()
    for obj in objects:
        candidates = obj.get("children") if isinstance(obj.get("children"), list) else [obj]
        if primary_per_group and isinstance(candidates, list):
            primary = next(
                (
                    child
                    for child in candidates
                    if isinstance(child, dict) and str(child.get("magicWriteRole") or "") == "main"
                ),
                None,
            )
            candidates = [primary or next((child for child in candidates if isinstance(child, dict)), None)]
        for child in candidates:
            if not isinstance(child, dict):
                continue
            family = str(child.get("fontFamily") or "").strip()
            key = family.lower()
            if family and key not in seen:
                families.append(family)
                seen.add(key)
    return families


__all__ = ["_font_families_from_magic_write"]
