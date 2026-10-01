"""Task 00, the worked example. All green from day one: read these first."""

import pytest

from petclinic.exceptions import NotFoundError, ValidationError


def test_add_doctor_assigns_id_and_strips_names(context):
    doctor = context.doctor_service.add_doctor("  James ", " Carter ")

    assert doctor.id == 1
    assert (doctor.first_name, doctor.last_name) == ("James", "Carter")
    assert doctor.specialties == set()


def test_ids_increment(context):
    first = context.doctor_service.add_doctor("James", "Carter")
    second = context.doctor_service.add_doctor("Helen", "Leary")

    assert (first.id, second.id) == (1, 2)


@pytest.mark.parametrize(("first_name", "last_name"), [("", "Carter"), ("James", "   ")])
def test_blank_names_are_rejected(context, first_name, last_name):
    with pytest.raises(ValidationError):
        context.doctor_service.add_doctor(first_name, last_name)


def test_get_unknown_doctor_raises_not_found(context):
    with pytest.raises(NotFoundError):
        context.doctor_service.get_doctor(42)


def test_list_doctors_is_sorted_by_last_name_then_first_name(context):
    context.doctor_service.add_doctor("Sharon", "Jenkins")
    context.doctor_service.add_doctor("James", "carter")
    context.doctor_service.add_doctor("Anna", "Jenkins")

    names = [(d.first_name, d.last_name) for d in context.doctor_service.list_doctors()]

    assert names == [("James", "carter"), ("Anna", "Jenkins"), ("Sharon", "Jenkins")]


def test_changes_are_not_stored_until_saved(context):
    doctor = context.doctor_service.add_doctor("James", "Carter")
    doctor.first_name = "Changed"

    assert context.doctor_service.get_doctor(doctor.id).first_name == "James"


def test_cli_add_doctor(cli):
    assert cli("doctor add --first-name James --last-name Carter") == "added #1 James Carter [none]"


def test_cli_quoted_arguments_keep_spaces(cli):
    output = cli('doctor add --first-name Rafael --last-name "de la Ortega"')

    assert output == "added #1 Rafael de la Ortega [none]"


def test_cli_missing_argument_is_a_usage_error(cli):
    assert "required" in cli("doctor add --first-name James")


def test_cli_validation_error_is_printed(cli):
    assert cli('doctor add --first-name "" --last-name Carter').startswith("error:")


def test_cli_list_doctors(cli):
    assert cli("doctor list") == "no doctors"

    cli("doctor add --first-name Helen --last-name Leary")
    cli("doctor add --first-name James --last-name Carter")

    assert cli("doctor list") == "#2 James Carter [none]\n#1 Helen Leary [none]"


def test_cli_unknown_resource(cli):
    assert "invalid choice" in cli("dragon add")
