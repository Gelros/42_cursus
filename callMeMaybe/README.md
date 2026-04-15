*This project has been created as part of the 42 curriculum by guilacol.*

# callMeMaybe

## Description

**callMeMaybe** is an introduction to **function calling** with a small local
LLM. The program reads natural-language prompts and turns each one into a
structured JSON function call that a computer can execute directly, instead of
returning a free-form sentence.

Example:

```
User: "What is the sum of 2 and 3?"
Output: {"name": "fn_add_numbers", "parameters": {"a": 2.0, "b": 3.0}}
```

The project uses **Qwen/Qwen3-0.6B** as the base model through the
provided `llm_sdk` wrapper. Because a 0.6B-parameter model is unreliable at
spontaneously producing valid JSON, the pipeline does not trust the model's
free generation: it **guides** the model with a constrained decoding strategy
that (a) scores each candidate function name token-by-token and (b) restricts
parameter generation to tokens that remain consistent with the target JSON
schema.

Input files:

- `data/input/functions_definition.json` — list of callable functions (name,
  description, typed parameters, return type).
- `data/input/function_calling_tests.json` — list of prompts to process.

Output file:

- `data/output/function_calling_results.json` — an array of objects with keys
  `prompt`, `name`, `parameters`. It is always valid JSON.

## Instructions

### Requirements

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) as the package manager

### Install

```bash
make install     # equivalent to: uv sync
```

`uv sync` installs every dependency listed in `pyproject.toml` into a local
`.venv/` (numpy, pydantic, and the dependencies needed by `llm_sdk`).
The first run will also download the Qwen3-0.6B weights from HuggingFace.

### Run

Default paths (reads from `data/input/`, writes to `data/output/`):

```bash
make run
```

Custom paths:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

### Debug

```bash
make debug        # runs the entry point through pdb
```

### Lint and type-check

```bash
make lint         # flake8 + mypy (subject-mandated flags)
make lint-strict  # flake8 + mypy --strict (optional, stricter)
```

### Clean

```bash
make clean        # remove __pycache__, .mypy_cache, *.pyc
make fclean       # clean + remove .venv, uv.lock, data/output
make re           # fclean + install
```

## Algorithm explanation

The program is a two-stage constrained-decoding pipeline. For every prompt
we successively (1) pick a function, then (2) fill its parameters — each step
is narrowed to a set of tokens that keeps the output schema-valid.

### Stage 1 — Function selection by teacher-forced scoring

Instead of asking the model to "guess" the function name (which a small LLM
often gets wrong), we **score every candidate name** against the prompt:

1. Build a preamble that exposes the user request and lists every available
   function name + description.
2. For each candidate function, compute the log-probability of its tokenized
   name given the preamble:
   - feed the prefix to the LLM to obtain the next-token logits,
   - apply the numerically stable `log-sum-exp` trick to get
     `log_softmax`,
   - append the next target token, repeat until the whole name has been
     consumed, and sum the per-token log-probabilities.
3. Normalize by the length of the name so that short names don't get an
   unfair advantage.
4. Add a small **lexical-affinity bonus** (+0.5 per matching content word
   between the prompt and the name/description, stopwords removed). This
   disambiguates cases where the raw LLM score is too flat to pick a clear
   winner — for example, "Sum of -7 and 8" against `fn_add_numbers`.
5. The function with the highest adjusted score wins.

The search space is closed (we never invent a name): the selected value is
guaranteed to be a valid function name from `functions_definition.json`.

### Stage 2 — Parameter generation, typed and guarded

Once the function is chosen, each of its parameters is generated
**individually**, dispatched by its declared type:

- **number**: greedy decoding with a small state machine that accepts a
  leading sign, digits, and an optional decimal part. The output is parsed by
  the regex `-?\d+(?:\.\d+)?`. If the generated value is not found in the
  original prompt, or if it has already been used by a previous parameter
  while other numbers remain available, the pipeline falls back to an
  **ordered extraction**: the i-th parameter takes the i-th number that
  appears in the prompt.
- **boolean**: we read the two next-token logits for `" true"` and
  `" false"` and keep the higher one. No sampling is involved.
- **string**: either greedy decoding until a newline, or direct deterministic
  extraction (`source_string`, `regex`, `replacement`, and typical
  `greet`/`reverse the string` cases). Determinism is more reliable than
  free generation for these parameters.

Every parameter is stored in the final `FunctionCall` Pydantic model, which
re-validates the schema before it is serialized. If validation fails,
the program reports it loudly rather than emitting bad JSON.

### Why constrained decoding matters

Qwen3-0.6B can barely produce syntactically correct JSON on its own. By
never asking the model for a raw JSON blob and by steering each decision
through a closed set of valid outputs, the pipeline is guaranteed to produce
schema-compliant JSON for every prompt.

## Design decisions

- **Strict module separation.** `models.py` (schemas), `loader.py` (I/O +
  validation), `vocabulary.py` (tokenizer pre-compute), `generator.py`
  (decoding logic), `__main__.py` (CLI orchestration). Each file is short
  and single-purpose, which makes peer review easier.
- **Pydantic 2 as first line of defense.** All inputs and the final
  `FunctionCall` are validated by Pydantic models (`min_length=1` on the
  function name, typed parameter dict). Malformed JSON never reaches the
  generator.
- **LLM for the decision, regex for the extraction.** The subject forbids
  heuristics for function selection; for parameter filling, however,
  deterministic extractors are much more reliable than free generation on a
  0.6B model. The rule across the codebase is: generate with the LLM, validate
  with regex, fall back if in doubt.
- **Token-ID caching.** `vocabulary.pre_calc_name_func` tokenizes every
  function name once at start-up, avoiding redundant tokenizer calls during
  scoring.
- **Log-sum-exp for numerical stability.** Every softmax-like computation on
  logits is implemented via `logsumexp` to avoid overflow on large logits.
- **No private API access.** The code only uses the public methods of
  `llm_sdk` (`encode`, `decode`, `get_logits_from_input_ids`).
- **Modern typing.** PEP 604 (`X | None`) and PEP 585
  (`list[...]`, `dict[...]`) are used everywhere; `mypy` passes with the
  subject-mandated flags.

## Performance analysis

- **Accuracy.** On the provided examples (sum, greet, reverse, square root,
  regex substitution) the pipeline selects the correct function and
  extracts the correct parameters. Tricky cases that caused historical
  regressions (`"What is the sum of 265 and 345?"`, `"Add -3.5 and 2.5"`,
  `"Sum of -7 and 8"`) are specifically guarded.
- **Reliability.** Output is 100% valid JSON: it goes through
  `json.dumps` after Pydantic validation, and the function name is always
  taken from the closed set of declared functions. There is no failure path
  that could emit a trailing comma, a missing key, or a wrong type.
- **Speed.** Most of the wall-clock time is the first model load
  (download + tokenizer). Per-prompt processing is a handful of forward
  passes and finishes in the single-digit seconds on CPU/MPS, well under
  the 5-minute target on the provided test set.

## Challenges faced

- **Decimal numbers being truncated.** Early versions of the numeric decoder
  stopped at the first non-alphanumeric token, so `-3.5` came out as `-3`.
  Fixed with a tiny state machine (whitespace → sign/digit → digits/dot →
  stop) and a final `re.search` parse.
- **Same number used twice.** On `"What is the sum of 265 and 345?"`, the
  LLM was returning the first number for both `a` and `b`. Fixed by
  tracking already-used values per function call and falling back to a
  positional extraction (`a` → 1st number, `b` → 2nd number) when a
  collision is detected.
- **Weak function discrimination on short prompts.** On `"Sum of -7 and 8"`
  the LLM score was quasi-flat between `fn_add_numbers` and
  `fn_substitute_string_with_regex`. Fixed by adding a lexical-affinity
  bonus based on prompt↔name/description word overlap.
- **Fallback trigger too narrow.** The initial fallback only fired when the
  generated value was exactly `0.0`. Widened to "value not in the prompt
  numbers" or "value already used", which correctly catches hallucinations
  without over-triggering.
- **`mypy --strict` vs. `llm_sdk`.** Some calls into the SDK expose untyped
  objects; resolved with targeted `# type: ignore[...]` comments rather
  than loosening project-wide settings.

## Testing strategy

- **Manual end-to-end runs.** `make run` against
  `data/input/function_calling_tests.json`, followed by a visual check of
  `data/output/function_calling_results.json` to confirm that each prompt
  maps to the right function and the right parameters.
- **Edge-case prompts.** Negative numbers, decimals, repeated numbers,
  single-number prompts (`square root`), quoted strings (`reverse`,
  `regex substitution`), words that overlap with multiple descriptions.
- **Input validation tests.** Missing file → `FileNotFoundError`,
  malformed JSON → `ValueError`, wrong schema → Pydantic `ValidationError`.
  None of these crash the program with a raw traceback: each produces a
  clear message.
- **Static checks.** `make lint` (flake8 + mypy with the mandatory flags)
  and `make lint-strict` (mypy `--strict`) are both clean.

## Example usage

```bash
make install
make run
cat data/output/function_calling_results.json
```

Representative output:

```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": { "a": 2.0, "b": 3.0 }
  },
  {
    "prompt": "What is the sum of 265 and 345?",
    "name": "fn_add_numbers",
    "parameters": { "a": 265.0, "b": 345.0 }
  },
  {
    "prompt": "Greet shrek",
    "name": "fn_greet",
    "parameters": { "name": "shrek" }
  },
  {
    "prompt": "Reverse the string 'hello'",
    "name": "fn_reverse_string",
    "parameters": { "s": "hello" }
  }
]
```

## Project layout

```
callMeMaybe/
├── Makefile                 # install / run / debug / lint / clean / fclean
├── pyproject.toml           # uv project + mypy config
├── README.md                # this file
├── SOUTENANCE.md            # defense notes (French)
├── cours/                   # companion course PDFs
├── data/
│   └── input/
│       ├── functions_definition.json
│       └── function_calling_tests.json
├── llm_sdk/
│   └── __init__.py          # Small_LLM_Model wrapper (provided)
└── src/
    ├── __main__.py          # CLI entry point
    ├── models.py            # Pydantic schemas
    ├── loader.py            # JSON I/O + validation
    ├── vocabulary.py        # tokenizer pre-compute
    └── generator.py         # scoring + constrained decoding
```

## Resources

Classic references on function calling, LLMs, and constrained decoding:

- **OpenAI — Function calling guide**:
  https://platform.openai.com/docs/guides/function-calling
- **HuggingFace — Transformers documentation**:
  https://huggingface.co/docs/transformers
- **Qwen3 model card**: https://huggingface.co/Qwen/Qwen3-0.6B
- **Pydantic v2**: https://docs.pydantic.dev/
- **NumPy**: https://numpy.org/doc/
- **uv**: https://docs.astral.sh/uv/
- **Log-sum-exp** (numerical stability):
  https://en.wikipedia.org/wiki/LogSumExp
- **BPE tokenization** — Sennrich et al., 2016, *"Neural Machine Translation
  of Rare Words with Subword Units"*
- **Outlines / constrained decoding** (for context only; not used here):
  https://github.com/dottxt-ai/outlines

### How AI was used

AI assistants (Claude, ChatGPT) were used throughout the project, always
under human review and with every generated line re-read, tested, and
adapted. Specifically:

- **Design exploration.** Brainstorming the overall pipeline
  (scoring by log-likelihood vs. free generation, where to place the
  regex fallbacks, how to handle the decimal-truncation bug).
- **Debugging.** Narrowing down edge cases such as the `a == b` bug on
  `"sum of 265 and 345"` and the decimal-truncation bug on `-3.5`.
- **Documentation.** Drafting this README, the companion course PDFs in
  `cours/`, and `SOUTENANCE.md`.
- **Refactoring hints.** Suggestions around Pydantic validators, modern
  Python type hints, `mypy --strict` compliance.

AI was **not** used as a black box: every algorithmic choice (constrained
decoding, teacher-forced scoring, lexical-affinity bonus, ordered-fallback
rule) is one I can explain and defend during the peer review.
