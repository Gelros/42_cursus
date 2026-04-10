from pydantic import BaseModel, Field

class ParameterDef(BaseModel):
    """Defines a single parameter or return type."""
    type: str
    

class FunctionDef(BaseModel):
    """Schema for a function that the AI can call."""
    name: str
    description: str
    parameters: dict[str, ParameterDef]
    returns: ParameterDef


class TestPrompt(BaseModel):
    """Simple wrapper for a test prompt string."""
    prompt: str


class FunctionCall(BaseModel):
    """Represents an AI's decision to call a specific function."""
    prompt: str
    name: str = Field(..., min_length=1)
    parameters: dict
