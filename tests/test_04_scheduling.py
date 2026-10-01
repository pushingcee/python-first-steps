"""Task 04: slot arithmetic. Pure functions, no services involved.

Open Monday to Friday, 09:00 to 17:00, 30-minute slots. 2026-10-05 is a Monday.
"""

from datetime import datetime
from itertools import islice

import pytest

from petclinic.service.scheduling import iter_slots, next_slot_start


@pytest.mark.parametrize(
    ("moment", "expected"),
    [
        (datetime(2026, 10, 5, 10, 0), datetime(2026, 10, 5, 10, 0)),  # on a slot boundary
        (datetime(2026, 10, 5, 10, 10), datetime(2026, 10, 5, 10, 30)),  # rounds up
        (datetime(2026, 10, 5, 10, 0, 30), datetime(2026, 10, 5, 10, 30)),  # seconds count too
        (datetime(2026, 10, 5, 7, 45), datetime(2026, 10, 5, 9, 0)),  # before opening
        (datetime(2026, 10, 5, 16, 30), datetime(2026, 10, 5, 16, 30)),  # last slot of the day
        (datetime(2026, 10, 5, 16, 31), datetime(2026, 10, 6, 9, 0)),  # too late for today
        (datetime(2026, 10, 5, 17, 0), datetime(2026, 10, 6, 9, 0)),  # closed
        (datetime(2026, 10, 9, 16, 45), datetime(2026, 10, 12, 9, 0)),  # Friday -> Monday
        (datetime(2026, 10, 10, 12, 0), datetime(2026, 10, 12, 9, 0)),  # Saturday -> Monday
    ],
)
def test_next_slot_start(moment, expected):
    assert next_slot_start(moment) == expected


def test_iter_slots_rolls_over_to_the_next_working_day():
    slots = list(islice(iter_slots(datetime(2026, 10, 9, 16, 0)), 3))  # Friday 16:00

    assert slots == [
        datetime(2026, 10, 9, 16, 0),
        datetime(2026, 10, 9, 16, 30),
        datetime(2026, 10, 12, 9, 0),
    ]


def test_a_full_day_has_sixteen_slots():
    day = [slot for slot in islice(iter_slots(datetime(2026, 10, 5)), 20) if slot.day == 5]

    assert len(day) == 16
