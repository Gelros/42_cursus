"""Turn-by-turn simulator producing TurnState snapshots from assignments."""

from dataclasses import dataclass

from src.scheduler import DroneAssignment


@dataclass
class TurnState:
    """Snapshot of the simulation at a given turn."""

    turn: int
    positions: dict[int, str]
    arrived: set[int]


class Simulator:
    """Replay drone assignments turn by turn into a list of TurnStates."""

    def __init__(self, assignments: list[DroneAssignment]) -> None:
        """Store assignments and pre-compute the simulation makespan."""
        self.assignments = assignments
        self.makespan: int = (
            max(a.end_turn for a in assignments) if assignments else 0
        )

    def run(self) -> list[TurnState]:
        """Return the full list of TurnStates from turn 1 to makespan."""
        return [
            self._build_turn_state(t)
            for t in range(1, self.makespan + 1)
        ]

    def _build_turn_state(self, turn: int) -> TurnState:
        """Aggregate all drones into the snapshot of a single *turn*."""
        positions: dict[int, str] = {}
        arrived: set[int] = set()

        for drone in self.assignments:
            if self._is_active(drone, turn):
                positions[drone.drone_id] = self._position(drone, turn)
            elif self._is_arrived(drone, turn):
                arrived.add(drone.drone_id)

        return TurnState(turn=turn, positions=positions, arrived=arrived)

    def _is_active(self, a: DroneAssignment, turn: int) -> bool:
        """Tell whether drone *a* is in flight at *turn*."""
        return a.start_turn <= turn <= a.end_turn

    def _is_arrived(self, a: DroneAssignment, turn: int) -> bool:
        """Tell whether drone *a* has already reached the end before *turn*."""
        return a.end_turn < turn

    def _position(self, a: DroneAssignment, turn: int) -> str:
        """Return the hub where drone *a* sits at *turn* (must be active)."""
        index = turn - a.start_turn
        return a.path[index]
