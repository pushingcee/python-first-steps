from datetime import datetime

from petclinic.clock import Clock
from petclinic.model import Specialty, Visit
from petclinic.repository.visit_repository import VisitRepository
from petclinic.service.doctor_service import DoctorService
from petclinic.service.pet_service import PetService


class VisitService:
    def __init__(
        self,
        visit_repository: VisitRepository,
        pet_service: PetService,
        doctor_service: DoctorService,
        clock: Clock,
    ) -> None:
        self._visits = visit_repository
        self._pet_service = pet_service
        self._doctor_service = doctor_service
        self._clock = clock

    # ---- TODO task 05 ------------------------------------------------------------------

    def first_available_slot(self, doctor_id: int) -> datetime:
        """The doctor's earliest slot, from now on, that has no visit booked.

        - Unknown doctor -> NotFoundError.
        - Use scheduling.iter_slots(). A set of booked start times makes "is it taken?" O(1).
        """
        raise NotImplementedError("task 05")

    def first_available_slots(self) -> dict[int, datetime]:
        """{doctor id: first available slot} for every doctor."""
        raise NotImplementedError("task 05")

    def book_visit(
        self,
        pet_id: int,
        description: str,
        *,
        doctor_id: int | None = None,
        specialty: Specialty | None = None,
    ) -> Visit:
        """Book the earliest free slot and save the visit.

        - Unknown pet or doctor -> NotFoundError. Blank description -> ValidationError.
        - Candidates: only doctor_id if given, else doctors with `specialty` if given,
          else every doctor.
        - doctor_id given but that doctor lacks `specialty` -> ValidationError.
        - No candidates -> ValidationError.
        - Pick the candidate with the earliest first available slot; on a tie, the lowest id.
        """
        raise NotImplementedError("task 05")

    def visits_for_pet(self, pet_id: int) -> list[Visit]:
        """The pet's visits sorted by start, then id. Unknown pet -> NotFoundError."""
        raise NotImplementedError("task 05")
