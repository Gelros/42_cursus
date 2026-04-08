.PHONY: install run debug clean fclean lint lint-strict

install:
	uv sync

run:
	uv run python -m src --input data/input/function_calling_tests.json

debug:
	uv run python -m pdb -m src

# Nettoie les fichiers temporaires de cache
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Nettoyage complet : fichiers de cache + environnement virtuel + lockfile
fclean: clean
	rm -rf .venv
	rm -f uv.lock

lint:
	uv run flake8 .
	uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict