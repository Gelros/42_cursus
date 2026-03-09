from maze.parsing import parsing

OUTPUT = parsing()["OUTPUT_FILE"]


def create_file_hex(data: list[list[str]],
                    start: list[int], end: list[int],
                    path: str = "") -> None:
    """
    Write the maze hex grid and metadata to a file.

    The output file contains the hex-encoded grid rows, followed by
    the entry coordinates, exit coordinates, and the solution path.

    Args:
        data: 2D list of hex-encoded strings representing the maze grid.
        start: Entry cell coordinates as [y, x].
        end: Exit cell coordinates as [y, x].
        path: String representation of the solution path. Defaults to "".
    """
    with open(OUTPUT, 'w') as f:
        for raw in data:
            res = str()
            for rw in raw:
                res += rw
            f.write(res)
            f.write("\n")
        f.write("\n")
        f.write(f"{start[0]},{start[1]}")
        f.write("\n")
        f.write(f"{end[0]},{end[1]}")
        f.write("\n")
        f.write(path)
