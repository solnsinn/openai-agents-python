<!--
PR template for contributors. Keep this short and focused on the key expectations.
-->
# Pull Request

Describe the change in a sentence or two. Keep PRs small and focused when possible.

## Checklist
- [ ] I ran `make dev-setup` and installed dev dependencies.
- [ ] I ran the test suite locally: `.venv/bin/python -m pytest tests` and all tests passed.
- [ ] I added or updated tests for any new behavior.
- [ ] I updated documentation where relevant (e.g., `CONTRIBUTING.md`, `examples/README.md`).

## Notes for reviewers
- If this PR touches packaging or dependencies, ensure `pyproject.toml` and the Makefile targets are updated.

Thank you for contributing!
### Summary

<!-- Please give a short summary of the change and the problem this solves. -->

### Test plan

<!-- Please explain how this was tested -->

### Issue number

<!-- For example: "Closes #1234" -->

### Checks

- [ ] I've added new tests (if relevant)
- [ ] I've added/updated the relevant documentation
- [ ] I've run `make lint` and `make format`
- [ ] I've made sure tests pass
