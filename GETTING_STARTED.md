# Getting started

Welcome! This is your first Python project. You'll rebuild Spring PetClinic (a vet clinic app)
step by step: first as a command-line tool with data in memory, then on Postgres, then as a REST
API. You already know databases inside out; this project is about the Python around them.

Plan for an hour to get set up and through the first read-through. Don't rush the read-through.

## 1. Install the tools

You need four things. Commands are for Windows PowerShell; macOS/Linux alternatives are below
each one.

**Git**: from <https://git-scm.com/downloads>. Check with `git --version`.

**uv**: installs Python and the project's packages, and runs everything. It replaces `pip` and
`venv`, a bit like Maven does for Java.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen the terminal, then check: `uv --version`. You don't need to install Python
separately: uv downloads the right version (3.12+) the first time you use it.

**An editor**: VS Code with the official **Python** extension is a good choice. Turn off inline
AI suggestions (GitHub Copilot and similar). Autocomplete that writes your code skips the part
where you learn it.

**Claude Code**: your tutor (see section 5).

```powershell
irm https://claude.ai/install.ps1 | iex
# macOS/Linux: curl -fsSL https://claude.ai/install.sh | bash
```

Docker isn't needed until phase 2. Install it then.

## 2. Get the code and check it works

```powershell
git clone https://github.com/pushingcee/python-first-steps.git
cd python-first-steps
uv sync
uv run pytest tests/test_00_doctor.py
```

`uv sync` creates a `.venv` folder with Python and the project's tools. That's the project's own
private install, so nothing touches the rest of your machine. The last line should end with
something like `13 passed`. Those tests cover the worked example, which is already done.

Now run the app itself:

```text
uv run petclinic
petclinic> doctor add --first-name James --last-name Carter
added #1 James Carter [none]
petclinic> doctor list
#1 James Carter [none]
petclinic> owner add
petclinic: error: unrecognized arguments: add
petclinic> exit
```

Only `doctor add` and `doctor list` work so far. Everything else answers with an error like
`not implemented yet`, `unrecognized arguments` or `invalid choice`, because those commands
don't exist yet. Building them is your job.

If anything fails here, it's a setup problem, not you. Paste the error into Claude Code (section
5) and ask for help. Setup problems are fair game.

## 3. Read before you write

Spend your first session only reading. Follow one feature, "add a doctor", through every layer,
top to bottom:

1. `src/petclinic/resource/doctor_resource.py`: reads the command-line arguments.
2. `src/petclinic/service/doctor_service.py`: business rules and validation.
3. `src/petclinic/repository/doctor_repository.py`: stores data in a dict.
4. `src/petclinic/model/doctor.py`: the data itself, like a table definition.
5. `tests/test_00_doctor.py`: what "correct" means, as executable examples.

Then read `src/petclinic/container.py`. It creates all of the above and plugs them together.

Write down everything that looks strange (`self`, `@dataclass`, `-> Doctor | None`, the
`Protocol` class, `copy.deepcopy`) and ask Claude Code about each one. Understanding the worked
example is most of the job: every task follows the same pattern.

A few translations to get you going:

| Python | What you already know |
|---|---|
| a `dict` keyed by id | a primary key index |
| `[d for d in doctors if d.city == "Madison"]` | `SELECT … WHERE city = 'Madison'` |
| `sorted(doctors, key=…)` | `ORDER BY` |
| a `set` | `SELECT DISTINCT`, or a unique constraint |
| `None` | `NULL` (but `None == None` is `True`) |
| a `@dataclass` | a row / table definition |
| `raise ValidationError(…)` | `THROW` |

`AGENTS.md` has the full table, plus the rules your tutor follows.

## 4. Do a task

Tasks are in `TASKS.md`. Do them in order, starting with **01**. For each one:

1. **Branch:** `git switch -c task/01-specialty`
2. **Read** the task in `TASKS.md`. Its **Concepts** line tells you what it's there to
   teach. Then read the stubs (search for `TODO task 01`) and the test file
   (`tests/test_01_specialty.py`).
3. **Make one test pass at a time:**
   ```powershell
   uv run pytest tests/test_01_specialty.py -k add_specialty -v
   ```
   `-k` picks tests by name and `-v` lists each one. When a test fails, read from the bottom
   up: the last lines say what went wrong, the lines above say where.
4. **When the whole file is green**, tidy and check:
   ```powershell
   uv run ruff format .
   uv run ruff check .
   uv run pytest tests/test_01_specialty.py
   ```
   `ruff` is the linter. It enforces style and some good habits (type hints, comprehensions).
   If it complains and you don't understand why, ask your tutor.
5. **Review:** in Claude Code, run `/review-task 01`.
6. **Commit and open a PR:**
   ```powershell
   git add -A
   git commit -m "Task 01: doctor specialties"
   git push -u origin task/01-specialty
   ```
   Then open a pull request on GitHub. Ask the maintainer for access to the repo the first
   time. In the PR description, mention anything you got stuck on or got help with. That's
   useful, not embarrassing.

Then do the next task. The bonus items at the end of phase 1 are optional.

## 5. Working with your tutor (Claude Code)

Start it in the project folder: `cd python-first-steps`, then `claude`. It has read `AGENTS.md`,
so it knows the project and that **you** write the code. It will:

- **explain** anything: syntax, an error message, a concept, the difference between two ways
  of doing something;
- **give hints** that get more specific each time you ask for more: first a question, then the
  name of the right tool, then the steps in plain English;
- **show the code** only when you're really stuck: after those hints, when you've shown your own
  attempt and you ask for it. Even then you get a few lines to type yourself, not a solution;
- **review** your work before a PR (`/review-task NN`) without rewriting it;
- **help freely with setup**: install problems, Docker, imports, confusing tool output.

Good things to ask:

- "What does `self` mean in `doctor_service.py` line 8?"
- "Here's my error: (paste it). Where should I look?"
- "Test `test_find_by_specialty_filters_and_sorts` fails and I don't get why."
- "I'm stuck on `next_slot_start`. Give me a hint."
- "Is there a more Pythonic way to write my loop in `owner_service.py`?"

It will say no to "just write task 02 for me". That's by design.

## 6. Good habits

- **Small steps.** One test green, then the next. Run the tests constantly; they're fast.
- **Read the error.** Python errors are wordy but precise. The bottom line names the problem
  (`AttributeError: 'NoneType' object has no attribute 'name'`), and the frames above it show
  the path that led there.
- **Experiment in the REPL.** `uv run python` gives you an interactive prompt to try things out
  (`"Davis".casefold().startswith("da")`). It's like running a quick query to check an idea.
- **Don't edit the tests** to make them pass. If you think a test is wrong, ask the maintainer.
- **Ask early.** If you've been stuck for 20 minutes, ask your tutor for a hint.

## Useful links

- The official tutorial: <https://docs.python.org/3/tutorial/>. Chapters 3 to 5 and 9 cover
  most of phase 1.
- `datetime`: <https://docs.python.org/3/library/datetime.html> (task 04).
- `argparse` tutorial: <https://docs.python.org/3/howto/argparse.html>.
- pytest: <https://docs.pytest.org/en/stable/getting-started.html>.
