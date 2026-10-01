"""Phase 3, task 20: the doctor endpoints and the error handlers. Skipped until FastAPI is
installed. `api` is FastAPI's TestClient (see conftest.py): it sends requests to the app
in-process, without starting a server."""

DOCTOR = {"first_name": "James", "last_name": "Carter"}


def test_create_doctor(api):
    response = api.post("/doctors", json=DOCTOR)

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "first_name": "James",
        "last_name": "Carter",
        "specialties": [],
    }


def test_get_doctor(api):
    api.post("/doctors", json=DOCTOR)

    response = api.get("/doctors/1")

    assert response.status_code == 200
    assert response.json()["last_name"] == "Carter"


def test_unknown_doctor_is_404_with_the_error_message(api):
    response = api.get("/doctors/42")

    assert response.status_code == 404
    assert response.json() == {"detail": "doctor 42 not found"}


def test_blank_name_is_400(api):
    response = api.post("/doctors", json={"first_name": "  ", "last_name": "Carter"})

    assert response.status_code == 400
    assert "first name" in response.json()["detail"]


def test_missing_field_is_422(api):
    # FastAPI rejects a body that doesn't match the request model before your code runs.
    assert api.post("/doctors", json={"first_name": "James"}).status_code == 422


def test_list_doctors_is_sorted(api):
    assert api.get("/doctors").json() == []

    api.post("/doctors", json={"first_name": "Helen", "last_name": "Leary"})
    api.post("/doctors", json=DOCTOR)

    assert [d["id"] for d in api.get("/doctors").json()] == [2, 1]


def test_add_and_remove_specialties(api):
    api.post("/doctors", json=DOCTOR)

    api.put("/doctors/1/specialties/surgery")
    response = api.put("/doctors/1/specialties/dentistry")

    assert response.status_code == 200
    assert response.json()["specialties"] == ["dentistry", "surgery"]

    response = api.delete("/doctors/1/specialties/surgery")

    assert response.status_code == 200
    assert response.json()["specialties"] == ["dentistry"]


def test_unknown_specialty_is_422(api):
    api.post("/doctors", json=DOCTOR)

    assert api.put("/doctors/1/specialties/cardiology").status_code == 422


def test_specialty_of_unknown_doctor_is_404(api):
    assert api.put("/doctors/42/specialties/surgery").status_code == 404


def test_filter_doctors_by_specialty(api):
    api.post("/doctors", json=DOCTOR)
    api.post("/doctors", json={"first_name": "Helen", "last_name": "Leary"})
    api.put("/doctors/2/specialties/radiology")

    response = api.get("/doctors", params={"specialty": "radiology"})

    assert [d["last_name"] for d in response.json()] == ["Leary"]
    assert api.get("/doctors", params={"specialty": "surgery"}).json() == []
