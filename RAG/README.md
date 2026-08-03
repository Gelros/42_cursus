*This project has been created as part of the 42 curriculum by guilacol.*

# RAG against the machine

A Retrieval-Augmented Generation (RAG) system that answers questions about the
**vLLM** codebase. It ingests the repository, indexes it with BM25, retrieves
the most relevant code/documentation chunks for a question, and generates a
grounded answer with the `Qwen/Qwen3-0.6B` language model.

---

## Description

Given a question such as *"How do I configure the OpenAI compatible server?"*,
the system:

1. **Retrieves** the most relevant chunks of the vLLM repository using BM25.
2. **Augments** the prompt with those chunks as context.
3. **Generates** a concise, source-grounded answer with Qwen3-0.6B.

It also evaluates retrieval quality with the **recall@k** metric against a
ground-truth dataset of annotated questions.

---

## Instructions

### Requirements

- **Python 3.10** (enforced by `pyproject.toml`).
- **[uv](https://docs.astral.sh/uv/)** as the package/project manager.

### Install

```bash
make install          # == uv sync
```

This creates a virtual environment and installs every dependency
(`pydantic`, `fire`, `tqdm`, `bm25s`, `transformers`, `torch`, ...).

### Data layout

The system expects the vLLM repository and the question datasets here
(not committed — generated/placed by the evaluator):

```
data/
├── raw/
│   └── vllm-0.10.1/                         # the repository to index
└── datasets/
    ├── AnsweredQuestions/                    # ground truth (with sources)
    │   ├── dataset_docs_public.json
    │   └── dataset_code_public.json
    └── UnansweredQuestions/                  # questions only (input)
        ├── dataset_docs_public.json
        └── dataset_code_public.json
```

### Full pipeline (copy/paste)

```bash
# 1. Build the index (default/recommended chunk size: 2000)
uv run python -m src index --max_chunk_size 2000

# 2. Ad-hoc search
uv run python -m src search "How to configure the OpenAI server?" --k 10

# 3. Batch search over a dataset of questions
uv run python -m src search_dataset \
    --dataset_path data/datasets/UnansweredQuestions/dataset_docs_public.json \
    --k 10 \
    --save_directory data/output/search_results

# 4. Evaluate retrieval against the ground truth
uv run python -m src evaluate \
    --student_answer_path data/output/search_results/dataset_docs_public.json \
    --dataset_path data/datasets/AnsweredQuestions/dataset_docs_public.json \
    --k 10

# 5. Answer a single question (loads Qwen3-0.6B, ~1.2 GB on first run)
uv run python -m src answer "How do I configure the OpenAI server?" --k 10

# 6. Generate answers for every question of a search-results file
uv run python -m src answer_dataset \
    --student_search_results_path data/output/search_results/dataset_docs_public.json \
    --save_directory data/output/search_results_and_answer
```

### Make targets

| Target          | Action                                              |
|-----------------|-----------------------------------------------------|
| `make install`  | Install dependencies with uv.                       |
| `make run`      | Run a sample search (`QUERY=...` `K=...` to override).|
| `make debug`    | Run the CLI under `pdb`.                             |
| `make lint`     | `flake8 .` + `mypy .` with the subject's flags.     |
| `make lint-strict` | `flake8 .` + `mypy . --strict`.                  |
| `make clean`    | Remove caches and Python artifacts.                 |

---

## System architecture

The pipeline is split into single-responsibility modules under `src/`:

```
src/
├── __main__.py    CLI (Python Fire): the 6 sub-commands. Pure orchestration.
├── models.py      Pydantic models (subject V.7) + the internal Chunk model.
├── chunking.py    walk_files + 3 chunkers + chunk_file dispatcher.
├── tokenizer.py   tokenize(): text -> tokens, shared by index and search.
├── indexer.py     build / save / load the BM25 index + search().
├── generator.py   QwenGenerator: load model once, answer(question, context).
└── evaluator.py   recall@k metric.
```

Data flow:

```
            INDEXING                                  QUERYING
 vllm repo --walk_files--> files                 question
            --chunk_file--> chunks                  |
            --build_index--> BM25 + chunks.json   --search--> chunk indices
            --save_index--> data/processed/          |
                                                   --lookup chunks.json--> MinimalSource
                                                     |
                                                   --QwenGenerator.answer--> answer
```

The CLI is invoked as `python -m src <command>` (the evaluation grid's
convention). `src/__main__.py` is the package entry point.

---

## Chunking strategy

The subject requires different strategies per file type (V.4). `chunk_file`
dispatches on the extension and enforces a configurable maximum chunk size
(default 2000):

- **Python (`.py`) — AST-based.** The file is parsed with the standard
  `ast` module; each top-level function / async function / class becomes one
  chunk. This keeps semantic units intact (a whole function rather than an
  arbitrary cut). On a `SyntaxError`, it falls back to fixed-window chunking.
- **Markdown (`.md`) — heading-based with merging.** The text is split on ATX
  headings (`#` … `######`), then consecutive sections are greedily merged up
  to `max_chunk_size`. Splitting on every heading alone yields many tiny
  chunks that align poorly with the reference source ranges (~1 kB on
  average); merging produces chunks close to that size and improved docs
  recall@5 from 0.77 to 0.80.
- **Fixed-window fallback.** A sliding window of `max_chunk_size` characters
  with a small overlap, used for any other file and to sub-chunk any
  oversized AST/Markdown chunk so the hard cap is always respected.

Every chunk records its `file_path` and exact `first/last_character_index`
**relative to the original file**, which is what the evaluation compares
against.

---

## Retrieval method

**BM25** (via the `bm25s` library). BM25 ranks each chunk by term frequency
(with saturation, parameter `k1`) and inverse document frequency, normalised
by document length (parameter `b`). Defaults `k1=1.5`, `b=0.75`.

Two implementation details matter:

- **Identifier-aware tokenization.** `tokenize()` splits `snake_case` and
  `camelCase` (`get_supported_mm_limits` → `get supported mm limits`) and
  lowercases everything. This lets a natural-language question match a code
  identifier — the single biggest lever for code recall.
- **Asymmetric stopword filtering.** The index keeps every token (correct IDF
  statistics), but **queries** drop grammatical stopwords (`how`, `what`,
  `the`, `is`, ...). Questions are verbose; removing this noise sharpens the
  ranking. This pushed docs recall@5 from 0.78 to 0.80.

The retriever stores only chunk *indices*; a parallel `chunks.json` maps each
index back to `(file_path, first_character_index, last_character_index)` so we
can emit the `MinimalSource` objects the subject requires.

---

## Performance analysis

Measured with the moulinette's IoU@0.05 metric, `max_chunk_size=2000`, on
Apple Silicon:

| Dataset | Recall@5 | Recall@10 | Threshold (R@5) |
|---------|----------|-----------|-----------------|
| docs    | **0.80** | 0.85      | 0.80 ✅         |
| code    | **0.54** | 0.67      | 0.50 ✅         |

Timings (largely below the subject's limits):

| Metric                          | Measured  | Subject limit |
|---------------------------------|-----------|---------------|
| Indexing (1926 files, 15k chunks) | ~5 s    | ≤ 5 min       |
| Cold start (model load)         | ~10–15 s  | ≤ 60 s        |
| Search throughput (200 queries) | < 2 s     | ≤ 90 s        |

**How recall is scored.** A retrieved source counts as a hit when its
character range overlaps a ground-truth range with Intersection-over-Union
> 0.05 (same file). This rewards chunks whose size is close to the reference
range — the reason markdown sections are merged toward `max_chunk_size`
rather than split at every heading.

---

## Design decisions

- **One unified index** for both code and docs, for simplicity. The subject
  allows separate indexes (V.8); that would add headroom on docs and is the
  natural next improvement.
- **Pydantic everywhere** for validation and for one-line JSON
  (de)serialization (`model_validate_json` / `model_dump_json`).
- **`QwenGenerator` is instantiated once** per command, never inside a loop —
  the ~10 s model load is paid a single time (respects the cold-start limit).
- **Deterministic generation** (`do_sample=False`) and **thinking mode
  disabled** (`enable_thinking=False`) so Qwen3 returns a concise,
  reproducible answer instead of a `<think>…</think>` reasoning trace.

---

## Challenges faced

- **Recall just under threshold.** Splitting markdown at every heading left
  docs recall@5 at ≈ 0.77: the tiny per-heading chunks overlapped the ~1 kB
  reference ranges too weakly under the IoU metric. Merging adjacent sections
  up to `max_chunk_size` (on top of identifier-aware tokenization and
  asymmetric query stopword filtering) brought it to 0.80.
- **Character indices after sub-chunking.** When an oversized chunk is split,
  the sub-chunk offsets are relative to the chunk, not the file. They are
  shifted by the parent chunk's start so the reported indices stay correct.
- **`transformers` typing friction.** `apply_chat_template`, `generate`, and
  `decode` are loosely typed; narrowed with `typing.cast` and one targeted
  `# type: ignore[misc]` so `mypy` passes with the subject's flags.

---

## Example usage

```bash
$ uv run python -m src search "How to configure the OpenAI server?" --k 3
{"file_path": "data/raw/vllm-0.10.1/docs/deployment/frameworks/dstack.md", ...}
{"file_path": "data/raw/vllm-0.10.1/docs/deployment/integrations/kubeai.md", ...}
{"file_path": "data/raw/vllm-0.10.1/docs/features/structured_outputs.md", ...}

$ uv run python -m src answer "How do I configure the OpenAI server?" --k 3
The OpenAI compatible server can be configured by appending the following to
your model arguments: `--quantization bitsandbytes`.

$ uv run python -m src evaluate \
    --student_answer_path data/output/search_results/dataset_docs_public.json \
    --dataset_path data/datasets/AnsweredQuestions/dataset_docs_public.json --k 10
{'Recall@1': 0.60, 'Recall@3': 0.72, 'Recall@5': 0.80, 'Recall@10': 0.85}
```

---

## Resources

- BM25 / Okapi BM25 — Robertson & Zaragoza, *The Probabilistic Relevance
  Framework: BM25 and Beyond*.
- [`bm25s`](https://github.com/xhluca/bm25s) — fast pure-Python BM25.
- [Hugging Face Transformers](https://huggingface.co/docs/transformers) and the
  [Qwen3](https://huggingface.co/Qwen/Qwen3-0.6B) model card.
- [Python Fire](https://github.com/google/python-fire) and
  [tqdm](https://github.com/tqdm/tqdm) documentation.

**Use of AI.** AI assistance was used as a tutor and reviewer, not a code
generator: to explain the underlying concepts (chunking, BM25, the Qwen
generation loop), to design the incremental exercises through which each
component was written and unit-tested, to review code for bugs and lint/type
issues, and to draft this README. Every component was implemented and is
understood by the author.
