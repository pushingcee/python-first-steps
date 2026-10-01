"""Phase 2, task 13: Postgres. Skipped unless PETCLINIC_DATABASE_URL is set.

With the variable set, every other test file also runs against Postgres (see conftest.py),
so `PETCLINIC_DATABASE_URL=... uv run pytest` is the whole definition of done. These tests add
what in-memory storage can't show: data outlives the process, and types survive the round trip.
"""

from datetime import date

import pytest
from conftest import DATABASE_URL, NOW

from petclinic.clock import FixedClock
from petclinic.container import create_context
from petclinic.model import PetType, Specialty

pytestmark = pytest.mark.skipif(
    not DATABASE_URL, reason="phase 2: set PETCLINIC_DATABASE_URL to run against Postgres"
)


@pytest.fixture
def restarted():
    """A second application on the same database, as if the shell had been restarted."""
    context = create_context(FixedClock(NOW))
    yield context
    context.close()


def test_doctor_and_specialties_survive_a_restart(context, restarted):
    doctor = context.doctor_service.add_doctor("James", "Carter")
    context.doctor_service.add_specialty(doctor.id, Specialty.SURGERY)
    context.doctor_service.add_specialty(doctor.id, Specialty.DENTISTRY)

    loaded = restarted.doctor_service.get_doctor(doctor.id)

    assert loaded.specialties == {Specialty.SURGERY, Specialty.DENTISTRY}
    assert all(isinstance(s, Specialty) for s in loaded.specialties)


def test_owner_pet_and_visit_survive_a_restart(context, restarted):
    owner = context.owner_service.add_owner(
        "George", "Franklin", "110 W. Liberty St.", "Madison", "6085551023"
    )
    pet = context.pet_service.add_pet(owner.id, "Leo", date(2020, 9, 7), PetType.CAT)
    context.doctor_service.add_doctor("James", "Carter")
    visit = context.visit_service.book_visit(pet.id, "rabies shot")

    assert restarted.owner_service.get_owner(owner.id) == owner
    loaded_pet = restarted.pet_service.get_pet(pet.id)
    assert loaded_pet == pet
    assert isinstance(loaded_pet.type, PetType)
    assert isinstance(loaded_pet.birth_date, date)
    assert restarted.visit_service.visits_for_pet(pet.id) == [visit]


def test_booked_slot_stays_taken_after_a_restart(context, restarted):
    owner = context.owner_service.add_owner(
        "George", "Franklin", "110 W. Liberty St.", "Madison", "6085551023"
    )
    pet = context.pet_service.add_pet(owner.id, "Leo", date(2020, 9, 7), PetType.CAT)
    doctor = context.doctor_service.add_doctor("James", "Carter")
    first = context.visit_service.book_visit(pet.id, "checkup")

    assert restarted.visit_service.first_available_slot(doctor.id) > first.start


@pytest.mark.parametrize("prefix", ["%", "_ranklin", "Fr%n"])
def test_like_wildcards_in_a_search_are_plain_characters(context, prefix):
    context.owner_service.add_owner(
        "George", "Franklin", "110 W. Liberty St.", "Madison", "6085551023"
    )

    assert context.owner_service.find_by_last_name(prefix) == []


def test_quotes_in_input_are_stored_as_text(context, restarted):
    owner = context.owner_service.add_owner(
        "Robert'); DROP TABLE owner;--", "O'Brien", "1 Main St.", "Madison", "6085551023"
    )

    assert restarted.owner_service.get_owner(owner.id).last_name == "O'Brien"
    assert [o.id for o in restarted.owner_service.find_by_last_name("o'b")] == [owner.id]
