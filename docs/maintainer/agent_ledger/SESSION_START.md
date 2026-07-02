# SESSION_START

## Project

Vision FSM Agent is a lightweight Python framework for building
computer-vision-driven automation agents with finite-state-machine
control and human-in-the-loop correction.

It is intended for **local, controlled demo environments, research, and
education**. It is not a game bot, cheating tool, or third-party
automation tool.

## Current Goal

Maintain and grow the repository as an active open-source project with
real issues, PR-ready commits, changelog updates, tests, release notes,
and safety documentation.

## Maintenance Cycle

Ongoing, structured as work rounds:

| Phase | Focus |
|-------|-------|
| 1 | README and demo clarity |
| 2 | Contributor experience and troubleshooting |
| 3 | v0.1.0 release materials |
| 4 | v0.1.1 maintenance polish |
| 5 | Documentation and roadmap finalization |

## Must Read

1. `README.md`
2. `AGENTS.md`
3. `docs/safety-boundaries.md`
4. `docs/maintainer/agent_ledger/NEXT.md`
5. `docs/maintainer/agent_ledger/DECISIONS.md`
6. `CHANGELOG.md` (especially `[Unreleased]`)

## Safety Rules

- Do **not** reintroduce game-specific automation, game names, or
  emulator references.
- Do **not** add anti-detection, evasion, or human-mimicry language.
- Do **not** add third-party game assets or screenshots.
- Do **not** remove or weaken safety boundaries.
- Do **not** push or release without explicit user approval.
- Do **not** commit API keys, tokens, or `.env` files.

## Done Criteria (per round)

- `pytest tests/ -q` passes (currently 63 tests)
- `python scripts/oss_readiness_check.py` passes
- No risky wording regression (Chinese zero-tolerance; English
  negative-context exempted)
- `git status` is clean or clearly reported
- `PROGRESS.md` and `NEXT.md` updated

## Quick Commands

```bash
# Run tests
pytest tests/ -q

# Run demo
python examples/visual_grid_world/run_demo.py --steps 20

# Run OSS readiness check
python scripts/oss_readiness_check.py
python scripts/oss_readiness_check.py --run-tests

# Generate demo assets
python scripts/generate_demo_assets.py

# Start HIL server (optional)
python run.py --hil

# Check git status
git status --short
```
