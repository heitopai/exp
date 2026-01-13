import random
import os
import networkx as nx

current_path = os.path.dirname(os.path.abspath(__file__))

random.seed(0)

root=0

def GenerateGraph(n,c):
    p=c/(n-1.0)
    print(p)
    G=nx.fast_gnp_random_graph(n, p, directed=True)

    for v in range(1,n):
        G.add_edge(random.randint(0, v-1), v)

    with open(current_path+f"\\{c}\\sparse{n}.txt",'w') as f:
        f.write(f"{n} {G.number_of_edges()} {root}\n")
        for edge in G.edges():
            f.write(f"{edge[0]} {edge[1]} {random.randint(0, 1000)}\n")
for c in range(10,51,10):
    print(c)
    os.makedirs(current_path + f"\\{c}", exist_ok=True)            
    for j in range(1,11):
        GenerateGraph(100*j, c)