from pathlib import Path
import networkx as nx
from pyvis.network import Network

RULES_FILE = "ex_impl\\courses.txt"
OUTPUT_HTML = "graph.html"

# parses line "A & B -> C" into (["A", "B"], "C")
def parse_implication_line(line: str):
    line = line.strip()

    implies = "->"
    left = right = None
    if implies in line:
        left, right = line.split(implies, 1)
    if left is None or right is None:
        raise ValueError(f"Could not parse rule line: {line!r}")

    left = left.strip()
    right = right.strip()
    if not left or not right:
        raise ValueError(f"Missing requirements: {line!r}")

    prereqs = [p.strip() for p in left.split("&") if p.strip()]

    return prereqs, right

# loads implication sentence lines of "A -> B" and returns a list of (A, B) pairs.
def load_implications_from_file(path: Path):
    implications = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pair = parse_implication_line(line)
            if pair is not None:
                implications.append(pair)
    return implications

# builds a directed graph from (A,B) pairs
def build_directed_graph(implications):
    G = nx.DiGraph()
    for prereqs, course in implications:
        G.add_node(course)
        for prereq in prereqs:
            G.add_node(prereq)
            G.add_edge(prereq, course)
    return G

def build_graph(G: nx.DiGraph):
    # undirected copy for layout
    undirected = nx.Graph()
    undirected.add_nodes_from(G.nodes())
    undirected.add_edges_from(G.edges())

    # pyvis network
    net = Network(
        height="750px",
        width="100%",
        bgcolor="#ffffff",
        font_color="#000000",
        directed=True
    )

    net.barnes_hut()
    net.show_buttons(filter_=["physics"])

    for node in undirected.nodes():
        net.add_node(
            node,
            label=str(node),
            shape="dot",
            size=14,
        )

    for u, v in G.edges():
        net.add_edge(u, v, color="#006aff", width=4)

    return net

def analyze_node(G: nx.DiGraph, start_node):
    if start_node not in G:
        raise ValueError(f"Node {start_node!r} not in graph.")
    
    reachable = nx.descendants(G, start_node)

    paths = {}
    for target in reachable:
        paths[target] = list(nx.shortest_path(G, start_node, target))
    return reachable, paths


def main():
    here = Path(__file__).resolve().parent
    rules_path = here / RULES_FILE
    implications = load_implications_from_file(rules_path)

    print(f"Loaded {len(implications)} implications from {RULES_FILE}.")

    G = build_directed_graph(implications)
    print(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    net = build_graph(G)

    output_path = here / OUTPUT_HTML
    net.show(str(output_path), notebook=False)

    print("Nodes in graph:", ", ".join(sorted(G.nodes())))
    print()

    while True:
        start = input("Enter a start node to analyze (or 'q' to quit): ").strip()
        if not start:
            continue
        if start.lower() in {"q", "quit", "exit"}:
            break

        if start not in G:
            print(f"Node {start!r} is not in the graph. Try again.")
            continue

        reachable, paths = analyze_node(G, start)

        if not reachable:
            print(f"No nodes are reachable from {start!r}.")
            continue

        print("--------------------------------")
        print(f"From {start!r}, you can reach {len(reachable)} node(s):")
        print("    |    " + ",\n    |    ".join(sorted(reachable)))
        print("--------------------------------")
        print("Shortest paths from", start, "to each reachable node:")
        for target in sorted(reachable):
            path_str = " -> ".join(paths[target])
            print(f"   |   {path_str}")
        print("--------------------------------")



main()
