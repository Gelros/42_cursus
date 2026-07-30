"""Recall@k evaluation metric (subject VI.1)."""

from .models import MinimalSource


def overlap_chars(a: MinimalSource, b: MinimalSource) -> int:
    """Number of characters shared by two sources (0 if disjoint or different files)."""
    if a.file_path != b.file_path:
        return 0
    overlap_start = max(a.first_character_index, b.first_character_index)
    overlap_end = min(a.last_character_index, b.last_character_index)
    overlap = overlap_end - overlap_start
    return overlap if overlap > 0 else 0


def is_found(
    gold: MinimalSource,
    retrieved: list[MinimalSource],
    threshold: float = 0.05,
) -> bool:
    """True if any retrieved source covers `gold` at >= `threshold` ratio."""
    gold_size = gold.last_character_index - gold.first_character_index
    if gold_size <= 0:
        return False
    for r in retrieved:
        if overlap_chars(gold, r) / gold_size >= threshold:
            return True
    return False


def recall_at_k(
    gold_sources: list[MinimalSource],
    retrieved_sources: list[MinimalSource],
    k: int,
    threshold: float = 0.05,
) -> float:
    """Recall@k for a single question (cf. subject VI.1.1)."""
    if not gold_sources or k <= 0:
        return 0.0
    top_k = retrieved_sources[:k]
    found = sum(is_found(g, top_k, threshold) for g in gold_sources)
    return found / len(gold_sources)


def mean_recall_at_k(
    pairs: list[tuple[list[MinimalSource], list[MinimalSource]]],
    k: int,
    threshold: float = 0.05,
) -> float:
    """Average recall@k over a dataset."""
    if not pairs:
        return 0.0
    total = sum(recall_at_k(g, r, k, threshold) for g, r in pairs)
    return total / len(pairs)
