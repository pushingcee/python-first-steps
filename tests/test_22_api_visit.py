"""Phase 3, task 22: visit endpoints. Now is Monday 2026-10-05 10:00 (see conftest.NOW)."""

import pytest


@pytest.fixture
def clinic(api):
    """Owner #1 with pet #1, doctor #1 Carter and doctor #2 Leary (radiology)."""
    api.post(
        "/owners",
        json={
            "first_name": "George",
            "last_name": "Franklin",
            "address": "110 W. Liberty St.",
            "city": "Madison",
            "telephone": "6085551023",
        },
    )
    api.post("/owners/1/pets", json={"name": "Leo", "birth_date": "2020-09-07", "type": "cat"})
    api.post("/doctors", json={"first_name": "James", "last_name": "Carter"})
    api.post("/doctors", json={"first_name": "Helen", "last_name": "Leary"})
    api.put("/doctors/2/specialties/radiology")
    return api


def test_slots(clinic):
    response = clinic.get("/visits/slots")

    assert response.status_code == 200
    assert response.json() == [
        {"doctor_id": 1, "start": "2026-10-05T10:00:00"},
        {"doctor_id": 2, "start": "2026-10-05T10:00:00"},
    ]


def test_book_visit(clinic):
    response = clinic.post("/pets/1/visits", json={"description": "rabies shot"})

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "pet_id": 1,
        "doctor_id": 1,
        "start": "2026-10-05T10:00:00",
        "description": "rabies shot",
    }
    assert clinic.get("/visits/slots").json()[0]["start"] == "2026-10-05T10:30:00"


def test_book_with_specialty_or_doctor(clinic):
    by_specialty = clinic.post(
        "/pets/1/visits", json={"description": "x", "specialty": "radiology"}
    )
    by_doctor = clinic.post("/pets/1/visits", json={"description": "y", "doctor_id": 1})

    assert by_specialty.json()["doctor_id"] == 2
    assert by_doctor.json()["doctor_id"] == 1


@pytest.mark.parametrize(
    ("body", "status"),
    [
        ({"description": "  "}, 400),
        ({"description": "x", "specialty": "surgery"}, 400),  # nobody has it
        ({"description": "x", "doctor_id": 1, "specialty": "radiology"}, 400),
        ({"description": "x", "doctor_id": 42}, 404),
        ({"description": "x", "specialty": "cardiology"}, 422),
        ({}, 422),
    ],
)
def test_booking_errors(clinic, body, status):
    assert clinic.post("/pets/1/visits", json=body).status_code == status


def test_book_for_unknown_pet_is_404(clinic):
    assert clinic.post("/pets/42/visits", json={"description": "x"}).status_code == 404


def test_list_visits_of_pet(clinic):
    assert clinic.get("/pets/1/visits").json() == []

    clinic.post("/pets/1/visits", json={"description": "first", "doctor_id": 1})
    clinic.post("/pets/1/visits", json={"description": "second", "doctor_id": 1})

    response = clinic.get("/pets/1/visits")

    assert [v["description"] for v in response.json()] == ["first", "second"]
    assert clinic.get("/pets/42/visits").status_code == 404
