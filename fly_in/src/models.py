"""Pydantic data models for parsed map elements (hubs, connexions, map)."""

from enum import Enum

from pydantic import BaseModel, Field, field_validator


class HubType(str, Enum):
    """Tag identifying a hub as start, end, or normal."""

    START = "start_hub"
    END = "end_hub"
    NORMAL = "hub"


class ZoneType(str, Enum):
    """Zone class controlling traversal cost and accessibility."""

    NORMAL = "normal"
    PRIORITY = "priority"
    RESTRICTED = "restricted"
    BLOCKED = "blocked"


class Hub(BaseModel):
    """A hub of the map (vertex of the graph)."""

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
        """Reject hub names containing dashes or spaces."""
        if "-" in v or " " in v:
            raise ValueError("Hub name cannot contain '-' or whitespace")
        return v


class Connexions(BaseModel):
    """An undirected connection between two hubs."""

    param_1: str
    param_2: str
    max_link_capacity: int = Field(default=1, ge=1)


class ParsedMap(BaseModel):
    """A fully parsed and validated map ready for graph construction."""

    nb_drones: int
    hub: list[Hub]
    connexions: list[Connexions]

    @field_validator("hub")
    @classmethod
    def valid_entry_end(cls, hub: list[Hub]) -> list[Hub]:
        """Ensure exactly one start hub and one end hub are declared."""
        n_start = sum(1 for h in hub if h.hub_type == HubType.START)
        n_end = sum(1 for h in hub if h.hub_type == HubType.END)
        if n_start != 1 or n_end != 1:
            raise ValueError(
                "A map must contain exactly one start_hub and one end_hub"
            )
        return hub
