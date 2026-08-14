"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _intent_terms(text: str, mood: str | None) -> list[str]:
    raw = f"{text} {mood or ''}".lower()
    terms = re.findall(r"[a-z0-9%]+", raw)

    intent_groups = [
        (("birthday", "bday", "party", "celebrate", "celebration"), ["birthday", "happy", "marker", "pop", "script"]),
        (("thank", "thanks", "grateful", "gratitude"), ["thank", "you", "clean", "serif", "script"]),
        (("bride", "groom", "wedding", "engaged", "engagement", "love"), ["bride", "groom", "luxury", "rose", "script"]),
        (("sale", "off", "discount", "%", "deal", "offer"), ["sale", "discount", "bold", "outline", "condensed"]),
        (("open", "opening", "launch", "new"), ["open", "neon", "glow", "bold"]),
        (("logo", "brand", "studio", "tattoo"), ["logo", "studio", "badge", "arc", "clean"]),
        (("target", "roadmap", "quarter", "business", "report"), ["editorial", "mono", "label", "clean"]),
        (("royal", "gold", "luxury", "premium"), ["royal", "gold", "luxury", "serif"]),
        (("neon", "glow", "night"), ["neon", "glow", "outline"]),
    ]
    for needles, additions in intent_groups:
        if any(needle in raw for needle in needles):
            terms.extend(additions)
    return terms


__all__ = ["_intent_terms"]
