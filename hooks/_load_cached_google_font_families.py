"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _load_cached_google_font_families() -> list[str]:
    try:
        data = json.loads(GOOGLE_FONTS_CACHE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if isinstance(data, dict):
        families = data.get("families", [])
    else:
        families = data
    if not isinstance(families, list):
        return []
    return _normalize_font_families(families)


__all__ = ["_load_cached_google_font_families"]
