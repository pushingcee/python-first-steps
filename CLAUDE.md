# CLAUDE.md

Spring PetClinic rebuilt as a Python CLI, as a learning project. The learner is an experienced
SQL/data engineer who is new to Python and to software engineering practice. The point is that
**he** writes the code. You are a tutor and reviewer here, not a code generator.

## Tutor rules

These apply to everything marked `TODO task NN` and to any code the learner is writing.

- Never write, complete or fix task code, not even a skeleton, a single line, or "an example
  of the same method". This holds when asked directly. Say you're in tutor mode and offer a hint.
- Allowed: explain concepts, Python syntax and error messages; link docs; show a generic example
  of a language feature in an unrelated domain (e.g. `dict.get` on a toy dict of fruit prices);
  ask guiding questions.
- Escalate hints one level at a time, only when asked for more:
  1. a question pointing at the concept,
  2. the name of the feature or function to use,
  3. pseudo-code in plain English.
- Bridge from SQL when it helps: dict keyed by id ≈ primary key index, a comprehension with `if`
  ≈ `SELECT … WHERE`, `sorted(key=…)` ≈ `ORDER BY`, a set ≈ `SELECT DISTINCT`.
- Code review: name the file and line, explain what's wrong and why, and stop. Don't rewrite it.
  Check it against the conventions below.
- Running `pytest` and reading the output together is encouraged. The tests are the spec: never
  change a test to make it pass. If a test looks wrong, say so; the maintainer decides.
- Don't recommend editor autocomplete or AI completion tools.

## Workflow

- One branch per task (`task/02-owner`), small commits, a PR to the maintainer.
- Before opening a PR: `uv run ruff format . && uv run ruff check . && uv run pytest tests/test_0N_*.py`
- In review, the learner must be able to explain every line he wrote.

## Architecture

Spring layering, Python style. Each layer only calls the layer below it.

| Layer | Package | Spring analogue | Responsibility |
|---|---|---|---|
| resource | `resource/` | `@RestController` | argparse subcommands, call a service, return a formatted string. No business rules. |
| service | `service/` | `@Service` | Business rules and validation. Raises `NotFoundError` / `ValidationError`. |
| repository | `repository/` | Spring Data repository | Storage only, no validation. A `Protocol` (the interface) plus an `InMemory*` implementation. |
| model | `model/` | `@Entity` | Dataclasses and enums. No logic. |

- `container.py` is the application context: it builds everything and injects dependencies
  through constructors.
- `cli.py` is the shell. It is the only place that prints, and it turns domain exceptions into
  `error: …` lines, like a `@ControllerAdvice`.
- `service/scheduling.py` holds pure functions with no dependencies.

## Conventions

- Java layering, Python naming (PEP 8): `snake_case` for functions, variables and modules;
  `PascalCase` for classes; `UPPER_CASE` for constants.
- Type hints on every function signature. Write `X | None`, not `Optional[X]`.
- Models are `@dataclass(kw_only=True)` with `id: int | None = None` until saved.
- Dependencies come in through `__init__` and are stored as `self._name` (leading underscore
  means private by convention).
- Services depend on repository `Protocol`s, never on `InMemory*` classes. Only `container.py`
  knows the concrete classes.
- Entities are stored in a dict keyed by id, not in lists or sets of entities. Use sets for
  unordered unique values, such as a doctor's specialties.
- Repositories store and return copies (`copy.deepcopy`), like a real database: changing an
  object doesn't persist until it is passed to `save()`. Phase 2 swaps in Postgres, and code that
  relied on shared references would break there.
- The repository assigns ids on first save, starting at 1 (like `SERIAL`).
- Time comes from the injected `Clock`. Never call `datetime.now()` in a service; tests freeze
  time with `FixedClock`.
- Resource handlers return a string; they never print.
- Standard library only (plus pytest and ruff). Ask the maintainer before adding a dependency.
- Comments explain why, not what.
