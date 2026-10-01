import argparse

from petclinic.service.pet_service import PetService


class PetResource:
    def __init__(self, pet_service: PetService) -> None:
        self._service = pet_service

    def register(self, subparsers: argparse._SubParsersAction) -> None:
        subparsers.add_parser("pet", help="manage pets (task 03)")
        # TODO task 03:
        #   pet add   --owner-id ID --name N --birth-date YYYY-MM-DD --type {cat,dog,...}
        #   pet list  --owner-id ID
        #   pet types
        # Hint: an argparse `type=` can be any function that takes a string and returns a value.
