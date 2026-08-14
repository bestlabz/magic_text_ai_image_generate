"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _system_font_path(family: str, bold: bool, allow_default: bool = True) -> Path | None:
    lowered = family.strip().lower()
    if bold and lowered in {"arial", "georgia"}:
        lowered = f"{lowered} bold"
    candidates = []
    if lowered in FONT_FILES:
        candidates.append(MAC_FONT_DIR / FONT_FILES[lowered])
    if "brush" in lowered:
        candidates.append(MAC_FONT_DIR / FONT_FILES["brush script"])
    if "script" in lowered or "vibes" in lowered or "roundhand" in lowered:
        candidates.append(MAC_FONT_DIR / FONT_FILES["snell roundhand"])
    if "serif" in lowered or "gold" in lowered or "georgia" in lowered:
        candidates.append(MAC_FONT_DIR / ("Georgia Bold.ttf" if bold else "Georgia.ttf"))
    if allow_default:
        candidates.extend(
            [
                MAC_FONT_DIR / ("Arial Bold.ttf" if bold else "Arial.ttf"),
                MAC_CORE_FONT_DIR / "Helvetica.ttc",
            ]
        )
    linux_sans = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    linux_serif = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    linux_mono = "DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"
    if "mono" in lowered or "courier" in lowered:
        candidates.extend(font_dir / linux_mono for font_dir in LINUX_FONT_DIRS)
    elif "serif" in lowered or lowered in {"georgia", "times new roman", "times new roman bold"}:
        candidates.extend(font_dir / linux_serif for font_dir in LINUX_FONT_DIRS)
    if allow_default:
        candidates.extend(font_dir / linux_sans for font_dir in LINUX_FONT_DIRS)
    return next((p for p in candidates if p.exists()), None)


__all__ = ["_system_font_path"]
