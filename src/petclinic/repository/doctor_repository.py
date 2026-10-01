import copy
from typing import Protocol

from petclinic.model import Doctor


class DoctorRepository(Protocol):
    """Storage contract for doctors (the Java `interface`). Services depend on this, not on
    a concrete class, so phase 2 can swap in a Postgres implementation."""

    def save(self, doctor: Doctor) -> Doctor: ...

    def find_by_id(self, doctor_id: int) -> Doctor | None: ...

    def find_all(self) -> list[Doctor]: ...


class InMemoryDoctorRepository:
    """Doctors in a dict keyed by id, the in-memory version of a primary key index.

    Stores and returns copies, like a real database: changing a returned Doctor does nothing
    until you save() it again.
    """

    def __init__(self) -> None:
        self._doctors: dict[int, Doctor] = {}
        self._next_id = 1

    def save(self, doctor: Doctor) -> Doctor:
        stored = copy.deepcopy(doctor)
        if stored.id is None:
            stored.id = self._next_id
            self._next_id += 1
        self._doctors[stored.id] = stored
        return copy.deepcopy(stored)

    def find_by_id(self, doctor_id: int) -> Doctor | None:
        doctor = self._doctors.get(doctor_id)
        return copy.deepcopy(doctor) if doctor is not None else None

    def find_all(self) -> list[Doctor]:
        return [copy.deepcopy(doctor) for doctor in self._doctors.values()]
