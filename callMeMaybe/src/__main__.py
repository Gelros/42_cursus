from llm_sdk import Small_LLM_Model
import json
import numpy as np
from src.models import load_functions_def


def main():
    model = Small_LLM_Model()
    
    print(load_functions_def("data/input/functions_definition.json"))


if __name__ == "__main__":
    main()
