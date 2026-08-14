"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _text_visual_height_for_child(child: dict[str, Any]) -> float:
    text = str(child.get("text") or "")
    lines = text.splitlines() or [text]
    size = float(child.get("fontSize") or 36)
    italic = str(child.get("fontStyle") or "").lower() == "italic"
    font = _load_font(child.get("fontFamily", "Arial"), size, child.get("fontWeight"), italic)
    draw = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line or " ", font=font)
        heights.append(max(bbox[3] - bbox[1], size * 0.5))
    return sum(heights) * float(child.get("lineHeight") or 1.0)


__all__ = ["_text_visual_height_for_child"]
