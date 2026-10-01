import argparse

from petclinic.model import Doctor
from petclinic.service.doctor_service import DoctorService


class DoctorResource:
    def __init__(self, doctor_service: DoctorService) -> None:
        self._service = doctor_service

    def register(self, subparsers: argparse._SubParsersAction) -> None:
        parser = subparsers.add_parser("doctor", help="manage doctors")
        commands = parser.add_subparsers(dest="command", required=True, metavar="<command>")

        add = commands.add_parser("add", help="add a doctor")
        add.add_argument("--first-name", required=True)
        add.add_argument("--last-name", required=True)
        add.set_defaults(handler=self.handle_add)

        list_ = commands.add_parser("list", help="list doctors")
        list_.set_defaults(handler=self.handle_list)

        # TODO task 01: register
        #   doctor add-specialty    --doctor-id ID --specialty {radiology,surgery,dentistry}
        #   doctor remove-specialty --doctor-id ID --specialty {radiology,surgery,dentistry}
        #   doctor list [--specialty {radiology,surgery,dentistry}]
        # Hint: argparse accepts `type=Specialty` and `choices=list(Specialty)`.

    def handle_add(self, args: argparse.Namespace) -> str:
        doctor = self._service.add_doctor(args.first_name, args.last_name)
        return f"added {format_doctor(doctor)}"

    def handle_list(self, args: argparse.Namespace) -> str:
        doctors = self._service.list_doctors()
        if not doctors:
            return "no doctors"
        return "\n".join(format_doctor(doctor) for doctor in doctors)


def format_doctor(doctor: Doctor) -> str:
    specialties = ", ".join(sorted(doctor.specialties)) or "none"
    return f"#{doctor.id} {doctor.first_name} {doctor.last_name} [{specialties}]"
