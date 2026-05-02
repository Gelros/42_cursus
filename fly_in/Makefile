.PHONY: install run run-raw debug clean lint lint-strict test

MAP ?= maps/easy/02_simple_fork.txt

install:
	uv sync --dev

run:
	uv run python -m src $(MAP)

run-raw:
	uv run python -m src $(MAP) --raw

debug:
	uv run python -m pdb -m src $(MAP)

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

test:
	uv run pytest

clean:
	rm -rf .mypy_cache .pytest_cache .ruff_cache .coverage htmlcov \
		build dist
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
