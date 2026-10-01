import os
from collections.abc import Callable, Iterator
from datetime import datetime

import pytest

from petclinic.cli import build_parser, run_command
from petclinic.clock import FixedClock
from petclinic.container import ApplicationContext, create_context

NOW = datetime(2026, 10, 5, 10, 0)  # a Monday, 10:00

# Phase 2: set this to run every test against Postgres instead of the in-memory repositories.
DATABASE_URL = os.environ.get("PETCLINIC_DATABASE_URL")


@pytest.fixture(autouse=True)
def _empty_database() -> None:
    """Against Postgres, every test starts from empty tables with ids back at 1, just like a
    fresh in-memory context. Does nothing in phase 1."""
    if DATABASE_URL:
        _truncate_all_tables(DATABASE_URL)


@pytest.fixture
def context() -> Iterator[ApplicationContext]:
    """A fresh application per test, with time frozen at NOW."""
    context = create_context(FixedClock(NOW))
    yield context
    context.close()


@pytest.fixture
def cli(context: ApplicationContext) -> Callable[[str], str]:
    """Runs one shell line against `context` and returns what would be printed."""
    parser = build_parser(context.resources)
    return lambda line: run_command(parser, line)


@pytest.fixture
def api(context: ApplicationContext):
    """Phase 3: an HTTP client for the FastAPI app built on `context`. Skips the test until
    FastAPI and httpx are installed."""
    testclient = pytest.importorskip("fastapi.testclient")
    from petclinic.api import create_app

    with testclient.TestClient(create_app(context)) as client:
        yield client


def _truncate_all_tables(database_url: str) -> None:
    import psycopg  # installed in phase 2
    from psycopg import sql

    with psycopg.connect(database_url, autocommit=True) as connection:
        rows = connection.execute(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        ).fetchall()
        if rows:
            tables = sql.SQL(", ").join(sql.Identifier(name) for (name,) in rows)
            connection.execute(sql.SQL("TRUNCATE {} RESTART IDENTITY CASCADE").format(tables))
