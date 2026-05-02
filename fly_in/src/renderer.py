"""Console rendering: subject-format raw output and Rich pretty output."""

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.solver import SolveResult


DRONE_COLORS: list[str] = [
    "red", "blue", "green", "yellow", "magenta", "cyan",
    "bright_red", "bright_blue", "bright_green",
    "bright_yellow", "bright_magenta", "bright_cyan",
]


class ConsoleRenderer:
    """Render a SolveResult to the console (raw or Rich-styled)."""

    def __init__(
        self,
        result: SolveResult,
        console: Console | None = None,
    ) -> None:
        """Store the result and an optional Console (testable injection)."""
        self.result = result
        self.console: Console = console or Console()

    def render(self) -> None:
        """Render the full Rich UI: header panel, turns table, summary."""
        self._render_header()
        self._render_turns()
        self._render_summary()

    def render_raw(self) -> None:
        """Print the subject-conformant format: one line per turn."""
        for state in self.result.states:
            tokens = [
                f"D{drone_id}-{hub}"
                for drone_id, hub in sorted(state.positions.items())
            ]
            print(" ".join(tokens))

    def _render_header(self) -> None:
        """Print the header panel with map metadata and makespan."""
        r = self.result
        unique_paths = len({tuple(p) for p in r.paths})

        header = Text()
        header.append("Drones    : ", style="bold")
        header.append(f"{r.parsed_map.nb_drones}\n")
        header.append("Hubs      : ", style="bold")
        header.append(f"{len(r.parsed_map.hub)}\n")
        header.append("Paths     : ", style="bold")
        header.append(
            f"{unique_paths} unique - {len(r.paths)} slot(s)/turn\n"
        )
        header.append("Total     : ", style="bold")
        header.append(f"{r.makespan} turns", style="bold cyan")

        self.console.print(Panel(
            header,
            title="[bold cyan]fly_in - Result[/]",
            title_align="left",
            border_style="cyan",
            padding=(1, 2),
        ))

    def _render_turns(self) -> None:
        """Print one row per turn with positions and arrived drones."""
        table = Table(
            title="Simulation",
            border_style="dim",
            box=box.ROUNDED,
            show_lines=False,
        )
        table.add_column(
            "Turn", style="bold cyan", justify="right", width=6
        )
        table.add_column("Positions")
        table.add_column("Arrived", style="dim green")

        for state in self.result.states:
            positions_text = self._format_positions(state.positions)
            arrived_text = ", ".join(
                f"D{d}" for d in sorted(state.arrived)
            )
            table.add_row(str(state.turn), positions_text, arrived_text)

        self.console.print(table)

    def _format_positions(self, positions: dict[int, str]) -> Text:
        """Build a colored Text listing each drone with its current hub."""
        text = Text()
        for i, (drone_id, hub) in enumerate(sorted(positions.items())):
            if i > 0:
                text.append(", ")
            color = self._color_for_drone(drone_id)
            text.append(f"D{drone_id}", style=f"bold {color}")
            text.append(f"@{hub}")
        return text

    def _render_summary(self) -> None:
        """Print the final success line."""
        r = self.result
        self.console.print()
        self.console.print(
            f"[green]OK[/] All drones arrived in "
            f"[bold]{r.makespan}[/] turns."
        )

    @staticmethod
    def _color_for_drone(drone_id: int) -> str:
        """Return a stable color for a given drone_id (cycling palette)."""
        return DRONE_COLORS[drone_id % len(DRONE_COLORS)]
