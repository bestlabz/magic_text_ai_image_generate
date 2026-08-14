"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _canva_design_object(
    obj: dict[str, Any],
    canvas_width: int,
    canvas_height: int,
    canva_title: str | None = None,
) -> dict[str, Any] | None:
    text_objects = _fabric_text_objects_from_internal(obj)
    if not text_objects:
        return None
    elements = [
        _canva_text_element(text_obj, index)
        for index, text_obj in enumerate(
            sorted(text_objects, key=lambda text_obj: int(text_obj.get("zIndex") or 0)),
            start=1,
        )
    ]
    title = str(canva_title or "").strip() or str(text_objects[0].get("text") or "Untitled")
    return {
        "type": "canva_design",
        "version": "1.0",
        "title": title[:255],
        "canvas": {
            "width": canvas_width,
            "height": canvas_height,
            "background": "rgba(0, 0, 0, 0)",
        },
        "pages": [
            {
                "id": "page_1",
                "index": 0,
                "elements": elements,
            },
        ],
    }


__all__ = ["_canva_design_object"]
