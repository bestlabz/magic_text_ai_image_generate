"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _assign_generation_text_ids(objects: list[dict[str, Any]], seed: int) -> None:
    id_rng = random.Random(f"magic-write-ids:{seed}")

    def assign(node: dict[str, Any]) -> None:
        if node.get("type") == "Text":
            node["id"] = f"text_{uuid.UUID(int=id_rng.getrandbits(128))}"
        elif node.get("type") == "Group":
            node["id"] = f"group_{uuid.UUID(int=id_rng.getrandbits(128))}"
        children = node.get("children")
        if isinstance(children, list):
            for child in children:
                if isinstance(child, dict):
                    assign(child)

    for obj in objects:
        if isinstance(obj, dict):
            assign(obj)


__all__ = ["_assign_generation_text_ids"]
