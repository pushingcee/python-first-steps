from collections.abc import Callable
from datetime import datetime

import pytest

from petclinic.cli import build_parser, run_command
from petclinic.clock import FixedClock
from petclinic.container import ApplicationContext, create_context

NOW = datetime(2026, 10, 5, 10, 0)  # a Monday, 10:00


@pytest.fixture
def context() -> ApplicationContext:
    """A fresh application per test, with time frozen at NOW."""
    return create_context(FixedClock(NOW))


@pytest.fixture
def cli(context: ApplicationContext) -> Callable[[str], str]:
    """Runs one shell line against `context` and returns what would be printed."""
    parser = build_parser(context.resources)
    return lambda line: run_command(parser, line)
