# Makefile — RAG against the machine
# Targets required by the subject (III.2): install, run, debug, clean, lint.
# lint-strict is the optional stricter variant.

.PHONY: install run debug clean lint lint-strict help

# Default query / paths used by `make run` and `make debug`.
QUERY ?= How to configure the OpenAI server?
K     ?= 10

help:
	@echo "Available targets:"
	@echo "  install      Install project dependencies with uv."
	@echo "  run          Run a sample search (override with QUERY=... K=...)."
	@echo "  debug        Run the CLI under pdb."
	@echo "  lint         flake8 + mypy with the subject's flags."
	@echo "  lint-strict  flake8 + mypy --strict."
	@echo "  clean        Remove caches and Python artifacts."

# III.2 install: install dependencies (we use uv as required by IV.2).
# On 42 machines, redirect uv's wheel cache (~2 GB) to goinfre so it does not
# fill the home quota. Falls back to the default cache when ~/goinfre is absent.
install:
	@if [ -d "$$HOME/goinfre" ]; then \
		mkdir -p "$$HOME/goinfre/uv-cache"; \
		echo "goinfre detected -> uv cache in $$HOME/goinfre/uv-cache"; \
		UV_CACHE_DIR="$$HOME/goinfre/uv-cache" uv sync; \
	else \
		uv sync; \
	fi

# III.2 run: execute the main script. Defaults to a search; override QUERY/K.
run:
	uv run python -m src search "$(QUERY)" --k=$(K)

# III.2 debug: run the main script under Python's built-in debugger.
debug:
	uv run python -m pdb -m src search "$(QUERY)" --k=$(K)

# III.2 lint: exact flags mandated by the subject.
lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# III.2 lint-strict (optional): the stricter variant.
lint-strict:
	uv run flake8 .
	uv run mypy . --strict

# III.2 clean: remove temporary files and caches.
clean:
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	find . -type d -name '.mypy_cache' -prune -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -prune -exec rm -rf {} +
	find . -type d -name '.ruff_cache' -prune -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete
