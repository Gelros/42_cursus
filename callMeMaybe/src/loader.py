from src.models import FunctionDef, TestPrompt, FunctionCall
from pydantic import ValidationError
import json
import os


def load_functions_def(path: str) -> list[FunctionDef]:
    """Reads a JSON file and converts it into a list of FunctionDef objects."""
    try:
        with open(path, 'r') as f:
            res = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide: {e}")

    funcs: list[FunctionDef] = []
    for raw in res:
        try:
            funcs.append(FunctionDef(**raw))
        except ValidationError as e:
            raise ValueError(f"Definition invalide: {e}")
    return funcs


def load_tests_prompt(path: str) -> list[TestPrompt]:
    """Reads a JSON file and converts it into a list of TestPrompt objects."""
    try:
        with open(path, 'r') as f:
            res = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide: {e}")

    tests: list[TestPrompt] = []
    for raw in res:
        try:
            tests.append(TestPrompt(**raw))
        except ValidationError as e:
            raise ValueError(f"Schema invalide: {e}")
    return tests


def save_results_in_json(results: list[FunctionCall], path: str) -> None:
    """Save result in json file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as f:
        json.dump([r.model_dump() for r in results], f, indent=2)