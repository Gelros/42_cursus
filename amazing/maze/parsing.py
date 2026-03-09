import sys
from typing import Dict, Any
from maze.generator import MazeGenerator

"""
Maze configuration parser.

This module provides functionality to parse a text file describing
a maze using a simple key=value format.

Each line in the file must follow this structure:
    key=value

The parser reads the file, validates the format, and returns a
dictionary representation of the maze configuration.

Lines starting with '#' and blank lines are ignored.
"""


def str_parser(filename: str) -> Dict[str, str]:
    """Parse the content of a file into a dictionary of str"""
    try:
        with open(filename, "r") as f:
            result = [line.strip().split("=", 1) for line in f.readlines()]
            try:
                dict_result = {r[0]: r[1] for r in result if r[0]
                               and not r[0].startswith("#")}
            except Exception:
                print("🚨ERROR: INVALID FORMAT, MUST USE KEY=VALUE🚨")
                sys.exit(1)
            return dict_result
    except FileNotFoundError:
        print("🚨ERROR: CONFIG FILE NOT FOUND🚨")
        sys.exit(1)


def convert_type(raw_dict: Dict[str, str]) -> Dict[str, Any]:
    """Convert the datas of the dict in the right type"""
    converted: Dict[str, Any] = {}

    for k, v in raw_dict.items():
        k = k.strip().upper()
        v = v.strip()
        if v == "":
            raise ValueError(f"MISSING {k} VALUE")

        match k:
            case "WIDTH" | "HEIGHT":
                converted[k] = int(v)

            case "ENTRY" | "EXIT":
                if isinstance(v, str):
                    v = v.strip("()")
                    split_v = v.split(",")
                    if len(split_v) != 2:
                        raise ValueError(f"INVALID FORMAT FOR {k}")
                    try:
                        converted[k] = tuple(int(part.strip())
                                             for part in split_v)
                    except ValueError:
                        raise ValueError(f"{k} MUST CONTAIN INTEGERS")
                else:
                    converted[k] = v

            case "OUTPUT_FILE":
                converted[k] = v

            case "PERFECT":
                if isinstance(v, str):
                    if v.lower() not in ["true", "false"]:
                        raise ValueError(
                            f"{k} MUST BE A BOOLEAN (True / False)")
                    converted[k] = (v.lower() == "true")
                else:
                    converted[k] = v

            case _:
                converted[k] = v
    return converted


def validate_data(datas: Dict[str, Any]) -> None:
    '''Check if datas are coherent and handle errors'''
    mandatory_keys = {"WIDTH", "HEIGHT", "ENTRY",
                      "EXIT", "OUTPUT_FILE", "PERFECT"}
    missing = mandatory_keys - datas.keys()
    if missing:
        raise KeyError("MISSING A MANDATORY KEY, UNABLE TO GENERATE THE MAZE")
    wall_42 = MazeGenerator.make_42(datas["WIDTH"], datas["HEIGHT"])

    if datas["WIDTH"] <= 1 or datas["HEIGHT"] <= 1:
        raise ValueError("WIDTH/HEIGHT MUST BE GREATER THAN 1")

    if datas["WIDTH"] >= 100 or datas["HEIGHT"] >= 100:
        raise ValueError("WIDTH/HEIGHT MUST BE LOWER THAN 950")

    if datas["ENTRY"] == datas["EXIT"]:
        raise ValueError("ENTRY AND EXIT MUST BE DIFFERENT")

    if datas["ENTRY"] in wall_42 or datas["EXIT"] in wall_42:
        raise ValueError("ENTRY/EXIT CANNOT BE INSIDE THE 42 LOGO")

    for k in ("ENTRY", "EXIT"):
        y, x = datas[k]
        if x < 0 or x >= datas["WIDTH"] or y < 0 or y >= datas["HEIGHT"]:
            raise ValueError(f"{k} OUT OF BOUNDARIES / USE (Y, X) FORMAT")

    if not datas["OUTPUT_FILE"].endswith(".txt"):
        raise ValueError("OUTPUT FILE MUST END BY .txt")


def parsing() -> Dict[str, Any]:
    '''Parse the config file and handle errors'''
    path = "config.txt"
    raw = str_parser(path)
    try:
        right_type = convert_type(raw)
        validate_data(right_type)
    except Exception as e:
        print(f"🚨​ERROR: {e} 🚨​")
        sys.exit(1)
    return right_type
