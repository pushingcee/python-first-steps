"""Phase 3, task 21: owner and pet endpoints. Today is 2026-10-05 (see conftest.NOW)."""

GEORGE = {
    "first_name": "George",
    "last_name": "Franklin",
    "address": "110 W. Liberty St.",
    "city": "Madison",
    "telephone": "6085551023",
}
LEO = {"name": "Leo", "birth_date": "2020-09-07", "type": "cat"}


def test_create_owner(api):
    response = api.post("/owners", json=GEORGE)

    assert response.status_code == 201
    assert response.json() == {"id": 1} | GEORGE


def test_invalid_telephone_is_400(api):
    assert api.post("/owners", json=GEORGE | {"telephone": "608-555"}).status_code == 400


def test_get_owner(api):
    api.post("/owners", json=GEORGE)

    assert api.get("/owners/1").json()["city"] == "Madison"
    assert api.get("/owners/42").status_code == 404


def test_find_owners_by_last_name(api):
    api.post("/owners", json=GEORGE)
    api.post("/owners", json=GEORGE | {"first_name": "Betty", "last_name": "Davis"})

    assert [o["id"] for o in api.get("/owners").json()] == [2, 1]
    assert [o["id"] for o in api.get("/owners", params={"last_name": "fr"}).json()] == [1]
    assert api.get("/owners", params={"last_name": "zz"}).json() == []


def test_patch_owner_changes_only_given_fields(api):
    api.post("/owners", json=GEORGE)

    response = api.patch("/owners/1", json={"city": "Sun Prairie"})

    assert response.status_code == 200
    assert response.json() == {"id": 1} | GEORGE | {"city": "Sun Prairie"}


def test_invalid_patch_is_400_and_not_stored(api):
    api.post("/owners", json=GEORGE)

    assert api.patch("/owners/1", json={"telephone": "abc"}).status_code == 400
    assert api.get("/owners/1").json()["telephone"] == GEORGE["telephone"]


def test_add_pet(api):
    api.post("/owners", json=GEORGE)

    response = api.post("/owners/1/pets", json=LEO)

    assert response.status_code == 201
    assert response.json() == {"id": 1, "owner_id": 1} | LEO


def test_add_pet_to_unknown_owner_is_404(api):
    assert api.post("/owners/42/pets", json=LEO).status_code == 404


def test_pet_born_in_the_future_is_400(api):
    api.post("/owners", json=GEORGE)

    assert api.post("/owners/1/pets", json=LEO | {"birth_date": "2026-10-06"}).status_code == 400


def test_bad_date_or_type_is_422(api):
    api.post("/owners", json=GEORGE)

    assert api.post("/owners/1/pets", json=LEO | {"birth_date": "2020-13-01"}).status_code == 422
    assert api.post("/owners/1/pets", json=LEO | {"type": "dragon"}).status_code == 422


def test_list_pets_of_owner(api):
    api.post("/owners", json=GEORGE)
    api.post("/owners/1/pets", json={"name": "Rosy", "birth_date": "2021-04-17", "type": "dog"})
    api.post("/owners/1/pets", json=LEO)

    response = api.get("/owners/1/pets")

    assert [p["name"] for p in response.json()] == ["Leo", "Rosy"]
    assert api.get("/owners/42/pets").status_code == 404


def test_pet_types(api):
    assert set(api.get("/pet-types").json()) == {"cat", "dog", "lizard", "snake", "bird", "hamster"}
