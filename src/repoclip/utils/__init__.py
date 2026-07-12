"""Utility subpackage for repoclip.

This subpackage groups helper utilities used across repoclip. It exposes
the :class:`Clipboard` helper for copying text to the system clipboard.
"""

from repoclip.utils.clipboard import Clipboard

__all__ = ["Clipboard"]
