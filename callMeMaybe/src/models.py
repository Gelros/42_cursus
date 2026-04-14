from pydantic import BaseModel, Field


class ParameterDef(BaseModel):
    """Single parameter schema."""

    type: str


class FunctionDef(BaseModel):
    """Callable function schema."""

    name: str
    description: str
    parameters: dict[str, ParameterDef]
    returns: ParameterDef


class TestPrompt(BaseModel):
    """Input prompt wrapper."""

    prompt: str


class FunctionCall(BaseModel):
    """Function call output item."""

    prompt: str
    name: str = Field(..., min_length=1)
    parameters: dict[str, object]
