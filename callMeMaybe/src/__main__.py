from llm_sdk import Small_LLM_Model
import json
import numpy as np


def main():
    model = Small_LLM_Model()
    input_ids = model.encode('What is the sum of 2 and 3?')[0].tolist()
    get_logits = model.get_logits_from_input_ids(input_ids)

    print()
    print("Ids = ", input_ids)
    print("Logits = ", get_logits)
    print()


if __name__ == "__main__":
    main()
