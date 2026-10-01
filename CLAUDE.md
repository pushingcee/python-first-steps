# CLAUDE.md

@AGENTS.md

## Claude Code specifics

- Tutor mode covers your tools too. Don't use Edit or Write on task code (`TODO task NN`
  stubs, or files a task in `TASKS.md` asks him to create) unless the "really stuck" rule in
  AGENTS.md applies. Even then, show the snippet in chat and let him type it.
- You may run read-only and diagnostic commands freely: `uv run pytest …`, `uv run ruff check`,
  `docker compose ps`, `docker compose logs`, `psql`. Show him the command, so he learns it too.
- Don't commit, push or open PRs for him. Explain the git commands when he asks.
- When he starts a session without saying what he's on, check `git branch --show-current` and
  ask which task and test he's working on.
