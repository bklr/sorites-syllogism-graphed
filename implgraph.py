from pathlib import Path
import networkx as nx
from pyvis.network import Network

RULES_FILE = "Soriteses_P60_E9.txt"
OUTPUT_HTML = "graph.html"

# loads implication sentence lines of "A -> B" and returns a list of (A, B) pairs.
def load_implications_from_file(path: Path):
    implications = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): # comment or empty
                continue
            pair = parse_implication_line(line)
            if pair is not None:
                implications.append(pair)
    return implications

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
        raise ValueError(f"Missing nodes on line: {line!r}")

    left = [a.strip() for a in left.split("&") if a.strip()]

    return left, right

# builds a directed graph from (A,B) pairs
def build_directed_graph(implications):
    G = nx.DiGraph()
    for A, B in implications:
        G.add_node(B)
        for a in A:
            G.add_node(a)
            G.add_edge(a, B)
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

    net.barnes_hut(
        spring_length=60,
        spring_strength=0.5,
        gravity=-15000,
        central_gravity=1,
        damping=0.12
    )
    net.show_buttons(filter_="physics")

    for node in undirected.nodes():
        net.add_node(
            node,
            label=str(node),
            shape="dot",
            size=14,
        )

    for u, v in G.edges():
        net.add_edge(
            u, 
            v, 
            color="#006aff", 
            width=4)

    return net

# returns set of reachable nodes and dict of shortest paths from start_node
def analyze_node(G: nx.DiGraph, start_node):
    if start_node not in G:
        raise ValueError(f"Node {start_node!r} not in graph.")
    
    reachable = nx.descendants(G, start_node)

    paths = {}
    for target in reachable:
        paths[target] = list(nx.shortest_path(G, start_node, target))
    return reachable, paths

# finds the longest shortest path between any two nodes in G (Sorites Conclusion)
def find_longest_chain(G: nx.DiGraph):
    longest_path = None
    for start in G.nodes():
        paths_from_start = nx.single_source_shortest_path_length(G, start)
        for target, length in paths_from_start.items():
            if longest_path is None or length > len(longest_path) - 1:
                longest_path = nx.shortest_path(G, start, target)
    return longest_path
    

def main():
    here = Path(__file__).resolve().parent
    rules_path = here / "Implication_Examples" / RULES_FILE
    implications = load_implications_from_file(rules_path)

    print(f"Loaded {len(implications)} implications from {RULES_FILE}.")

    G = build_directed_graph(implications)
    print(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    net = build_graph(G)

    output_path = here / OUTPUT_HTML
    net.show(str(output_path), notebook=False)

    print("Nodes in graph:", ", ".join(sorted(G.nodes())))
    print()

    longest_path = find_longest_chain(G)
    longest_str = " -> ".join(longest_path)
    print("-------------------------")
    print("Longest implication chain in graph (Sorites Conclusion):")
    print("   |   " + longest_str)
    print(f"   |   Concludes: {longest_path[0]} -> {longest_path[-1]}")
    print("-------------------------")

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
