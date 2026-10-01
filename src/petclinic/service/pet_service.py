from datetime import date

from petclinic.clock import Clock
from petclinic.model import Pet, PetType
from petclinic.repository.pet_repository import PetRepository
from petclinic.service.owner_service import OwnerService


class PetService:
    def __init__(
        self, pet_repository: PetRepository, owner_service: OwnerService, clock: Clock
    ) -> None:
        self._pets = pet_repository
        self._owner_service = owner_service
        self._clock = clock

    # ---- TODO task 03 ------------------------------------------------------------------

    def add_pet(self, owner_id: int, name: str, birth_date: date, pet_type: PetType) -> Pet:
        """Validate and save a new pet.

        - Unknown owner -> NotFoundError.
        - Name is stripped and must not be blank.
        - Birth date must not be after today (today comes from self._clock, not datetime.now()).
        - An owner can't have two pets with the same name, ignoring case. Different owners can.
        """
        raise NotImplementedError("task 03")

    def get_pet(self, pet_id: int) -> Pet:
        """The pet with this id, or NotFoundError."""
        raise NotImplementedError("task 03")

    def pets_of_owner(self, owner_id: int) -> list[Pet]:
        """The owner's pets sorted by name (case-insensitive). Unknown owner -> NotFoundError."""
        raise NotImplementedError("task 03")
