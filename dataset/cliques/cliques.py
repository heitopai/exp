import random
import os
import networkx as nx

current_path = os.path.dirname(os.path.abspath(__file__))

random.seed(0)

root = 0


def GenerateGraph(n, c, clique_size):
    p = c / (n - 1.0)
    print(f"n={n}, c={c}, clique_size={clique_size}, p={p}")

    G = nx.fast_gnp_random_graph(n, p, directed=True)

    for v in range(1, n):
        G.add_edge(random.randint(0, v - 1), v)

    clique_nodes = random.sample(range(n), clique_size)

    for u in clique_nodes:
        for v in clique_nodes:
            if u != v:
                G.add_edge(u, v)

    folder = current_path + f"\\{c}"
    os.makedirs(folder, exist_ok=True)

    with open(folder + f"\\clique{n}_{clique_size}.txt", "w") as f:
        f.write(f"{n} {G.number_of_edges()} {root}\n")
        for u, v in G.edges():
            f.write(f"{u} {v} {random.randint(0, 1000)}\n")


c = 10
os.makedirs(current_path + f"\\{c}", exist_ok=True)   
for i in range(1, 11):
    GenerateGraph(500, c, 50 * i)
