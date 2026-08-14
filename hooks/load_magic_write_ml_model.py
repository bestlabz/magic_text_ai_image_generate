"""Generated hook module for Magic Write.

The shared runtime lives in hooks.magic_write_core so the split modules keep
all constants, datasets, and helper functions consistent with the original
single-file implementation.
"""

from . import magic_write_core as _core

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")):
        globals()[_name] = getattr(_core, _name)

def load_magic_write_ml_model(path: str | os.PathLike[str]) -> dict[str, Any]:
    model_path = Path(path)
    if model_path.suffix.lower() == ".pkl":
        model = pickle.loads(model_path.read_bytes())
    else:
        model = json.loads(model_path.read_text(encoding="utf-8"))
    if not isinstance(model, dict):
        raise ValueError(f"{model_path} is not a Magic Write ML model")
    if model.get("format") != MAGIC_WRITE_ML_MODEL_FORMAT:
        raise ValueError(f"{model_path} is not a Magic Write ML model")
    return model


__all__ = ["load_magic_write_ml_model"]
