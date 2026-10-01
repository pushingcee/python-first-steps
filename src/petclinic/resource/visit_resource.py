import argparse

from petclinic.service.doctor_service import DoctorService
from petclinic.service.visit_service import VisitService


class VisitResource:
    def __init__(self, visit_service: VisitService, doctor_service: DoctorService) -> None:
        self._service = visit_service
        self._doctor_service = doctor_service

    def register(self, subparsers: argparse._SubParsersAction) -> None:
        subparsers.add_parser("visit", help="book and list visits (task 05)")
        # TODO task 05:
        #   visit slots
        #   visit book --pet-id ID --description D [--doctor-id ID] [--specialty S]
        #   visit list --pet-id ID
