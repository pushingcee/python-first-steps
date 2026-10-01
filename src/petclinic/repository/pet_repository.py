from typing import Protocol

from petclinic.model import Pet


class PetRepository(Protocol):
    def save(self, pet: Pet) -> Pet: ...

    def find_by_id(self, pet_id: int) -> Pet | None: ...

    def find_by_owner_id(self, owner_id: int) -> list[Pet]:
        """All pets of one owner, in any order. SQL: WHERE owner_id = ?"""
        ...


class InMemoryPetRepository:
    """TODO task 03."""

    def __init__(self) -> None:
        pass  # TODO task 03

    def save(self, pet: Pet) -> Pet:
        raise NotImplementedError("task 03")

    def find_by_id(self, pet_id: int) -> Pet | None:
        raise NotImplementedError("task 03")

    def find_by_owner_id(self, owner_id: int) -> list[Pet]:
        raise NotImplementedError("task 03")
