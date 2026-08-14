"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def _resolve_generation_seed(seed: int | None = None) -> int:
    if seed is not None:
        return int(seed)
    return random.SystemRandom().randrange(0, 2**63)


__all__ = ["_resolve_generation_seed"]
