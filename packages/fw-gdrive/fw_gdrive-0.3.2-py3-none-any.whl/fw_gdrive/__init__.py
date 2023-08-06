"""Flywheel Googl Drive utilities helper library."""
import typing as t
from importlib.metadata import version
from pathlib import Path

try:
    # To find the version of the current module
    __version__ = version(__package__)
except:
    pass
ROOT_FOLDER = Path(__file__).parents[1]

AnyPath = t.Union[str, Path]
