from llm_sdk import Small_LLM_Model
from src.models import FunctionDef
import json


def load_vocab(model: Small_LLM_Model) -> dict[str, int]:
    """Load vocabulary from LLM_MODEL in dictionary."""
    path = model.get_path_to_tokenizer_file()
    try:
        with open(path, 'r') as f:
            tokens_data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier vocabulaire introuvable : {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide dans le vocabulaire : {e}")
    try:
        return tokens_data["model"]["vocab"]
    except KeyError as e:
        raise ValueError(f"Structure tokenizer inattendue : {e}")
    

def id_to_tokens(vocab: dict[str, int]) -> dict[int, str]:
    """Return dictionnary (id: token) from LLM vocabulary"""
    return {v: k for k, v in vocab.items()}

def pre_calc_name_func(
    functions: list[FunctionDef],
    model: Small_LLM_Model
) -> dict[str, list[int]]:
    """Pre-calculate the token IDs for each function name."""
    result: dict[str, list[int]] = {}
    for func in functions:
        result[func.name] = model.encode(func.name)[0].tolist()
    return result