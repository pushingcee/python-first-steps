import argparse
from typing import Protocol


class Resource(Protocol):
    """One CLI resource (the @RestController of this app).

    register() adds a top-level command (`doctor`, `owner`, ...) with its subcommands.
    Every subcommand sets `handler` via set_defaults(); a handler takes the parsed
    argparse.Namespace and returns the text to print.
    """

    def register(self, subparsers: argparse._SubParsersAction) -> None: ...
