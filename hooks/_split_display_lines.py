"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _split_display_lines(text: str, max_lines: int = 2) -> list[str]:
    lines = _text_lines(text)
    connectors = {"&", "+", "and", "AND"}
    compacted: list[str] = []
    index = 0
    while index < len(lines):
        if index + 2 < len(lines) and lines[index + 1].strip() in connectors:
            compacted.append(f"{lines[index]} {lines[index + 1].strip()}")
            compacted.append(lines[index + 2])
            index += 3
            continue
        compacted.append(lines[index])
        index += 1

    if len(compacted) <= max_lines:
        return compacted
    lines = compacted
    words = re.findall(r"\S+", " ".join(lines))
    if len(words) <= 2:
        return [" ".join(words)] if words else lines
    midpoint = max(1, len(words) // 2)
    return [" ".join(words[:midpoint]), " ".join(words[midpoint:])]


__all__ = ["_split_display_lines"]
