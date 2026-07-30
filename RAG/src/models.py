"""Pydantic models for the RAG pipeline.

Models from the subject (V.7) :
    MinimalSource, UnansweredQuestion, AnsweredQuestion, RagDataset,
    MinimalSearchResults, MinimalAnswer,
    StudentSearchResults, StudentSearchResultsAndAnswer.

Project-specific :
    Chunk — extends MinimalSource with the chunk's textual content. Used
    internally during indexing; not part of the output JSON.
"""

import uuid
from pydantic import BaseModel, Field


# ----------------------------------------------------------------------
# Subject models (V.7) — DO NOT change field names or types.
# ----------------------------------------------------------------------

class MinimalSource(BaseModel):
    file_path: str
    first_character_index: int
    last_character_index: int


class UnansweredQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    sources: list[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    rag_questions: list[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    question_id: str
    question: str
    retrieved_sources: list[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    answer: str


class StudentSearchResults(BaseModel):
    search_results: list[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(StudentSearchResults):
    # Field override prescribed by the subject (V.7). Pydantic validates it at
    # runtime; mypy only objects because list is invariant.
    search_results: list[MinimalAnswer]  # type: ignore[assignment]


# ----------------------------------------------------------------------
# Project-specific
# ----------------------------------------------------------------------

class Chunk(MinimalSource):
    """A chunk = a MinimalSource enriched with its actual text content.

    Stored on disk during indexing so that we can rebuild context for
    answer generation without re-reading the source files.
    """
    text: str
