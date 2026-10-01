"""Task 03: pets (the clinic's patients). Today is 2026-10-05 (see conftest.NOW)."""

from datetime import date

import pytest

from petclinic.exceptions import NotFoundError, ValidationError
from petclinic.model import PetType

ADD_OWNER = (
    'owner add --first-name George --last-name Franklin --address "110 W. Liberty St." '
    "--city Madison --telephone 6085551023"
)


@pytest.fixture
def owner(context):
    return context.owner_service.add_owner(
        "George", "Franklin", "110 W. Liberty St.", "Madison", "6085551023"
    )


@pytest.fixture
def other_owner(owner, context):
    return context.owner_service.add_owner(
        "Betty", "Davis", "638 Cardinal Ave.", "Sun Prairie", "6085551749"
    )


def add_pet(context, owner_id, name="Leo", birth_date=date(2020, 9, 7), pet_type=PetType.CAT):
    return context.pet_service.add_pet(owner_id, name, birth_date, pet_type)


def test_add_pet(context, owner):
    pet = add_pet(context, owner.id, name=" Leo ")

    assert pet.id == 1
    assert (pet.name, pet.type, pet.owner_id) == ("Leo", PetType.CAT, owner.id)
    assert pet.birth_date == date(2020, 9, 7)


def test_add_pet_to_unknown_owner(context):
    with pytest.raises(NotFoundError):
        add_pet(context, 42)


def test_blank_name_is_rejected(context, owner):
    with pytest.raises(ValidationError):
        add_pet(context, owner.id, name="  ")


def test_birth_date_in_the_future_is_rejected(context, owner):
    with pytest.raises(ValidationError):
        add_pet(context, owner.id, birth_date=date(2026, 10, 6))


def test_born_today_is_allowed(context, owner):
    assert add_pet(context, owner.id, birth_date=date(2026, 10, 5)).id == 1


def test_pet_names_are_unique_per_owner_case_insensitive(context, owner, other_owner):
    add_pet(context, owner.id, name="Leo")

    with pytest.raises(ValidationError):
        add_pet(context, owner.id, name="LEO")
    assert add_pet(context, other_owner.id, name="Leo").owner_id == other_owner.id


def test_changes_are_not_stored_until_saved(context, owner):
    pet = add_pet(context, owner.id)
    pet.name = "Changed"

    assert context.pet_service.get_pet(pet.id).name == "Leo"
    assert [p.name for p in context.pet_service.pets_of_owner(owner.id)] == ["Leo"]


def test_get_unknown_pet(context):
    with pytest.raises(NotFoundError):
        context.pet_service.get_pet(42)


def test_pets_of_owner_only_returns_their_pets_sorted_by_name(context, owner, other_owner):
    add_pet(context, owner.id, name="Rosy", pet_type=PetType.DOG)
    add_pet(context, other_owner.id, name="Basil", pet_type=PetType.HAMSTER)
    add_pet(context, owner.id, name="jewel", pet_type=PetType.DOG)

    pets = context.pet_service.pets_of_owner(owner.id)

    assert [p.name for p in pets] == ["jewel", "Rosy"]


def test_pets_of_unknown_owner(context):
    with pytest.raises(NotFoundError):
        context.pet_service.pets_of_owner(42)


def test_cli_add_pet(cli):
    cli(ADD_OWNER)

    output = cli("pet add --owner-id 1 --name Leo --birth-date 2020-09-07 --type cat")

    assert output == "added #1 Leo (cat, born 2020-09-07), owner #1"


@pytest.mark.parametrize(
    "arguments",
    ["--birth-date 2020-13-01 --type cat", "--birth-date 2020-09-07 --type dragon"],
)
def test_cli_bad_date_or_type_is_a_usage_error(cli, arguments):
    cli(ADD_OWNER)

    assert "invalid" in cli(f"pet add --owner-id 1 --name Leo {arguments}")


def test_cli_list_pets(cli):
    cli(ADD_OWNER)
    assert cli("pet list --owner-id 1") == "no pets"

    cli("pet add --owner-id 1 --name Rosy --birth-date 2021-04-17 --type dog")
    cli("pet add --owner-id 1 --name Leo --birth-date 2020-09-07 --type cat")

    assert cli("pet list --owner-id 1") == (
        "#2 Leo (cat, born 2020-09-07), owner #1\n#1 Rosy (dog, born 2021-04-17), owner #1"
    )


def test_cli_list_pets_of_unknown_owner(cli):
    assert cli("pet list --owner-id 42").startswith("error:")


def test_cli_pet_types(cli):
    assert set(cli("pet types").splitlines()) == {pet_type.value for pet_type in PetType}
