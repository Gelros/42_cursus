from maze.generator import SOUTH, EAST, MazeGenerator
import shutil

WIDTH = shutil.get_terminal_size().columns


def display_title() -> None:
    """Display the welcome title and ASCII art header."""
    print("=" * WIDTH)
    print(" Welcome to A-Maze-Ing ! ".center(WIDTH, "¦"))
    print("=" * WIDTH)
    print("\t\033[3mRealized by guilacol & tmoga\033[0m".center(WIDTH))
    print()
    print("------------------".center(WIDTH))
    print("| Your maze here |".center(WIDTH))
    print("------------------".center(WIDTH))
    print()


def display_options() -> None:
    """Display the main menu options."""
    print("1 - Generate a maze".center(WIDTH))
    print("2 - Show/hide path ".center(WIDTH))
    print("3 - Show config    ".center(WIDTH))
    print("4 - Modify config  ".center(WIDTH))
    print("5 - Change colour  ".center(WIDTH))
    print("6 - Maze data      ".center(WIDTH))
    print("7 - !EPILEPSY!     ".center(WIDTH))
    print("8 - Maze type change".center(WIDTH))
    print("0 - Exit program   ".center(WIDTH))
    print()


def display_config() -> None:
    """Read and display the current configuration file."""
    with open("config.txt", "r") as f:
        print()
        print(" CURRENT CONFIG ".center(WIDTH, "¦"))
        print()
        print(f.read())
        print()
        print("¦" * WIDTH)
        print()


def _fill_cell(row: list[str], grid: list[list[int]], y: int, x: int,
               mask: set[tuple[int, int]], entry: tuple[int, int],
               end: tuple[int, int], east_wall: str) -> None:
    """
    Append the cell content and its east separator to a row.

    Args:
        row: The current row being built.
        grid: The maze grid.
        y: Row index of the cell.
        x: Column index of the cell.
        mask: Set of cells occupied by the 42 logo.
        entry: Entry cell coordinates as (y, x).
        end: Exit cell coordinates as (y, x).
        east_wall: Character to use when an east wall is present.
    """
    if mask and (y, x) in mask:
        row.append("██")
    elif (y, x) == entry:
        row.append("E ")
    elif (y, x) == end:
        row.append("S ")
    else:
        row.append("  ")
    row.append(" " if grid[y][x] & EAST == 0 else east_wall)


def generate_maze(grid: list[list[int]], width: int, height: int,
                  entry: tuple[int, int], end: tuple[int, int],
                  mask: set[tuple[int, int]],
                  what_maze: bool) -> list[list[str]]:
    """
    Build the ASCII representation of the maze as a list of rows.

    Args:
        grid: 2D list of integers encoding walls as bitmasks.
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        entry: Entry cell coordinates as (y, x).
        end: Exit cell coordinates as (y, x).
        mask: Set of cells occupied by the 42 logo.
        what_maze: If True, use classic ASCII characters; otherwise use
                   Unicode box-drawing characters.

    Returns:
        A 2D list of strings representing the maze display.
    """
    display: list[list[str]] = []
    row: list[str] = []

    if what_maze:
        # Classic ASCII mode
        display.append(["+"] + ["--", "+"] * width)

        for y in range(height):
            row = ["|"]
            for x in range(width):
                _fill_cell(row, grid, y, x, mask, entry, end, "|")
            display.append(row)

            row = ["+"]
            for x in range(width):
                row.append("--" if grid[y][x] & SOUTH else "  ")
                row.append("+")
            display.append(row)

    else:
        # Unicode box-drawing mode
        row = ["┌"]
        for x in range(width):
            row.append("──")
            row.append("┬" if x < width - 1 else "┐")
        display.append(row)

        for y in range(height):
            row = ["│"]
            for x in range(width):
                _fill_cell(row, grid, y, x, mask, entry, end, "│")
            display.append(row)

            if y < height - 1:
                row = ["├"]
                for x in range(width):
                    row.append("──" if grid[y][x] & SOUTH else "  ")
                    row.append("┼" if x < width - 1 else "┤")
            else:
                row = ["└"]
                for x in range(width):
                    row.append("──" if grid[y][x] & SOUTH else "  ")
                    row.append("┴" if x < width - 1 else "┘")
            display.append(row)

    return display


def display_path(grid: list[list[int]], path: list[tuple[int, int]],
                 width: int, height: int, entry: tuple[int, int],
                 end: tuple[int, int], what_maze: bool) -> list[list[str]]:
    """
    Build the maze display with the solution path marked.

    Cells along the path are marked with 'x ', except for the entry
    and exit cells.

    Args:
        grid: 2D list of integers encoding walls as bitmasks.
        path: List of (y, x) tuples representing the solution path.
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        entry: Entry cell coordinates as (y, x).
        end: Exit cell coordinates as (y, x).
        what_maze: If True, use classic ASCII; otherwise use Unicode.

    Returns:
        A 2D list of strings representing the maze with the path displayed.
    """
    wall_42 = MazeGenerator.make_42(width, height)
    maze_ascii = generate_maze(grid, width, height, entry, end,
                               wall_42, what_maze)

    for n in path:
        for y in range(height):
            for x in range(width):
                if (y, x) == n and (y, x) != entry and (y, x) != end:
                    maze_ascii[y * 2 + 1][x * 2 + 1] = "x "

    return maze_ascii
