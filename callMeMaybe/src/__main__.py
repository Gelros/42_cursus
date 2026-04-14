import argparse
from src.models import FunctionCall
from src.vocabulary import pre_calc_name_func
from src.loader import load_functions_def, load_tests_prompt, save_results_in_json
from llm_sdk import Small_LLM_Model
from src.generator import GenerationContext, generate_function_call


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate function calls from prompts."
    )
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
    )
    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json",
    )
    parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json",
    )
    args = parser.parse_args()

    functions_def = load_functions_def(args.functions_definition)
    tests = load_tests_prompt(args.input)
    model = Small_LLM_Model()
    func_tokens = pre_calc_name_func(functions_def, model)

    results: list[FunctionCall] = []

    for test in tests:
        ctx = GenerationContext(
            functions=functions_def,
            func_tokens=func_tokens,
        )
        results.append(generate_function_call(model, test.prompt, ctx))

    save_results_in_json(results, args.output)
    print(f"Saved {len(results)} function calls to {args.output}")


if __name__ == "__main__":
    main()
