from petclinic.exceptions import NotFoundError
from petclinic.model import Doctor, Specialty
from petclinic.repository.doctor_repository import DoctorRepository
from petclinic.service.validation import require_text


class DoctorService:
    def __init__(self, doctor_repository: DoctorRepository) -> None:
        self._doctors = doctor_repository

    def add_doctor(self, first_name: str, last_name: str) -> Doctor:
        doctor = Doctor(
            first_name=require_text(first_name, "first name"),
            last_name=require_text(last_name, "last name"),
        )
        return self._doctors.save(doctor)

    def get_doctor(self, doctor_id: int) -> Doctor:
        doctor = self._doctors.find_by_id(doctor_id)
        if doctor is None:
            raise NotFoundError(f"doctor {doctor_id} not found")
        return doctor

    def list_doctors(self) -> list[Doctor]:
        """All doctors, ordered by last name, then first name (case-insensitive)."""
        return sorted(self._doctors.find_all(), key=_by_name)

    # ---- TODO task 01 ------------------------------------------------------------------

    def add_specialty(self, doctor_id: int, specialty: Specialty) -> Doctor:
        """Add a specialty to a doctor and persist it.

        - Unknown doctor -> NotFoundError (hint: there's already a method for that).
        - Adding a specialty the doctor already has changes nothing (sets are your friend).
        - Returns the updated doctor.
        """
        raise NotImplementedError("task 01")

    def remove_specialty(self, doctor_id: int, specialty: Specialty) -> Doctor:
        """Remove a specialty from a doctor and persist it.

        - Unknown doctor -> NotFoundError.
        - Removing a specialty the doctor doesn't have is not an error.
        """
        raise NotImplementedError("task 01")

    def find_by_specialty(self, specialty: Specialty) -> list[Doctor]:
        """Doctors with the given specialty, sorted like list_doctors()."""
        raise NotImplementedError("task 01")


def _by_name(doctor: Doctor) -> tuple[str, str]:
    return doctor.last_name.casefold(), doctor.first_name.casefold()
