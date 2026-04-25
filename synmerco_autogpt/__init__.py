"""synmerco-autogpt — 46 AutoGPT commands for AI agent commerce.

Two ways to use:
    1. AutoGPT Component: SynmercoComponent (CommandProvider)
    2. Standalone: SynmercoCommands (no AutoGPT needed)
"""

from synmerco_autogpt._commands import SynmercoCommands
from synmerco_autogpt._component import SynmercoComponent, is_autogpt_available
from synmerco_autogpt._client import SynmercoHTTPClient, SynmercoAPIError

__version__ = "1.0.0"
__all__ = ["SynmercoCommands", "SynmercoComponent", "is_autogpt_available", "SynmercoHTTPClient", "SynmercoAPIError"]
