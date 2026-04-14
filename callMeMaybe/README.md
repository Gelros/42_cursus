# callMeMaybe

`callMeMaybe` converts natural language prompts into structured function-call
objects.

## What It Does

The pipeline reads:
- function definitions (`name`, `description`, `parameters`, `returns`)
- prompt test cases

And writes:
- a JSON array of items with `prompt`, `name`, and `parameters`

## Project Layout

- `src/models.py`: Pydantic schemas
- `src/loader.py`: JSON loading/saving with validation
- `src/generator.py`: function and parameter generation
- `src/__main__.py`: CLI entrypoint
- `llm_sdk/__init__.py`: local model wrapper

## Setup

Requirements:
- Python 3.10+
- `uv`

Install dependencies:

```bash
make install
```

## Run

```bash
make run
```

or:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

## Quality Checks

Run static checks:

```bash
make lint
```

This runs:
- `flake8` for style
- `mypy` for typing

## Example Output

```json
{
  "prompt": "What is the sum of 2 and 3?",
  "name": "fn_add_numbers",
  "parameters": {
    "a": 2.0,
    "b": 3.0
  }
}
```
