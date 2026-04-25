from llm_sdk import Small_LLM_Model
from src.models import FunctionDef
import json


def load_vocab(model: Small_LLM_Model) -> dict[str, int]:
    """Return the token-to-id mapping from the model's tokenizer file."""
    path = model.get_path_to_tokenizer_file()
    try:
        with open(path, "r") as f:
            tokens_data = json.load(f)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Vocabulary file not found: {path}") from exc
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid vocabulary JSON: {e}") from e
    try:
        vocab: dict[str, int] = tokens_data["model"]["vocab"]
        return vocab
    except KeyError as e:
        raise ValueError(f"Unexpected tokenizer structure: {e}") from e


def pre_calc_name_func(
    functions: list[FunctionDef], model: Small_LLM_Model
) -> dict[str, list[int]]:
    """Pre-tokenize all function names once at startup to avoid redundant calls."""
    result: dict[str, list[int]] = {}
    for func in functions:
        result[func.name] = model.encode(func.name)[0].tolist()
    return result
