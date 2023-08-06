"""
Initialize the app
"""

# Standard Library
from importlib import metadata

__version__ = metadata.version("aa-fleetfinder")
__title__ = "Fleet Finder"
__verbose_name__ = "Fleet Finder for Alliance Auth"

del metadata
