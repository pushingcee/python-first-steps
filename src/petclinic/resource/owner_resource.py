import argparse

from petclinic.service.owner_service import OwnerService


class OwnerResource:
    def __init__(self, owner_service: OwnerService) -> None:
        self._service = owner_service

    def register(self, subparsers: argparse._SubParsersAction) -> None:
        subparsers.add_parser("owner", help="manage owners (task 02)")
        # TODO task 02: add subcommands and handlers. Use DoctorResource as your template.
        #   owner add    --first-name F --last-name L --address A --city C --telephone T
        #   owner find   [--last-name PREFIX]
        #   owner show   --id ID
        #   owner update --id ID [--address A] [--city C] [--telephone T]
        # Output formats are in TASKS.md; tests/test_02_owner.py has the exact strings.
