import random

NORTH = 1 << 0
EAST = 1 << 1
SOUTH = 1 << 2
WEST = 1 << 3
OPPOSE = {NORTH: SOUTH, EAST: WEST, SOUTH: NORTH, WEST: EAST}
MOVEMENT: dict[int, tuple[int, int]] = {
    NORTH: (-1, 0), EAST: (0, 1), SOUTH: (1, 0), WEST: (0, -1)
}


class MazeGenerator():
    """
    A reusable maze generator.

    Args:
        width (int): Width of the maze.
        height (int): Height of the maze.

    Example:
        mg = MazeGenerator(width=10, height=10)
        mg.generate()
        print(mg.get_maze())
        print(mg.get_solution())
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize the maze generator.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
        """
        self.width = width
        self.height = height
        self.grid: list[list[int]] = []
        self.visited: set[tuple[int, int]] = set()

    def generate(self) -> None:
        """Fill the grid with fully walled cells and pre-visit the 42 logo."""
        for _ in range(self.height):
            self.grid.append([0b1111] * self.width)
        self.visited = MazeGenerator.make_42(self.width, self.height)

    def get_grid(self) -> list[list[int]]:
        """Return the maze grid."""
        return self.grid

    def remove_wall(self, x: int, y: int) -> None:
        """
        Recursively carve passages using a depth-first search.

        Args:
            x: Column index of the current cell.
            y: Row index of the current cell.
        """
        self.visited.add((y, x))
        directions = [NORTH, EAST, SOUTH, WEST]
        random.shuffle(directions)
        for dir in directions:
            dy, dx = MOVEMENT[dir]
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (ny, nx) not in self.visited:
                    self.grid[y][x] &= ~dir
                    self.grid[ny][nx] &= ~OPPOSE[dir]
                    self.remove_wall(nx, ny)

    def imperfect_maze(self) -> None:
        """
        Break dead ends to create multiple paths, making the maze imperfect.

        Finds all dead end cells (only one open passage) and removes one
        additional wall from each, creating alternative routes.
        """
        bloqued = []
        for y in range(self.height):
            for x in range(self.width):
                passages = sum(
                    1 for d in [NORTH, EAST, SOUTH, WEST]
                    if not self.grid[y][x] & d
                )
                if passages == 1:
                    bloqued.append((y, x))
        random.shuffle(bloqued)
        for y, x in bloqued:
            for d in [NORTH, EAST, SOUTH, WEST]:
                dy, dx = MOVEMENT[d]
                ny, nx = dy + y, dx + x
                if (
                    self.grid[y][x] & d
                    and 0 <= ny < self.height
                    and 0 <= nx < self.width
                    and (ny, nx) not in self.visited
                ):
                    self.grid[y][x] &= ~d
                    self.grid[ny][nx] &= ~OPPOSE[d]
                    break

    @staticmethod
    def make_42(width: int, height: int) -> set[tuple[int, int]]:
        """
        Generate the set of cells forming the 42 logo, centered in the grid.

        Returns an empty set if the grid is too small to display the logo.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.

        Returns:
            Set of (y, x) coordinates occupied by the 42 logo.
        """
        if width < 10 or height < 10:
            return set()
        if not width % 2 == 0:
            two = [
                (0, 5), (0, 6), (1, 6), (2, 5), (2, 6), (3, 5), (4, 5), (4, 6)
            ]
        else:
            two = [
                (0, 4), (0, 5), (1, 5), (2, 4), (2, 5), (3, 4), (4, 4), (4, 5)
            ]
        four = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (4, 2)]
        raw: set[tuple[int, int]] = set([(y, x) for y, x in four + two])
        offset_y = (height - 5) // 2
        offset_x = (width - 6) // 2
        return {(y + offset_y, x + offset_x) for y, x in raw}
