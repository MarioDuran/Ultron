from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
BASE = "S000"
OUTLET = "OUTLET"


@dataclass
class CaseData:
    stations: list[str]
    roads: list[tuple[str, str, int, int]]
    conflict_edges: list[tuple[str, str]]
    pipes: list[tuple[str, str, int]]
    checkpoints: list[str]
    travel_graph: dict[str, list[tuple[str, int]]]
    cable_graph: dict[str, list[tuple[str, int]]]
    conflict_graph: dict[str, set[str]]
    pipe_graph: dict[str, list[tuple[str, int]]]


def read_csv(name: str) -> list[dict[str, str]]:
    """Read a file from ./data. utf-8-sig also accepts CSVs with a BOM."""
    with (DATA / name).open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def make_undirected_graph(
    nodes: list[str], edges: list[tuple[str, str, int]]
) -> dict[str, list[tuple[str, int]]]:
    graph = {node: [] for node in nodes}
    for a, b, weight in edges:
        graph[a].append((b, weight))
        graph[b].append((a, weight))
    return graph


def make_directed_graph(
    nodes: list[str], edges: list[tuple[str, str, int]]
) -> dict[str, list[tuple[str, int]]]:
    graph = {node: [] for node in nodes}
    for a, b, capacity in edges:
        graph[a].append((b, capacity))
    return graph


def load_case() -> CaseData:
    """Load and validate all inputs, retaining distinct models for each network."""
    station_rows = read_csv("stations.csv")
    road_rows = read_csv("roads.csv")
    conflict_rows = read_csv("interference.csv")
    pipe_rows = read_csv("pipes.csv")
    checkpoint_rows = read_csv("checkpoints.csv")

    stations = [r["id"] for r in station_rows]
    assert len(stations) == 196 and len(set(stations)) == 196
    assert stations == [f"S{i:03d}" for i in range(196)]
    station_set = set(stations)

    roads = [(r["source"], r["target"], int(r["travel_minutes"]),
              int(r["cable_cost"])) for r in road_rows]
    assert len(roads) == 690
    assert all(a in station_set and b in station_set and a != b and t > 0 and c > 0
               for a, b, t, c in roads)
    assert len({tuple(sorted((a, b))) for a, b, _, _ in roads}) == len(roads)

    conflict_edges = [(r["node_a"], r["node_b"]) for r in conflict_rows]
    assert len(conflict_edges) == 1000
    assert all(a in station_set and b in station_set and a != b
               for a, b in conflict_edges)
    assert len({tuple(sorted((a, b))) for a, b in conflict_edges}) == len(conflict_edges)

    pipes = [(r["source"], r["target"], int(r["capacity_per_minute"]))
             for r in pipe_rows]
    assert len(pipes) == 689
    hydraulic_nodes = station_set | {"SOURCE", "OUTLET"}
    assert all(a in hydraulic_nodes and b in hydraulic_nodes and a != b and cap > 0
               for a, b, cap in pipes)
    assert len({(a, b) for a, b, _ in pipes}) == len(pipes)

    checkpoints = [r["station_id"] for r in checkpoint_rows]
    assert len(checkpoints) == 12 and len(set(checkpoints)) == 12
    assert all(p in station_set and p != BASE for p in checkpoints)

    travel_graph = make_undirected_graph(stations, [(a, b, t) for a, b, t, _ in roads])
    cable_graph = make_undirected_graph(stations, [(a, b, c) for a, b, _, c in roads])
    conflict_graph: dict[str, set[str]] = {s: set() for s in stations}
    for a, b in conflict_edges:
        conflict_graph[a].add(b)
        conflict_graph[b].add(a)
    pipe_graph = make_directed_graph(sorted(hydraulic_nodes), pipes)

    return CaseData(stations, roads, conflict_edges, pipes, checkpoints,
                    travel_graph, cable_graph, conflict_graph, pipe_graph)


# ------- Your work starts here. Implement the algorithms named below. -------


def times_from_one_station(graph: dict[str, list[tuple[str, int]]], start: str) -> dict[str, int]:
    """TODO (Dijkstra): shortest travel times from a single starting station."""
    raise NotImplementedError


def times_between_all_stations(graph: dict[str, list[tuple[str, int]]]) -> dict[str, dict[str, int]]:
    """TODO (Floyd-Warshall): shortest travel times for all pairs of stations."""
    raise NotImplementedError


def cheapest_backbone(
    stations: list[str], roads: list[tuple[str, str, int, int]], approach: str
) -> tuple[list[tuple[str, str]], int]:
    """TODO (Prim and Kruskal): minimum spanning tree using cable costs.

    Implement both: approach='grow' for Prim and approach='sort' for Kruskal.
    Compare the costs, and inspect the chosen tree edges.
    """
    raise NotImplementedError


def frequency_assignment(conflicts: dict[str, set[str]]) -> dict[str, int]:
    """TODO (graph coloring): use the minimum possible frequencies."""
    raise NotImplementedError


def inspection_loop(
    start: str, checkpoints: list[str], distances: dict[str, dict[str, int]]
) -> tuple[int, list[str]]:
    """TODO (Traveling Salesperson / Held-Karp): exact tour, ties lexicographic.

    The returned station sequence should begin and end at 'start'.
    """
    raise NotImplementedError


def maximum_delivery(
    pipes: list[tuple[str, str, int]], injection: str, outlet: str
) -> int:
    """TODO (maximum flow): Ford-Fulkerson or Edmonds-Karp.

    Follow directed edges and do not assign a supply limit to 'injection'.
    """
    raise NotImplementedError


def investigate(case: CaseData) -> None:
    """TODO: apply the six clues from README.md in order.

    Suggested structure:
      1. Begin with all 196 station IDs.
      2. Compute the evidence required by each clue.
      3. Filter candidates after every clue, recording the remaining IDs.
      4. Show the chosen station and why the other candidates are excluded.
    """
    raise NotImplementedError


def main() -> None:
    case = load_case()
    print("Operation Ultron Loaded")
    print(f"Stations:       {len(case.stations)}")
    print(f"Roads:          {len(case.roads)} (undirected)")
    print(f"Radio conflicts:{len(case.conflict_edges):>5} (undirected)")
    print(f"Pipes:          {len(case.pipes)} (directed)")
    print(f"Checkpoints:    {len(case.checkpoints)} (unordered)")
    print("Graphs ready. Complete the TODO functions to begin the investigation.")
    # When ready, uncomment the next line:
    # investigate(case)


if __name__ == "__main__":
    main()
