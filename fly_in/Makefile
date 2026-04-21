.PHONY: install run debug clean lint lint-strict test

install:
	uv sync --dev

run:
	uv run python -m src

debug:
	uv run python -m pdb src

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

test:
	uv run pytest

clean:
	rm -rf .mypy_cache .pytest_cache .ruff_cache .coverage htmlcov build dist .venv
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
