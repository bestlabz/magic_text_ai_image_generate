"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _remove_duplicate_text_children(children: list[dict[str, Any]]) -> list[dict[str, Any]]:
    children = [
        child
        for child in children
        if not isinstance(child, dict)
        or child.get("type") != "Text"
        or str(child.get("text") or "").strip()
    ]
    grouped: dict[str, list[dict[str, Any]]] = {}
    order: list[str] = []
    for child in children:
        if not isinstance(child, dict):
            continue
        key = re.sub(r"\s+", " ", str(child.get("text") or "").strip()).lower()
        if not key:
            continue
        if key not in grouped:
            grouped[key] = []
            order.append(key)
        grouped[key].append(child)

    keep_ids: set[str] = set()
    for key in order:
        candidates = grouped[key]
        chosen = next(
            (child for child in candidates if str(child.get("magicWriteRole") or "") == "main"),
            max(candidates, key=lambda child: float(child.get("fontSize") or 0)),
        )
        keep_ids.add(str(chosen.get("id") or ""))
        depth_candidates = [
            child
            for child in candidates
            if child.get("magicWriteKeepDuplicate")
            and str(child.get("id") or "") != str(chosen.get("id") or "")
        ]
        if depth_candidates:
            chosen_x = float(chosen.get("x") or 0)
            chosen_y = float(chosen.get("y") or 0)
            depth = min(
                depth_candidates,
                key=lambda child: (
                    abs(float(child.get("x") or 0) - chosen_x) + abs(float(child.get("y") or 0) - chosen_y),
                    int(child.get("zIndex") or 0),
                ),
            )
            keep_ids.add(str(depth.get("id") or ""))

    return [
        child
        for child in children
        if not isinstance(child, dict)
        or not str(child.get("text") or "").strip()
        or str(child.get("id") or "") in keep_ids
    ]


__all__ = ["_remove_duplicate_text_children"]
