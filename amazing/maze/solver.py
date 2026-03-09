from maze.generator import MOVEMENT, MazeGenerator
from typing import Any
from maze.parsing import parsing


class MazeSolver:
    """
    Solves a maze using either BFS (imperfect) or DFS (perfect).

    Args:
        width (int): Width of the maze.
        height (int): Height of the maze.
        grid (list[list[int]): Maze configuration

    Example:
        ms = MazeSolver(width=10, height=10, grid)
        print(ms.solve())
    """

    def __init__(self, width: int, height: int, grid: list[list[int]]) -> None:
        """
        Initialize the maze solver.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
            grid: 2D list of integers encoding walls as bitmasks.
        """
        self.width = width
        self.height = height
        self.grid = grid
        self.visited: set[tuple[int, int]] = set()
        self.path: list[tuple[int, int]] = []

    def solve(self, start: tuple[int, int],
              end: tuple[int, int]) -> list[tuple[int, int]] | None:
        """
        Solve the maze from start to end.

        Uses BFS for imperfect mazes (shortest path) and DFS for perfect
        mazes (unique path).

        Args:
            start: Starting cell as (y, x).
            end: Target cell as (y, x).

        Returns:
            List of (y, x) tuples representing the path, or None if unsolvable.
        """
        self.visited.clear()
        self.path.clear()
        self.visited = MazeGenerator.make_42(self.width, self.height)

        if parsing().get("PERFECT") is not True:
            path_is_ok = self.bfs(start, end)
        else:
            path_is_ok = self._unique_way(start[0], start[1], end)

        return list(self.path) if path_is_ok else None

    def bfs(self, start: tuple[int, int], end: tuple[int, int]) -> bool:
        """
        Find the shortest path using Breadth-First Search.

        Explores all cells level by level, guaranteeing the shortest path
        in an imperfect maze with multiple routes.

        Args:
            start: Starting cell as (y, x).
            end: Target cell as (y, x).

        Returns:
            True if the end cell is reachable, False otherwise.
        """
        queue = [[start]]
        self.visited.add(start)

        while queue:
            self.path = queue.pop(0)
            y, x = self.path[-1]

            if (y, x) == end:
                return True

            for direction, (dy, dx) in MOVEMENT.items():
                ny, nx = y + dy, x + dx
                if (
                    not (self.grid[y][x] & direction)
                    and 0 <= ny < self.height
                    and 0 <= nx < self.width
                    and (ny, nx) not in self.visited
                ):
                    self.visited.add((ny, nx))
                    queue.append(self.path + [(ny, nx)])

        return False

    def _unique_way(self, y: int, x: int, end: tuple[int, int]) -> bool:
        """
        Find the unique path using an iterative Depth-First Search.

        Suitable for perfect mazes where only one path exists between
        any two cells. Uses an explicit stack to avoid recursion limit errors.

        Args:
            y: Starting row index.
            x: Starting column index.
            end: Target cell as (y, x).

        Returns:
            True if the end cell is reachable from (y, x), False otherwise.
        """
        stack: list[tuple[int, int, Any]] = [(y, x, iter(MOVEMENT.items()))]
        self.visited.add((y, x))
        self.path.append((y, x))

        while stack:
            y, x, directions = stack[-1]

            if (y, x) == end:
                return True

            try:
                direction, (dy, dx) = next(directions)
                ny, nx = y + dy, x + dx
                if (
                    not (self.grid[y][x] & direction)
                    and 0 <= ny < self.height
                    and 0 <= nx < self.width
                    and (ny, nx) not in self.visited
                ):
                    self.visited.add((ny, nx))
                    self.path.append((ny, nx))
                    stack.append((ny, nx, iter(MOVEMENT.items())))
            except StopIteration:
                stack.pop()
                self.path.pop()

        return False
