"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

class MagicWriteModel:
    """Small reusable local wrapper for separate projects."""

    def __init__(
        self,
        model: str | None = None,
        timeout: int = 45,
        canvas_width: int = DEFAULT_CANVAS_WIDTH,
        canvas_height: int = DEFAULT_CANVAS_HEIGHT,
    ) -> None:
        # model/timeout are accepted for backwards compatibility; generation is local.
        self.model = LOCAL_MAGIC_WRITE_MODEL
        self.timeout = timeout
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.dataset = get_magic_write_training_dataset()

    def generate(
        self,
        text: str,
        count: int = 12,
        modern: bool = True,
        seed: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return generate_magic_write(
            text=text,
            count=count,
            model=self.model,
            timeout=self.timeout,
            canvas_width=self.canvas_width,
            canvas_height=self.canvas_height,
            modern=modern,
            seed=seed,
            **kwargs,
        )


__all__ = ["MagicWriteModel"]
