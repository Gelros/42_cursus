from pydantic import BaseModel, Field, field_validator
from enum import Enum

class HubType(str, Enum):
    START = "start_hub"
    END = "end_hub"
    NORMAL = "hub"

class ZoneType(str, Enum):
    NORMAL = "normal"
    PRIORITY = "priority"
    RESTRICTED = "restricted"
    BLOCKED = "blocked"


class Hub(BaseModel):
    hub_type: HubType
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = Field(default=1, ge=1)

    @field_validator("name")
    @classmethod
    def valid_name(cls, v: str) -> str:
        if "-" in v or " " in v:
            raise ValueError("Le nom ne peut contenir de '-' ou d'espaces")
        return v


class Connexions(BaseModel):
    param_1: str
    param_2: str
    max_link_capacity: int = Field(default=1, ge=1)


class ParsedMap(BaseModel):
    nb_drones: int
    hub: list[Hub]
    connexions: list[Connexions]
