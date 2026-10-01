"""Task 01: doctor specialties. Specialties live in a set on Doctor."""

import pytest

from petclinic.exceptions import NotFoundError
from petclinic.model import Specialty


@pytest.fixture
def carter(context):
    return context.doctor_service.add_doctor("James", "Carter")


def test_add_specialty_is_persisted(context, carter):
    context.doctor_service.add_specialty(carter.id, Specialty.SURGERY)

    assert context.doctor_service.get_doctor(carter.id).specialties == {Specialty.SURGERY}


def test_add_specialty_returns_updated_doctor(context, carter):
    doctor = context.doctor_service.add_specialty(carter.id, Specialty.RADIOLOGY)

    assert doctor.specialties == {Specialty.RADIOLOGY}


def test_adding_same_specialty_twice_keeps_one(context, carter):
    context.doctor_service.add_specialty(carter.id, Specialty.SURGERY)
    context.doctor_service.add_specialty(carter.id, Specialty.SURGERY)

    assert context.doctor_service.get_doctor(carter.id).specialties == {Specialty.SURGERY}


def test_add_specialty_to_unknown_doctor(context):
    with pytest.raises(NotFoundError):
        context.doctor_service.add_specialty(42, Specialty.SURGERY)


def test_remove_specialty(context, carter):
    context.doctor_service.add_specialty(carter.id, Specialty.SURGERY)
    context.doctor_service.add_specialty(carter.id, Specialty.DENTISTRY)

    context.doctor_service.remove_specialty(carter.id, Specialty.SURGERY)

    assert context.doctor_service.get_doctor(carter.id).specialties == {Specialty.DENTISTRY}


def test_removing_absent_specialty_is_a_no_op(context, carter):
    doctor = context.doctor_service.remove_specialty(carter.id, Specialty.SURGERY)

    assert doctor.specialties == set()


def test_find_by_specialty_filters_and_sorts(context, carter):
    leary = context.doctor_service.add_doctor("Helen", "Leary")
    ortega = context.doctor_service.add_doctor("Rafael", "Ortega")
    context.doctor_service.add_specialty(ortega.id, Specialty.SURGERY)
    context.doctor_service.add_specialty(leary.id, Specialty.RADIOLOGY)
    context.doctor_service.add_specialty(carter.id, Specialty.SURGERY)

    surgeons = context.doctor_service.find_by_specialty(Specialty.SURGERY)

    assert [d.last_name for d in surgeons] == ["Carter", "Ortega"]


def test_cli_add_specialty(cli):
    cli("doctor add --first-name James --last-name Carter")

    output = cli("doctor add-specialty --doctor-id 1 --specialty surgery")

    assert output == "updated #1 James Carter [surgery]"


def test_cli_specialties_are_listed_alphabetically(cli):
    cli("doctor add --first-name James --last-name Carter")
    cli("doctor add-specialty --doctor-id 1 --specialty surgery")
    cli("doctor add-specialty --doctor-id 1 --specialty dentistry")

    assert cli("doctor list") == "#1 James Carter [dentistry, surgery]"


def test_cli_remove_specialty(cli):
    cli("doctor add --first-name James --last-name Carter")
    cli("doctor add-specialty --doctor-id 1 --specialty surgery")

    assert cli("doctor remove-specialty --doctor-id 1 --specialty surgery") == (
        "updated #1 James Carter [none]"
    )


def test_cli_list_filtered_by_specialty(cli):
    cli("doctor add --first-name James --last-name Carter")
    cli("doctor add --first-name Helen --last-name Leary")
    cli("doctor add-specialty --doctor-id 2 --specialty radiology")

    assert cli("doctor list --specialty radiology") == "#2 Helen Leary [radiology]"
    assert cli("doctor list --specialty surgery") == "no doctors"


def test_cli_unknown_specialty_is_a_usage_error(cli):
    cli("doctor add --first-name James --last-name Carter")

    assert "invalid" in cli("doctor add-specialty --doctor-id 1 --specialty cardiology")


def test_cli_add_specialty_to_unknown_doctor(cli):
    assert cli("doctor add-specialty --doctor-id 42 --specialty surgery").startswith("error:")
