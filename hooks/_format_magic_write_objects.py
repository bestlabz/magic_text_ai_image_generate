"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _format_magic_write_objects(
    objects: list[dict[str, Any]],
    output_format: str,
    canvas_width: int,
    canvas_height: int,
    canva_title: str | None = None,
) -> list[dict[str, Any]]:
    if output_format == "konva":
        return [
            stage
            for obj in objects
            if isinstance(obj, dict)
            for stage in [_konva_stage_object(obj, canvas_width, canvas_height)]
            if stage is not None
        ]
    if output_format == "fabric":
        return [
            canvas
            for obj in objects
            if isinstance(obj, dict)
            for canvas in [_fabric_canvas_object(obj, canvas_width, canvas_height)]
            if canvas is not None
        ]
    if output_format == "canvas":
        return [
            canvas
            for obj in objects
            if isinstance(obj, dict)
            for canvas in [_canvas_json_object(obj, canvas_width, canvas_height)]
            if canvas is not None
        ]
    return [
        design
        for obj in objects
        if isinstance(obj, dict)
        for design in [_canva_design_object(obj, canvas_width, canvas_height, canva_title)]
        if design is not None
    ]


__all__ = ["_format_magic_write_objects"]
