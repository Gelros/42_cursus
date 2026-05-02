"""Pathfinding algorithms: ABC contract + min-cost max-flow implementation."""

import heapq
import itertools
from abc import ABC, abstractmethod

from src.graph import Graph, Node


Path = list[str]


class PathFinder(ABC):
    """Abstract base class for any path-finding strategy."""

    def __init__(self, graph: Graph) -> None:
        """Store the graph the algorithm will operate on."""
        self.graph = graph

    @abstractmethod
    def find(self) -> list[Path]:
        """Return all augmenting paths used by the algorithm."""
        ...

    def _reconstruct_path(
        self,
        predecessor: dict[str, str],
        start: str,
        end: str,
    ) -> Path:
        """Walk *predecessor* backwards from *end* to *start*, then reverse."""
        path = [end]
        current = end
        while current != start:
            current = predecessor[current]
            path.append(current)
        return path[::-1]


class MinCostMaxFlowPathFinder(PathFinder):
    """Min-cost max-flow using Dijkstra on the residual graph."""

    def find(self) -> list[Path]:
        """Iteratively augment flow until no path is found."""
        paths_used: list[Path] = []

        while True:
            path = self._find_augmenting_path()
            if path is None:
                break
            amount = self._bottleneck(path)
            self._update_flow(path, amount)
            for _ in range(amount):
                paths_used.append(path)

        return paths_used

    def _find_augmenting_path(self) -> Path | None:
        """Hook returning the next augmenting path (Dijkstra on residual)."""
        return self._dijkstra_residual(self.graph.start, self.graph.end)

    def _dijkstra_residual(self, start: Node, end: Node) -> Path | None:
        """Return the lowest-cost path from *start* to *end*."""
        dist: dict[str, float] = {start.name: 0}
        predecessor: dict[str, str] = {}
        counter = itertools.count()
        queue: list[tuple[float, int, Node]] = []
        heapq.heappush(queue, (0, next(counter), start))

        while queue:
            cost, _, current = heapq.heappop(queue)

            if current.name == end.name:
                return self._reconstruct_path(
                    predecessor, start.name, end.name
                )

            if cost > dist.get(current.name, float("inf")):
                continue

            for n_name, edge in current.neighbors.items():
                if edge.residual <= 0:
                    continue
                neighbor = self.graph.node(n_name)
                if neighbor.is_blocked:
                    continue

                new_cost = cost + neighbor.cost
                if new_cost < dist.get(n_name, float("inf")):
                    dist[n_name] = new_cost
                    predecessor[n_name] = current.name
                    heapq.heappush(
                        queue, (new_cost, next(counter), neighbor)
                    )

        return None

    def _bottleneck(self, path: Path) -> int:
        """Return the minimum residual capacity along *path*."""
        return min(
            self.graph.edge(path[i], path[i + 1]).residual
            for i in range(len(path) - 1)
        )

    def _update_flow(self, path: Path, amount: int) -> None:
        """Push *amount* units of flow forward and reduce reverse residual."""
        for i in range(len(path) - 1):
            forward = self.graph.edge(path[i], path[i + 1])
            backward = self.graph.edge(path[i + 1], path[i])
            forward.flow += amount
            backward.flow -= amount
