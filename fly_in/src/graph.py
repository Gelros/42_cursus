"""Graph structures (Node, Edge, Graph) built on top of a ParsedMap."""

import math
from dataclasses import dataclass, field

from src.models import Hub, HubType, ParsedMap, ZoneType


@dataclass
class Edge:
    """Directed edge with capacity and current flow."""

    src: str
    dst: str
    capacity: int
    flow: int = 0

    @property
    def residual(self) -> int:
        """Return remaining capacity available for additional flow."""
        return self.capacity - self.flow


@dataclass
class Node:
    """Graph vertex wrapping a Hub with its outgoing edges."""

    name: str
    hub: Hub
    neighbors: dict[str, Edge] = field(default_factory=dict)

    @property
    def cost(self) -> float:
        """Return the per-turn traversal cost based on the hub's zone."""
        match self.hub.zone_type:
            case ZoneType.NORMAL:
                return 1
            case ZoneType.PRIORITY:
                return 1
            case ZoneType.RESTRICTED:
                return 2
            case ZoneType.BLOCKED:
                return math.inf

    @property
    def is_blocked(self) -> bool:
        """Tell whether this node sits in a blocked zone."""
        return self.hub.zone_type == ZoneType.BLOCKED


class Graph:
    """Adjacency-list graph with bidirectional edges and flow tracking."""

    def __init__(self, parsed: ParsedMap) -> None:
        """Build the graph from a parsed map (creates both edge directions)."""
        self._nodes: dict[str, Node] = {
            h.name: Node(name=h.name, hub=h, neighbors={})
            for h in parsed.hub
        }

        for c in parsed.connexions:
            if c.param_1 not in self._nodes:
                raise ValueError(f"Unknown hub: {c.param_1}")
            if c.param_2 not in self._nodes:
                raise ValueError(f"Unknown hub: {c.param_2}")

            self._nodes[c.param_1].neighbors[c.param_2] = Edge(
                src=c.param_1,
                dst=c.param_2,
                capacity=c.max_link_capacity,
            )
            self._nodes[c.param_2].neighbors[c.param_1] = Edge(
                src=c.param_2,
                dst=c.param_1,
                capacity=c.max_link_capacity,
            )

    @property
    def start(self) -> Node:
        """Return the unique start hub of the map."""
        for node in self._nodes.values():
            if node.hub.hub_type == HubType.START:
                return node
        raise ValueError("No start_hub found in the map")

    @property
    def end(self) -> Node:
        """Return the unique end hub of the map."""
        for node in self._nodes.values():
            if node.hub.hub_type == HubType.END:
                return node
        raise ValueError("No end_hub found in the map")

    def node(self, name: str) -> Node:
        """Look up a node by its hub name."""
        if name not in self._nodes:
            raise KeyError(f"Unknown hub: {name}")
        return self._nodes[name]

    def neighbors(self, name: str) -> dict[str, Edge]:
        """Return the outgoing-edges dict of *name*."""
        return self.node(name).neighbors

    def edge(self, src: str, dst: str) -> Edge:
        """Return the edge from *src* to *dst* (raises KeyError if missing)."""
        return self.node(src).neighbors[dst]

    def reset_flow(self) -> None:
        """Reset all edge flows to zero (for re-running an algorithm)."""
        for node in self._nodes.values():
            for edge in node.neighbors.values():
                edge.flow = 0
