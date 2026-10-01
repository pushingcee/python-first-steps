from typing import Protocol

from petclinic.model import Visit


class VisitRepository(Protocol):
    def save(self, visit: Visit) -> Visit: ...

    def find_by_id(self, visit_id: int) -> Visit | None: ...

    def find_by_pet_id(self, pet_id: int) -> list[Visit]: ...

    def find_by_doctor_id(self, doctor_id: int) -> list[Visit]: ...


class InMemoryVisitRepository:
    """TODO task 05."""

    def __init__(self) -> None:
        pass  # TODO task 05

    def save(self, visit: Visit) -> Visit:
        raise NotImplementedError("task 05")

    def find_by_id(self, visit_id: int) -> Visit | None:
        raise NotImplementedError("task 05")

    def find_by_pet_id(self, pet_id: int) -> list[Visit]:
        raise NotImplementedError("task 05")

    def find_by_doctor_id(self, doctor_id: int) -> list[Visit]:
        raise NotImplementedError("task 05")
