"""High-level orchestrator wiring parser, graph, pathfinder, scheduler, sim."""

from dataclasses import dataclass

from src.graph import Graph
from src.models import ParsedMap
from src.parser import parse_map
from src.pathfinder import (
    MinCostMaxFlowPathFinder,
    Path,
    PathFinder,
)
from src.scheduler import DroneAssignment, Scheduler
from src.simulator import Simulator, TurnState


@dataclass
class SolveResult:
    """Aggregated output of the full pipeline (for renderers and tests)."""

    parsed_map: ParsedMap
    paths: list[Path]
    assignments: list[DroneAssignment]
    states: list[TurnState]
    makespan: int


class Solver:
    """End-to-end driver: parse, build, route, schedule, simulate."""

    def __init__(
        self,
        path: str,
        pathfinder_cls: type[PathFinder] = MinCostMaxFlowPathFinder,
    ) -> None:
        """Store the map path and the pathfinder strategy to use."""
        self.path = path
        self.pathfinder_cls = pathfinder_cls

    def solve(self) -> SolveResult:
        """Run the pipeline end-to-end and return a SolveResult."""
        parsed = parse_map(self.path)
        graph = Graph(parsed)
        raw_paths = self.pathfinder_cls(graph).find()
        paths = [self._expand_for_costs(p, graph) for p in raw_paths]
        assignments = Scheduler(
            paths=paths, nb_drones=parsed.nb_drones
        ).assign()
        simulator = Simulator(assignments)

        return SolveResult(
            parsed_map=parsed,
            paths=paths,
            assignments=assignments,
            states=simulator.run(),
            makespan=simulator.makespan,
        )

    @staticmethod
    def _expand_for_costs(path: Path, graph: Graph) -> Path:
        """Inject in-transit markers for hubs whose cost is > 1.

        For a hub whose traversal cost is N, the drone first occupies the
        connection toward it for ``N - 1`` turns, then arrives at the hub
        on the last turn. The transit turns are encoded as the synthetic
        name ``<src>~<dst>``, so the simulator never reports an in-transit
        drone as occupying the destination hub. This both keeps
        ``len(path) - 1`` aligned with the real number of turns and
        prevents false ``max_drones`` overflows on restricted hubs.
        """
        expanded: Path = [path[0]]
        for i in range(1, len(path)):
            cur = path[i]
            prev = path[i - 1]
            cost = int(graph.node(cur).cost)
            for _ in range(cost - 1):
                expanded.append(f"{prev}~{cur}")
            expanded.append(cur)
        return expanded
