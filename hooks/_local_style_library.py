"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _local_style_library(text: str, mood: str | None, rng: random.Random,
                         randomize: bool) -> list[dict[str, Any]]:
    library = [deepcopy(style) for style in STYLE_PRESETS]
    library.extend(deepcopy(style) for style in MODERN_MAGIC_WRITE_DATASET)
    terms = [term for term in _intent_terms(text, mood) if len(term) >= 2]

    scored: list[tuple[int, int, dict[str, Any]]] = []
    for index, style in enumerate(library):
        haystack = _style_search_text(style)
        score = sum(3 if term in haystack else 0 for term in terms)
        kind = _font_kind(str(style.get("fontFamily") or ""))
        if kind in terms:
            score += 2
        scored.append((score, index, style))

    if any(score for score, _, _ in scored):
        scored.sort(key=lambda item: (-item[0], item[1]))
        return [style for _, _, style in scored]

    if randomize:
        rng.shuffle(library)
    return library


__all__ = ["_local_style_library"]
