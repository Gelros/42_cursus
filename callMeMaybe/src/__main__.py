import numpy as np
from src.models import FunctionCall
from pathlib import Path
from src.vocabulary import load_vocab, id_to_tokens, pre_calc_name_func
from src.loader import load_functions_def, load_tests_prompt
from llm_sdk import Small_LLM_Model
from src.generator import GenerationContext, JsonState, get_valid_tokens
import random


def main():
    model = Small_LLM_Model()
    functions_def = load_functions_def("data/input/functions_definition.json")
    load_tests_prompt("data/input/function_calling_tests.json")
    vocab = load_vocab(model)
    ctx = GenerationContext(
        state=JsonState.NAME,
        functions=functions_def,
        func_tokens=pre_calc_name_func(functions_def, model),
        chosen_func=None,
        params_done=[],
        tokens_so_far=[8822],
        current_param=None
    )
    ctx.tokens_so_far = ctx.tokens_so_far + get_valid_tokens(ctx, vocab, model)
    print(model.decode(ctx.tokens_so_far))
        
        

if __name__ == "__main__":
    main()
