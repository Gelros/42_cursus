import time
import sys


def path_hex(path: list[tuple[int, int]], n: tuple[int, int],
             e: tuple[int, int], s: tuple[int, int],
             w: tuple[int, int]) -> str:
    """
    Convert a list of cell coordinates into a string of cardinal directions.

    Computes the direction between each consecutive pair of cells in the path
    and maps it to N, E, S, or W.

    Args:
        path: List of (y, x) tuples representing the solution path.
        n: Movement vector for north as (dy, dx).
        e: Movement vector for east as (dy, dx).
        s: Movement vector for south as (dy, dx).
        w: Movement vector for west as (dy, dx).

    Returns:
        A string of direction characters (e.g. "NNEESW").
    """
    lst_dir = []
    len_path = len(path)
    path_parse = str()
    for i in range(1, len_path):
        lst_dir.append((path[i][0] - path[i - 1][0], path[i][1] -
                        path[i - 1][1]))
    for item in lst_dir:
        if item == n:
            path_parse += "N"
        if item == e:
            path_parse += "E"
        if item == s:
            path_parse += "S"
        if item == w:
            path_parse += "W"
    return path_parse


def colorize(text: str, color: str | None) -> str:
    """
    Wrap a string with ANSI color codes.

    Args:
        text: The string to colorize.
        color: Color name. If None, returns the text with only a reset code.

    Returns:
        The colorized string with a reset code appended.
    """
    colors = {
        "red":     "\033[31m",
        "green":   "\033[32m",
        "yellow":  "\033[33m",
        "blue":    "\033[34m",
        "magenta": "\033[35m",
        "cyan":    "\033[36m",
        "white":   "\033[0;37m"
    }
    if color is None:
        return f"{text}\033[0m"
    return f"{colors[color]}{text}\033[0m"


def blink(text: str) -> None:
    """
    Make a text blink in the terminal for a short duration.

    Args:
        text: The string to display as blinking text.
    """
    for _ in range(4):
        sys.stdout.write('\033[5m' + text + '\033[0m')
        sys.stdout.flush()
        time.sleep(0.6)
        sys.stdout.write('\r' + ' ' * len(text) + '\r')
