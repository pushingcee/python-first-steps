"""Clinic opening hours and 30-minute slots. Pure functions: no repositories, no clock."""

from collections.abc import Iterator
from datetime import datetime, time, timedelta

OPENING_TIME = time(9, 0)
CLOSING_TIME = time(17, 0)
SLOT_LENGTH = timedelta(minutes=30)
WORKING_DAYS = {0, 1, 2, 3, 4}  # Monday to Friday, as datetime.weekday() numbers

# ---- TODO task 04 ----------------------------------------------------------------------


def next_slot_start(moment: datetime) -> datetime:
    """The earliest slot start at or after `moment`.

    Slots start every 30 minutes from opening time, and the whole slot must end by closing
    time, so the last slot of a day starts at 16:30. Weekends are skipped.
    Useful: datetime.combine(), .date(), .weekday(), and timedelta arithmetic.
    """
    raise NotImplementedError("task 04")


def iter_slots(start: datetime) -> Iterator[datetime]:
    """Every slot start from `start` onwards, in order, forever.

    Write this as a generator (a function that uses `yield`). Callers take as many slots as
    they need, so it never has to stop.
    """
    raise NotImplementedError("task 04")
