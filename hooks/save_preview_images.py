"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def save_preview_images(result: dict[str, Any], output_dir: str | Path) -> list[Path]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for index, preview in enumerate(result.get("preview_image") or [], start=1):
        uri = preview.get("image", "")
        if not isinstance(uri, str) or "," not in uri:
            continue
        raw = base64.b64decode(uri.split(",", 1)[1])
        path = output / f"magic_write_{index}.png"
        path.write_bytes(raw)
        written.append(path)
    return written


__all__ = ["save_preview_images"]
