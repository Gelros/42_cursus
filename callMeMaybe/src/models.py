from pydantic import BaseModel, Field


class ParameterDef(BaseModel):
    """Parameter descriptor: holds the declared type string."""

    type: str


class FunctionDef(BaseModel):
    """Full definition of a callable function: name, description, parameters, return."""

    name: str
    description: str
    parameters: dict[str, ParameterDef]
    returns: ParameterDef


class TestPrompt(BaseModel):
    """Single natural-language prompt to process."""

    prompt: str


class FunctionCall(BaseModel):
    """Result of the pipeline: the selected function and its resolved arguments."""

    prompt: str
    name: str = Field(..., min_length=1)
    parameters: dict[str, object]
