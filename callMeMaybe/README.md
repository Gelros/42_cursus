*This project has been created by guilacol*

# callMeMaybe

## Description

`callMeMaybe` is a function-calling pipeline that converts natural-language prompts into structured function-call objects.

The project reads:
- a list of available function definitions (`name`, `description`, `parameters`, `returns`),
- a list of prompts to process,

and produces:
- a JSON array of function-calling decisions with exactly:
  - `prompt`
  - `name`
  - `parameters`

The goal is to make outputs machine-usable, schema-aware, and robustly formatted.

## Instructions

### Requirements

- Python 3.10+
- `uv` for dependency management

### Install

```bash
make install
```

### Run

```bash
make run
```

or explicitly:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint
```

## Algorithm Explanation

The pipeline follows these steps:

1. **Load and validate input files**
   - Function definitions and prompts are read from JSON files.
   - Data is validated with Pydantic models.

2. **Function selection**
   - The model is used to score/select the target function name from the available set.

3. **Parameter construction**
   - Parameters are built according to the selected function schema.
   - Type consistency is enforced (`number`, `string`, `boolean`, etc.).

4. **Output generation**
   - For each prompt, a `FunctionCall` object is created.
   - All results are serialized to a valid JSON output file.

This design prioritizes schema compliance and robust output formatting.

## Design Decisions

- **Pydantic-first data layer**: strict schema validation for inputs and outputs.
- **Separated responsibilities**:
  - `models.py` for data contracts,
  - `loader.py` for I/O and serialization,
  - `generator.py` for function-call generation logic,
  - `__main__.py` for CLI orchestration.
- **Fail-fast error handling**: explicit exceptions with readable messages for malformed files and invalid states.

## Performance Analysis

- **Speed**: processing the provided test set is fast on standard hardware.
- **Reliability**:
  - output JSON remains parseable,
  - output objects keep required keys and expected structure.
- **Trade-off**:
  - with a small model, strict reliability may require additional constraints and deterministic safeguards around extraction/validation.

## Challenges Faced

- Preventing degenerate model outputs on small LLMs (repetitive tokens, unstable function choices).
- Keeping strong schema correctness while maintaining model-driven behavior.
- Handling environment/network constraints during model/tokenizer loading.

## Testing Strategy

- Run end-to-end generation on the full prompt set.
- Manually validate output file structure:
  - JSON validity,
  - required keys per item,
  - type consistency against function definitions.
- Re-run after every major change in `generator.py`.
- Use lint checks (`flake8`, `mypy`) to keep code quality stable.

## Example Usage

Input prompt:
- `"What is the sum of 2 and 3?"`

Expected output item shape:

```json
{
  "prompt": "What is the sum of 2 and 3?",
  "name": "fn_add_numbers",
  "parameters": {
    "a": 2.0,
    "b": 3.0
  }
}
```

## Resources

### Technical References

- [Transformers Documentation](https://huggingface.co/docs/transformers/index)
- [Hugging Face Hub Documentation](https://huggingface.co/docs/huggingface_hub/index)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [NumPy Documentation](https://numpy.org/doc/)

### AI Usage Disclosure

AI assistance was used for:
- architecture iteration and refactoring suggestions,
- debugging strategy proposals,
- documentation drafting support.

All generated suggestions were manually reviewed, adapted, and validated before integration.
