"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _normalize_output_format(output_format: str | None = None, output_type: str | None = None) -> str:
    normalized = str(output_format or output_type or "konva").strip().lower()
    aliases = {
        "konva": "konva",
        "canvas": "canvas",
        "html_canvas": "canvas",
        "html-canvas": "canvas",
        "canva": "canvas",
        "canva_design": "canva_design",
        "canva-design": "canva_design",
        "canva_export": "canva_design",
        "canva-export": "canva_design",
        "fabric": "fabric",
        "fabricjs": "fabric",
        "fabric.js": "fabric",
    }
    if normalized not in aliases:
        raise ValueError("output format must be 'konva', 'canvas', 'canva', 'canva_design', or 'fabric'")
    return aliases[normalized]


__all__ = ["_normalize_output_format"]
