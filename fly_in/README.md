_This project has been created as part of the 42 curriculum by guilacol._

# fly_in

## Description

**fly_in** is a drone routing simulator written in Python. Given a textual
description of a network (hubs and connexions with capacities, zones, and
costs), the program computes how to move all drones from a single start hub
to a single end hub in the fewest possible simulation turns, then prints
their movements turn by turn.

The map format and the simulation rules follow the 42 *fly_in* subject:

- The graph has a unique `start_hub`, a unique `end_hub`, and any number of
  intermediate `hub`s.
- Hubs may carry a `zone` type — `normal`, `priority`, `restricted`, or
  `blocked` — that influences pathfinding cost or accessibility.
- Hubs may carry a `max_drones` limit and connexions a `max_link_capacity`
  limit, which constrain the number of drones simultaneously sharing a
  vertex or an edge.
- Drones move turn by turn; the goal is to deliver every drone to the end
  hub while respecting all capacity constraints.

The project is fully **object-oriented**, fully **type-checked** (passes
`mypy --strict`), fully **flake8-clean**, and tested with **pytest**.

## Instructions

Requires Python 3.10+ and the [`uv`](https://docs.astral.sh/uv/) package
manager (or any other resolver of your choice — a `pyproject.toml` is
provided).

### Install

```sh
make install
```

This runs `uv sync --dev`, which installs all production and development
dependencies into a local virtual environment.

### Run

The default entry point reads a map and prints the simulation. Two output
modes are available:

```sh
# Subject-conformant output (one line per turn, "Dn-hub" tokens):
uv run python -m src maps/easy/02_simple_fork.txt --raw

# Rich-styled console output (header panel + colored table):
uv run python -m src maps/easy/02_simple_fork.txt
```

The provided `Makefile` exposes shortcuts:

```sh
make run            # runs the default map with Rich rendering
make debug          # runs the program under pdb
make lint           # flake8 + mypy with subject flags
make lint-strict    # flake8 + mypy --strict
make test           # full pytest suite
make clean          # removes caches and build artefacts
```

### Output format

In `--raw` mode, the program emits one line per simulation turn. Each line
lists every drone in flight separated by spaces, in the format
`D<id>-<hub>`:

```
D0-start
D0-junction D1-start
D0-path_a D1-junction D2-start
D0-goal D1-path_a D2-junction
D1-goal D2-path_a
D2-goal
```

In Rich mode, the same data is rendered as a colored table with a header
panel summarising the map metadata (drones, hubs, makespan).

### Available maps

The `maps/` directory ships with ten levels grouped by difficulty.
Reference targets come from the subject (Section VII.7).

| Path | Drones | Target ≤ | Solver |
|---|---:|---:|---:|
| `maps/easy/01_linear_path.txt` | 2 | 6 | 5 |
| `maps/easy/02_simple_fork.txt` | 3 | 6 | 6 |
| `maps/easy/03_basic_capacity.txt` | 4 | 8 | 7 |
| `maps/medium/01_dead_end_trap.txt` | 5 | 15 | 9 |
| `maps/medium/02_circular_loop.txt` | 6 | 20 | 12 |
| `maps/medium/03_priority_puzzle.txt` | 4 | 12 | 8 |
| `maps/hard/01_maze_nightmare.txt` | 8 | 45 | 15 |
| `maps/hard/02_capacity_hell.txt` | 12 | 60 | 19 |
| `maps/hard/03_ultimate_challenge.txt` | 15 | 35 | 27 |
| `maps/challenger/01_the_impossible_dream.txt` | 25 | 45 (record) | 44 |

Run any of them with:

```sh
make run     MAP=maps/<difficulty>/<file>.txt   # Rich UI
make run-raw MAP=maps/<difficulty>/<file>.txt   # subject format
make debug   MAP=maps/<difficulty>/<file>.txt   # under pdb
```

## Algorithm

The pipeline is split into focused, independently testable modules:

| Module | Role |
|---|---|
| `src/parser.py` | Tokenise and validate the map file into a `ParsedMap`. |
| `src/models.py` | Pydantic data models (`Hub`, `Connexions`, `ParsedMap`). |
| `src/graph.py` | Build a `Graph` of `Node`s and `Edge`s with bidirectional capacities and flow tracking. |
| `src/pathfinder.py` | Compute augmenting paths (min-cost max-flow with Dijkstra on the residual). |
| `src/scheduler.py` | Greedy assignment of drones to paths minimising the makespan. |
| `src/simulator.py` | Replay assignments turn by turn into a list of `TurnState`. |
| `src/renderer.py` | Two-mode console rendering (raw subject format / Rich UI). |
| `src/solver.py` | Orchestrator wiring all modules together. |
| `src/__main__.py` | CLI entry point. |

### Pathfinding — min-cost max-flow

The core algorithm is a **min-cost max-flow** based on the Edmonds-Karp
template, where the augmenting-path search is **Dijkstra on the residual
graph**:

1. Build a residual graph with forward/backward edges (initialised with the
   declared `max_link_capacity` and zero flow).
2. While Dijkstra finds a path from `start` to `end` whose every edge has a
   strictly positive residual capacity:
   - Compute the bottleneck (minimum residual on the path).
   - Push that amount of flow forward along the path and subtract it from
     the reverse residual edges.
   - Record the path once per unit of flow pushed.
3. When Dijkstra finally returns `None`, every disjoint route the network
   can carry simultaneously has been found.

Dijkstra is preferred over a plain BFS because it accounts for **per-zone
costs**: a `restricted` hub costs 2 turns to traverse, a `normal` or
`priority` hub costs 1, and a `blocked` hub is infinite (skipped). On maps
that mix zones, this makes the solver pick paths that minimise *total time*
rather than *number of edges*.

### Scheduling — greedy makespan minimisation

The pathfinder returns a multiset of paths (each entry represents one
drone-slot per turn). The scheduler picks, for each drone in turn, the
path that yields the smallest end turn given the drones already assigned.
The next start turn for a path is `(assigned // capacity) + 1`, ensuring
the per-turn capacity is never exceeded.

### Simulation

The `Simulator` builds, for each turn from 1 to the makespan, a `TurnState`
that lists drones currently in flight (with their hub) and drones that
have already arrived. Flying drones are detected by their start/end-turn
window; arrived drones are tracked cumulatively.

### Visual representation

Two output modes are exposed:

- **Raw mode** (`--raw`) writes the canonical subject format directly to
  `stdout` — easy to diff, parse, and check against the scoring rules.
- **Rich mode** uses the `rich` library to render a header panel with
  map metadata and a colored table where each drone keeps a stable color
  across turns. This is the default when no flag is given.

## Resources

- *Introduction to Algorithms* (CLRS), chapters on graph algorithms,
  shortest paths (Dijkstra), and max-flow / Ford-Fulkerson.
- Edmonds-Karp algorithm: original paper "Theoretical Improvements in
  Algorithmic Efficiency for Network Flow Problems" (Edmonds & Karp,
  1972).
- `heapq` and `itertools.count` documentation from the Python standard
  library, used to implement Dijkstra without an external priority queue.
- [Rich](https://rich.readthedocs.io/) and
  [Pydantic](https://docs.pydantic.dev/) official documentation.
- 42 *lem-in* subject (closely related routing problem), used as a mental
  model for the disjoint-paths formulation.

### About AI usage

This project was developed with the help of an AI coding assistant
(Claude). AI was used as a **paired-programming partner** for the
following tasks:

- Brainstorming the architecture (modules, responsibilities, types).
- Writing the initial test scaffolding, then iterating on edge cases.
- Explaining theory (BFS / Dijkstra / max-flow / min-cost max-flow), the
  residual-graph trick, and the consequences of using Dijkstra instead of
  BFS for augmenting paths.
- Reviewing flake8 / mypy reports and proposing minimal-impact fixes.
- Drafting docstrings and this README.

Every line of code was read, understood, and validated manually before
being committed; the AI did not produce any unreviewed code. The
architectural decisions, the algorithm choice, and the implementation
are mine. AI was deliberately **not** used to write any algorithmic core
without first understanding the underlying mathematics.

## Known limitations

- The connection naming for in-transit drones (subject format
  `D<id>-<connection>`) uses a synthetic identifier `<src>~<dst>` because
  the map format does not name connections explicitly. For instance, a
  drone in transit toward `overflow_hell1` (restricted) coming from
  `micro_gate1` is reported as `D0-micro_gate1~overflow_hell1` for one
  turn, then `D0-overflow_hell1` once the drone has actually reached the
  destination hub. This keeps capacity rules unambiguous: only the
  arrival turn counts against the destination's `max_drones`.
- The scheduler is a greedy heuristic; for some pathological topologies a
  more sophisticated joint optimisation (e.g. flow-based scheduling) could
  yield strictly fewer turns.
