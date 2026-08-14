#!/usr/bin/env python3
"""Compatibility entry point for the split Magic Write implementation."""

from __future__ import annotations

from hooks import magic_write_core as _core
from hooks import *  # noqa: F401,F403 - preserve the original magic_write module API.

for _name in dir(_core):
    if not (_name.startswith("__") and _name.endswith("__")) and _name not in globals():
        globals()[_name] = getattr(_core, _name)

__all__ = [
    _name
    for _name in globals()
    if not (_name.startswith("__") and _name.endswith("__"))
    and _name not in {"annotations", "_core"}
]
