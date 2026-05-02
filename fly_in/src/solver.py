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
        paths = self.pathfinder_cls(graph).find()
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
