"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _composition_alpha_bbox(
    children: list[dict[str, Any]],
    canvas_width: int,
    canvas_height: int,
    scale: int = 2,
) -> tuple[float, float, float, float] | None:
    width = canvas_width * scale
    height = canvas_height * scale
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ordered = [child for child in children if isinstance(child, dict)]
    ordered.sort(key=lambda child: int(child.get("zIndex") or 0))
    for child in ordered:
        if child.get("type") == "Text":
            _draw_text_object_on_layer(img, child, scale)
    bbox = img.getchannel("A").getbbox()
    if not bbox:
        return None
    return tuple(value / scale for value in bbox)  # type: ignore[return-value]


__all__ = ["_composition_alpha_bbox"]
