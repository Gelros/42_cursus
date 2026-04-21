from src.parser import ParsedMap, Hub, ZoneType
from dataclasses import field, dataclass

@dataclass
class Node:
    """Un hub enrichi pour les algos (capacité, voisins, zone)."""
    name: str
    hub: Hub
    neighbors: dict[str, "Edge"] = field(default_factory=dict)

    @property
    def cost(self) -> int:
        """Coût de traversée selon la zone (1 normal, 2 restricted, ∞ blocked)."""
        ...

    @property
    def is_blocked(self) -> bool: ...


@dataclass
class Edge:
    """Arête orientée ou bidirectionnelle avec capacité."""
    src: str
    dst: str
    capacity: int
    flow: int = 0   # utile pour max-flow

    @property
    def residual(self) -> int:
        return self.capacity - self.flow


class Graph:
    def __init__(self, parsed: ParsedMap) -> None:
        ...

    def start(self) -> 