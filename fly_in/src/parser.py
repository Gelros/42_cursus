"""Map file parser: turns a .txt map file into a validated ParsedMap."""

import re
from typing import Any

from pydantic import ValidationError

from src.models import Connexions, Hub, HubType, ParsedMap


class ParseError(Exception):
    """Raised when a map file cannot be parsed (with line context)."""


_DRONES_REGEX = r"^nb_drones:\s*(\d+)$"
_HUB_REGEX = (
    r"^(start_hub|end_hub|hub):\s+(\S+)\s+(-?\d+)\s+(-?\d+)"
    r"(?:\s+\[(.*)\])?$"
)
_CONNEXIONS_REGEX = r"^connection:\s+(\S+)-(\S+)(?:\s+\[(.*)\])?$"
_META_REGEX = r"(\w+)\s*=\s*(\S+)"


def _parse_nb_drones(line: str, line_no: int) -> int:
    """Parse a `nb_drones: N` line into a positive integer."""
    match = re.match(_DRONES_REGEX, line)
    if not match:
        raise ValueError(f"Invalid nb_drones line at {line_no}")
    nb = int(match.groups()[0])
    if nb < 1:
        raise ValueError(f"nb_drones must be >= 1, line {line_no}")
    return nb


def _parse_hub(line: str, line_no: int) -> Hub:
    """Parse a hub declaration line into a validated Hub instance."""
    match = re.match(_HUB_REGEX, line)
    if not match:
        raise ValueError(f"Invalid hub line at {line_no}: {line!r}")
    h_type_str, h_name, h_x, h_y, h_tags = match.groups()
    meta = _parse_metadata(h_tags, line_no)

    try:
        return Hub(
            hub_type=HubType(h_type_str),
            name=h_name,
            x=int(h_x),
            y=int(h_y),
            zone_type=meta.get("zone", "normal"),
            color=meta.get("color"),
            max_drones=meta.get("max_drones", 1),
        )
    except ValidationError as e:
        raise ValueError(f"Invalid hub at line {line_no}: {e}") from e


def _parse_connexion(line: str, line_no: int) -> Connexions:
    """Parse a `connection: a-b [meta]` line into a Connexions instance."""
    match = re.match(_CONNEXIONS_REGEX, line)
    if not match:
        raise ValueError(f"Invalid connection line at {line_no}")
    meta = _parse_metadata(match.group(3), line_no) if match.group(3) else {}

    try:
        return Connexions(
            param_1=match.groups()[0],
            param_2=match.groups()[1],
            max_link_capacity=meta.get("max_link_capacity", 1),
        )
    except ValidationError as e:
        raise ValueError(f"Invalid connection at line {line_no}: {e}") from e


def _parse_metadata(block: str | None, line_no: int) -> dict[str, Any]:
    """Parse a `[key=value key=value]` block into a typed dict."""
    if block is None:
        return {}

    matches = re.findall(_META_REGEX, block)
    if not matches:
        raise ValueError(f"Empty or invalid metadata at line {line_no}")

    allowed_keys = {"zone", "color", "max_drones", "max_link_capacity"}
    allowed_zones = {"normal", "blocked", "restricted", "priority"}
    int_keys = {"max_drones", "max_link_capacity"}
    result: dict[str, Any] = {}

    for key, value in matches:
        if key not in allowed_keys:
            raise ValueError(
                f"Unknown metadata key '{key}' at line {line_no}"
            )
        if key in int_keys:
            if not re.fullmatch(r"-?\d+", value):
                raise ValueError(
                    f"{key} must be an integer at line {line_no}"
                )
            ivalue = int(value)
            if ivalue < 1:
                raise ValueError(
                    f"{key} must be >= 1 at line {line_no}"
                )
            result[key] = ivalue
        elif key == "zone":
            if value not in allowed_zones:
                raise ValueError(
                    f"Invalid zone type '{value}' at line {line_no}"
                )
            result[key] = value
        else:
            result[key] = value

    return result


def parse_map(path: str) -> ParsedMap:
    """Parse a map file at *path* into a validated ParsedMap."""
    nb_drones: int | None = None
    hubs: list[Hub] = []
    connexions: list[Connexions] = []
    seen_hub_names: set[str] = set()
    seen_connections: set[frozenset[str]] = set()

    try:
        with open(path, "r", encoding="utf-8") as f:
            for count_line, raw_line in enumerate(f, start=1):
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("nb_drones:"):
                    nb_drones = _parse_nb_drones(line, count_line)
                elif line.startswith(("hub:", "start_hub:", "end_hub:")):
                    hub = _parse_hub(line, count_line)
                    if hub.name in seen_hub_names:
                        raise ParseError(
                            f"Line {count_line}: duplicate hub "
                            f"name '{hub.name}'"
                        )
                    seen_hub_names.add(hub.name)
                    hubs.append(hub)
                elif line.startswith("connection:"):
                    cnx = _parse_connexion(line, count_line)
                    key = frozenset({cnx.param_1, cnx.param_2})
                    if key in seen_connections:
                        raise ParseError(
                            f"Line {count_line}: duplicate connection "
                            f"'{cnx.param_1}-{cnx.param_2}'"
                        )
                    if cnx.param_1 not in seen_hub_names:
                        raise ParseError(
                            f"Line {count_line}: connection refers to "
                            f"undefined hub '{cnx.param_1}'"
                        )
                    if cnx.param_2 not in seen_hub_names:
                        raise ParseError(
                            f"Line {count_line}: connection refers to "
                            f"undefined hub '{cnx.param_2}'"
                        )
                    seen_connections.add(key)
                    connexions.append(cnx)
                else:
                    raise ParseError(
                        f"Line {count_line}: unknown content -> '{line}'"
                    )
    except FileNotFoundError as e:
        raise ParseError(f"File not found: {path}") from e
    except ValueError as e:
        raise ParseError(str(e)) from e

    if nb_drones is None:
        raise ParseError("Missing 'nb_drones:' declaration in map")

    try:
        return ParsedMap(
            nb_drones=nb_drones, hub=hubs, connexions=connexions
        )
    except ValidationError as e:
        raise ParseError(f"Invalid map: {e}") from e
