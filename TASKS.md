# Tasks

Do them in order; later tasks build on earlier ones. A task is done when its test file passes:

```bash
uv run pytest tests/test_01_specialty.py -v
```

Each stub's docstring states the rules. The tests have the exact expectations, including output
strings. Read the test file before you start.

## 00 Doctors (worked example, already done)

Read every layer of it before starting task 01. Things to notice: the repository hands out
copies, the service validates and raises domain exceptions, the resource only parses arguments
and formats output.

## 01 Doctor specialties

`service/doctor_service.py`, `resource/doctor_resource.py`

- Service: `add_specialty`, `remove_specialty`, `find_by_specialty`.
- CLI: `doctor add-specialty`, `doctor remove-specialty`, `doctor list --specialty S`.
- Output: `updated #1 James Carter [dentistry, surgery]` (specialties sorted, `none` if empty).

Concepts: sets, enums, the get → change → save pattern.

## 02 Owners

`repository/owner_repository.py`, `service/owner_service.py`, `resource/owner_resource.py`

- Repository: write `InMemoryOwnerRepository` yourself, modelled on the doctor one.
- Service: `add_owner`, `get_owner`, `find_by_last_name`, `update_contact`.
- CLI: `owner add`, `owner find`, `owner show`, `owner update`.
- Output: `#1 George Franklin, 110 W. Liberty St., Madison, 6085551023`, prefixed with
  `added ` or `updated ` for those commands. An empty search prints `no owners`.

Concepts: dicts, keyword-only arguments, `None` as "not given", string methods.

## 03 Pets

`repository/pet_repository.py`, `service/pet_service.py`, `resource/pet_resource.py`

- Service: `add_pet`, `get_pet`, `pets_of_owner`.
- CLI: `pet add`, `pet list --owner-id`, `pet types`.
- Output: `#1 Leo (cat, born 2020-09-07), owner #1`. An owner with no pets prints `no pets`.
  `pet types` prints one type per line.

Concepts: `date`, parsing dates in argparse, services calling other services, the injected clock.

## 04 Scheduling

`service/scheduling.py`

- `next_slot_start` and `iter_slots`. Monday to Friday, 09:00 to 17:00, 30-minute slots.

Concepts: `datetime` and `timedelta` arithmetic, generators (`yield`), `itertools.islice` in the
tests.

## 05 Visits

`repository/visit_repository.py`, `service/visit_service.py`, `resource/visit_resource.py`

- Service: `first_available_slot`, `first_available_slots`, `book_visit`, `visits_for_pet`.
- CLI: `visit slots`, `visit book`, `visit list --pet-id`.
- Output:
  - slots: `#1 James Carter: 2026-10-05 10:00`, one line per doctor, or `no doctors`
  - book: `booked #1 2026-10-05 10:00 pet #1 with doctor #1: rabies shot`
  - list: the same line without `booked `, or `no visits`

Concepts: combining services, sets for fast lookup, `min` with a `key`, tie-breaking with tuples.

## Bonus (no tests: write your own)

- `--seed`: start the shell with Spring PetClinic's sample data (vets, owners, pets).
- `visit cancel --id ID`, which frees the slot.
- `owner show` also lists the owner's pets and their visits.
