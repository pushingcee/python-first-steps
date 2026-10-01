"""Task 02: owners."""

import pytest

from petclinic.exceptions import NotFoundError, ValidationError

GEORGE = {
    "first_name": "George",
    "last_name": "Franklin",
    "address": "110 W. Liberty St.",
    "city": "Madison",
    "telephone": "6085551023",
}
ADD_GEORGE = (
    'owner add --first-name George --last-name Franklin --address "110 W. Liberty St." '
    "--city Madison --telephone 6085551023"
)


def add_owner(context, **overrides):
    return context.owner_service.add_owner(**(GEORGE | overrides))


def test_add_owner_assigns_id_and_strips_fields(context):
    owner = add_owner(context, first_name=" George ", city=" Madison ")

    assert owner.id == 1
    assert (owner.first_name, owner.city) == ("George", "Madison")


@pytest.mark.parametrize("field", list(GEORGE))
def test_blank_fields_are_rejected(context, field):
    with pytest.raises(ValidationError):
        add_owner(context, **{field: "  "})


@pytest.mark.parametrize("telephone", ["608-555", "60855510231", "phone", "６０８"])
def test_telephone_must_be_up_to_ten_ascii_digits(context, telephone):
    with pytest.raises(ValidationError):
        add_owner(context, telephone=telephone)


def test_get_unknown_owner_raises_not_found(context):
    with pytest.raises(NotFoundError):
        context.owner_service.get_owner(42)


def test_find_by_last_name_prefix_is_case_insensitive_and_sorted(context):
    add_owner(context, first_name="Harold", last_name="Davis")
    add_owner(context, first_name="Jeff", last_name="Black")
    add_owner(context, first_name="Betty", last_name="Davis")

    for prefix in ("da", "DAV", "Davis"):
        found = context.owner_service.find_by_last_name(prefix)
        assert [o.first_name for o in found] == ["Betty", "Harold"]
    assert context.owner_service.find_by_last_name("x") == []


def test_find_with_empty_prefix_returns_everyone_sorted(context):
    add_owner(context, first_name="Harold", last_name="Davis")
    add_owner(context, first_name="Jeff", last_name="Black")

    found = context.owner_service.find_by_last_name()

    assert [o.last_name for o in found] == ["Black", "Davis"]


def test_update_contact_changes_only_given_fields(context):
    owner = add_owner(context)

    context.owner_service.update_contact(owner.id, city="Sun Prairie")

    updated = context.owner_service.get_owner(owner.id)
    assert updated.city == "Sun Prairie"
    assert (updated.address, updated.telephone) == (GEORGE["address"], GEORGE["telephone"])


def test_invalid_update_is_rejected_and_not_stored(context):
    owner = add_owner(context)

    with pytest.raises(ValidationError):
        context.owner_service.update_contact(owner.id, telephone="not a number")

    assert context.owner_service.get_owner(owner.id).telephone == GEORGE["telephone"]


def test_update_unknown_owner(context):
    with pytest.raises(NotFoundError):
        context.owner_service.update_contact(42, city="Madison")


def test_changes_are_not_stored_until_saved(context):
    owner = add_owner(context)
    owner.city = "Changed"

    assert context.owner_service.get_owner(owner.id).city == "Madison"


def test_cli_add_owner(cli):
    assert cli(ADD_GEORGE) == "added #1 George Franklin, 110 W. Liberty St., Madison, 6085551023"


def test_cli_add_owner_with_bad_telephone(cli):
    assert cli(ADD_GEORGE.replace("6085551023", "abc")).startswith("error:")


def test_cli_find_owners(cli):
    cli(ADD_GEORGE)

    assert cli("owner find --last-name fr").startswith("#1 George Franklin")
    assert cli("owner find").startswith("#1 George Franklin")
    assert cli("owner find --last-name zz") == "no owners"


def test_cli_show_owner(cli):
    cli(ADD_GEORGE)

    assert cli("owner show --id 1") == "#1 George Franklin, 110 W. Liberty St., Madison, 6085551023"
    assert cli("owner show --id 99").startswith("error:")


def test_cli_update_owner(cli):
    cli(ADD_GEORGE)

    output = cli('owner update --id 1 --city "Sun Prairie" --telephone 6085550000')

    assert output == "updated #1 George Franklin, 110 W. Liberty St., Sun Prairie, 6085550000"
