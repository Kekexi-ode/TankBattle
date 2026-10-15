"""
tankbattle package wrapper
This package provides a simple entrypoint so you can run the uploaded game with:

    python -m tankbattle

It delegates execution to the uploaded script located at the repository path "坦克大战/main.py" so we don't have to move your files.
"""

from .__main__ import main

__all__ = ["main"]
