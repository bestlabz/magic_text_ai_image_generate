"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _render_group_preview_data_uri(
    group_obj: dict[str, Any],
    canvas_width: int,
    canvas_height: int,
    scale: int,
) -> str:
    width = canvas_width * scale
    height = canvas_height * scale
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    group_x = float(group_obj.get("x") or 0)
    group_y = float(group_obj.get("y") or 0)
    children = [deepcopy(child) for child in group_obj.get("children", []) if isinstance(child, dict)]
    children.sort(key=lambda child: int(child.get("zIndex") or 0))
    for child in children:
        if child.get("type") == "Text":
            child["x"] = float(child.get("x") or 0) + group_x
            child["y"] = float(child.get("y") or 0) + group_y
            _draw_text_object_on_layer(img, child, scale)
    img = _trim_transparent_preview(img, scale)
    out = io.BytesIO()
    img.save(out, format="PNG")
    return "data:image/png;base64," + base64.b64encode(out.getvalue()).decode("ascii")


__all__ = ["_render_group_preview_data_uri"]
