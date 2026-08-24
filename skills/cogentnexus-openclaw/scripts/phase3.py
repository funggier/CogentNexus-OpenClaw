#!/usr/bin/env python3
"""Deprecated compatibility entry point; use runtime.py."""
from pathlib import Path
import runpy
import warnings

warnings.warn("phase3.py is deprecated; use runtime.py", DeprecationWarning, stacklevel=2)
runpy.run_path(str(Path(__file__).with_name("runtime.py")), run_name="__main__")
