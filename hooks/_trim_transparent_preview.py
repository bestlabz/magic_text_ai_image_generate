"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _trim_transparent_preview(
    img: Image.Image,
    scale: int,
    padding: int = 10,
    output_scale: float = DEFAULT_PREVIEW_OUTPUT_SCALE,
) -> Image.Image:
    rgba = img.convert("RGBA")
    alpha_bbox = rgba.getchannel("A").getbbox()
    if not alpha_bbox:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))

    pad = max(int(padding * scale), 0)
    left = max(alpha_bbox[0] - pad, 0)
    top = max(alpha_bbox[1] - pad, 0)
    right = min(alpha_bbox[2] + pad, rgba.width)
    bottom = min(alpha_bbox[3] + pad, rgba.height)
    cropped = rgba.crop((left, top, right, bottom))

    source_scale = max(float(scale), 1.0)
    retained_scale = min(max(float(output_scale), 1.0), source_scale)
    target_width = max(1, int(round(cropped.width * retained_scale / source_scale)))
    target_height = max(1, int(round(cropped.height * retained_scale / source_scale)))
    if target_width == cropped.width and target_height == cropped.height:
        return cropped
    return cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)


__all__ = ["_trim_transparent_preview"]
