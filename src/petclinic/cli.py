"""Interactive shell. In-memory storage only lives as long as the process, so the app runs
as a REPL: each line is parsed with argparse, just like a one-shot command would be."""

import argparse
import shlex
from collections.abc import Sequence
from typing import NoReturn

from petclinic.container import create_context
from petclinic.exceptions import PetClinicError
from petclinic.resource.resource import Resource


class CliUsageError(Exception):
    """Raised instead of argparse's default behaviour of printing and exiting."""


class CliArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise CliUsageError(f"{self.prog}: error: {message}")


def build_parser(resources: Sequence[Resource]) -> CliArgumentParser:
    parser = CliArgumentParser(prog="petclinic", description="Spring PetClinic, CLI edition")
    subparsers = parser.add_subparsers(dest="resource", required=True, metavar="<resource>")
    for resource in resources:
        resource.register(subparsers)
    return parser


def run_command(parser: argparse.ArgumentParser, line: str) -> str:
    """Parse one line, dispatch it to its handler and return the text to print."""
    try:
        args = parser.parse_args(shlex.split(line))
    except CliUsageError as e:
        return str(e)
    except ValueError as e:  # shlex: unbalanced quotes
        return f"error: {e}"
    except SystemExit:  # --help printed the help text and tried to exit
        return ""

    handler = getattr(args, "handler", None)
    if handler is None:
        return "error: command not implemented yet"
    try:
        return handler(args)
    except PetClinicError as e:
        return f"error: {e}"
    except NotImplementedError as e:
        return f"error: not implemented yet ({e})"


def main() -> int:
    context = create_context()
    try:
        return _repl(build_parser(context.resources))
    finally:
        context.close()


def _repl(parser: argparse.ArgumentParser) -> int:
    print("PetClinic shell. Try `doctor --help`. `help` lists resources, `exit` quits.")
    while True:
        try:
            line = input("petclinic> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if line in {"exit", "quit"}:
            return 0
        if not line:
            continue
        output = run_command(parser, "--help" if line == "help" else line)
        if output:
            print(output)
