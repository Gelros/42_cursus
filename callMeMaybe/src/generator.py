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
    state        : JsonState                    # Où on en est dans la structure JSON
    functions    : list[FunctionDef]            # Toutes les fonctions disponibles
    func_tokens  : dict[str, list[int]]         # Noms de fonctions convertis en IDs
    chosen_func  : FunctionDef | None = None    # Fonction choisie par l'IA
    tokens_so_far: list[int] = field(default_factory=list)  # Tokens générés pour le nom courant
    params_done  : list[str] = field(default_factory=list)  # Paramètres déjà remplis
    current_param: str | None = None            # Paramètre en cours de remplissage
    current_value: str = ""                     # Valeur en cours de génération (number/bool)

def _get_number_tokens(
    vocab: dict[str, int],
    current_value: str,
) -> list[int]:
    """Retourne les token IDs valides pour générer un nombre.

    Args:
        vocab: Vocabulaire token -> ID.
        current_value: La valeur numérique déjà générée (ex: "2", "2.").

    Returns:
        Liste des token IDs autorisés.
    """
    has_dot = "." in current_value
    has_exp = "e" in current_value.lower()
    res: list[int] = []

    for token, tid in vocab.items():
        t = token.strip()
        if not t:
            continue
        if t[0].isdigit() or t.lstrip("-").isdigit():
            res.append(tid)
        elif not has_dot and not has_exp and t == ".":
            res.append(tid)
        elif t in (",", "}"):
            res.append(tid)

    return res

def get_valid_tokens(
    ctx: GenerationContext,
    vocab: dict[str, int],
    model: Small_LLM_Model,
    id_to_token: dict[int, str]
) -> list[int]:
    if ctx.state == JsonState.START:
        return [vocab['{']]
    if ctx.state == JsonState.NAME:
        valid = []
        for name, token_ids in ctx.func_tokens.items():
            n = len(ctx.tokens_so_far)
            if token_ids[:n] == ctx.tokens_so_far and n < len(token_ids):
                valid.append(token_ids[n])
                return valid
        if not valid:
            raise ValueError("Token invalid")
            
    if ctx.state == JsonState.PARAM_KEY:
        n = len(ctx.tokens_so_far)
        if ctx.chosen_func:
            allowed = [
                p for p in ctx.chosen_func.parameters.keys()
                if p not in ctx.params_done
            ]
        else:
            raise ValueError("Pas de fonction choisie")
        if not allowed:
            raise ValueError("PARAM_KEY : plus de paramètres restants")
        ids = model.encode(allowed[0])[0].tolist()
        if n < len(ids):
            return [ids[n]]
    
    if ctx.state == JsonState.PARAM_VAL:
        type_of_param = ctx.chosen_func.parameters[ctx.current_param].type
        if type_of_param == "boolean":
            return [vocab["true"], vocab["false"]]
        elif type_of_param == "string":
            return [vocab['"']]
        elif type_of_param == "number":
            return _get_number_tokens(vocab, ctx.current_value)
    
    if ctx.state == JsonState.IN_STRING:
        quote_id = vocab['"']
        return [v for k, v in vocab.items() if v != quote_id]

    if ctx.state == JsonState.PARAM_NEXT:
        if len(ctx.params_done) != len(ctx.chosen_func.parameters):
            return [vocab[',']]
        return [vocab['}']]
            


def _update_state(
    ctx: GenerationContext,
    token_id: int,
    id_to_token: dict[int, str],
    model: Small_LLM_Model,
) -> None:
    """Met à jour le contexte après chaque token généré.

    Args:
        ctx: Contexte de génération (modifié en place).
        token_id: ID du token qui vient d'être généré.
        id_to_token: Table inverse ID -> token string.
        model: Instance du modèle (pour encoder les noms de paramètres).
    """
    token_str = id_to_token.get(token_id, "")

    if ctx.state == JsonState.NAME:
        ctx.tokens_so_far.append(token_id)
        for func_name, token_ids in ctx.func_tokens.items():
            if ctx.tokens_so_far == token_ids:
                ctx.chosen_func = next(
                    f for f in ctx.functions if f.name == func_name
                )
                ctx.state = JsonState.PARAM_KEY
                ctx.tokens_so_far = []
                return

    elif ctx.state == JsonState.PARAM_KEY:
        ctx.tokens_so_far.append(token_id)
        # Trouver le prochain paramètre attendu
        all_params = list(ctx.chosen_func.parameters.keys())
        remaining = [p for p in all_params if p not in ctx.params_done]
        if not remaining:
            return
        next_param = remaining[0]
        param_ids = model.encode(next_param)[0].tolist()
        # Nom complet ?
        if ctx.tokens_so_far == param_ids:
            ctx.current_param = next_param
            ctx.tokens_so_far = []
            ctx.state = JsonState.PARAM_VAL

    elif ctx.state == JsonState.PARAM_VAL:
        ptype = ctx.chosen_func.parameters[ctx.current_param].type
        if ptype == "string":
            # Le " ouvre la string → passer en IN_STRING
            ctx.state = JsonState.IN_STRING
        else:
            # number ou boolean → accumuler et détecter la fin
            ctx.current_value += token_str
            if token_str.strip() in (",", "}"):
                ctx.params_done.append(ctx.current_param)
                ctx.current_param = None
                ctx.current_value = ""
                ctx.state = JsonState.PARAM_NEXT

    elif ctx.state == JsonState.IN_STRING:
        # Le " fermant termine la string
        if token_str == '"':
            ctx.params_done.append(ctx.current_param)
            ctx.current_param = None
            ctx.current_value = ""
            ctx.state = JsonState.PARAM_NEXT

    elif ctx.state == JsonState.PARAM_NEXT:
        if token_str.strip() == ",":
            ctx.tokens_so_far = []
            ctx.state = JsonState.PARAM_KEY
        elif token_str.strip() == "}":
            ctx.state = JsonState.END
            
        


def apply_mask(logits: np.ndarray, allowed_ids: list[int]) -> np.ndarray:
    mask = np.full_like(logits, -np.inf)
    mask[allowed_ids] = 0
    return mask

def generate(model: Small_LLM_Model, context: GenerationContext) -> None:
    ...

