"""CLI entry point: parse a map and run the simulation.

Usage:
    python -m src <path/to/map.txt>            # Rich pretty output
    python -m src <path/to/map.txt> --raw      # Subject-format output
"""

import sys

from src.parser import ParseError
from src.renderer import ConsoleRenderer
from src.solver import Solver


def main() -> None:
    """Parse argv, run the solver, and dispatch to the chosen renderer."""
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(
            "Usage: python -m src <map.txt> [--raw]\n"
            "  --raw   subject-conformant format (one line per turn)",
            file=sys.stderr,
        )
        sys.exit(1)

    path = args[0]
    raw = "--raw" in args[1:]

    try:
        result = Solver(path).solve()
    except ParseError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)

    renderer = ConsoleRenderer(result)
    if raw:
        renderer.render_raw()
    else:
        renderer.render()


if __name__ == "__main__":
    main()
