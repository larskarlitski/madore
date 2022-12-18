"""
    python-enhanced markdown reports
"""

from .render import render, register
from .cli import main

# register built-in renderers
from . import type_renderers


__all__ = [
    "render",
    "register",
    "main"
]
