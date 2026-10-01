"""Task 05: booking visits. Now is Monday 2026-10-05 10:00 (see conftest.NOW)."""

from datetime import date, datetime

import pytest

from petclinic.exceptions import NotFoundError, ValidationError
from petclinic.model import PetType, Specialty

MONDAY_10_00 = datetime(2026, 10, 5, 10, 0)
MONDAY_10_30 = datetime(2026, 10, 5, 10, 30)


@pytest.fixture
def pet(context):
    owner = context.owner_service.add_owner(
        "George", "Franklin", "110 W. Liberty St.", "Madison", "6085551023"
    )
    return context.pet_service.add_pet(owner.id, "Leo", date(2020, 9, 7), PetType.CAT)


@pytest.fixture
def carter(context):
    return context.doctor_service.add_doctor("James", "Carter")  # id 1


@pytest.fixture
def leary(context, carter):
    leary = context.doctor_service.add_doctor("Helen", "Leary")  # id 2
    return context.doctor_service.add_specialty(leary.id, Specialty.RADIOLOGY)


def test_first_available_slot_starts_now(context, carter):
    assert context.visit_service.first_available_slot(carter.id) == MONDAY_10_00


def test_first_available_slot_of_unknown_doctor(context):
    with pytest.raises(NotFoundError):
        context.visit_service.first_available_slot(42)


def test_booking_takes_the_slot_of_that_doctor_only(context, pet, carter, leary):
    visit = context.visit_service.book_visit(pet.id, "checkup", doctor_id=carter.id)

    assert (visit.id, visit.doctor_id, visit.start) == (1, carter.id, MONDAY_10_00)
    assert context.visit_service.first_available_slot(carter.id) == MONDAY_10_30
    assert context.visit_service.first_available_slot(leary.id) == MONDAY_10_00


def test_first_available_slots_covers_every_doctor(context, pet, carter, leary):
    context.visit_service.book_visit(pet.id, "checkup", doctor_id=carter.id)

    assert context.visit_service.first_available_slots() == {
        carter.id: MONDAY_10_30,
        leary.id: MONDAY_10_00,
    }


def test_booking_without_doctor_picks_earliest_slot_then_lowest_id(context, pet, carter, leary):
    visits = [context.visit_service.book_visit(pet.id, f"visit {n}") for n in range(3)]

    assert [(v.doctor_id, v.start) for v in visits] == [
        (carter.id, MONDAY_10_00),
        (leary.id, MONDAY_10_00),
        (carter.id, MONDAY_10_30),
    ]


def test_booking_by_specialty_only_considers_matching_doctors(context, pet, carter, leary):
    visits = [
        context.visit_service.book_visit(pet.id, "x-ray", specialty=Specialty.RADIOLOGY)
        for _ in range(2)
    ]

    assert [(v.doctor_id, v.start) for v in visits] == [
        (leary.id, MONDAY_10_00),
        (leary.id, MONDAY_10_30),
    ]


def test_doctor_without_requested_specialty_is_rejected(context, pet, carter):
    with pytest.raises(ValidationError):
        context.visit_service.book_visit(
            pet.id, "x-ray", doctor_id=carter.id, specialty=Specialty.RADIOLOGY
        )


def test_no_doctor_with_specialty_is_rejected(context, pet, carter, leary):
    with pytest.raises(ValidationError):
        context.visit_service.book_visit(pet.id, "surgery", specialty=Specialty.SURGERY)


def test_booking_with_no_doctors_is_rejected(context, pet):
    with pytest.raises(ValidationError):
        context.visit_service.book_visit(pet.id, "checkup")


def test_booking_for_unknown_pet_or_doctor(context, pet, carter):
    with pytest.raises(NotFoundError):
        context.visit_service.book_visit(42, "checkup")
    with pytest.raises(NotFoundError):
        context.visit_service.book_visit(pet.id, "checkup", doctor_id=42)


def test_blank_description_is_rejected(context, pet, carter):
    with pytest.raises(ValidationError):
        context.visit_service.book_visit(pet.id, "  ")


def test_visits_for_pet_are_stored_and_sorted_by_start(context, pet, carter, leary):
    later = context.visit_service.book_visit(pet.id, "second", doctor_id=carter.id)
    context.visit_service.book_visit(pet.id, "blocks leary's first slot", doctor_id=leary.id)
    context.visit_service.book_visit(pet.id, "blocks carter's second slot", doctor_id=carter.id)

    visits = context.visit_service.visits_for_pet(pet.id)

    assert visits[0] == later
    assert [v.start for v in visits] == sorted(v.start for v in visits)
    assert len(visits) == 3


def test_changes_are_not_stored_until_saved(context, pet, carter):
    visit = context.visit_service.book_visit(pet.id, "checkup")
    visit.description = "Changed"

    assert context.visit_service.visits_for_pet(pet.id)[0].description == "checkup"


def test_visits_for_unknown_pet(context):
    with pytest.raises(NotFoundError):
        context.visit_service.visits_for_pet(42)


def test_cli_slots(cli, carter, leary):
    assert cli("visit slots") == (
        "#1 James Carter: 2026-10-05 10:00\n#2 Helen Leary: 2026-10-05 10:00"
    )


def test_cli_slots_without_doctors(cli):
    assert cli("visit slots") == "no doctors"


def test_cli_book_and_list(cli, pet, carter, leary):
    assert cli('visit book --pet-id 1 --description "rabies shot"') == (
        "booked #1 2026-10-05 10:00 pet #1 with doctor #1: rabies shot"
    )
    assert cli('visit book --pet-id 1 --description "x-ray" --specialty radiology') == (
        "booked #2 2026-10-05 10:00 pet #1 with doctor #2: x-ray"
    )
    assert cli("visit list --pet-id 1").splitlines() == [
        "#1 2026-10-05 10:00 pet #1 with doctor #1: rabies shot",
        "#2 2026-10-05 10:00 pet #1 with doctor #2: x-ray",
    ]


def test_cli_list_without_visits(cli, pet):
    assert cli("visit list --pet-id 1") == "no visits"


def test_cli_book_for_unknown_pet(cli, carter):
    assert cli('visit book --pet-id 42 --description "checkup"').startswith("error:")
