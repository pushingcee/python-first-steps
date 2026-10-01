from dataclasses import dataclass, field

from petclinic.model.specialty import Specialty


@dataclass(kw_only=True)
class Doctor:
    """A vet working at the clinic. Spring PetClinic calls this `Vet`."""

    id: int | None = None  # None until the repository saves it
    first_name: str
    last_name: str
    specialties: set[Specialty] = field(default_factory=set)
