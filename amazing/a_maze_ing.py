from maze.generator import MazeGenerator, NORTH, SOUTH, EAST, WEST, MOVEMENT
from file_hex import create_file_hex
from maze.parsing import parsing
from maze.solver import MazeSolver
from display import (generate_maze, display_path,
                     display_options, display_title, display_config)
from utils import path_hex, colorize, blink
import shutil
import sys
import os
import random
from config_modifier import modify_config


WIDTH = shutil.get_terminal_size().columns
width = parsing()["WIDTH"]
height = parsing()["HEIGHT"]
entry = parsing()["ENTRY"]
end = parsing()["EXIT"]
output = parsing()["OUTPUT_FILE"]

grid_hex: list[list[str]] = []
grid: list[list[list[int]]] = []
SHOW = False
LAB = False
INDEX = 0
COLOURS = ["yellow", "cyan", "magenta", "blue", "white"]
CURRENT_COLOUR = None
INDEX = 0
wall_42 = MazeGenerator.make_42(width, height)


def display_maze(grid: list[list[list[int]]], width: int, height: int,
                 entry: tuple[int, int], end: tuple[int, int],
                 color: str | None = None) -> None:
    """
    Generate and print the maze to the terminal.

    Warns the user if the maze is too small to display the 42 logo.
    If no color is provided, only entry and exit markers are colorized.
    Otherwise, wall characters are colorized according to the current
    maze type (classic ASCII or Unicode box-drawing).

    Args:
        grid: Nested list containing the maze grid.
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        entry: Entry cell coordinates as (y, x).
        end: Exit cell coordinates as (y, x).
        color: Wall color name. If None, no wall colorization is applied.
    """
    if width < 10 or height < 10:
        print()
        print(
            (
                " Please note that the maze is too small "
                "to display the 42 logo :( "
            ).center(WIDTH, "-")
            )
        print()

    res = generate_maze(grid[0], width, height, entry, end, wall_42, LAB)

    if color is None:
        for row in res:
            line = "".join(row).center(WIDTH)
            line = line.replace("E ", colorize("E ", "green"))
            line = line.replace("S ", colorize("S ", "red"))
            print(line)
    else:
        for row in res:
            raw_line = "".join(row).center(WIDTH)
            colored_line = ""

            i = 0
            if not LAB:
                while i < len(raw_line):
                    if raw_line[i:i+2] == "--" or raw_line[i:i+2] == "──":
                        colored_line += colorize(raw_line[i:i+2], color)
                        i += 2
                    elif raw_line[i] in "+|│┌┐└┘┬┴├┤┼":
                        colored_line += colorize(raw_line[i], color)
                        i += 1
                    elif raw_line[i:i+2] == "E ":
                        colored_line += colorize("E ", "green")
                        i += 2
                    elif raw_line[i:i+2] == "S ":
                        colored_line += colorize("S ", "red")
                        i += 2
                    elif raw_line[i:i+2] == "x ":
                        colored_line += colorize("x ", "yellow")
                        i += 2
                    else:
                        colored_line += raw_line[i]
                        i += 1
                colored_line = colored_line.replace(
                    "██", colorize("██", COLOURS[-1]))
            else:
                while i < len(raw_line):
                    if raw_line[i:i+2] == "--":
                        colored_line += colorize("--", color)
                        i += 2
                    elif raw_line[i] in "+|":
                        colored_line += colorize(raw_line[i], color)
                        i += 1
                    elif raw_line[i:i+2] == "E ":
                        colored_line += colorize("E ", "green")
                        i += 2
                    elif raw_line[i:i+2] == "S ":
                        colored_line += colorize("S ", "red")
                        i += 2
                    elif raw_line[i:i+2] == "x ":
                        colored_line += colorize("x ", "yellow")
                        i += 2
                    else:
                        colored_line += raw_line[i]
                        i += 1
                    colored_line = colored_line.replace(
                        "██", colorize("██", COLOURS[-1]))
            print(colored_line)


def show_path() -> None:
    """
    Solve the maze and display the solution path.

    Warns the user if the maze is too small to display the 42 logo.
    Solves the maze using the appropriate algorithm based on config,
    writes the hex path to file, and prints the maze with the path
    marked using a randomly chosen logo symbol.
    Wall colorization is applied if a current color is set.
    """
    if width < 10 or height < 10:
        print()
        print(
            (
                " Please note that the maze is too small "
                "to display the 42 logo :( "
            ).center(WIDTH, "-")
            )
        print()
    solver = MazeSolver(width, height, grid[0])
    solver.solve(entry, end)

    pth = path_hex(solver.path, MOVEMENT[NORTH],
                   MOVEMENT[EAST], MOVEMENT[SOUTH],
                   MOVEMENT[WEST])
    create_file_hex(grid_hex, list(entry), list(end), pth)
    res = display_path(grid[0], solver.path,
                       width, height, entry, end, LAB)
    path_logo = [". ", "◉ ", "■ ", "🍆"]
    logo_choice = random.choice(path_logo)
    if not LAB:
        for row in res:
            line = "".join(row).center(WIDTH)
            line = line.replace("E ", colorize("E ", "green"))
            line = line.replace("S ", colorize("S ", "red"))
            line = line.replace("x ", colorize(logo_choice, "magenta"))
            if CURRENT_COLOUR:
                for ch in [
                        "┌", "┐", "└", "┘", "┬", "┴", "├", "┤", "┼", "│", "──"
                        ]:
                    line = line.replace(ch, colorize(ch, CURRENT_COLOUR))
            if SHOW:
                line = line.replace(
                    "██", colorize("██", random.choice(COLOURS)))
            else:
                line = line.replace(
                    "██", colorize("██", "white"))
            print(line)
    else:
        for row in res:
            line = "".join(row).center(WIDTH)
            line = line.replace("E ", colorize("E ", "green"))
            line = line.replace("S ", colorize("S ", "red"))
            line = line.replace("x ", colorize(logo_choice, "magenta"))
            if CURRENT_COLOUR:
                line = line.replace("+", colorize("+", CURRENT_COLOUR))
                line = line.replace("--",
                                    colorize("--", CURRENT_COLOUR))
                line = line.replace("|", colorize("|", CURRENT_COLOUR))
                if SHOW:
                    line = line.replace(
                        "██", colorize("██", random.choice(COLOURS)))
                else:
                    line = line.replace(
                        "██", colorize("██", "white"))
            print(line)


def user_choice(choice: str) -> None:
    """
    Process the user's menu choice and call the appropriate function.

    Args:
        choice: A single digit string representing the user's menu selection.
    """
    global width, height, entry, end, SHOW, INDEX, wall_42, CURRENT_COLOUR, LAB
    match choice:
        case "0":
            '''exit'''
            print()
            print(" Bye bye ! ".center(WIDTH, "¦"))
            print()
            sys.exit(0)

        case "1":
            '''maze_generator'''
            print()
            CURRENT_COLOUR = None
            INDEX = 0
            SHOW = False
            grid.clear()
            grid_hex.clear()
            gen = MazeGenerator(width, height)
            gen.generate()
            seed = parsing().get("SEED")
            if seed is not None:
                random.seed(seed)

            y, x = entry

            gen.remove_wall(x, y)

            if parsing().get("PERFECT") is True:
                grid.append(gen.grid)
                display_maze(grid, width, height, entry, end)
            else:
                gen.visited = {(y, x) for y, x in gen.visited if (y, x)
                               in wall_42}
                gen.imperfect_maze()
                grid.append(gen.grid)
                display_maze(grid, width, height, entry, end)

            for rw in gen.grid:
                grid_hex.append([format(cell, 'X') for cell in rw])
            SHOW = False
            create_file_hex(grid_hex, list(entry), list(end))
            print()

        case "2":
            '''show path'''
            print()
            SHOW = not SHOW
            if SHOW:
                try:
                    show_path()
                except Exception:
                    print(
                        "No maze generated, unable to show path!".center(WIDTH)
                        )
            else:
                display_maze(
                    grid, width, height, entry, end, CURRENT_COLOUR
                    )
            print()

        case "3":
            '''show config'''
            display_config()

        case "4":
            '''modify config'''
            while True:
                display_config()
                print()
                k = input("What do you want to modify ? >> ")
                v = input("New value >> ")
                try:
                    modify_config(k, v)
                    width = parsing()["WIDTH"]
                    height = parsing()["HEIGHT"]
                    entry = parsing()["ENTRY"]
                    end = parsing()["EXIT"]
                    wall_42 = MazeGenerator.make_42(width, height)
                except Exception as e:
                    print(e)
                q = input("Continue to modify? (y/n) >> ")
                if q.lower().strip() == "n":
                    display_config()
                    break
                elif q.lower().strip() == "y":
                    os.system('clear')
                    continue
                else:
                    os.system('clear')
                    print("Please enter a correct value")

        case "5":
            '''change colour'''
            print()
            if not SHOW:
                CURRENT_COLOUR = COLOURS[INDEX]
                display_maze(grid, width, height, entry, end, CURRENT_COLOUR)
                INDEX = (INDEX + 1) % len(COLOURS)
            else:
                CURRENT_COLOUR = COLOURS[INDEX]
                INDEX = (INDEX + 1) % len(COLOURS)
                show_path()
            print()

        case "6":
            '''maze data (hex grid)'''
            with open(output, "r") as f:
                print()
                print(" MAZE DATA ".center(WIDTH, "¦"))
                print()
                print(f.read())
                print()
                print("¦" * WIDTH)
                print()

        case "7":
            '''epilepsy mode'''
            print()
            colours = ["red", "green", "yellow", "cyan",
                       "magenta", "blue"]
            try:
                while True:
                    os.system('clear')
                    display_maze(grid, width, height, entry, end,
                                 colours[INDEX])
                    INDEX += 1
                    if INDEX >= len(colours):
                        INDEX = 0
            except KeyboardInterrupt:
                print()
                print("END OF EPILEPSY MODE, HOW FUNNY?".center(WIDTH))
                print()
            except Exception:
                print()
                print("CANNOT LAUNCH EPILEPSY MODE :(".center(WIDTH))
                print("GENERATE A MAZE FIRST".center(WIDTH))
                print()

        case "8":
            '''Maze type change'''
            print()
            LAB = not LAB
            display_maze(grid, width, height, entry, end)
            print()

        case _:
            "Please select a correct number"


def main() -> None:
    """Entry point of the program. Starts the main interaction loop."""
    sys.setrecursionlimit(4000)
    if len(sys.argv) != 2:
        print("FORMAT ERROR: USE python3 a_maze_ing.py config.txt")
        sys.exit(1)

    display_title()
    while True:
        display_options()
        choice = input("Your choice >> ")
        os.system('clear')
        choice = choice.strip()
        if choice.isdigit() and 0 <= int(choice) <= 8:
            user_choice(choice)
        else:
            blink("Please enter a valid number, from 0 to 8")


if __name__ == "__main__":
    main()
