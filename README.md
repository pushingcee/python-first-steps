# PetClinic (Python CLI edition)

[Spring PetClinic](https://github.com/spring-projects/spring-petclinic) rebuilt in Python, as a
learning project. Same domain, same layering (resource → service → repository), Python syntax.
Naming differences: Spring's `Vet` is `Doctor` here, and a pet is a patient.

## Setup

With [uv](https://docs.astral.sh/uv/) (recommended):

```bash
uv sync
uv run pytest tests/test_00_doctor.py   # the worked example, already green
uv run petclinic                        # start the shell
```

Without uv:

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e . pytest ruff
pytest tests/test_00_doctor.py
python -m petclinic
```

## Using the shell

Storage is in memory, so data lives as long as the shell does. Each line is parsed with argparse.

```
petclinic> doctor add --first-name James --last-name Carter
added #1 James Carter [none]
petclinic> doctor list
#1 James Carter [none]
petclinic> doctor --help
petclinic> exit
```

## How to work

1. Read `CLAUDE.md` (the rules) and everything involved in the doctor feature end to end:
   `resource/doctor_resource.py` → `service/doctor_service.py` →
   `repository/doctor_repository.py` → `model/doctor.py`, then `tests/test_00_doctor.py`.
2. Do the tasks in `TASKS.md` in order. Each one has a test file; it's done when the file is green.
3. One branch and one PR per task.

## Layout

```
src/petclinic/
  cli.py          shell: parse a line, dispatch, print
  container.py    wires everything together (the Spring context)
  clock.py        injectable time
  exceptions.py   NotFoundError, ValidationError
  model/          dataclasses and enums
  repository/     storage interfaces + in-memory implementations
  service/        business rules; scheduling.py has the slot arithmetic
  resource/       argparse commands per resource
tests/            one file per task; conftest.py freezes time at Monday 2026-10-05 10:00
```

## Roadmap

1. **Now:** in-memory CLI.
2. **Postgres:** Postgres in Docker with a named volume. Add `Postgres*Repository` classes using
   psycopg next to the in-memory ones; only `container.py` changes, and the same service tests
   must pass.
3. **FastAPI:** an HTTP resource layer calling the same services.
4. **Containerize:** a Dockerfile for the app, and the app added to compose.
