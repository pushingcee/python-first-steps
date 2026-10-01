"""Composition root: builds every object and wires dependencies through constructors.
This is the Spring application context, written by hand."""

from dataclasses import dataclass

from petclinic.clock import Clock, SystemClock
from petclinic.repository.doctor_repository import InMemoryDoctorRepository
from petclinic.repository.owner_repository import InMemoryOwnerRepository
from petclinic.repository.pet_repository import InMemoryPetRepository
from petclinic.repository.visit_repository import InMemoryVisitRepository
from petclinic.resource.doctor_resource import DoctorResource
from petclinic.resource.owner_resource import OwnerResource
from petclinic.resource.pet_resource import PetResource
from petclinic.resource.resource import Resource
from petclinic.resource.visit_resource import VisitResource
from petclinic.service.doctor_service import DoctorService
from petclinic.service.owner_service import OwnerService
from petclinic.service.pet_service import PetService
from petclinic.service.visit_service import VisitService


@dataclass
class ApplicationContext:
    clock: Clock
    doctor_service: DoctorService
    owner_service: OwnerService
    pet_service: PetService
    visit_service: VisitService
    resources: list[Resource]


def create_context(clock: Clock | None = None) -> ApplicationContext:
    clock = clock or SystemClock()

    doctor_service = DoctorService(InMemoryDoctorRepository())
    owner_service = OwnerService(InMemoryOwnerRepository())
    pet_service = PetService(InMemoryPetRepository(), owner_service, clock)
    visit_service = VisitService(InMemoryVisitRepository(), pet_service, doctor_service, clock)

    resources: list[Resource] = [
        DoctorResource(doctor_service),
        OwnerResource(owner_service),
        PetResource(pet_service),
        VisitResource(visit_service, doctor_service),
    ]
    return ApplicationContext(
        clock=clock,
        doctor_service=doctor_service,
        owner_service=owner_service,
        pet_service=pet_service,
        visit_service=visit_service,
        resources=resources,
    )
