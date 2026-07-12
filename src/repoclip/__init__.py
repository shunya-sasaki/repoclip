"""Repoclip package.

Read the contents of files in a repository and copy them to the system
clipboard.

This package exposes the :class:`Repoclip` application class and the
:func:`run` console entry point.
"""

from repoclip.repoclip import Repoclip
from repoclip.repoclip import run

__all__ = ["Repoclip", "run"]
