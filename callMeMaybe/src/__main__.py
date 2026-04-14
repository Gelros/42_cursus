import numpy as np
from src.models import FunctionCall
from pathlib import Path
from src.vocabulary import load_vocab, id_to_tokens, pre_calc_name_func
from src.loader import load_functions_def, load_tests_prompt
from llm_sdk import Small_LLM_Model
from src.generator import GenerationContext, JsonState, generate_function_call
import random


def main():
    model = Small_LLM_Model()
    functions_def = load_functions_def("data/input/functions_definition.json")
    load_tests_prompt("data/input/function_calling_tests.json")
    vocab = load_vocab(model)
    ctx = GenerationContext(
        state=JsonState.START,
        functions=functions_def,
        func_tokens=pre_calc_name_func(functions_def, model),
        chosen_func=None,
        params_done=[],
        tokens_so_far=[],
        current_param=None
    )
    generate_function_call(model, "What is the sum of 2 and 3?", ctx, vocab)

        
        

if __name__ == "__main__":
    main()
