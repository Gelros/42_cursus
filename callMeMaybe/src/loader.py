from src.models import FunctionDef, TestPrompt, FunctionCall
from pydantic import ValidationError
import json
import os


def load_functions_def(path: str) -> list[FunctionDef]:
    """Load and validate function definitions from JSON."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            res = json.load(f)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File not found: {path}") from exc
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e

    funcs: list[FunctionDef] = []
    for raw in res:
        try:
            funcs.append(FunctionDef(**raw))
        except ValidationError as e:
            raise ValueError(f"Invalid function definition: {e}") from e
    return funcs


def load_tests_prompt(path: str) -> list[TestPrompt]:
    """Load and validate test prompts from JSON."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            res = json.load(f)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File not found: {path}") from exc
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e

    tests: list[TestPrompt] = []
    for raw in res:
        try:
            tests.append(TestPrompt(**raw))
        except ValidationError as e:
            raise ValueError(f"Invalid prompt schema: {e}") from e
    return tests


def save_results_in_json(results: list[FunctionCall], path: str) -> None:
    """Save function call results as JSON."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in results], f, indent=2)
