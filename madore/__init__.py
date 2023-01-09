"""
    python-enhanced markdown reports
"""

import builtins
import importlib
import os
import pkgutil

from .render import render, register
from .cli import main


__all__ = [
    "render",
    "register",
    "main"
]

#
# Renderers are named after python packages. Hook into the import machinery to
# only load them when the corresponding package is loaded, so that madore
# doesn't hard-depend on all of them.
#

modules = { m.name for m in pkgutil.iter_modules([__path__[0] + "/renderers"]) }

def madore_import(name, *args, **kwargs):
    if name in modules:
        importlib.import_module(f".renderers.{name}", __package__)
    return importlib.__import__(name, *args, **kwargs)

builtins.__import__ = madore_import
