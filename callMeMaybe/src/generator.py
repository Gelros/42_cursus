from enum import Enum, auto
from dataclasses import dataclass, field
from src.models import FunctionDef
from typing import Any
from llm_sdk import Small_LLM_Model
from src.vocabulary import id_to_tokens
import numpy as np


class JsonState(Enum):
    START     = auto() # On commence à générer (on attend le '{')
    NAME      = auto() # On est en train d'écrire le nom de la fonction
    PARAM_KEY = auto() # On écrit le nom d'un argument (ex: "a")
    PARAM_VAL = auto() # On écrit la valeur de l'argument (ex: 2.0)
    IN_STRING = auto() # On écrit la chaine de caractère
    PARAM_NEXT= auto() # On a fini un param, on attend une virgule ou la fin '}'
    END       = auto() # JSON terminé, on ne génère plus rien

@dataclass
class GenerationContext:
    state        : JsonState # Savoir où nous en sommes dans la structure JSON
    functions    : list[FunctionDef] # Liste de toutes les fonctions disponibles
    func_tokens  : dict[str, list[int]] # Les noms de fonctions déjà convertis en IDs
    chosen_func  : FunctionDef | None = None # La fonction que l'IA a fini par choisir
    tokens_so_far: list[int] = field(default_factory=list) # Historique des chiffres générés par l'IA
    params_done  : list[str] = field(default_factory=list) # Noms des paramètres déjà remplis
    current_param: str | None = None # Le paramètre qu'on est en train de remplir actuellement

def _get_number_tokens(
    vocab: dict[str, int],
    tokens_so_far: list[int],
    id_to_token: dict[int, str],
) -> list[int]:
    generated = "".join(id_to_token[i] for i in tokens_so_far)
    has_dot = '.' in generated
    res = []
    for token, id in vocab.items():
        t = token.strip()
        if not t: continue

        if t[0].isdigit(): res.append(id)

        elif t.lstrip('-').isdigit(): res.append(id)

        elif t == '-': res.append(id)

        elif not has_dot and t == '.': res.append(id)

        elif t in ('}', ','): res.append(id)
    return res

def get_valid_tokens(
    context: GenerationContext,
    vocab: dict[str, int],
    model: Small_LLM_Model
) -> list[int]:
    if context.state == JsonState.START:
        return [vocab['{']]
    if context.state == JsonState.NAME:
        valid = []
        for name, token_ids in context.func_tokens.items():
            n = len(context.tokens_so_far)
            if token_ids[:n] == context.tokens_so_far and n < len(token_ids):
                valid.append(token_ids[n])
                return valid
        if not valid:
            raise ValueError("Token invalid")
            
    if context.state == JsonState.PARAM_KEY:
        n = len(context.tokens_so_far)
        if context.chosen_func:
            allowed = [
                p for p in context.chosen_func.parameters.keys()
                if p not in context.params_done
            ]
        else:
            raise ValueError("Pas de fonction choisie")
        if not allowed:
            raise ValueError("PARAM_KEY : plus de paramètres restants")
        ids = model.encode(allowed[0])[0].tolist()
        if n < len(ids):
            return [ids[n]]
    
    if context.state == JsonState.PARAM_VAL:
        type_of_param = context.chosen_func.parameters[context.current_param].type
        if isinstance(type_of_param, bool):
            return [vocab["true"], vocab["false"]]
        elif isinstance(type_of_param, str):
            return [vocab['"']]
        elif isinstance(type_of_param, int, float):
            return _get_number_tokens(vocab, context.tokens_so_far, id_to_tokens)
    
    if context.state == JsonState.IN_STRING:
        quote_id = vocab['"']
        return [v for k, v in vocab.items() if v != quote_id]
            


def _updtate_state(context: GenerationContext, token_str: str) -> None:
    ...


def apply_mask(logits: np.ndarray, allowed_ids: list[int]) -> np.ndarray:
    mask = np.full_like(logits, -np.inf)
    mask[allowed_ids] = 0
    return mask

def generate(model: Small_LLM_Model, context: GenerationContext) -> None:
    ...

