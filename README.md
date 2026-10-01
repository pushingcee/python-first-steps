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

1. Read `AGENTS.md` (the rules; your AI assistant follows them too: it will guide you rather
   than write your code) and everything involved in the doctor feature end to end:
   `resource/doctor_resource.py` → `service/doctor_service.py` →
   `repository/doctor_repository.py` → `model/doctor.py`, then `tests/test_00_doctor.py`.
2. Do the tasks in `TASKS.md` in order. Most have a test file; a task is done when its file is
   green. Tests for later phases are skipped until you get there.
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
  api/            phase 3: FastAPI routes (you create it)
tests/            one file per task; conftest.py freezes time at Monday 2026-10-05 10:00
AGENTS.md         rules for you and for AI assistants (CLAUDE.md imports it)
TASKS.md          the tasks, phase by phase
```

## Phases

Details and the definition of done for each phase are in `TASKS.md`.

1. **In-memory CLI** (tasks 00 to 05): Python syntax, data structures, layering.
2. **Postgres** (tasks 10 to 13): Postgres in Docker with a named volume, a schema, and
   `Postgres*Repository` classes using psycopg next to the in-memory ones. Only `container.py`
   changes, and the whole suite must pass against Postgres too.
3. **REST API** (tasks 20 to 23): a FastAPI layer calling the same services.
4. **Containerize** (task 30): a Dockerfile for the app, and the app added to compose.
