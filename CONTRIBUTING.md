# Contributing to OpenAI Agents Python SDK

Thank you for your interest in contributing!

## Development environment setup

To get started with development, clone the repository and set up a local Python virtual environment with all development dependencies:

```bash
make dev-setup
```

This will:
- Create a `.venv` directory (if not present)
- Install the package in editable mode
- Install all common development tools (pytest, pytest-asyncio, pytest-mock, mypy, ruff, rich, etc.)

## Running tests

To run the full test suite:

```bash
.venv/bin/python -m pytest tests
```

Or use the Makefile target:

```bash
make tests
```

## Running the example

To run the minimal agent example:

```bash
make run-example
```

Or directly:

```bash
PYTHONPATH=. .venv/bin/python -m examples.basic.run_agent_example
```

## Additional notes
- The `dev-setup` target will use `uv` for dependency management if available, otherwise falls back to pip.
- If you add new dependencies, update `pyproject.toml` and the Makefile as needed.
- For more details, see `AGENTS.md` and `examples/README.md`.

## CI badges

This repository displays CI status badges in the top-level `README.md` for quick visibility.

- The **Tests** badge shows the result of our lint/typecheck/test pipeline. Click it to view logs for failures.
- The **Dev Setup & Example** badge runs `make dev-setup`, the test suite, and the example to validate developer ergonomics.

If a badge is failing on your PR, open the workflow run to inspect logs. Common issues are missing dev deps (run `make dev-setup`) or tests that rely on environment variables — check the workflow environment and the PR details.
