import random
import networkx as nx
import numpy as np

def generateRandom():
    vN = random.randint(10, 500)
    m = min(int((vN * (vN - 1))), 2*vN)
    print(vN, m)
    eN = random.randint(vN, m)

    G = nx.Graph()
    vertices = np.random.permutation(vN)

    G.add_nodes_from(vertices)

    connected = [vertices[0]]

    for i in range(1, len(vertices)):
        u = connected[random.randint(0, len(connected) - 1)]
        v = vertices[i]
        connected.append(v)
        G.add_edge(u, v)
        eN -= 1

    for i in range(eN):
        u = random.randint(0, vN-1)
        v = random.randint(0, vN-1)

        while u == v or (u, v) in G.edges() or (v, u) in G.edges():
            u = random.randint(0, vN - 1)
            v = random.randint(0, vN - 1)

        G.add_edge(u, v)

    edges = []
    for edge in G.edges():
        if edge[0] < edge[1]:
            edges.append((edge[0], edge[1]))
        else:
            edges.append((edge[1], edge[0]))

    for edge in sorted(edges):
        print("E", edge[0], edge[1])

def generateRandomWithCycle():
    vN = random.randint(1000, 1200)
    m = min(int((vN * (vN - 1))), int(1.3 * vN))
    print(vN, m)
    eN = random.randint(vN, m)

    G = nx.Graph()
    vertices = np.random.permutation(vN)

    G.add_nodes_from(vertices)

    for i in range(vN):
        G.add_edge(i, i + 1)
        eN -= 1

    G.add_edge(vN, 0)

    for i in range(eN):
        u = random.randint(0, vN - 1)
        v = random.randint(0, vN - 1)

        while u == v or (u, v) in G.edges() or (v, u) in G.edges():
            u = random.randint(0, vN - 1)
            v = random.randint(0, vN - 1)

        G.add_edge(u, v)

    edges = []
    for edge in G.edges():
        if edge[0] < edge[1]:
            edges.append((edge[0], edge[1]))
        else:
            edges.append((edge[1], edge[0]))

    for edge in sorted(edges):
        print("E", edge[0], edge[1])


if __name__ == '__main__':
    # generateRandom()
    generateRandomWithCycle()
