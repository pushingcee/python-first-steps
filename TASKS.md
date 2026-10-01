# Tasks

Three phases, the same app each time: an in-memory CLI, then Postgres, then a REST API. The
services you write in phase 1 never change; later phases only add layers around them.

| Phase | Tasks | Done when |
|---|---|---|
| 1. In-memory CLI | 00 to 05 | `uv run pytest` is green (phase 2 and 3 tests are skipped) |
| 2. Postgres | 10 to 13 | `PETCLINIC_DATABASE_URL=… uv run pytest` is green |
| 3. REST API | 20 to 23 | the same, with FastAPI installed, so nothing is skipped |
| 4. Containerize | 30 | `docker compose up` runs the app and the database |

# Phase 1: in-memory CLI

Do them in order; later tasks build on earlier ones. A task is done when its test file passes:

```bash
uv run pytest tests/test_01_specialty.py -v
```

Each stub's docstring states the rules. The tests have the exact expectations, including output
strings. Read the test file before you start.

Each task's **Concepts** line is what it's there to teach. Green tests are half of done; the
other half is using those concepts. Before the PR, run `/review-task NN` in Claude Code (or ask
your agent for a pre-PR review) to check both.

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

# Phase 2: Postgres

Goal: the same app, but data survives a restart. You know SQL better than Python, so in this
phase the SQL is the easy part and the lesson is talking to a database from Python, plus Docker.

New dependency, already approved: `uv add "psycopg[binary]"` (psycopg 3, not psycopg2).
You'll need Docker Desktop (or Docker Engine) installed.

## 10 Postgres in Docker

No tests. Done when you can connect with `psql` or your SQL client.

1. Run it by hand once, to see the moving parts:
   `docker run --name petclinic-db -e POSTGRES_PASSWORD=… -p 5432:5432 -d postgres:17`.
   Connect, create a table, then `docker rm -f petclinic-db` and run it again. The table is
   gone: that's why you need a volume.
2. Write `compose.yaml` with a `db` service: the `postgres:17` image, a **named volume** for
   `/var/lib/postgresql/data`, port 5432, and a healthcheck using `pg_isready`.
3. Credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) come from a `.env` file,
   which is gitignored. Commit a `.env.example` with placeholder values instead.
4. `docker compose up -d`, `docker compose ps`, `docker compose logs db`, `docker compose down`
   (and what `down -v` does differently).

Concepts: images vs containers, ports, volumes, environment variables, why secrets stay out of git.

## 11 Schema

`db/schema.sql`. No tests yet, but task 13's tests will exercise it.

- One table per model, plus whatever a doctor's set of specialties needs. Spring PetClinic
  uses a join table (`vet_specialties`); an enum or an array column are alternatives. Pick
  one and be ready to explain why.
- Ids: `GENERATED ALWAYS AS IDENTITY` (Postgres' `IDENTITY(1,1)` / `AUTO_INCREMENT`).
- Visit start: `timestamp` (without time zone), because the app uses naive datetimes.
- Put the rules the database can enforce into the schema too: foreign keys, `NOT NULL`, a
  `CHECK` for the telephone, a unique index on an owner's pet names ignoring case. The
  service still validates first. The constraints are the safety net.
- Mount the `db/` folder at `/docker-entrypoint-initdb.d` in compose. Postgres runs it only
  when the volume is empty, so after a schema change, recreate the volume.

Postgres differences you'll hit: `TOP n` is `LIMIT n`, `ILIKE` is a case-insensitive `LIKE`,
identifiers are lower-cased unless quoted, and `user` is a reserved word.

## 12 Postgres repositories

`repository/*_repository.py`: a `Postgres*Repository` next to each `InMemory*` one, matching
the same `Protocol`. Write the doctor one first, then the rest.

- The constructor takes a `psycopg.Connection`. The repository doesn't open connections.
- `save()` inserts when `id is None` (`INSERT … RETURNING id`) and updates otherwise. It
  returns a new object; don't change the one passed in.
- Parameterized queries only: `cursor.execute("… WHERE id = %s", (doctor_id,))`. Never
  build SQL from input with f-strings. `test_13_postgres.py` checks that quotes and `%`/`_`
  in input are just text.
- Convert on the way out: rows hold plain strings, the models hold `PetType`/`Specialty`.
- Look up `row_factory`. `psycopg.rows.class_row` or `dict_row` can save you a lot of
  `row[0], row[1]`.

Concepts: context managers (`with`), DB-API cursors, transactions and autocommit, mapping rows to
dataclasses, SQL injection.

## 13 Wiring

`container.py`

- When the environment variable `PETCLINIC_DATABASE_URL` is set, `create_context()` opens
  **one** connection and builds the Postgres repositories with it. Otherwise it keeps the
  in-memory ones. Nothing outside `container.py` changes.
- Register closing that connection in `ApplicationContext.shutdown_hooks`. The shell and the
  tests call `context.close()` on exit.
- Use autocommit, or commit after each `save()`, so a second context sees the data.

Done when the **whole** suite passes against Postgres (conftest empties every table before each
test):

```bash
docker compose up -d
PETCLINIC_DATABASE_URL=postgresql://user:password@localhost:5432/petclinic uv run pytest
```

Concepts: `os.environ`, the composition root, why the in-memory tests never had to change.

# Phase 3: REST API

Goal: the same services behind HTTP instead of argparse. The `api/` package plays the role of
`resource/`: parse the request, call a service, shape the response. No business rules.

New dependencies, already approved: `uv add fastapi uvicorn` and `uv add --dev httpx` (the
test client needs it). Until they're installed, the `test_2x` files are skipped.

Read the FastAPI tutorial up to and including "Handling Errors" first. The Spring mapping:

| FastAPI | Spring |
|---|---|
| `@app.get("/doctors/{doctor_id}")` | `@GetMapping("/doctors/{doctorId}")` |
| function parameter `doctor_id: int` | `@PathVariable` |
| parameter with a default, `specialty: Specialty \| None = None` | `@RequestParam(required = false)` |
| Pydantic `BaseModel` parameter | `@RequestBody` + a DTO + bean validation |
| `response_model=…`, `status_code=201` | `ResponseEntity<Dto>` + `HttpStatus.CREATED` |
| `@app.exception_handler(NotFoundError)` | `@ControllerAdvice` + `@ExceptionHandler` |
| `APIRouter` | one `@RestController` class |

## 20 Doctor endpoints and error handling

`api/__init__.py`, `api/doctor_routes.py`, `api/schemas.py` (layout is a suggestion)

- `create_app(context: ApplicationContext) -> FastAPI` builds the app from an existing context.
  The tests call it with a frozen clock, and that's how services get into your routes.
- `NotFoundError` -> 404, `ValidationError` -> 400, both with body `{"detail": "<message>"}`.
  A malformed request is FastAPI's own 422.
- Routes: `POST /doctors` (201), `GET /doctors[?specialty=]`, `GET /doctors/{id}`,
  `PUT` and `DELETE /doctors/{id}/specialties/{specialty}`.
- Response bodies are DTOs, not the dataclasses. Specialties come out as a sorted list.

## 21 Owners and pets

- `POST /owners` (201), `GET /owners[?last_name=]`, `GET /owners/{id}`, `PATCH /owners/{id}`
  (only the fields sent).
- `POST /owners/{owner_id}/pets` (201), `GET /owners/{owner_id}/pets`, `GET /pet-types`.
- Dates are ISO strings in JSON (`"2020-09-07"`); Pydantic converts them for you.

## 22 Visits

- `GET /visits/slots`: `[{"doctor_id": 1, "start": "2026-10-05T10:00:00"}, …]` by doctor id.
- `POST /pets/{pet_id}/visits` (201) with `description` and optional `doctor_id`/`specialty`.
- `GET /pets/{pet_id}/visits`.

## 23 Run it (no tests)

- An entry point so `uv run uvicorn …` serves the app with the real clock and storage chosen
  by `PETCLINIC_DATABASE_URL`, like the shell.
- Open `/docs` (Swagger UI) and book a visit by hand.

# Phase 4: containerize

## 30 Dockerfile and compose (no tests)

- A `Dockerfile` for the API: a slim Python base image, dependencies installed in their own
  layer before the code is copied (why does the order matter?), and a non-root user.
- An `app` service in `compose.yaml` that waits for `db` to be healthy and gets
  `PETCLINIC_DATABASE_URL` from the environment. Inside compose the host is `db`, not
  `localhost`.
- `.dockerignore` so `.venv/` and `.env` don't end up in the image.
