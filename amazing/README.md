*This project has been created as part of the 42 curriculum by guilacol, tmoga.*

# Maze Generator & Solver with spicy functionalities!

## Description

This project implements a **maze generator and solver** written in Python.
It reads a configuration file (`config.txt`) describing the maze parameters, generates a maze accordingly, and computes a valid path from the entry point to the exit.

The main objectives of the project are:

* Generate a valid maze based on configurable parameters.
* Ensure the maze respects given constraints (size, entry/exit positions, seed, etc.).
* Provide a solver capable of finding a path through the maze.
* Produce the resulting maze in a `.txt` output file.

---

# Instructions

## Requirements

* Python 3.10 or newer

## Installation

Clone the repository:

```bash
git clone <repository_url>
cd <repository_name>
```

A Makefile is provided, please use these commands:

* ***make install*** -> Create a venv and install required dependencies,
* ***make run*** -> Execute the program with the right config file,
* ***make lint*** -> Check if the program is correct according to Flake8 and MyPy,
* ***make debug*** -> Launch debug mode,
* ***make clean*** -> Clear caches and other undesired files.


## Execution

By default, the program reads its configuration from a file named `config.txt`.
But once the program is launched, you can edit this file directly in the program.

You can also launch the program with:

python3 a_maze_ing.py config.txt

If the configuration is valid, the program will:

1. Parse the configuration file
2. Generate the maze
3. Solve the maze
4. Save the result to the specified output file

You can interact with the program as long as it's running.
If an error occurs (invalid format, missing values, invalid parameters), the program will display a descriptive error message.

---

# Configuration File

The maze configuration must be defined in a file named `config.txt` using the following format:

```
KEY=VALUE
```

Blank lines and lines starting with `#` are ignored.

## Complete Configuration Structure

Example:

```
WIDTH=20
HEIGHT=20
ENTRY=(0,1)
EXIT=(19,18)
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Parameters

| Key         | Type          | Description                               |
| ----------- | ------------- | ----------------------------------------- |
| WIDTH       | integer       | Width of the maze                         |
| HEIGHT      | integer       | Height of the maze                        |
| ENTRY       | tuple `(y,x)` | Entry coordinates in the maze             |
| EXIT        | tuple `(y,x)` | Exit coordinates in the maze              |
| OUTPUT_FILE | string        | Name of the output `.txt` file            |
| PERFECT     | boolean       | Whether the maze must be a *perfect maze* |

### Constraints

* `WIDTH` and `HEIGHT` must be **greater than 2**
* `WIDTH` and `HEIGHT` must be **lower than 100**
* `ENTRY` and `EXIT` must be **different**
* `ENTRY` and `EXIT` must be **inside maze boundaries**
* * `ENTRY` and `EXIT` must be **outside the 42 logo**
* `OUTPUT_FILE` must end with `.txt`
* Note that is `WIDTH` or `HEIGHT` are **below** 10, the maze will not display the 42 logo and will display a special message.

Optional key `SEED` is allowed. If detected with any value, the maze will not change anymore. 
Write `#SEED` into the config file to bypass.

---

# Maze Generation Algorithm

The maze generation is based on a **Depth-First Search (DFS) recursive backtracking algorithm**.

## How it works

1. Start from a random cell.
2. Mark the cell as visited.
3. Randomly choose an unvisited neighboring cell.
4. Remove the wall between the current cell and the chosen neighbor.
5. Move to that neighbor and repeat the process.
6. If no unvisited neighbors remain, backtrack to the previous cell.

This process continues until all cells have been visited.

---

# Why This Algorithm

The **DFS recursive backtracking algorithm** was chosen because:

* It is **simple to implement**
* It guarantees the generation of a **perfect maze**
* It produces visually interesting mazes with long corridors
* It has **linear time complexity** relative to the number of cells

It is also a common reference algorithm in procedural maze generation, making it well documented and easy to study.

---

# Maze Solver

The solver computes a path from the entry point to the exit using a **graph traversal algorithm**.

The maze is treated as a graph where:

* Each cell is a node
* Passages between cells represent edges

The solver explores the maze until it finds the exit, returning a valid path.

---

# Reusable Components

Several parts of the project were designed to be reusable:

### MazeGenerator class

The `MazeGenerator` class can be reused in other projects requiring:

* procedural maze generation
* grid-based generation algorithms

### MazeSolver class

The `MazeSolver` class can be reused in other projects requiring:

* testing of pathfinding algorithms
* find optimal solution for both perfect and imperfect mazes

## Using the mazegen module

### Install
pip install mazegen-1.0.0-py3-none-any.whl

### Quickstart
from maze import MazeGenerator
from maze import MazeSolver
from maze import parsing

WIDTH = parsing()["WIDTH"]
HEIGHT = parsing()["HEIGHT"]

mg = MazeGenerator(WIDTH, HEIGHT)
mg.generate()
y, x = parsing()["ENTRY"]
end = parsing()["EXIT"]
mg.remove_wall(x, y)

grid = mg.grid
print(f"Grid : {grid}")

print()
ms = MazeSolver(WIDTH, HEIGHT, grid)
print(f"Solution : {ms.solve((y, x), end)}")


If needed, you can do "help(MazeGenerator)" or "help(MazeSolver)"

### Parameters
| Param  | Type | Default | Description        |
|--------|------|---------|--------------------|
| width  | int  | 10      | Width of the maze  |
| height | int  | 10      | Height of the maze |
| seed   | int  | None    | Random seed        |

---

# Team & Project Management

## Team Roles

We regularly held review sessions to walk each other through our code. It would be inaccurate to describe the work as a strictly separated task distribution, since we both worked on multiple parts of the project. 
However, the overall contributions can roughly be summarized as follows:

* **guilacol**

  * Maze generation algorithm
  * Maze solving algorithm
  * Performance optimization
  * Maze ASCII display

* **tmoga**

  * Configuration parsing & validation system
  * Error handling
  * Direct modification of config file
  * Main menu and display customization
  * Makefile

---

## Project Planning

Initial planning included:

* defining the maze data structure
* selecting the generation algorithm
* designing the configuration format
* implementing parsing and validation
* integrating the solver

During development, some adjustments were made:

* improving error handling in the parser
* Refactoring some functions
* Rethinking some design choices

---

## What Worked Well

* Clear separation between modules (parsing, generation, solving)
* Early validation of configuration parameters
* Good communication between team mates

## What Could Be Improved

* Adding support for **multiple generation algorithms**
* Improving visualization of the maze (path)
* Improving code readibility
* Having a better provisional schedule or using apps like Miro...

---

# AI Usage

AI tools were used as development assistance for:

* understanding static typing issues with **MyPy**
* explaining algorithmic concepts
* proofreading documentation
* Some parts of README.md
* Some docstrings to fit the PEP 257 format

All design decisions, implementation, and debugging were performed by the project authors.

---

# Advanced features

We also decided to extend the project by implementing a few additional features, some of them purely for fun:

* A feature allowing the config.txt file to be modified directly from within the program.
* The ability to change the color of the 42 logo located at the center of the maze.
* A different characters to represent the path taken by the solver.
* An “epilepsy mode” that rapidly flashes the maze in multiple colors.
* Toggle between different maze displays

___

# Resources

Some useful references related to maze generation and pathfinding:

* *Mazes for Programmers* — Jamis Buck
* https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap
* https://en.wikipedia.org/wiki/Maze_generation_algorithm
* https://en.wikipedia.org/wiki/Depth-first_search
* https://en.wikipedia.org/wiki/Pathfinding
* https://youtu.be/HyK_Q5rrcr4?si=sinaZAqTKH7xJqb9
* https://mypy.readthedocs.io/en/stable/
