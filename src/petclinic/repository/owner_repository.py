from typing import Protocol

from petclinic.model import Owner


class OwnerRepository(Protocol):
    def save(self, owner: Owner) -> Owner: ...

    def find_by_id(self, owner_id: int) -> Owner | None: ...

    def find_by_last_name_prefix(self, prefix: str) -> list[Owner]:
        """Owners whose last name starts with `prefix`, case-insensitive, in any order.
        An empty prefix matches everyone. SQL: WHERE last_name ILIKE 'prefix%'."""
        ...


class InMemoryOwnerRepository:
    """TODO task 02. Model it on InMemoryDoctorRepository: dict keyed by id, ids from 1,
    store and return copies."""

    def __init__(self) -> None:
        pass  # TODO task 02: your storage goes here

    def save(self, owner: Owner) -> Owner:
        raise NotImplementedError("task 02")

    def find_by_id(self, owner_id: int) -> Owner | None:
        raise NotImplementedError("task 02")

    def find_by_last_name_prefix(self, prefix: str) -> list[Owner]:
        raise NotImplementedError("task 02")
