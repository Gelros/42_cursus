from typing import Any
from src.models import ParsedMap, Hub, Connexions, HubType, ZoneType
from pydantic import ValidationError
import re


class ParseError(Exception):
    """Erreur de parsing avec numéro de ligne."""


_DRONES_REGEX = r"^nb_drones:\s*(\d+)$"
_HUB_REGEX = r"^(start_hub|end_hub|hub):\s+(\S+)\s+(-?\d+)\s+(-?\d+)(?:\s+\[(.*)\])?$"
_CONNEXIONS_REGEX = r"^connection:\s+(\S+)-(\S+)(?:\s+\[(.*)\])?$"
_META_REGEX = r"(\w+)\s*=\s*(\S+)"


def _parse_nb_drones(line: str, line_no: int) -> int:
    match = re.match(_DRONES_REGEX, line)

    if not match:
        raise ValueError(f"Ligne invalide (nb_drones) n°: {line_no}")
    nb = int(match.groups()[0])
    if nb < 1:
        raise ValueError(f"nb_drones doit être >= 1, ligne {line_no}")
    return nb


def _parse_hub(line: str, line_no: int) -> Hub:
    match = re.match(_HUB_REGEX, line)
    if not match:
        raise ValueError(f"Ligne invalide n°: {line_no} ligne = {line}")
    h_type_str, h_name, h_x, h_y, h_tags = match.groups()
    meta_data = _parse_metadata(h_tags, line_no)

    try:
        return Hub(
            hub_type=HubType(h_type_str),
            name=h_name,
            x=int(h_x),
            y=int(h_y),
            zone_type=meta_data.get("zone", "normal"),
            color=meta_data.get("color"),
            max_drones=meta_data.get("max_drones", 1)
        )
    except ValidationError as e:
        raise ValueError(f"Hub invalide ligne {line_no}: {e}") from e


def _parse_connexion(line: str, line_no: int) -> Connexions:
    match = re.match(_CONNEXIONS_REGEX, line)
    if not match:
        raise ValueError(f"Ligne invalide (connexions) n°: {line_no}")
    meta = _parse_metadata(match.group(3), line_no) if match.group(3) else {}

    try:
        return Connexions(
            param_1=match.groups()[0],
            param_2=match.groups()[1],
            max_link_capacity=meta.get("max_link_capacity", 1)
        )
    except ValidationError as e:
        raise ValueError(f"Connexion invalide ligne {line_no}: {e}") from e


def _parse_metadata(block: str, line_no: int) -> dict[str, Any]:
    if block is None:
        return {}

    match = re.findall(_META_REGEX, block)
    if not match:
        raise ValueError(f"Metadata vide ou invalide, ligne {line_no}")

    allowed_keys = {"zone", "color", "max_drones", "max_link_capacity"}
    allowed_zones = {"normal", "blocked", "restricted", "priority"}
    int_keys = {"max_drones", "max_link_capacity"}
    result = {}

    for k, v in match:
        if not k in allowed_keys:
            raise ValueError(f"Clé metadata inconnue '{k}' ligne {line_no}")

        elif k in int_keys:
            if not re.fullmatch(r"-?\d+", v):
                raise ValueError(f"{k} doit être un entier, ligne {line_no}")
            ivalue = int(v)
            if ivalue < 1:
                raise ValueError(f"{k} doit être >= 1, ligne {line_no}")
            result[k] = ivalue

        elif k == "zone":
            if not v in allowed_zones:
                raise ValueError(f"Type de zone invalide '{v}', ligne {line_no}")
            result[k] = v
        else:
            result[k] = v
        

    return result


def parse_map(path: str) -> ParsedMap:
    try:
        nb_drones: int | None = None
        hub = []
        connexions = []

        with open(path, "r") as f:
            line_no = 0
            for count_line, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("nb_drones:"):
                    nb_drones = _parse_nb_drones(line, count_line)
                elif line.startswith(("hub:", "start_hub:", "end_hub:")):
                    hub.append(_parse_hub(line, count_line))
                elif line.startswith("connection:"):
                    connexions.append(_parse_connexion(line, count_line))
                else:
                    raise ParseError(f"Ligne {count_line} : Contenu inconnu -> '{line.strip()}'")
            if not nb_drones:
                raise ParseError(f"Pas assez de drones, ligne: {line_no}")

    except FileNotFoundError as e:
        raise ParseError(f"Fichier introuvable : {path}") from e

    try:
        return ParsedMap(nb_drones=nb_drones, hub=hub, connexions=connexions)
    except ValidationError as e:
        raise ParseError(f"Map invalide : {e}") from e
