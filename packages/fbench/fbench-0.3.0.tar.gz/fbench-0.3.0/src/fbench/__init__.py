from importlib import metadata

__version__ = metadata.version("fbench")

from .config import *
from .function import *
from .validation import *
from .visualization import *

del (
    metadata,
    config,
    function,
    validation,
    visualization,
)
