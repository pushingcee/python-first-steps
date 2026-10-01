from dataclasses import dataclass
from datetime import date
from enum import StrEnum


class PetType(StrEnum):
    CAT = "cat"
    DOG = "dog"
    LIZARD = "lizard"
    SNAKE = "snake"
    BIRD = "bird"
    HAMSTER = "hamster"


@dataclass(kw_only=True)
class Pet:
    """A patient of the clinic.

    Pets reference their owner by id (a foreign key) instead of the owner holding a list of
    pets. This keeps the in-memory model close to the Postgres schema of phase 2.
    """

    id: int | None = None
    name: str
    birth_date: date
    type: PetType
    owner_id: int
