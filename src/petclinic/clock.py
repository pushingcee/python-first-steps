"""Injectable time source, like java.time.Clock.

Services never call datetime.now() directly, so tests can freeze time with FixedClock.
"""

from datetime import datetime
from typing import Protocol


class Clock(Protocol):
    def now(self) -> datetime: ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now().replace(second=0, microsecond=0)


class FixedClock:
    """Always returns the same instant. Used in tests."""

    def __init__(self, instant: datetime) -> None:
        self._instant = instant

    def now(self) -> datetime:
        return self._instant
