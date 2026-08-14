"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _font_kind(font_family: str) -> str:
    lowered = font_family.lower()
    if any(word in lowered for word in (
        "script", "vibes", "pacifico", "lobster", "dancing", "roundhand", "brush",
        "satisfy", "yellowtail", "courgette", "sacramento", "allura", "parisienne",
        "calligraffitti", "cookie", "kaushan", "marck", "caveat", "handlee",
        "shadows", "permanent marker", "patrick hand"
    )):
        return "script"
    if any(word in lowered for word in (
        "playfair", "cinzel", "garamond", "merriweather", "bodoni", "georgia", "times",
        "abril", "baskerville", "cormorant", "prata", "serif", "lora", "vollkorn",
        "crimson", "bitter", "spectral", "cardo", "domine", "alegreya"
    )):
        return "serif"
    if any(word in lowered for word in (
        "bebas", "anton", "impact", "league", "goldman", "oswald", "bungee",
        "righteous", "fredoka", "alfa", "archivo black", "teko", "staatliches",
        "black ops", "luckiest", "passion one", "paytone", "rammetto"
    )):
        return "display"
    if any(word in lowered for word in ("monoton", "faster", "moonrocks", "shade", "ewert", "rye", "creepster", "frijole")):
        return "decorative"
    if any(word in lowered for word in ("courier", "mono", "code", "plex mono", "space mono", "source code")):
        return "mono"
    return "sans"


__all__ = ["_font_kind"]
