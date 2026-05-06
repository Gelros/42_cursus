"""Drone-to-path scheduler producing per-drone start-turn assignments."""

from collections import Counter
from dataclasses import dataclass

from src.pathfinder import Path


@dataclass
class DroneAssignment:
    """Plan for a single drone: which path, and when to start it."""

    drone_id: int
    path: Path
    start_turn: int

    def __post_init__(self) -> None:
        """Validate identifier and start turn after construction."""
        if self.drone_id < 0:
            raise ValueError(f"Negative drone_id: {self.drone_id}")
        if self.start_turn < 1:
            raise ValueError(
                f"start_turn must be >= 1, got {self.start_turn}"
            )

    @property
    def end_turn(self) -> int:
        """Return the turn at which the drone reaches the end hub."""
        return self.start_turn + len(self.path) - 1


class Scheduler:
    """Greedy assigner of drones to paths minimising the makespan."""

    def __init__(self, paths: list[Path], nb_drones: int) -> None:
        """Build per-path capacity counters from *paths* and *nb_drones*."""
        if nb_drones < 1:
            raise ValueError(
                f"nb_drones must be >= 1, got {nb_drones}"
            )
        if not paths:
            raise ValueError("No path provided to Scheduler")

        self.nb_drones: int = nb_drones
        self.path_capacity: Counter[tuple[str, ...]] = Counter(
            tuple(p) for p in paths
        )
        self.assigned_count: dict[tuple[str, ...], int] = dict.fromkeys(
            self.path_capacity, 0
        )

    def assign(self) -> list[DroneAssignment]:
        """Return assignments for all drones using a greedy heuristic."""
        self.assigned_count = dict.fromkeys(self.path_capacity, 0)
        assignments: list[DroneAssignment] = []

        for drone_id in range(self.nb_drones):
            best_path: Path | None = None
            best_start: int = 1
            best_end: float = float("inf")

            for path_tuple in self.path_capacity:
                candidate = list(path_tuple)
                start = self._next_start_turn(candidate)
                end = start + len(candidate) - 1
                if end < best_end:
                    best_path = candidate
                    best_start = start
                    best_end = end

            assert best_path is not None
            assignments.append(
                DroneAssignment(
                    drone_id=drone_id,
                    path=best_path,
                    start_turn=best_start,
                )
            )
            self.assigned_count[tuple(best_path)] += 1

        return assignments

    def _next_start_turn(self, path: Path) -> int:
        """Return the earliest turn a new drone can start on *path*."""
        key = tuple(path)
        cap = self.path_capacity[key]
        assigned = self.assigned_count[key]
        return (assigned // cap) + 1
