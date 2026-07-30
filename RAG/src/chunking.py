"""Chunking strategies and file walking.

Three low-level chunkers (file-agnostic, return raw (start, end, text)
tuples) and one high-level dispatcher `chunk_file(path)` that produces
project Chunks (with file_path).
"""

import ast
import re
from pathlib import Path
from typing import NamedTuple

from .models import Chunk


def walk_files(root: Path, extensions: tuple[str, ...]) -> list[Path]:
    """Recursively list files under `root` whose suffix is in `extensions`.

    - Hidden directories (starting with '.') are skipped.
    - Result is sorted alphabetically (reproducibility).
    - Paths are returned relative to root.parent (so they start with the
      repo prefix expected by the subject, e.g. data/raw/vllm-0.10.1/...).
    """
    paths: list[Path] = []
    for suffix in extensions:
        for p in root.rglob(f"*{suffix}"):
            if any(part.startswith(".") for part in p.parts):
                continue
            paths.append(p)
    return sorted(paths)


class RelChunk(NamedTuple):
    """A chunk relative to a single text (no file info yet).

    Convention : `end` is exclusive (Python slice convention), so
    `text[start:end] == text_content`.
    """
    start: int
    end: int
    text: str


def chunk_fixed(
    text: str,
    max_size: int = 1500,
    overlap: int = 200,
) -> list[RelChunk]:
    """Sliding window with overlap. Universal fallback."""
    if not text:
        return []
    if max_size <= 0 or overlap < 0 or overlap >= max_size:
        raise ValueError("Invalid max_size / overlap parameters")

    chunks: list[RelChunk] = []
    start = 0
    while start < len(text):
        end = min(start + max_size, len(text))
        chunks.append(RelChunk(start, end, text[start:end]))
        if end == len(text):
            break
        start = end - overlap
    return chunks


def _line_offsets(source: str) -> list[int]:
    """Pre-compute the byte offset of each line start (1-indexed lines)."""
    offsets = [0]
    for i, c in enumerate(source):
        if c == "\n":
            offsets.append(i + 1)
    return offsets


def _offset_of(line_offsets: list[int], line: int, col: int) -> int:
    """Convert (1-indexed line, 0-indexed col) -> char offset."""
    return line_offsets[line - 1] + col


def chunk_python_ast(source: str) -> list[RelChunk]:
    """Top-level FunctionDef / AsyncFunctionDef / ClassDef as chunks.

    Raises SyntaxError if `source` is not valid Python (caller decides
    whether to catch and fall back to fixed-window).
    """
    chunks: list[RelChunk] = []
    tree = ast.parse(source)
    line_offsets = _line_offsets(source)
    TARGET = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    for node in tree.body:
        if not isinstance(node, TARGET):
            continue
        assert node.end_lineno is not None and node.end_col_offset is not None
        start = _offset_of(line_offsets, node.lineno, node.col_offset)
        end = _offset_of(line_offsets, node.end_lineno, node.end_col_offset)
        chunks.append(RelChunk(start, end, source[start:end]))
    return chunks


HEADING_RE = re.compile(r"^#{1,6}[ \t]+\S", re.MULTILINE)


def chunk_markdown(text: str) -> list[RelChunk]:
    """Split on ATX headings (# ... ######)."""
    if not text:
        return []
    matches = list(HEADING_RE.finditer(text))
    if not matches:
        return [RelChunk(0, len(text), text)]

    chunks: list[RelChunk] = []
    first = matches[0].start()
    if first != 0 and text[:first].strip():
        chunks.append(RelChunk(0, first, text[:first]))
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunks.append(RelChunk(start, end, text[start:end]))
    return chunks


# ----------------------------------------------------------------------
# High-level dispatcher : pick the right strategy per file.
# ----------------------------------------------------------------------

def chunk_file(path: Path, max_chunk_size: int = 2000) -> list[Chunk]:
    """Read `path` and chunk it with the appropriate strategy.

    Strategy choice :
        .py   -> AST  (fallback fixed-window if SyntaxError)
        .md   -> Markdown headings
        other -> fixed-window

    Then any RelChunk larger than `max_chunk_size` is sub-chunked with
    chunk_fixed to respect the subject's hard cap (V.4 : 2000 chars max).
    Returned Chunks carry file_path = str(path) so that file_path matches
    the expected `data/raw/vllm-0.10.1/...` prefix.

    Returns an empty list on read failure (unreadable file, weird encoding).
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    if path.suffix == ".py":
        try:
            rel_chunks = chunk_python_ast(text)
        except SyntaxError:
            rel_chunks = chunk_fixed(text, max_chunk_size)
    elif path.suffix == ".md":
        rel_chunks = chunk_markdown(text)
    else:
        rel_chunks = chunk_fixed(text, max_chunk_size)

    res: list[Chunk] = []
    for rc in rel_chunks:
        if len(rc.text) <= max_chunk_size:
            res.append(Chunk(
                file_path=str(path),
                first_character_index=rc.start,
                last_character_index=rc.end,
                text=rc.text,
            ))
        else:
            for sub in chunk_fixed(rc.text, max_chunk_size):
                res.append(Chunk(
                    file_path=str(path),
                    first_character_index=rc.start + sub.start,
                    last_character_index=rc.start + sub.end,
                    text=sub.text,
                ))
    return res
