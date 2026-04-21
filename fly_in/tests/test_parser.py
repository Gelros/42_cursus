"""
Battery of tests for src/parser.py

Run with:
    uv run pytest tests/test_parser.py -v
    uv run pytest tests/test_parser.py -v --tb=short   # shorter tracebacks
"""

import pytest
from pathlib import Path

from src.parser import (
    ParseError,
    _parse_nb_drones,
    _parse_hub,
    _parse_connexion,
    _parse_metadata,
    parse_map,
)
from src.models import HubType, ZoneType


# ──────────────────────────────────────────────────────────────────────────────
# Helpers / fixtures
# ──────────────────────────────────────────────────────────────────────────────

def make_map(tmp_path: Path, content: str) -> str:
    """Write a temporary map file and return its path as str."""
    p = tmp_path / "test_map.txt"
    p.write_text(content)
    return str(p)


MINIMAL_VALID_MAP = """\
nb_drones: 2
start_hub: start 0 0 [color=green]
hub: mid 1 0 [color=blue]
end_hub: goal 2 0 [color=red]
connection: start-mid
connection: mid-goal
"""


# ──────────────────────────────────────────────────────────────────────────────
# 1. _parse_nb_drones
# ──────────────────────────────────────────────────────────────────────────────

class TestParseNbDrones:

    def test_returns_integer(self):
        result = _parse_nb_drones("nb_drones: 5", 1)
        assert result == 5
        assert isinstance(result, int)

    def test_single_drone(self):
        assert _parse_nb_drones("nb_drones: 1", 1) == 1

    def test_large_number(self):
        assert _parse_nb_drones("nb_drones: 100", 1) == 100

    def test_extra_spaces(self):
        # Format avec espaces multiples — doit matcher ou lever une erreur claire
        result = _parse_nb_drones("nb_drones:  25", 1)
        assert result == 25

    def test_missing_value_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_nb_drones("nb_drones:", 1)

    def test_zero_raises(self):
        """0 drone n'a pas de sens."""
        with pytest.raises((ValueError, ParseError)):
            _parse_nb_drones("nb_drones: 0", 1)

    def test_negative_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_nb_drones("nb_drones: -3", 1)

    def test_float_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_nb_drones("nb_drones: 2.5", 1)

    def test_garbage_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_nb_drones("nb_drones: abc", 1)

    def test_wrong_key_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_nb_drones("drones: 5", 1)


# ──────────────────────────────────────────────────────────────────────────────
# 2. _parse_hub
# ──────────────────────────────────────────────────────────────────────────────

class TestParseHub:

    # --- hub types ---

    def test_start_hub(self):
        hub = _parse_hub("start_hub: start 0 0 [color=green]", 1)
        assert hub.hub_type == HubType.START
        assert hub.name == "start"

    def test_end_hub(self):
        hub = _parse_hub("end_hub: goal 10 10 [color=red]", 1)
        assert hub.hub_type == HubType.END
        assert hub.name == "goal"

    def test_regular_hub(self):
        hub = _parse_hub("hub: waypoint 3 4 [color=blue]", 1)
        assert hub.hub_type == HubType.NORMAL

    # --- coordinates ---

    def test_positive_coords(self):
        hub = _parse_hub("hub: A 3 7 [color=blue]", 1)
        assert hub.x == 3
        assert hub.y == 7

    def test_negative_coords(self):
        hub = _parse_hub("hub: B -2 -5 [color=red]", 1)
        assert hub.x == -2
        assert hub.y == -5

    def test_zero_coords(self):
        hub = _parse_hub("hub: origin 0 0 [color=green]", 1)
        assert hub.x == 0
        assert hub.y == 0

    # --- name ---

    def test_name_parsed(self):
        hub = _parse_hub("hub: my_zone 1 1 [color=blue]", 1)
        assert hub.name == "my_zone"

    def test_name_with_numbers(self):
        hub = _parse_hub("hub: waypoint2 2 0 [color=blue]", 1)
        assert hub.name == "waypoint2"

    def test_name_with_dash_raises(self):
        with pytest.raises(Exception):
            _parse_hub("hub: bad-name 1 1 [color=blue]", 1)

    # --- metadata defaults ---

    def test_no_metadata_defaults(self):
        """Un hub sans [] doit avoir les valeurs par défaut."""
        hub = _parse_hub("hub: bare 1 1", 1)
        assert hub.zone_type == ZoneType.NORMAL
        assert hub.max_drones == 1
        assert hub.color is None

    def test_metadata_color(self):
        hub = _parse_hub("hub: A 1 0 [color=blue]", 1)
        assert hub.color == "blue"

    def test_metadata_max_drones(self):
        hub = _parse_hub("hub: A 1 0 [color=orange max_drones=4]", 1)
        assert hub.max_drones == 4

    def test_metadata_zone_restricted(self):
        hub = _parse_hub("hub: slow 2 2 [zone=restricted color=red]", 1)
        assert hub.zone_type == ZoneType.RESTRICTED

    def test_metadata_zone_priority(self):
        hub = _parse_hub("hub: fast 2 2 [zone=priority color=cyan]", 1)
        assert hub.zone_type == ZoneType.PRIORITY

    def test_metadata_zone_blocked(self):
        hub = _parse_hub("hub: wall 5 5 [zone=blocked color=gray]", 1)
        assert hub.zone_type == ZoneType.BLOCKED

    def test_metadata_all_keys(self):
        hub = _parse_hub(
            "hub: complex 3 3 [zone=priority color=lime max_drones=2]", 1
        )
        assert hub.zone_type == ZoneType.PRIORITY
        assert hub.color == "lime"
        assert hub.max_drones == 2

    def test_invalid_line_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_hub("hub: 1 2", 1)  # manque le nom

    def test_float_coords_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_hub("hub: A 1.5 2.0 [color=blue]", 1)


# ──────────────────────────────────────────────────────────────────────────────
# 3. _parse_connexion
# ──────────────────────────────────────────────────────────────────────────────

class TestParseConnexion:

    def test_basic_connection(self):
        conn = _parse_connexion("connection: start-goal", 1)
        assert conn.param_1 == "start"
        assert conn.param_2 == "goal"

    def test_default_capacity(self):
        conn = _parse_connexion("connection: a-b", 1)
        assert conn.max_link_capacity == 1

    def test_custom_capacity(self):
        conn = _parse_connexion("connection: gate1-gate2 [max_link_capacity=3]", 1)
        assert conn.max_link_capacity == 3

    def test_capacity_one_explicit(self):
        conn = _parse_connexion("connection: a-b [max_link_capacity=1]", 1)
        assert conn.max_link_capacity == 1

    def test_both_zones_parsed(self):
        conn = _parse_connexion("connection: zone_a-zone_b", 1)
        assert conn.param_1 == "zone_a"
        assert conn.param_2 == "zone_b"

    def test_invalid_line_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_connexion("connection: onlyone", 1)

    def test_missing_zones_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_connexion("connection:", 1)


# ──────────────────────────────────────────────────────────────────────────────
# 4. _parse_metadata
# ──────────────────────────────────────────────────────────────────────────────

class TestParseMetadata:

    def test_color_only(self):
        result = _parse_metadata("color=green", 1)
        assert result["color"] == "green"

    def test_zone_normal(self):
        result = _parse_metadata("zone=normal", 1)
        assert result["zone"] == "normal"

    def test_zone_priority(self):
        result = _parse_metadata("zone=priority", 1)
        assert result["zone"] == "priority"

    def test_zone_restricted(self):
        result = _parse_metadata("zone=restricted", 1)
        assert result["zone"] == "restricted"

    def test_zone_blocked(self):
        result = _parse_metadata("zone=blocked", 1)
        assert result["zone"] == "blocked"

    def test_max_drones_int(self):
        result = _parse_metadata("max_drones=4", 1)
        assert result["max_drones"] == 4
        assert isinstance(result["max_drones"], int)

    def test_max_link_capacity_int(self):
        result = _parse_metadata("max_link_capacity=2", 1)
        assert result["max_link_capacity"] == 2

    def test_multiple_keys(self):
        result = _parse_metadata("zone=priority color=cyan max_drones=2", 1)
        assert result["zone"] == "priority"
        assert result["color"] == "cyan"
        assert result["max_drones"] == 2

    def test_key_order_irrelevant(self):
        r1 = _parse_metadata("color=blue zone=normal", 1)
        r2 = _parse_metadata("zone=normal color=blue", 1)
        assert r1 == r2

    def test_unknown_key_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_metadata("unknown_key=value", 1)

    def test_invalid_zone_type_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_metadata("zone=invisible", 1)

    def test_max_drones_zero_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_metadata("max_drones=0", 1)

    def test_max_drones_negative_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_metadata("max_drones=-1", 1)

    def test_max_drones_float_raises(self):
        with pytest.raises((ValueError, ParseError)):
            _parse_metadata("max_drones=1.5", 1)

    def test_none_returns_empty(self):
        """Pas de bloc metadata → dict vide, pas d'exception."""
        result = _parse_metadata(None, 1)
        assert result == {}

    def test_multiword_color(self):
        """Couleurs composées genre 'darkred' doivent passer."""
        result = _parse_metadata("color=darkred", 1)
        assert result["color"] == "darkred"


# ──────────────────────────────────────────────────────────────────────────────
# 5. parse_map — cas valides avec les vraies cartes
# ──────────────────────────────────────────────────────────────────────────────

MAPS_DIR = Path("maps")


@pytest.mark.parametrize("map_path,expected_drones,expected_hubs,expected_conns", [
    # easy
    ("easy/01_linear_path.txt",    2, 4, 3),
    ("easy/02_simple_fork.txt",    3, 5, 5),
    ("easy/03_basic_capacity.txt", 4, 4, 3),
    # medium
    ("medium/01_dead_end_trap.txt",   5, 6, 5),
    ("medium/02_circular_loop.txt",   6, None, None),  # counts non-testés ici
    ("medium/03_priority_puzzle.txt", 4, 8, 8),
])
def test_real_maps_parse_without_error(map_path, expected_drones, expected_hubs, expected_conns):
    """Les vraies cartes doivent parser sans exception."""
    path = str(MAPS_DIR / map_path)
    result = parse_map(path)

    assert result.nb_drones == expected_drones

    if expected_hubs is not None:
        assert len(result.hub) == expected_hubs

    if expected_conns is not None:
        assert len(result.connexions) == expected_conns


class TestParseMapStructure:

    def test_minimal_map(self, tmp_path):
        path = make_map(tmp_path, MINIMAL_VALID_MAP)
        result = parse_map(path)

        assert result.nb_drones == 2
        assert len(result.hub) == 3        # start + mid + end
        assert len(result.connexions) == 2

    def test_start_hub_identified(self, tmp_path):
        path = make_map(tmp_path, MINIMAL_VALID_MAP)
        result = parse_map(path)
        starts = [h for h in result.hub if h.hub_type == HubType.START]
        assert len(starts) == 1
        assert starts[0].name == "start"

    def test_end_hub_identified(self, tmp_path):
        path = make_map(tmp_path, MINIMAL_VALID_MAP)
        result = parse_map(path)
        ends = [h for h in result.hub if h.hub_type == HubType.END]
        assert len(ends) == 1
        assert ends[0].name == "goal"

    def test_comments_ignored(self, tmp_path):
        content = """\
# this is a comment
nb_drones: 3
# another comment
start_hub: s 0 0 [color=green]
end_hub: e 1 0 [color=red]
connection: s-e
"""
        path = make_map(tmp_path, content)
        result = parse_map(path)
        assert result.nb_drones == 3

    def test_empty_lines_ignored(self, tmp_path):
        content = """\
nb_drones: 2

start_hub: s 0 0 [color=green]

end_hub: e 1 0 [color=red]

connection: s-e
"""
        path = make_map(tmp_path, content)
        result = parse_map(path)
        assert len(result.hub) == 2

    def test_zone_types_propagated(self, tmp_path):
        content = """\
nb_drones: 1
start_hub: s 0 0 [color=green]
hub: slow 1 0 [zone=restricted color=red]
hub: fast 2 0 [zone=priority color=cyan]
hub: wall 3 0 [zone=blocked color=gray]
end_hub: e 4 0 [color=green]
connection: s-slow
connection: s-fast
connection: fast-e
"""
        path = make_map(tmp_path, content)
        result = parse_map(path)

        by_name = {h.name: h for h in result.hub}
        assert by_name["slow"].zone_type == ZoneType.RESTRICTED
        assert by_name["fast"].zone_type == ZoneType.PRIORITY
        assert by_name["wall"].zone_type == ZoneType.BLOCKED

    def test_max_drones_propagated(self, tmp_path):
        content = """\
nb_drones: 4
start_hub: s 0 0 [color=green max_drones=4]
hub: bottle 1 0 [color=orange max_drones=2]
end_hub: e 2 0 [color=red max_drones=4]
connection: s-bottle
connection: bottle-e
"""
        path = make_map(tmp_path, content)
        result = parse_map(path)

        by_name = {h.name: h for h in result.hub}
        assert by_name["s"].max_drones == 4
        assert by_name["bottle"].max_drones == 2

    def test_connection_capacity_propagated(self, tmp_path):
        content = """\
nb_drones: 2
start_hub: s 0 0 [color=green]
end_hub: e 1 0 [color=red]
connection: s-e [max_link_capacity=3]
"""
        path = make_map(tmp_path, content)
        result = parse_map(path)
        assert result.connexions[0].max_link_capacity == 3


# ──────────────────────────────────────────────────────────────────────────────
# 6. parse_map — cas d'erreur
# ──────────────────────────────────────────────────────────────────────────────

class TestParseMapErrors:

    def test_file_not_found(self):
        with pytest.raises((FileNotFoundError, ParseError, Exception)):
            parse_map("maps/nonexistent/missing.txt")

    def test_missing_nb_drones(self, tmp_path):
        content = """\
start_hub: s 0 0 [color=green]
end_hub: e 1 0 [color=red]
connection: s-e
"""
        path = make_map(tmp_path, content)
        with pytest.raises((ParseError, Exception)):
            parse_map(path)

    def test_unknown_line_raises(self, tmp_path):
        content = """\
nb_drones: 2
start_hub: s 0 0 [color=green]
end_hub: e 1 0 [color=red]
connection: s-e
this_is_garbage
"""
        path = make_map(tmp_path, content)
        with pytest.raises((ParseError, ValueError)):
            parse_map(path)

    def test_invalid_zone_type_in_map(self, tmp_path):
        content = """\
nb_drones: 1
start_hub: s 0 0 [color=green]
hub: bad 1 0 [zone=invisible color=red]
end_hub: e 2 0 [color=red]
connection: s-bad
connection: bad-e
"""
        path = make_map(tmp_path, content)
        with pytest.raises((ValueError, ParseError)):
            parse_map(path)

    def test_invalid_max_drones_zero(self, tmp_path):
        content = """\
nb_drones: 1
start_hub: s 0 0 [color=green]
hub: bad 1 0 [max_drones=0]
end_hub: e 2 0 [color=red]
connection: s-bad
connection: bad-e
"""
        path = make_map(tmp_path, content)
        with pytest.raises((ValueError, ParseError)):
            parse_map(path)

    def test_zero_drones_raises(self, tmp_path):
        content = """\
nb_drones: 0
start_hub: s 0 0 [color=green]
end_hub: e 1 0 [color=red]
connection: s-e
"""
        path = make_map(tmp_path, content)
        with pytest.raises((ValueError, ParseError)):
            parse_map(path)

    def test_name_with_dash_raises(self, tmp_path):
        content = """\
nb_drones: 1
start_hub: bad-name 0 0 [color=green]
end_hub: e 1 0 [color=red]
connection: bad-name-e
"""
        path = make_map(tmp_path, content)
        with pytest.raises(Exception):
            parse_map(path)


# ──────────────────────────────────────────────────────────────────────────────
# 7. Tests hard / challenger (smoke tests — juste "ça parse sans crash")
# ──────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("map_path", [
    "hard/01_maze_nightmare.txt",
    "hard/02_capacity_hell.txt",
    "hard/03_ultimate_challenge.txt",
    "challenger/01_the_impossible_dream.txt",
])
def test_hard_maps_smoke(map_path):
    """Les cartes complexes doivent parser sans lever d'exception."""
    result = parse_map(str(MAPS_DIR / map_path))
    assert result.nb_drones >= 1
    assert len(result.hub) > 0
    assert len(result.connexions) > 0
