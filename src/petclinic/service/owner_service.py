from petclinic.model import Owner
from petclinic.repository.owner_repository import OwnerRepository

MAX_TELEPHONE_DIGITS = 10


class OwnerService:
    def __init__(self, owner_repository: OwnerRepository) -> None:
        self._owners = owner_repository

    # ---- TODO task 02 ------------------------------------------------------------------

    def add_owner(
        self, first_name: str, last_name: str, address: str, city: str, telephone: str
    ) -> Owner:
        """Validate and save a new owner.

        - Every field is stripped and must not be blank (ValidationError).
        - Telephone: 1 to MAX_TELEPHONE_DIGITS ASCII digits only, so "608-555" and "６０８"
          (full-width digits) are both rejected.
        """
        raise NotImplementedError("task 02")

    def get_owner(self, owner_id: int) -> Owner:
        """The owner with this id, or NotFoundError."""
        raise NotImplementedError("task 02")

    def find_by_last_name(self, prefix: str = "") -> list[Owner]:
        """Owners whose last name starts with `prefix` (case-insensitive), sorted by last
        name, then first name. An empty prefix returns everyone."""
        raise NotImplementedError("task 02")

    def update_contact(
        self,
        owner_id: int,
        *,
        address: str | None = None,
        city: str | None = None,
        telephone: str | None = None,
    ) -> Owner:
        """Change only the fields that are not None, with the same validation as add_owner.
        If anything is invalid, nothing is stored."""
        raise NotImplementedError("task 02")
