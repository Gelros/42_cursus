"""Student CLI — `uv run python -m student <command>`.

Six sub-commands required by the subject (V.2.5):
    index            : build and persist the BM25 index from data/raw/vllm-0.10.1
    search           : run a single ad-hoc query
    search_dataset   : process every question in a JSON dataset
    answer           : answer a single question with retrieved context
    answer_dataset   : generate answers for every search result of a dataset
    evaluate         : recall@k of search results against ground truth

Default paths follow the subject's example (V.6.*):
    data/raw/vllm-0.10.1                    -> ingest from
    data/processed/bm25_index               -> index location
    data/output/search_results              -> search outputs
    data/output/search_results_and_answer   -> answer outputs
"""

from pathlib import Path

import fire
from tqdm import tqdm

from .chunking import chunk_file, walk_files
from .evaluator import mean_recall_at_k
from .generator import QwenGenerator
from .indexer import build_index, load_index, save_index, search
from .models import (
    AnsweredQuestion,
    Chunk,
    MinimalAnswer,
    MinimalSearchResults,
    MinimalSource,
    RagDataset,
    StudentSearchResults,
    StudentSearchResultsAndAnswer,
)


# Default paths from the subject.
RAW_DIR = Path("data/raw/vllm-0.10.1")
INDEX_DIR = Path("data/processed/bm25_index")


class Student:
    """RAG system over the vLLM codebase."""

    # ------------------------------------------------------------------
    # 1. index — build the BM25 index from the repo
    # ------------------------------------------------------------------
    def index(
        self,
        max_chunk_size: int = 2000,
        raw_dir: str = str(RAW_DIR),
        index_dir: str = str(INDEX_DIR),
    ) -> str:
        """Ingest the vLLM repo and persist a searchable BM25 index.

        Steps:
            1. List every .py and .md file under `raw_dir`.
            2. Chunk each file with chunk_file (dispatched by extension).
            3. Build the BM25 index on the chunk texts.
            4. Save (retriever + chunks) under `index_dir`.
        """
        raw = Path(raw_dir)
        out = Path(index_dir)
        files = walk_files(raw, (".py", ".md"))
        chunks: list[Chunk] = []

        for f in tqdm(files, desc="Chunking", unit="file"):
            chunks.extend(chunk_file(f, max_chunk_size=max_chunk_size))

        retriever = build_index(chunks)
        save_index(retriever, chunks, out)

        return f"Indexed {len(chunks)} chunks from {len(files)} files -> {out}"

    # ------------------------------------------------------------------
    # 2. search — single query
    # ------------------------------------------------------------------
    def search(
        self,
        query: str,
        k: int = 10,
        index_dir: str = str(INDEX_DIR),
    ) -> list[dict]:
        """Return the top-k MinimalSource matches for `query`."""
        retriever, chunks = load_index(Path(index_dir))
        hits = search(retriever, query, k=k)

        sources = [
            MinimalSource(
                file_path=chunks[i].file_path,
                first_character_index=chunks[i].first_character_index,
                last_character_index=chunks[i].last_character_index,
            )
            for i, _ in hits
        ]

        return [s.model_dump() for s in sources]

    # ------------------------------------------------------------------
    # 3. search_dataset — batch over a JSON of questions
    # ------------------------------------------------------------------
    def search_dataset(
        self,
        dataset_path: str,
        k: int = 10,
        save_directory: str = "data/output/search_results",
        index_dir: str = str(INDEX_DIR),
    ) -> str:
        """Run search() on every question of a dataset, write a JSON output."""
        ds = RagDataset.model_validate_json(Path(dataset_path).read_text())
        retriever, chunks = load_index(Path(index_dir))

        results: list[MinimalSearchResults] = []
        for q in tqdm(ds.rag_questions, desc="Searching"):
            hits = search(retriever, q.question, k=k)
            sources = [
                MinimalSource(
                    file_path=chunks[i].file_path,
                    first_character_index=chunks[i].first_character_index,
                    last_character_index=chunks[i].last_character_index,
                )
                for i, _ in hits
            ]
            results.append(
                MinimalSearchResults(
                    question_id=q.question_id,
                    question=q.question,
                    retrieved_sources=sources,
                )
            )

        payload = StudentSearchResults(search_results=results, k=k)
        out = Path(save_directory)
        out.mkdir(parents=True, exist_ok=True)
        out_path = out / Path(dataset_path).name
        out_path.write_text(payload.model_dump_json(indent=2))

        return f"Saved student_search_results to {out_path}"

    # ------------------------------------------------------------------
    # 4. answer — single question + generation
    # ------------------------------------------------------------------
    def answer(
        self,
        question: str,
        k: int = 10,
        index_dir: str = str(INDEX_DIR),
        max_new_tokens: int = 128,
    ) -> str:
        """Answer one question by retrieving k chunks and feeding Qwen."""
        retriever, chunks = load_index(Path(index_dir))
        hits = search(retriever, question, k=k)
        context = "\n\n---\n\n".join(chunks[i].text for i, _ in hits)
        gen = QwenGenerator()

        return gen.answer(question, context, max_new_tokens=max_new_tokens)

    # ------------------------------------------------------------------
    # 5. answer_dataset — generate for every search result
    # ------------------------------------------------------------------
    def answer_dataset(
        self,
        student_search_results_path: str,
        save_directory: str = "data/output/search_results_and_answer",
        index_dir: str = str(INDEX_DIR),
        max_new_tokens: int = 128,
    ) -> str:
        """For each MinimalSearchResults entry, generate an answer with Qwen."""
        raw = Path(student_search_results_path).read_text()
        sr = StudentSearchResults.model_validate_json(raw)
        _, chunks = load_index(Path(index_dir))

        by_key = {
            (c.file_path, c.first_character_index, c.last_character_index): c
            for c in chunks
        }

        gen = QwenGenerator()
        answers: list[MinimalAnswer] = []
        for r in tqdm(sr.search_results, desc="Answering"):
            context_texts = [
                by_key[key].text
                for s in r.retrieved_sources
                for key in [(
                    s.file_path,
                    s.first_character_index,
                    s.last_character_index,
                )]
                if key in by_key
            ]
            context = "\n\n---\n\n".join(context_texts)
            ans = gen.answer(r.question, context, max_new_tokens=max_new_tokens)
            answers.append(
                MinimalAnswer(
                    question_id=r.question_id,
                    question=r.question,
                    retrieved_sources=r.retrieved_sources,
                    answer=ans,
                )
            )

        payload = StudentSearchResultsAndAnswer(search_results=answers, k=sr.k)
        out = Path(save_directory)
        out.mkdir(parents=True, exist_ok=True)
        out_path = out / Path(student_search_results_path).name
        out_path.write_text(payload.model_dump_json(indent=2))

        return f"Saved student_search_results_and_answer to {out_path}"

    # ------------------------------------------------------------------
    # 6. evaluate — recall@k of student results vs ground truth
    # ------------------------------------------------------------------
    def evaluate(
        self,
        student_answer_path: str,
        dataset_path: str,
        k: int = 10,
        max_context_length: int = 2000,
    ) -> dict:
        """Compute Recall@{1,3,5,10} on a (predictions, ground-truth) pair."""
        sr = StudentSearchResults.model_validate_json(
            Path(student_answer_path).read_text()
        )
        ds = RagDataset.model_validate_json(Path(dataset_path).read_text())

        gold_by_id = {
            q.question_id: q.sources
            for q in ds.rag_questions
            if isinstance(q, AnsweredQuestion)
        }
        pairs = [
            (gold_by_id[r.question_id], r.retrieved_sources)
            for r in sr.search_results
            if r.question_id in gold_by_id
        ]

        return {
            "Recall@1": mean_recall_at_k(pairs, k=1),
            "Recall@3": mean_recall_at_k(pairs, k=3),
            "Recall@5": mean_recall_at_k(pairs, k=5),
            "Recall@10": mean_recall_at_k(pairs, k=10),
        }


def main() -> None:
    """Entry point: Fire exposes every Student method as a sub-command."""
    fire.Fire(Student)


if __name__ == "__main__":
    main()
