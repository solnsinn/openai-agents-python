This folder contains runnable examples that demonstrate how to use the `agents` library.

Run the minimal example (uses a local DummyProvider that does not need an API key):

This folder contains runnable examples that demonstrate how to use the `agents` library.

Run the minimal example (uses a local DummyProvider that does not need an API key):

```bash
# Create and prepare a local venv (optional; recommended)
make prepare-venv

# Run the example as a module
PYTHONPATH=. .venv/bin/python -m examples.basic.run_agent_example
```

Run the unit test for the dummy provider:

```bash
# After `make prepare-venv`
.venv/bin/python -m pytest tests/test_dummy_provider.py
```

Notes:
- The example uses a local dummy model provider (`examples/model_providers/local_dummy_provider.py`) so it does not call external APIs.
- To run the real OpenAI provider, set the `OPENAI_API_KEY` environment variable and run examples that use the default provider.
- The example prints `final_output` when available. If `final_output` is empty, the example falls back to printing items from `raw_responses` (this is used by the DummyProvider to show the reply).
