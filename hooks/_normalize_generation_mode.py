"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _normalize_generation_mode(
    generation_mode: str | None,
    modern: bool,
    ml_model_path: str | os.PathLike[str] | None,
    all_google_fonts: bool,
    all_fonts: bool,
    font_families: list[str] | tuple[str, ...] | str | None,
) -> str:
    if all_google_fonts:
        return "all_google_fonts"
    if all_fonts or font_families:
        return "all_fonts"
    if generation_mode is None:
        if ml_model_path:
            return "ml"
        return "modern_text" if modern else "classic"
    normalized = str(generation_mode).strip().lower().replace("-", "_")
    aliases = {
        "modern": "modern_text",
        "modern_text": "modern_text",
        "text": "modern_text",
        "modern_composition": "modern_composition",
        "composition": "modern_composition",
        "classic": "classic",
        "style_presets": "classic",
        "ml": "ml",
        "machine_learning": "ml",
    }
    if normalized not in aliases:
        raise ValueError("generation mode must be 'modern_text', 'modern_composition', 'classic', or 'ml'")
    mode = aliases[normalized]
    if mode == "ml" and not ml_model_path:
        raise ValueError("generation mode 'ml' requires ml_model_path")
    return mode


__all__ = ["_normalize_generation_mode"]
