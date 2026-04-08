from pydantic import BaseModel, Field, ValidationError
import json

class ParameterDef(BaseModel):
    type: str
    

class FunctionDef(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParameterDef]
    returns: ParameterDef


class TestPrompt(BaseModel):
    prompt: str


class FunctionCall(BaseModel):
    prompt: str
    name: str = Field(..., min_length=1)
    parameters: dict


def load_functions_def(path: str) -> list[FunctionDef]:
    with open(path, 'r') as e:
        res = json.load(e)

    funcs = []
    try:
        for raw in res:
            funcs.append(FunctionDef(**raw))
    except ValidationError as e:
        print("Model Pydantic invalide", e)
    return funcs