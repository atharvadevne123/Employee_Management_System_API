# Contributing to Employee Management System API

Thank you for contributing! Please follow these guidelines.

## Getting Started

```bash
git clone https://github.com/atharvadevne123/Employee_Management_System_API.git
cd Employee_Management_System_API
pip install -r requirements.txt
cp .env.example .env
make migrate
make test
```

## Development Workflow

1. Fork the repository and create a feature branch: `git checkout -b feat/my-feature`
2. Make your changes and add tests for new functionality
3. Run `make lint` and `make test` — both must pass
4. Commit using Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`
5. Open a pull request against `main`

## Code Standards

- Python 3.10+ type annotations required on all public functions
- Google-style docstrings on all classes and public methods
- Use `logging.getLogger(__name__)` — no bare `print()` statements
- All new API endpoints must have at least 3 tests (happy path + 2 edge cases)
- `ruff check . --select E,F,W,I --ignore E501` must exit 0

## Running Tests

```bash
make test              # run full test suite with coverage
pytest tests/test_employees.py -v   # run specific file
```

## Reporting Issues

Open a GitHub issue with: steps to reproduce, expected vs actual behaviour, and Python/Django version.
