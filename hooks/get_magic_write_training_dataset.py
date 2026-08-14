"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def get_magic_write_training_dataset() -> dict[str, Any]:
    """Return the reusable Magic Write trained dataset/configuration."""
    return {
        "name": "magic_write",
        "version": MAGIC_WRITE_DATASET_VERSION,
        "canvas": {
            "width": DEFAULT_CANVAS_WIDTH,
            "height": DEFAULT_CANVAS_HEIGHT,
            "preview_scale": DEFAULT_PREVIEW_SCALE,
        },
        "fonts": {
            "families": deepcopy(CANVA_FONT_FAMILIES),
            "groups": deepcopy(CANVA_FONT_GROUPS),
            "kind_order": deepcopy(FONT_KIND_ORDER),
        },
        "style_presets": deepcopy(STYLE_PRESETS),
        "modern_style_dataset": deepcopy(MODERN_MAGIC_WRITE_DATASET),
        "modern_composition_templates": deepcopy(MODERN_COMPOSITION_TEMPLATES),
        "modern_composition_palettes": deepcopy(MODERN_COMPOSITION_PALETTES),
        "modern_composition_effects": deepcopy(MODERN_COMPOSITION_EFFECTS),
    }


__all__ = ["get_magic_write_training_dataset"]
