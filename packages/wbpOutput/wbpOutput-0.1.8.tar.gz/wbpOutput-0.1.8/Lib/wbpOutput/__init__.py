"""
Implementation of the output plugin.
"""

from .outputwin import outputPanel
from .preferences import OutputWinPreferences

__version__ = "0.1.8"

panels = [outputPanel]
preferencepages = [OutputWinPreferences]
