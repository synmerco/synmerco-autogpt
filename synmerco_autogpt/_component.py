"""AutoGPT Component — implements CommandProvider protocol.

Compat: Uses real AutoGPT CommandProvider when available,
falls back to standalone mode without AutoGPT installed.
"""

from __future__ import annotations

from typing import Any, Iterator

from synmerco_autogpt._commands import SynmercoCommands
from synmerco_autogpt._registry import TOOLS

# Compat shim for AutoGPT component architecture
try:
    from forge.agent.components import AgentComponent
    from forge.command import Command, command
    from forge.agent.protocols import CommandProvider
    _AUTOGPT_AVAILABLE = True
except ImportError:
    _AUTOGPT_AVAILABLE = False

    class AgentComponent:
        pass

    class CommandProvider:
        pass


class SynmercoComponent(AgentComponent, CommandProvider):
    """AutoGPT component that provides 46 Synmerco commerce commands.

    Usage:
        class MyAgent(Agent):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.synmerco = SynmercoComponent(api_key="...")
    """

    def __init__(self, api_key: str | None = None, base_url: str | None = None, timeout: float = 30.0):
        self.cmds = SynmercoCommands(api_key=api_key, base_url=base_url, timeout=timeout)

    def get_commands(self) -> Iterator:
        """Yield all Synmerco commands for AutoGPT command registration."""
        for t in TOOLS:
            name = t["name"]
            method = getattr(self.cmds, name, None)
            if method:
                yield name, t["description"], method


def is_autogpt_available() -> bool:
    return _AUTOGPT_AVAILABLE
