"""Tokenization pipeline shared between indexing and search.

Rule of thumb : the same `tokenize` function MUST be used both when
building the index and when querying it. Asymmetric tokenization
breaks BM25 silently.
"""

from collections.abc import Set as AbstractSet
import re


QUERY_STOPWORDS = frozenset({
    "how", "what", "why", "when", "where", "which", "who", "whom",
    "do", "does", "did", "is", "are", "was", "were", "be", "been", "being",
    "can", "could", "should", "would", "will", "shall", "may", "might",
    "the", "a", "an", "this", "that", "these", "those",
    "to", "of", "in", "on", "at", "by", "for", "with", "from", "into",
    "and", "or", "as", "if", "it", "its",
    "i", "you", "we", "they", "he", "she",
})


WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

CAMEL_RE = re.compile(r"[A-Z]?[a-z0-9]+|[A-Z]+(?=[A-Z]|$)")


def tokenize(
    text: str,
    stopwords: AbstractSet[str] | None = None,
) -> list[str]:
    """Tokenize a text for BM25 indexing / querying.

    Pipeline :
        1. Extract identifier-like words.
        2. Split each word on '_' (snake_case).
        3. Split each piece on case boundaries (camelCase, acronyms).
        4. Lowercase every sub-token.
        5. If `stopwords` is provided, drop any token in it.

    Duplicates are preserved (BM25 needs the term frequency).

    Examples:
        >>> tokenize("get_supported_mm_limits")
        ['get', 'supported', 'mm', 'limits']
        >>> tokenize("URLParser")
        ['url', 'parser']
    """
    if not text:
        return []
    tokens: list[str] = []
    for word in WORD_RE.findall(text):
        for piece in word.split("_"):
            if not piece:
                continue
            for sub in CAMEL_RE.findall(piece):
                tok = sub.lower()
                if stopwords is not None and tok in stopwords:
                    continue
                tokens.append(tok)
    return tokens
