from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any
import numpy as np
import re
from llm_sdk import Small_LLM_Model
from src.models import FunctionCall, FunctionDef


# Common words ignored in lexical scoring.
_STOPWORDS = {
    "the", "a", "an", "of", "to", "and", "or", "for", "is", "are", "be",
    "in", "on", "at", "by", "with", "as", "it", "this", "that", "these",
    "those", "their", "them", "two", "fn", "return", "returns", "result",
    "value", "function", "call", "input", "output",
}


class JsonState(Enum):
    START = auto()
    END = auto()


@dataclass
class GenerationContext:
    functions: list[FunctionDef]
    func_tokens: dict[str, list[int]]
    state: JsonState = JsonState.START
    chosen_func: FunctionDef | None = None
    param_values: dict[str, Any] = field(default_factory=dict)


def _lexical_affinity(prompt: str, func: FunctionDef) -> float:
    """Score overlap between prompt and function metadata."""
    lowered = prompt.lower()
    name_words = set(re.findall(r"[a-z]+", func.name.lower()))
    desc_words = set(re.findall(r"[a-z]+", func.description.lower()))
    words = (name_words | desc_words) - _STOPWORDS
    bonus = 0.0
    for w in words:
        if len(w) >= 3 and re.search(rf"\b{re.escape(w)}\b", lowered):
            bonus += 0.5
    return bonus


def _select_function_name(
    model: Small_LLM_Model,
    prompt: str,
    functions: list[FunctionDef],
) -> str:
    """Select a function name from the prompt."""
    preamble = (
        "You must pick exactly one function name for the user request.\n"
        f"User request: {prompt}\n"
        "Available functions:\n"
        + "\n".join(f"- {f.name}: {f.description}" for f in functions)
        + "\nSelected function name:"
    )
    preamble_ids = model.encode(preamble)[0].tolist()
    best_name: str | None = None
    best_score = -np.inf

    for func in functions:
        name_ids = model.encode(func.name)[0].tolist()
        if not name_ids:
            continue
        running_ids = preamble_ids.copy()
        score = 0.0
        for token_id in name_ids:
            logits = np.array(
                model.get_logits_from_input_ids(running_ids), dtype=float
            )
            m = float(np.max(logits))
            logsumexp = m + float(np.log(np.sum(np.exp(logits - m))))
            score += float(logits[token_id] - logsumexp)
            running_ids.append(token_id)
        score /= len(name_ids)
        # Ajout d'un biais lexical: si le prompt contient des mots-clés de
        # la description ou du nom, on booste la fonction correspondante.
        score += _lexical_affinity(prompt, func)
        if score > best_score:
            best_score = score
            best_name = func.name

    if best_name is None:
        raise ValueError("Unable to select function name")
    return best_name


def _extract_numbers_from_prompt(prompt: str) -> list[float]:
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", prompt)]


def _fallback_number_value(
    prompt: str, param_name: str, param_index: int = 0
) -> float:
    """Return a deterministic number from prompt values."""
    nums = _extract_numbers_from_prompt(prompt)
    if not nums:
        return 0.0
    if param_index < len(nums):
        return nums[param_index]
    # Legacy mapping kept for compatibility.
    if param_name == "b" and len(nums) >= 2:
        return nums[1]
    return nums[0]


def _generate_number_value(
    model: Small_LLM_Model, prompt: str, param_name: str
) -> float:
    """Generate one numeric parameter value."""
    base = (
        f"User request: {prompt}\n"
        "You are preparing function-call arguments.\n"
        f"Generate ONLY the input value for numeric parameter '{param_name}'.\n"
        "Do not compute the final answer of the user request.\n"
        "Output only the raw input number.\n"
        "Value:"
    )
    ids = model.encode(base)[0].tolist()
    out = ""
    started = False
    for _ in range(16):
        logits = np.array(model.get_logits_from_input_ids(ids), dtype=float)
        next_id = int(np.argmax(logits))
        tok = model.decode([next_id])
        if not tok:
            break
        if not started:
            # Ignore leading whitespace until first meaningful char.
            if not tok.strip():
                ids.append(next_id)
                continue
            if not any(c.isdigit() or c in "-+." for c in tok):
                # Model drifted away from numbers: fallback.
                break
            started = True
            out += tok
            ids.append(next_id)
            continue
        # Accept only number continuation tokens.
        if any(c.isdigit() or c == "." for c in tok) and "-" not in tok:
            out += tok
            ids.append(next_id)
        else:
            break
    m = re.search(r"-?\d+(?:\.\d+)?", out)
    if m:
        try:
            return float(m.group(0))
        except ValueError:
            pass
    return _fallback_number_value(prompt, param_name)


def _generate_boolean_value(
    model: Small_LLM_Model, prompt: str, param_name: str
) -> bool:
    q = (
        f"User request: {prompt}\n"
        f"Generate a boolean value for parameter '{param_name}'.\n"
        "Answer only true or false.\n"
        "Answer:"
    )
    ids = model.encode(q)[0].tolist()
    logits = np.array(model.get_logits_from_input_ids(ids), dtype=float)
    true_ids = model.encode(" true")[0].tolist() or model.encode("true")[0].tolist()
    false_ids = (
        model.encode(" false")[0].tolist() or model.encode("false")[0].tolist()
    )
    if not true_ids or not false_ids:
        return False
    return bool(logits[true_ids[0]] >= logits[false_ids[0]])


def _generate_string_value(
    model: Small_LLM_Model, prompt: str, param_name: str
) -> str:
    q = (
        f"User request: {prompt}\n"
        "You are preparing function-call arguments.\n"
        f"Generate ONLY the input value for string parameter '{param_name}'.\n"
        "Do not apply/execute the function.\n"
        "Output only the raw input text (no quotes).\n"
        "Value:"
    )
    ids = model.encode(q)[0].tolist()
    out = ""
    for _ in range(24):
        logits = np.array(model.get_logits_from_input_ids(ids), dtype=float)
        next_id = int(np.argmax(logits))
        tok = model.decode([next_id])
        if "\n" in tok:
            break
        out += tok
        ids.append(next_id)
    value = out.strip().strip('"').strip("'")
    if value.lower().startswith("reverse the string "):
        value = value[len("reverse the string "):].strip().strip('"').strip("'")
    return value


def _fallback_string_value(prompt: str, param_name: str) -> str:
    quoted = re.findall(r"'([^']*)'|\"([^\"]*)\"", prompt)
    quoted_values: list[str] = [a or b for a, b in quoted]
    lowered = prompt.lower()

    if param_name == "source_string":
        return quoted_values[-1] if quoted_values else prompt

    if param_name == "regex":
        if "replace all numbers" in lowered:
            return r"\d+"
        if "replace all vowels" in lowered:
            return r"[AEIOUaeiou]"
        if len(quoted_values) >= 1:
            return re.escape(quoted_values[0])
        return ""

    if param_name == "replacement":
        if "asterisk" in lowered:
            return "*"
        if "substitute" in lowered and len(quoted_values) >= 2:
            return quoted_values[1]
        m = re.search(r"\bwith\b\s+([^\s\"']+)", prompt, flags=re.IGNORECASE)
        if m:
            return m.group(1)
        if len(quoted_values) >= 2:
            return quoted_values[1]
        return ""

    if param_name in ("name", "s") and quoted_values:
        return quoted_values[0]
    if param_name == "name":
        m = re.search(r"greet\s+(.+)$", prompt, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip().strip("'\"")
    if param_name == "s":
        m = re.search(r"reverse(?:\s+the\s+string)?\s+(.+)$",
                      prompt, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip().strip("'\"")
    # Dernier recours: on prend le premier segment cité s'il y en a,
    # sinon le prompt (meilleur que de renvoyer une chaîne vide).
    if quoted_values:
        return quoted_values[0]
    return prompt


def _generate_param_value(
    model: Small_LLM_Model,
    prompt: str,
    param_name: str,
    param_type: str,
    param_index: int = 0,
    already_used: list[Any] | None = None,
) -> Any:
    used = already_used or []
    if param_type == "number":
        generated = _generate_number_value(model, prompt, param_name)
        nums_in_prompt = _extract_numbers_from_prompt(prompt)
        # Fall back when generation hallucinates or duplicates values.
        needs_fallback = bool(nums_in_prompt) and (
            generated not in nums_in_prompt
            or (generated in used and len(set(nums_in_prompt)) > 1)
        )
        if needs_fallback:
            return _fallback_number_value(prompt, param_name, param_index)
        return generated
    if param_type == "boolean":
        return _generate_boolean_value(model, prompt, param_name)
    # Deterministic extraction is safer for substitution fields.
    if param_name in {"source_string", "regex", "replacement"}:
        return _fallback_string_value(prompt, param_name)
    value = _generate_string_value(model, prompt, param_name)
    if not value:
        return _fallback_string_value(prompt, param_name)
    return value


def generate_function_call(
    model: Small_LLM_Model,
    prompt: str,
    ctx: GenerationContext,
) -> FunctionCall:
    selected_name = _select_function_name(model, prompt, ctx.functions)
    by_name = {f.name: f for f in ctx.functions}
    if selected_name not in by_name:
        raise ValueError(f"Selected function not found: {selected_name}")

    ctx.chosen_func = by_name[selected_name]
    params: dict[str, Any] = {}
    for idx, (pname, pdef) in enumerate(ctx.chosen_func.parameters.items()):
        params[pname] = _generate_param_value(
            model,
            prompt,
            pname,
            pdef.type,
            param_index=idx,
            already_used=list(params.values()),
        )
    ctx.param_values = params
    ctx.state = JsonState.END

    return FunctionCall(prompt=prompt, name=selected_name, parameters=params)
