"""BM25 index + metadata persistence.

The bm25s retriever knows only chunk INDICES; it cannot reconstruct
`MinimalSource` results on its own. We therefore persist the list of
`Chunk` in a JSON file next to the index, and reload them together.
"""

import json
from pathlib import Path

import bm25s

from .models import Chunk
from .tokenizer import QUERY_STOPWORDS, tokenize


# ----------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------

def build_index(chunks: list[Chunk]) -> bm25s.BM25:
    """Tokenize every chunk and build the BM25 index."""
    if not chunks:
        raise ValueError("Empty chunks list — nothing to index.")
    corpus_tokens = [tokenize(c.text) for c in chunks]
    retriever = bm25s.BM25()
    retriever.index(corpus_tokens, show_progress=False)
    return retriever


# ----------------------------------------------------------------------
# Save / load
# ----------------------------------------------------------------------

CHUNKS_FILENAME = "chunks.json"


def save_index(
    retriever: bm25s.BM25,
    chunks: list[Chunk],
    index_dir: Path,
) -> None:
    """Persist both the BM25 retriever and the chunk metadata.

    Layout :
        <index_dir>/
          ├── data.csc.index.npy   (bm25s internals)
          ├── ...
          └── chunks.json           (list of Chunk dumps, one entry per
                                     indexed chunk, in the same order)
    """
    index_dir.mkdir(parents=True, exist_ok=True)
    retriever.save(str(index_dir))
    with open(index_dir / CHUNKS_FILENAME, "w", encoding="utf-8") as f:
        json.dump([c.model_dump() for c in chunks], f)


def load_index(index_dir: Path) -> tuple[bm25s.BM25, list[Chunk]]:
    """Reload a previously saved (retriever, chunks) pair."""
    retriever = bm25s.BM25.load(str(index_dir), load_corpus=False)
    with open(index_dir / CHUNKS_FILENAME, "r", encoding="utf-8") as f:
        chunks = [Chunk(**d) for d in json.load(f)]
    return retriever, chunks


# ----------------------------------------------------------------------
# Search
# ----------------------------------------------------------------------

def search(
    retriever: bm25s.BM25,
    query: str,
    k: int = 10,
) -> list[tuple[int, float]]:
    """Return up to k (chunk_index, score) tuples, sorted by score desc."""
    if k <= 0:
        return []

    # Asymmetric tokenization: drop stopwords from the query only.
    query_tokens = tokenize(query, stopwords=QUERY_STOPWORDS)
    if not query_tokens:
        return []

    k = min(k, retriever.scores["num_docs"])
    indices, scores = retriever.retrieve(
        [query_tokens], k=k, show_progress=False,
    )

    return [(int(i), float(s)) for i, s in zip(indices[0], scores[0])]
