PYTHON = python3
VENV = venv
PIP = $(VENV)/bin/pip
PY = $(VENV)/bin/python3
REQUIREMENTS = requirements.txt
MAIN = a_maze_ing
CONFIG = config.txt
DELETE = maze/__pycache__ $(VENV) .mypy_cache __pycache__ \
		maze.txt dist build *.egg-info maze/*.egg-info \
		*.whl
FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
				--disallow-untyped-defs --check-untyped-defs --no-error-summary

install:
	@echo "Creating a new venv..."
	@$(PYTHON) -m venv $(VENV)
	@echo "Done!"

	@echo "Installing dependencies..."
	@$(PIP) install -r $(REQUIREMENTS)
	@echo "Done!"

run: $(CONFIG)
	$(PY) -m $(MAIN) $(CONFIG)

debug:
	@echo "Debug mode..."
	$(PY) -m pdb -m $(MAIN) $(CONFIG)

clean:
	@echo "Cleaning..."
	rm -rf $(DELETE)

lint:
	@echo "Linters activation..."
	$(PY) -m flake8 .
	$(PY) -m mypy . $(FLAGS)
	@echo "Done!"

build:
	@$(PY) -m build
	@cp dist/*.whl .
	@cp dist/*.tar.gz .
	@echo "Done! Package available in root and dist/"

.PHONY: install run debug clean lint build

